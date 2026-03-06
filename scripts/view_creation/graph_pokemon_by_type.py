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
SELECT type_name, nb_pokemon
FROM v_pokemon_by_type
ORDER BY nb_pokemon DESC;
"""

df = pd.read_sql(query, db)

plt.figure(figsize=(10,6))
plt.bar(df["type_name"], df["nb_pokemon"])
plt.xticks(rotation=45)
plt.xlabel("Type")
plt.ylabel("Nombre de Pokémon")
plt.title("Nombre de Pokémon par type")
plt.tight_layout()

plt.savefig("pokemon_par_type.png")

db.close()
print("Graphique généré : pokemon_par_type.png")