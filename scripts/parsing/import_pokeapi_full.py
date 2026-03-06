import os
import time
import re
from typing import Dict, Any, List, Tuple, Optional, Set

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import mysql.connector
from mysql.connector import Error
from tqdm import tqdm


POKEAPI = "https://pokeapi.co/api/v2"


# ---------------------------
# Utils HTTP / parsing
# ---------------------------
def id_from_url(url: str) -> int:
    m = re.search(r"/(\d+)/?$", url)
    if not m:
        raise ValueError(f"Impossible d'extraire l'id depuis l'URL: {url}")
    return int(m.group(1))


def make_session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=6,
        backoff_factor=0.7,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({"User-Agent": "pokeapi-import/2.1"})
    return s


def fetch_json(session: requests.Session, url: str, sleep_s: float = 0.0) -> Dict[str, Any]:
    r = session.get(url, timeout=30)
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code} sur {url}: {r.text[:250]}")
    if sleep_s > 0:
        time.sleep(sleep_s)
    return r.json()


# ---------------------------
# DB helpers
# ---------------------------
def connect_db():
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "poke_user")
    password = os.getenv("DB_PASSWORD", "MotDePasseFortIci")
    database = os.getenv("DB_NAME", "poke_db")

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        autocommit=False,
    )


def ensure_staging_table(cur):
    # Table sans FK, pour stocker temporairement les relations pokemon<->move
    cur.execute("""
        CREATE TABLE IF NOT EXISTS use_move_staging (
            id_pokemon INT NOT NULL,
            id_move INT NOT NULL,
            PRIMARY KEY (id_pokemon, id_move),
            KEY idx_staging_move (id_move)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)


def optional_reset(cur, db):
    reset = os.getenv("RESET", "0").strip() == "1"
    if not reset:
        return

    print("⚠️ RESET=1 : TRUNCATE de toutes les tables (attention aux données).")
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    for t in ["use_move", "pokemon_type", "pokemon", "move", "type_ref", "nature", "generation", "game", "use_move_staging"]:
        try:
            cur.execute(f"TRUNCATE TABLE {t}")
        except Exception:
            pass
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    db.commit()


# ---------------------------
# Import steps
# ---------------------------
def upsert_types(cur, session: requests.Session, sleep_s: float):
    data = fetch_json(session, f"{POKEAPI}/type?limit=200", sleep_s=sleep_s)
    rows = [(id_from_url(t["url"]), t["name"]) for t in data["results"]]

    sql = """
    INSERT INTO type_ref (id, name)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE name=VALUES(name)
    """
    cur.executemany(sql, rows)


def upsert_generations(cur, session: requests.Session, sleep_s: float):
    data = fetch_json(session, f"{POKEAPI}/generation?limit=50", sleep_s=sleep_s)
    rows = [(id_from_url(g["url"]),) for g in data["results"]]

    sql = """
    INSERT INTO generation (id)
    VALUES (%s)
    ON DUPLICATE KEY UPDATE id=VALUES(id)
    """
    cur.executemany(sql, rows)


def upsert_pokemons_types_and_stage_moves(
    cur,
    session: requests.Session,
    sleep_s: float,
    limit_pokemon: Optional[int] = None,
) -> Set[int]:
    """
    - Insère pokemon
    - Insère pokemon_type (FK-safe : pokemon toujours inséré avant)
    - Remplit use_move_staging
    - Retourne l'ensemble des move_id rencontrés
    """
    index = fetch_json(session, f"{POKEAPI}/pokemon?limit=100000&offset=0", sleep_s=sleep_s)
    poke_refs = index["results"]
    if limit_pokemon is not None:
        poke_refs = poke_refs[:limit_pokemon]

    sql_pokemon = """
    INSERT INTO pokemon (id, name, evo_state, shiny, nature_id, generation_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      name=VALUES(name),
      evo_state=VALUES(evo_state),
      shiny=VALUES(shiny),
      nature_id=VALUES(nature_id),
      generation_id=VALUES(generation_id)
    """

    sql_ptype = """
    INSERT INTO pokemon_type (id_pokemon, id_type, slot)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE id_type=VALUES(id_type)
    """

    sql_stage = """
    INSERT IGNORE INTO use_move_staging (id_pokemon, id_move)
    VALUES (%s, %s)
    """

    # Buffers
    pokemon_rows: List[Tuple] = []
    ptype_rows: List[Tuple] = []
    staging_rows: List[Tuple] = []
    move_ids: Set[int] = set()

    # Seuils
    POKEMON_BATCH = 300
    PTYPE_BATCH = 1200
    STAGING_BATCH = 4000

    def flush_pokemon():
        nonlocal pokemon_rows
        if pokemon_rows:
            cur.executemany(sql_pokemon, pokemon_rows)
            pokemon_rows.clear()

    def flush_ptype_fk_safe():
        nonlocal ptype_rows
        # ⚠️ FK SAFE : on flush d'abord pokemon
        flush_pokemon()
        if ptype_rows:
            cur.executemany(sql_ptype, ptype_rows)
            ptype_rows.clear()

    def flush_staging():
        nonlocal staging_rows
        if staging_rows:
            cur.executemany(sql_stage, staging_rows)
            staging_rows.clear()

    for p in tqdm(poke_refs, desc="Pokemon (details)", unit="pokemon"):
        d = fetch_json(session, p["url"], sleep_s=sleep_s)

        pid = d["id"]
        name = d["name"]

        # génération via species
        species = fetch_json(session, d["species"]["url"], sleep_s=sleep_s)
        gen_id = id_from_url(species["generation"]["url"]) if species.get("generation") else None

        # champs non "canon" (PokéAPI ne fixe pas shiny/nature pour une espèce)
        evo_state = None
        shiny = 0
        nature_id = None

        pokemon_rows.append((pid, name, evo_state, shiny, nature_id, gen_id))

        # types
        for t in d.get("types", []):
            slot = t["slot"]
            type_id = id_from_url(t["type"]["url"])
            ptype_rows.append((pid, type_id, slot))

        # moves -> staging + set unique
        for mv in d.get("moves", []):
            mid = id_from_url(mv["move"]["url"])
            move_ids.add(mid)
            staging_rows.append((pid, mid))

        # Flush contrôlé
        if len(pokemon_rows) >= POKEMON_BATCH:
            flush_pokemon()

        if len(ptype_rows) >= PTYPE_BATCH:
            flush_ptype_fk_safe()

        if len(staging_rows) >= STAGING_BATCH:
            flush_staging()

    # Flush final (ordre important)
    flush_pokemon()
    flush_ptype_fk_safe()
    flush_staging()

    return move_ids


def should_keep_move(move_detail: Dict[str, Any], mode: str) -> bool:
    power = move_detail.get("power")
    accuracy = move_detail.get("accuracy")

    if mode == "all":
        return True
    if mode == "combat":
        return power is not None
    if mode == "useful":
        return (power is not None) or (accuracy is not None)
    return True


def upsert_moves_from_ids(
    cur,
    session: requests.Session,
    sleep_s: float,
    move_ids: Set[int],
    move_filter: str,
) -> int:
    sql_move = """
    INSERT INTO move (id, name, power, accuracy, pp, type_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      name=VALUES(name),
      power=VALUES(power),
      accuracy=VALUES(accuracy),
      pp=VALUES(pp),
      type_id=VALUES(type_id)
    """

    rows: List[Tuple] = []
    kept = 0
    MOVE_BATCH = 800

    for mid in tqdm(sorted(move_ids), desc="Moves (details)", unit="move"):
        d = fetch_json(session, f"{POKEAPI}/move/{mid}/", sleep_s=sleep_s)
        if not should_keep_move(d, move_filter):
            continue

        kept += 1
        name = d["name"]
        power = d["power"]
        accuracy = d["accuracy"]
        pp = d["pp"]
        type_id = id_from_url(d["type"]["url"])

        rows.append((mid, name, power, accuracy, pp, type_id))

        if len(rows) >= MOVE_BATCH:
            cur.executemany(sql_move, rows)
            rows.clear()

    if rows:
        cur.executemany(sql_move, rows)

    return kept


def finalize_use_move(cur):
    # Insère les couples staging uniquement si le move existe (FK safe)
    cur.execute("""
        INSERT IGNORE INTO use_move (id_pokemon, id_move)
        SELECT s.id_pokemon, s.id_move
        FROM use_move_staging s
        INNER JOIN move m ON m.id = s.id_move
    """)
    cur.execute("DROP TABLE IF EXISTS use_move_staging")


# ---------------------------
# Main
# ---------------------------
def main():
    # LIMIT_POKEMON=0 => pas de limite (tout)
    limit_pokemon_env = os.getenv("LIMIT_POKEMON", "0").strip()
    limit_pokemon = int(limit_pokemon_env) if limit_pokemon_env else 0
    if limit_pokemon <= 0:
        limit_pokemon = None

    sleep_s = float(os.getenv("SLEEP_S", "0.05"))

    # all | combat | useful
    move_filter = os.getenv("MOVE_FILTER", "useful").strip().lower()
    if move_filter not in ("all", "combat", "useful"):
        print(f"⚠️ MOVE_FILTER inconnu ({move_filter}) -> fallback 'useful'")
        move_filter = "useful"

    session = make_session()

    db = None
    cur = None
    try:
        db = connect_db()
        cur = db.cursor()

        optional_reset(cur, db)
        ensure_staging_table(cur)
        db.commit()

        print("[1/6] Import types...")
        upsert_types(cur, session, sleep_s=sleep_s)
        db.commit()

        print("[2/6] Import generations...")
        upsert_generations(cur, session, sleep_s=sleep_s)
        db.commit()

        print("[3/6] Import pokemon + pokemon_type + staging use_move...")
        move_ids = upsert_pokemons_types_and_stage_moves(
            cur, session, sleep_s=sleep_s, limit_pokemon=limit_pokemon
        )
        db.commit()
        print(f"   -> Moves uniques rencontrés: {len(move_ids)}")

        print(f"[4/6] Import moves depuis IDs (filtre: {move_filter}) ...")
        kept = upsert_moves_from_ids(cur, session, sleep_s=sleep_s, move_ids=move_ids, move_filter=move_filter)
        db.commit()
        print(f"   -> Moves gardés après filtre: {kept}")

        print("[5/6] Finalize use_move (FK-safe) ...")
        finalize_use_move(cur)
        db.commit()

        print("[6/6] Terminé ✅")

    except Error as e:
        print("❌ Erreur MySQL:", e)
        if db:
            db.rollback()
        raise
    except Exception as e:
        print("❌ Erreur:", e)
        if db:
            db.rollback()
        raise
    finally:
        try:
            if cur:
                cur.close()
        except Exception:
            pass
        try:
            if db:
                db.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
