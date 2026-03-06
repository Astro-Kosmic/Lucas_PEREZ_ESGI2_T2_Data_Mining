/* Pokémon par génération */
CREATE OR REPLACE VIEW v_pokemon_by_generation AS
SELECT 
    generation_id,
    COUNT(*) AS nb_pokemon
FROM pokemon
WHERE id <= 1025
GROUP BY generation_id

/* Pokémon par type */
CREATE OR REPLACE VIEW v_pokemon_by_type AS
SELECT 
    t.name AS type_name,
    COUNT(*) AS nb_pokemon
FROM pokemon p
JOIN pokemon_type pt ON p.id = pt.id_pokemon
JOIN type_ref t ON pt.id_type = t.id
WHERE p.id <= 1025
GROUP BY t.name;

/* Nombre d'attaques par Pokémon */
CREATE OR REPLACE VIEW v_nb_moves_pokemon AS
SELECT 
    p.id,
    p.name,
    COUNT(um.id_move) AS nb_moves
FROM pokemon p
LEFT JOIN use_move um ON p.id = um.id_pokemon
WHERE p.id <= 1025
GROUP BY p.id, p.name;

/* Nombre d'attaques par type */
CREATE OR REPLACE VIEW v_moves_by_type AS
SELECT 
    t.name AS type_name,
    COUNT(*) AS nb_moves
FROM move m
JOIN type_ref t ON m.type_id = t.id
GROUP BY t.name;

/* Combinaison double types */
CREATE OR REPLACE VIEW v_type_combinations AS
SELECT 
    t1.name AS type_1,
    t2.name AS type_2,
    COUNT(*) AS nb_pokemon
FROM pokemon_type pt1
JOIN pokemon_type pt2 
    ON pt1.id_pokemon = pt2.id_pokemon
   AND pt1.id_type < pt2.id_type
JOIN type_ref t1 ON pt1.id_type = t1.id
JOIN type_ref t2 ON pt2.id_type = t2.id
WHERE pt1.id_pokemon <= 1025
GROUP BY t1.name, t2.name
ORDER BY nb_pokemon DESC;

/* Répartition mono-types et doubles-types */
CREATE OR REPLACE VIEW v_pokemon_type_count AS
SELECT 
    p.id,
    p.name,
    COUNT(pt.id_type) AS nb_types
FROM pokemon p
JOIN pokemon_type pt ON p.id = pt.id_pokemon
WHERE p.id <= 1025
GROUP BY p.id, p.name;

/* Moyenne des attaques par type */
CREATE OR REPLACE VIEW v_avg_power_by_type AS
SELECT 
    t.name AS type_name,
    AVG(m.power) AS avg_power
FROM move m
JOIN type_ref t ON m.type_id = t.id
WHERE m.power IS NOT NULL
GROUP BY t.name
ORDER BY avg_power DESC;

/* Répaertition des attaques selon leur puissance */
CREATE OR REPLACE VIEW v_move_power_distribution AS
SELECT power
FROM move
WHERE power IS NOT NULL;