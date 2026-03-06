CREATE DATABASE poke_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'poke_user'@'localhost' IDENTIFIED BY 'MotDePasseFortIci';
GRANT ALL PRIVILEGES ON poke_db.* TO 'poke_user'@'localhost';
FLUSH PRIVILEGES;

USE poke_db;

-- Référentiels
CREATE TABLE generation (
  id INT PRIMARY KEY
) ENGINE=InnoDB;

CREATE TABLE nature (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE type_ref (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Entités
CREATE TABLE pokemon (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  evo_state INT NULL,
  shiny BOOLEAN NOT NULL DEFAULT 0,
  nature_id INT NULL,
  generation_id INT NULL,

  CONSTRAINT fk_pokemon_nature
    FOREIGN KEY (nature_id) REFERENCES nature(id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  CONSTRAINT fk_pokemon_generation
    FOREIGN KEY (generation_id) REFERENCES generation(id)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE game (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  release_date DATE NULL,
  generation_id INT NOT NULL,

  CONSTRAINT fk_game_generation
    FOREIGN KEY (generation_id) REFERENCES generation(id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE move (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  power INT NULL,
  accuracy INT NULL,
  pp INT NULL,
  type_id INT NOT NULL,

  CONSTRAINT fk_move_type
    FOREIGN KEY (type_id) REFERENCES type_ref(id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Associations
CREATE TABLE pokemon_type (
  id_pokemon INT NOT NULL,
  id_type INT NOT NULL,
  slot INT NOT NULL, -- 1 ou 2 (voire plus si tu gères des formes spéciales)
  PRIMARY KEY (id_pokemon, slot),

  CONSTRAINT fk_pokemon_type_pokemon
    FOREIGN KEY (id_pokemon) REFERENCES pokemon(id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_pokemon_type_type
    FOREIGN KEY (id_type) REFERENCES type_ref(id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE use_move (
  id_pokemon INT NOT NULL,
  id_move INT NOT NULL,
  PRIMARY KEY (id_pokemon, id_move),

  CONSTRAINT fk_use_move_pokemon
    FOREIGN KEY (id_pokemon) REFERENCES pokemon(id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_use_move_move
    FOREIGN KEY (id_move) REFERENCES move(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Index utiles (requêtes + perf)
CREATE INDEX idx_pokemon_generation ON pokemon(generation_id);
CREATE INDEX idx_pokemon_nature ON pokemon(nature_id);

CREATE INDEX idx_game_generation ON game(generation_id);

CREATE INDEX idx_move_type ON move(type_id);

CREATE INDEX idx_pokemon_type_type ON pokemon_type(id_type);
CREATE INDEX idx_use_move_move ON use_move(id_move);