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
SELECT type_name, avg_power
FROM v_avg_power_by_type;
"""

df = pd.read_sql(query, db)

plt.figure(figsize=(10,6))

plt.scatter(df["type_name"], df["avg_power"])

plt.xticks(rotation=45)
plt.xlabel("Type")
plt.ylabel("Puissance moyenne")
plt.title("Comparaison des puissances moyennes des attaques par type")

plt.tight_layout()
plt.savefig("avg_power_scatter.png")

db.close()
print("Graphique généré : avg_power_scatter.png")