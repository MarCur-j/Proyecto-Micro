import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def conectar_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def guardar_datos(valores):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensores (temperatura, humedad, proximidad, presion) VALUES (%s, %s, %s, %s)",
        valores
    )
    conn.commit()
    cursor.close()
    conn.close()