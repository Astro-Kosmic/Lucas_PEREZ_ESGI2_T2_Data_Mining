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
SELECT power
FROM v_move_power_distribution;
"""

df = pd.read_sql(query, db)

plt.figure(figsize=(6,6))
plt.boxplot(df["power"], vert=True)

plt.ylabel("Puissance")
plt.title("Distribution de la puissance des attaques")

plt.tight_layout()
plt.savefig("move_power_boxplot.png")

db.close()
print("Graphique généré : move_power_boxplot.png")