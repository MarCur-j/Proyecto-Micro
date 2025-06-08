import tkinter as tk
from tkinter import ttk, PhotoImage
import os
import pandas as pd
import matplotlib.pyplot as plt
from serial_handler import leer_datos_serial
from db_handler import guardar_datos
from csv_handler import exportar_csv
from aws_uploader import subir_archivo

# ---- Función para grabar datos ----
def grabar():
    datos = leer_datos_serial()
    if datos:
        try:
            valores = tuple(map(float, datos.split(',')))

            guardar_datos(valores)
            exportar_csv(valores)

            try:
                subir_archivo("historico.csv", "proyecto-micro")
            except Exception as e:
                lbl_resultado.config(text=f"No se subió a AWS: {e}", fg="red")

            resultado = (
                f"🌡️ Temp: {valores[0]}°C  | "  # Usamos '|' como separador y acortamos el texto
                f"💧 Hum: {valores[1]}%  | "
                f"📏 Dist: {valores[2]}cm  | "
                f"🔥 Gas: {valores[3]}"
            )
            lbl_resultado.config(text=resultado, fg="black")

            if len(tabla.get_children()) >= 10:
                tabla.delete(tabla.get_children()[0])
            tabla.insert("", "end", values=valores)

        except ValueError:
            lbl_resultado.config(text="Error: datos no numéricos", fg="red")
    else:
        lbl_resultado.config(text="No se leyeron datos del Arduino", fg="red")


# ---- Modo automático sin límite ----
def auto_leer():
    grabar()
    app.after(3000, auto_leer)  # Ejecutar cada 3 segundos

# ---- Mostrar gráfica con matplotlib ----
def mostrar_grafica():
    try:
        df = pd.read_csv("historico.csv", sep=';', header=None, names=["Fecha", "Temp", "Hum", "Dist", "Gas"], on_bad_lines='skip')
        ultimos = df.tail(10)

        plt.figure(figsize=(8, 5))
        plt.plot(ultimos["Temp"], label="Temperatura (°C)", marker='o')
        plt.plot(ultimos["Hum"], label="Humedad (%)", marker='o')
        plt.plot(ultimos["Dist"], label="Distancia (cm)", marker='o')
        plt.plot(ultimos["Gas"], label="Nivel de Gas", marker='o')

        plt.title("📊 Últimas 10 lecturas")
        plt.xlabel("Lecturas")
        plt.ylabel("Valores")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        lbl_resultado.config(text=f"Error al graficar: {e}", fg="red")

# ---- Abrir archivo CSV directamente ----
def abrir_csv():
    try:
        os.startfile("historico.csv")
    except Exception as e:
        lbl_resultado.config(text=f"No se pudo abrir CSV: {e}", fg="red")

# --- Reiniciar historicos--
def reiniciar_csv():
    with open("historico.csv", "w", newline="") as file:
        pass  # Vacía el archivo local
    lbl_resultado.config(text="🗑 CSV reiniciado (solo local). AWS sigue igual.", fg="blue")


# ---- INTERFAZ GRÁFICA ----
app = tk.Tk()
app.title("Monitor de Sensores IoT")
app.geometry("560x780")
app.configure(bg="#f9f9f9")

# ---- Encabezado formal ----
tk.Label(app, text="UNIVERSIDAD NACIONAL DE PIURA", font=("Segoe UI", 18, "bold"), bg="#f9f9f9", fg="#0b129c").pack(pady=2)
tk.Label(app, text="🦾Monitor de Sensores IoT🤖", font=("Segoe UI", 16, "bold"), bg="#f9f9f9", fg="#000").pack(pady=2)
tk.Label(app, text="Curso: MICROCONTROLADORES II", font=("Segoe UI", 12, "bold"), bg="#f9f9f9", fg="#000").pack(pady=2)
tk.Label(app, text="Estudiantes: Curo Jacinto, Mario Alberto", font=("Segoe UI", 10, "italic"), bg="#f9f9f9", fg="#000").pack(pady=3)
tk.Label(app, text="Cruz Chingel, Iván", font=("Segoe UI", 10, "italic"), bg="#f9f9f9", fg="#000").pack(pady=1)
tk.Label(app, text="Ramirez Rosado, Robert", font=("Segoe UI", 10, "italic"), bg="#f9f9f9", fg="#000").pack(pady=1)

# --- Añadir imagen del escudo de la universidad ---
try:
    shield_img = PhotoImage(file="app/escudo.unp.png")
    shield_img = shield_img.subsample(5, 5) # Ejemplo: la hace 1/6 del tamaño
    shield_label = tk.Label(app, image=shield_img, bg="#f9f9f9")
    shield_label.image = shield_img # Mantén una referencia para evitar la recolección de basura
    shield_label.pack(pady=10) # Ajusta pady para el espaciad

except Exception as e:
    print(f"Error al cargar la imagen del escudo: {e}")




# --- Contenedor para los botones (Frame) ---
button_frame = tk.Frame(app, bg="#f9f9f9")
button_frame.pack(pady=5) # Ajusta el padding del frame si es necesario

tk.Button(button_frame, text="📥Grabar una vez", font=("Segoe UI", 10), command=grabar,
          bg="#4CAF50", fg="white", activebackground="#45a049").pack(side="left", padx=5) # side="left" y padx
tk.Button(button_frame, text="🔁 Automático", font=("Segoe UI", 10), command=auto_leer, # Texto más corto
          bg="#2196F3", fg="white", activebackground="#1976D2").pack(side="left", padx=5)
tk.Button(button_frame, text="📈 Gráfica", font=("Segoe UI", 11), command=mostrar_grafica, # Texto más corto
          bg="#FF9800", fg="white", activebackground="#FB8C00").pack(side="left", padx=5)
tk.Button(button_frame, text="📂 Abrir .CSV", font=("Segoe UI", 10), command=abrir_csv,
          bg="#9C27B0", fg="white", activebackground="#7B1FA2").pack(side="left", padx=5)
tk.Button(button_frame, text="🗑 Reiniciar .CSV", font=("Segoe UI", 10), command=reiniciar_csv, # Texto más corto
          bg="#f44336", fg="white", activebackground="#c62828").pack(side="left", padx=5)

lbl_resultado = tk.Label(app, text="Esperando datos...", font=("Segoe UI", 12), bg="#f9f9f9", fg="gray")
lbl_resultado.pack(pady=5)

# ---- Tabla de últimas lecturas ----
tabla = ttk.Treeview(app, columns=("Temp", "Hum", "Dist", "Gas"), show="headings", height=10)
tabla.heading("Temp", text="Temp (°C)")
tabla.heading("Hum", text="Humedad (%)")
tabla.heading("Dist", text="Distancia (cm)")
tabla.heading("Gas", text="Gas (ADC)")
tabla.column("Temp", width=100, anchor="center")
tabla.column("Hum", width=120, anchor="center")
tabla.column("Dist", width=130, anchor="center")
tabla.column("Gas", width=100, anchor="center")
tabla.pack(pady=5)

app.mainloop()
