import csv
from datetime import datetime

def exportar_csv(valores, archivo="historico.csv"):
    with open(archivo, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat()] + list(valores))
