import csv
from datetime import datetime

def exportar_csv(valores, archivo="historico.csv"):
    with open(archivo, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        fila = [datetime.now().strftime("%d/%m/%Y %H:%M:%S")] + list(valores)  # Agrega la fecha al inicio
        writer.writerow(fila)
