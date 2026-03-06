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

plt.figure(figsize=(10, 6))
plt.bar(df["type_name"], df["nb_moves"])
plt.xticks(rotation=45)
plt.xlabel("Type")
plt.ylabel("Nombre d'attaques")
plt.title("Nombre d'attaques par type")
plt.tight_layout()

plt.savefig("moves_par_type.png")

db.close()
print("Graphique généré : moves_par_type.png")