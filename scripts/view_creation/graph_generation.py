import mysql.connector
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

db = mysql.connector.connect(
    host="localhost",
    user="poke_user",
    password="MotDePasseFortIci",
    database="poke_db"
)

query = """
SELECT generation_id, nb_pokemon
FROM v_pokemon_by_generation
ORDER BY generation_id;
"""

df = pd.read_sql(query, db)

plt.figure(figsize=(8, 5))
plt.bar(df["generation_id"], df["nb_pokemon"])
plt.xlabel("Génération")
plt.ylabel("Nombre de Pokémon")
plt.title("Nombre de Pokémon par génération")
plt.xticks(df["generation_id"])
plt.tight_layout()
plt.savefig("pokemon_par_generation.png")

db.close()
print("Graphique généré : pokemon_par_generation.png")
