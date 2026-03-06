/*Nombre de Pokémon par type*/
SELECT t.name, COUNT(*) AS nb_pokemon
FROM pokemon p
JOIN pokemon_type pt ON p.id = pt.id_pokemon
JOIN type_ref t ON t.id = pt.id_type
WHERE p.id <= 1025
GROUP BY t.name
ORDER BY nb_pokemon DESC;

/*Pokémon avec le plus d’attaques*/
SELECT p.name, COUNT(*) AS nb_moves
FROM pokemon p
JOIN use_move um ON p.id = um.id_pokemon
GROUP BY p.id, p.name
ORDER BY nb_moves DESC
LIMIT 10;

/*Pokémon avec deux types*/
SELECT p.name
FROM pokemon p
JOIN pokemon_type pt ON p.id = pt.id_pokemon
GROUP BY p.id
HAVING COUNT(pt.id_type) = 2;

/*Pokémon feu*/
SELECT p.name
FROM pokemon p
JOIN pokemon_type pt ON p.id = pt.id_pokemon
JOIN type_ref t ON t.id = pt.id_type
WHERE t.name = 'fire'
AND p.id <= 1025
ORDER BY p.id;

/*Nombre de Pokémon par génération*/
SELECT generation_id, COUNT(*) AS nb_pokemon
FROM pokemon
WHERE id <= 1025
GROUP BY generation_id
ORDER BY generation_id;