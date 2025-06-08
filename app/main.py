import tkinter as tk
from serial_handler import leer_datos_serial
from db_handler import guardar_datos
from csv_handler import exportar_csv
from aws_uploader import subir_archivo

def grabar():
    datos = leer_datos_serial()
    if datos:
        valores = tuple(map(float, datos.split(',')))
        guardar_datos(valores)
        exportar_csv(valores)
        subir_archivo("historico.csv", "proyecto-micro", "historico.csv")
        lbl.config(text=f"Grabado: {valores}")
    else:
        lbl.config(text="No se leyeron datos.")

app = tk.Tk()
app.title("Monitor de Sensores")
tk.Button(app, text="Grabar", command=grabar).pack(pady=10)
lbl = tk.Label(app, text="Esperando datos...")
lbl.pack(pady=10)
app.mainloop()
