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
SELECT type_name, nb_moves
FROM v_moves_by_type
ORDER BY nb_moves DESC;
"""

df = pd.read_sql(query, db)

plt.figure(figsize=(8, 8))
plt.pie(
    df["nb_moves"],
    labels=df["type_name"],
    autopct="%1.1f%%"
)

plt.title("Répartition des attaques par type")
plt.tight_layout()
plt.savefig("moves_by_type_pie.png")

db.close()
print("Graphique généré : moves_by_type_pie.png")