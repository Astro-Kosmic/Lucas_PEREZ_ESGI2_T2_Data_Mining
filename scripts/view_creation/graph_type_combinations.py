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
SELECT type_1, type_2, nb_pokemon
FROM v_type_combinations
ORDER BY nb_pokemon DESC
LIMIT 10;
"""

df = pd.read_sql(query, db)

df["combination"] = df["type_1"] + " + " + df["type_2"]

plt.figure(figsize=(10,6))
plt.barh(df["combination"], df["nb_pokemon"])

plt.xlabel("Nombre de Pokémon")
plt.ylabel("Combinaison de types")
plt.title("Top 10 des combinaisons de types les plus fréquentes")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("type_combinations.png")

db.close()
print("Graphique généré : type_combinations.png")