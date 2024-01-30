from config import *
import csv

# Créer la table
mycursor.execute("CREATE TABLE card (code CHAR(10) NOT NULL, rarity VARCHAR(10) NOT NULL, name VARCHAR(100), price FLOAT(5,2), PRIMARY KEY (code, rarity))")

# Récupérer les données d'un fichier csv et les mettre dans une liste de tuples
csv_file = ""

with open(csv_file) as f:
    reader = csv.reader(f)
    data = list(tuple(line) for line in reader)

# Pour insérer des données sans passer par un csv:
# data = [('code', 'rarity', 'name', null), ...] 

# Insérer les données
sql_insert = "INSERT INTO card VALUES (%s, %s, %s, %s)"

mycursor.executemany(sql_insert, data)
mydb.commit()

print(mycursor.rowcount, "was inserted.")