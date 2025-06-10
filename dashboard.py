import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dashboard de Sensores", layout="centered")
st.title("📊 Dashboard en Vivo - Proyecto Microcontroladores")
st.markdown("**Universidad Nacional de Piura**  \nCurso: *Microcontroladores II*  \nIntegrantes: 👥")

# Verificar si el CSV existe
if not os.path.exists("historico.csv"):
    st.warning("No se encontró el archivo `historico.csv`. Asegúrate de haber ejecutado la app.")
else:
    # Leer CSV (con separador correcto si usás ; o ,)
    try:
        df = pd.read_csv("historico.csv", sep=";", names=["Fecha", "Temp", "Hum", "Dist", "Gas"])
    except:
        df = pd.read_csv("historico.csv", names=["Fecha", "Temp", "Hum", "Dist", "Gas"])

    # Mostrar tabla
    st.subheader("📋 Últimas 10 Lecturas")
    st.dataframe(df.tail(10), use_container_width=True)

    # Mostrar gráfica
    st.subheader("📈 Temperatura")
    st.line_chart(df["Temp"].tail(10))
    st.subheader("💧 Humedad")
    st.line_chart(df["Hum"].tail(10))
    st.subheader("📏 Distancia")
    st.line_chart(df["Dist"].tail(10))
    st.subheader("🔥 Nivel de Gas")
    st.line_chart(df["Gas"].tail(10))

    # Botón de descarga
    st.download_button(
        label="📥 Descargar histórico completo",
        data=open("historico.csv", "rb"),
        file_name="historico.csv",
        mime="text/csv"
    )
