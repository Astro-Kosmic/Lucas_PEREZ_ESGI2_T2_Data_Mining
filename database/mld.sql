// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table pokemon {
  id integer [PK]
  name varchar
  evo_state integer
  shiny bool
  nature_id integer
  generation_id integer
}

Table move {
  id integer [PK]
  name varchar
  power integer
  accuracy integer
  pp integer
  type_id integer
}

Table type {
  id integer [PK]
  name varchar
}

Table game {
  id integer [PK]
  name varchar
  release_date date
  generation_id integer
}

Table generation {
  id integer [PK]
}

Table use_move {
  id_pokemon integer
  id_move integer
}

Table pokemon_type {
  id_pokemon integer
  id_type integer
  slot integer // 1 = type principal, 2 = type secondaire

  indexes {
    (id_pokemon, slot) [PK] // max 2 lignes par pokemon (slot 1 et 2)
    (id_pokemon, id_type) [unique] // évite de mettre deux fois le même type
  }
}


// Table use_move
Ref: use_move.id_pokemon < pokemon.id
Ref: use_move.id_move < move.id

// Table pokemon_type
Ref: pokemon_type.id_pokemon > pokemon.id
Ref: pokemon_type.id_type > type.id

// Table pokemon
Ref: pokemon.generation_id < generation.id

// Table game
Ref: game.generation_id < generation.id

// Table move
Ref : move.type_id < type.id
