import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Dashboard Predictivo", layout="wide", initial_sidebar_state="collapsed")

# Busca automáticamente cualquier archivo HTML válido en tu carpeta web
archivos_buscados = ["index.html", "reporte.html", "analisis_completo.html"]
archivo_final = None

for archivo in archivos_buscados:
    if os.path.exists(archivo):
        archivo_final = archivo
        break

if archivo_final:
    with open(archivo_final, 'r', encoding='utf-8') as f:
        html_data = f.read()
    # Altura inmensa (4500px) para que tu reporte se estire sin crear dobles barras de scroll molestas
    components.html(html_data, height=4500, scrolling=True)
else:
    st.error("No se encontró ningún archivo HTML en los archivos de tu repositorio GitHub.")
    st.info(f"Asegúrate de que haya subido un archivo llamado: {', '.join(archivos_buscados)}")
