# =============================================================
# Dashboard de Analisis Bibliometrico - Scopus
# Tema: Mantenimiento predictivo y deteccion de fallas con IA
# Curso: Data Mining Basico / Algoritmo y Estructura de Datos Basados en IA
# Autor: Marcelo Marquez
# =============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# ----------------- Configuracion de la pagina -----------------
st.set_page_config(
    page_title="Dashboard Scopus - Mantenimiento Predictivo",
    page_icon="\U0001F527",
    layout="wide"
)

# ----------------- URL del CSV en GitHub -----------------
# Carga automatica desde el repositorio publico
URL_GITHUB = "https://raw.githubusercontent.com/mmarquez88/dashboard_scopus_pa3_Grupo2/main/scopus.csv"

# ----------------- Encabezado y texto explicativo -----------------
st.title("\U0001F527 Dashboard Bibliometrico - Scopus")
st.markdown("""
### Mantenimiento predictivo y deteccion de fallas con Inteligencia Artificial

**Pregunta de investigacion:** como contribuye el machine learning al
mantenimiento predictivo y la deteccion de fallas de equipos industriales?

**Palabras clave:** `predictive maintenance` - `machine learning` - `fault detection` - `industry`

Esta aplicacion analiza **20 articulos cientificos** extraidos de la base de datos **Scopus**,
publicados entre 2019 y 2026. A continuacion se presentan visualizaciones que responden
a la pregunta de investigacion: evolucion de las publicaciones en el tiempo, los autores
mas productivos, los articulos mas influyentes y los temas predominantes en la literatura.
""")

st.divider()

# ----------------- Carga de datos -----------------
st.sidebar.header("\u2699\uFE0F Configuracion")
fuente = st.sidebar.radio(
    "Fuente de datos:",
    ["Automatica (desde GitHub)", "Subir CSV manualmente"]
)

@st.cache_data
def cargar_desde_github(url):
    return pd.read_csv(url)

df = None

if fuente == "Automatica (desde GitHub)":
    try:
        df = cargar_desde_github(URL_GITHUB)
        st.sidebar.success("Datos cargados desde GitHub")
    except Exception as e:
        st.sidebar.error("No se pudo cargar desde GitHub.")
        st.sidebar.caption("Detalle: " + str(e))
        st.sidebar.info("Usa la opcion 'Subir CSV manualmente'.")
else:
    archivo = st.sidebar.file_uploader("Sube tu archivo scopus.csv", type=["csv"])
    if archivo is not None:
        df = pd.read_csv(archivo)

# ----------------- Validacion -----------------
if df is None:
    st.info("Esperando datos. Selecciona una fuente en la barra lateral.")
    st.stop()

# Limpiar nombres de columnas
df.columns = [c.strip() for c in df.columns]
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)

# ----------------- Metricas principales -----------------
st.subheader("\U0001F4CC Resumen general")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Articulos", len(df))
col2.metric("Periodo", str(int(df['Year'].min())) + " - " + str(int(df['Year'].max())))
col3.metric("Maximo de citas", int(df["Cited by"].max()))
col4.metric("Promedio de citas", round(df["Cited by"].mean(), 1))

st.divider()

# ----------------- Grafico 1: Publicaciones por anio -----------------
st.subheader("\U0001F4C5 Evolucion de publicaciones por anio")
st.caption("Muestra como ha crecido el interes academico en el tema a lo largo del tiempo.")
por_anio = df["Year"].value_counts().sort_index().reset_index()
por_anio.columns = ["Anio", "Cantidad"]
fig1 = px.bar(por_anio, x="Anio", y="Cantidad", text="Cantidad",
              color="Cantidad", color_continuous_scale="Blues")
fig1.update_traces(textposition="outside")
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# ----------------- Grafico 2: Articulos mas citados -----------------
st.subheader("\U0001F3C6 Top 10 articulos mas citados")
st.caption("Los articulos mas influyentes segun el numero de citas recibidas.")
top = df.nlargest(10, "Cited by")[["Title", "Cited by"]].copy()
top["Titulo corto"] = top["Title"].apply(lambda t: t[:60] + "..." if len(t) > 60 else t)
fig2 = px.bar(top, x="Cited by", y="Titulo corto", orientation="h",
              color="Cited by", color_continuous_scale="Teal",
              hover_data={"Title": True, "Titulo corto": False})
fig2.update_layout(yaxis=dict(autorange="reversed", title=""), showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# ----------------- Grafico 3: Autores mas frecuentes -----------------
st.subheader("\U0001F465 Autores con mas publicaciones")
st.caption("Investigadores que aparecen con mayor frecuencia en el conjunto de articulos.")
autores = []
for fila in df["Authors"].dropna():
    autores.extend([a.strip() for a in str(fila).split(";")])
conteo = Counter(autores).most_common(10)
df_aut = pd.DataFrame(conteo, columns=["Autor", "Publicaciones"])
fig3 = px.bar(df_aut, x="Publicaciones", y="Autor", orientation="h",
              color="Publicaciones", color_continuous_scale="Purples")
fig3.update_layout(yaxis=dict(autorange="reversed"), showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

# ----------------- Grafico 4: Palabras frecuentes en abstracts -----------------
st.subheader("\U0001F524 Temas predominantes (palabras frecuentes en abstracts)")
st.caption("Las palabras mas repetidas en los resumenes revelan los temas centrales de la literatura.")
texto = " ".join(df["Abstract"].dropna().astype(str)).lower()
palabras = re.findall(r"[a-z]{4,}", texto)
stopwords = {"this", "that", "with", "from", "were", "have", "been", "their",
             "which", "these", "such", "also", "based", "using", "results",
             "study", "paper", "data", "more", "than", "other", "into",
             "between", "however", "used", "model", "models", "method",
             "methods", "approach", "proposed", "system", "systems", "both",
             "each", "well", "show", "shown", "high", "different", "while",
             "they", "when", "where", "could", "would", "first", "case"}
palabras = [p for p in palabras if p not in stopwords]
top_palabras = Counter(palabras).most_common(15)
df_pal = pd.DataFrame(top_palabras, columns=["Palabra", "Frecuencia"])
fig4 = px.bar(df_pal, x="Palabra", y="Frecuencia",
              color="Frecuencia", color_continuous_scale="Oranges")
fig4.update_layout(showlegend=False)
st.plotly_chart(fig4, use_container_width=True)

# ----------------- Tabla de datos -----------------
st.divider()
st.subheader("\U0001F5C2\uFE0F Explorar el dataset completo")
st.caption("Tabla interactiva con los 20 articulos analizados. Puedes ordenar por cualquier columna.")
columnas = [c for c in ["Authors", "Title", "Year", "Source title", "Cited by", "DOI"] if c in df.columns]
st.dataframe(df[columnas], use_container_width=True, height=400)

# ----------------- Pie de pagina -----------------
st.divider()
st.markdown("""
---
**Desarrollado con** Streamlit - **Fuente de datos:** Scopus (Elsevier) - **Licencia:** Apache 2.0

*Proyecto academico - Analisis bibliometrico sobre mantenimiento predictivo con IA*
""")
