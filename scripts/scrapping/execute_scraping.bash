source venv/bin/activate
export DB_HOST=localhost
export DB_USER=poke_user
export DB_PASSWORD='MotDePasseFortIci'
export DB_NAME=poke_db

export RESET=1
export LIMIT_POKEMON=0
export MOVE_FILTER=useful
export SLEEP_S=0.05

python3 ./scripts/parsing/import_pokeapi_full.py