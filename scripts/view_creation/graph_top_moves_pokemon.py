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
SELECT name, nb_moves
FROM v_nb_moves_pokemon
ORDER BY nb_moves DESC
LIMIT 10;
"""

df = pd.read_sql(query, db)

plt.figure(figsize=(10, 6))
plt.barh(df["name"], df["nb_moves"])
plt.xlabel("Nombre d'attaques")
plt.ylabel("Pokémon")
plt.title("Top 10 des Pokémon avec le plus d'attaques")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("top_pokemon_moves.png")

db.close()
print("Graphique généré : top_pokemon_moves.png")