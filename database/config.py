import mysql.connector

# Si la base de données n'existe pas:
# - enlever "database" dans la variable mydb
# - utiliser l'instruction suivante':
#     mycursor.execute("CREATE DATABASE tcgCollection")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="tcgCollection"
)

mycursor = mydb.cursor()