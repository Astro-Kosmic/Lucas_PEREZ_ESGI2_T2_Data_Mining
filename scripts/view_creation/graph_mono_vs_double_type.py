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
SELECT nb_types, COUNT(*) AS nb_pokemon
FROM v_pokemon_type_count
GROUP BY nb_types
ORDER BY nb_types;
"""

df = pd.read_sql(query, db)

labels = []
for n in df["nb_types"]:
    if n == 1:
        labels.append("Mono-type")
    elif n == 2:
        labels.append("Double-type")
    else:
        labels.append(f"{n} types")

plt.figure(figsize=(7, 7))
plt.pie(
    df["nb_pokemon"],
    labels=labels,
    autopct="%1.1f%%"
)
plt.title("Répartition des Pokémon mono-type et double-type")
plt.tight_layout()
plt.savefig("mono_vs_double_type.png")

db.close()
print("Graphique généré : mono_vs_double_type.png")