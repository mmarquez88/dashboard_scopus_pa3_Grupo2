# =============================================================
# Dashboard de Analisis Bibliometrico - Scopus
# Tema: Mantenimiento predictivo y deteccion de fallas con IA
# Curso: Data Mining Basico / Algoritmo y Estructura de Datos Basados en IA
# Autor: Marcelo Marquez
# =============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# ----------------- Configuracion de la pagina -----------------
st.set_page_config(
    page_title="Dashboard Scopus - Mantenimiento Predictivo con IA",
    page_icon="\U0001F527",
    layout="wide",
    initial_sidebar_state="expanded"
)

URL_GITHUB = "https://raw.githubusercontent.com/mmarquez88/dashboard_scopus_pa3_Grupo2/main/scopus.csv"

# ----------------- Estilos personalizados (CSS) -----------------
st.markdown("""
<style>
    /* Paleta industrial: azul acero + naranja seguridad */
    .stApp {
        background: linear-gradient(160deg, #0d1b2a 0%, #1b263b 100%);
    }
    /* Tarjeta de pregunta de investigacion */
    .tarjeta-pregunta {
        background: linear-gradient(135deg, rgba(30,58,95,0.6), rgba(27,38,59,0.6));
        border: 1px solid #2e6da4;
        border-left: 5px solid #ff9505;
        border-radius: 14px;
        padding: 22px 28px;
        margin: 10px 0 18px 0;
    }
    .label-pregunta {
        color: #ff9505;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 8px;
    }
    .texto-pregunta {
        color: #e0e1dd;
        font-size: 20px;
        font-weight: 500;
        text-align: center;
        line-height: 1.5;
    }
    /* Chips de keywords */
    .chip {
        display: inline-block;
        background: rgba(46,109,164,0.25);
        color: #7cc4f0;
        border: 1px solid #2e6da4;
        border-radius: 20px;
        padding: 6px 16px;
        margin: 4px 6px 4px 0;
        font-family: monospace;
        font-size: 14px;
        font-weight: 600;
    }
    /* Titulos de seccion */
    h1, h2, h3 { color: #e0e1dd !important; }
    /* Tarjetas de metricas */
    [data-testid="stMetric"] {
        background: rgba(46,109,164,0.15);
        border: 1px solid #2e6da4;
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="stMetricValue"] { color: #ff9505 !important; }
    [data-testid="stMetricLabel"] { color: #a9c5e0 !important; }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0a1420;
        border-right: 1px solid #2e6da4;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: Fuente de datos y filtros -----------------
st.sidebar.markdown("## \U0001F4C1 Fuente de datos")
fuente = st.sidebar.radio(
    "Elige como cargar el CSV:",
    ["Dataset incluido", "Cargar archivo local", "URL publica de GitHub"]
)

@st.cache_data
def cargar(url):
    return pd.read_csv(url)

df = None
if fuente == "Dataset incluido":
    try:
        df = cargar(URL_GITHUB)
        st.sidebar.success(f"\u2705 Dataset oficial cargado \u2014 {len(df)} articulos")
    except Exception as e:
        st.sidebar.error("No se pudo cargar desde GitHub.")
        st.sidebar.caption(str(e))
elif fuente == "Cargar archivo local":
    up = st.sidebar.file_uploader("Sube tu scopus.csv", type=["csv"])
    if up is not None:
        df = pd.read_csv(up)
        st.sidebar.success(f"\u2705 Archivo cargado \u2014 {len(df)} articulos")
else:
    url = st.sidebar.text_input("Pega la URL RAW del CSV")
    if url:
        try:
            df = cargar(url)
            st.sidebar.success(f"\u2705 Cargado \u2014 {len(df)} articulos")
        except Exception as e:
            st.sidebar.error(str(e))

# ----------------- Encabezado principal -----------------
st.markdown("""
<div style='text-align:center; margin-bottom:6px;'>
    <span style='font-size:46px;'>\U0001F527</span>
    <span style='font-size:42px; font-weight:800; color:#e0e1dd; vertical-align:middle;'>
        Mantenimiento Predictivo con IA</span>
</div>
<p style='text-align:center; color:#7cc4f0; font-size:17px; margin-top:0;'>
    Analisis bibliometrico \u00b7 Scopus \u00b7 2019\u20132026</p>
""", unsafe_allow_html=True)

# Tarjeta de pregunta de investigacion
st.markdown("""
<div class='tarjeta-pregunta'>
    <div class='label-pregunta'>\U0001F52C PREGUNTA DE INVESTIGACION</div>
    <div class='texto-pregunta'>
        \u00bfComo contribuye el machine learning al mantenimiento predictivo y la
        deteccion temprana de fallas en equipos industriales?
    </div>
</div>
""", unsafe_allow_html=True)

# Chips de keywords
with st.expander("\U0001F4CC Keywords utilizadas", expanded=True):
    st.markdown("""
    <span class='chip'>predictive maintenance</span>
    <span class='chip'>machine learning</span>
    <span class='chip'>fault detection</span>
    <span class='chip'>industry</span>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='background:rgba(46,109,164,0.15); border-radius:10px; padding:14px 18px;
    color:#a9c5e0; margin-top:10px; font-size:14px;'>
    Puedes usar el dataset incluido, cargar un CSV local desde la barra lateral o leerlo
    desde una URL RAW de GitHub. El dashboard detecta automaticamente columnas clave como
    autores, titulo, ano, citas y abstract.
    </div>
    """, unsafe_allow_html=True)

# ----------------- Validacion -----------------
if df is None:
    st.info("\U0001F448 Selecciona una fuente de datos en la barra lateral para comenzar.")
    st.stop()

df.columns = [c.strip() for c in df.columns]
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# ----------------- FILTROS en sidebar -----------------
st.sidebar.markdown("---")
st.sidebar.markdown("## \U0001F9F0 Filtros")

anio_min, anio_max = int(df["Year"].min()), int(df["Year"].max())
if anio_min < anio_max:
    rango = st.sidebar.slider("Rango de anos", anio_min, anio_max, (anio_min, anio_max))
else:
    rango = (anio_min, anio_max)

tipos_disponibles = sorted(df["Document Type"].dropna().unique().tolist())
tipos_sel = st.sidebar.multiselect("Tipo de documento", tipos_disponibles, default=tipos_disponibles)

# Aplicar filtros
df_f = df[(df["Year"] >= rango[0]) & (df["Year"] <= rango[1])]
if tipos_sel:
    df_f = df_f[df_f["Document Type"].isin(tipos_sel)]

st.sidebar.markdown(f"**Mostrando:** {len(df_f)} articulos")

if len(df_f) == 0:
    st.warning("No hay articulos con los filtros seleccionados. Ajusta los filtros.")
    st.stop()

# ----------------- Resumen del dataset (metricas) -----------------
st.markdown("---")
st.markdown("## \U0001F4CA Resumen del dataset")
c1, c2, c3, c4 = st.columns(4)
c1.metric("\U0001F4C4 Articulos", len(df_f))
c2.metric("\U0001F4C5 Periodo", f"{int(df_f['Year'].min())}\u2013{int(df_f['Year'].max())}")
c3.metric("\U0001F3C6 Max. citas", int(df_f["Cited by"].max()))
c4.metric("\U0001F4C8 Citas promedio", round(df_f["Cited by"].mean(), 1))

# Plantilla oscura para todos los graficos
PLANTILLA = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e0e1dd"),
    title_font=dict(color="#e0e1dd")
)

# ----------------- Grafico 1: Publicaciones por ano -----------------
st.markdown("---")
st.markdown("### \U0001F4C5 Evolucion de publicaciones por ano")
st.caption("Refleja como ha crecido el interes academico en el tema a lo largo del tiempo.")
por_anio = df_f["Year"].value_counts().sort_index().reset_index()
por_anio.columns = ["Ano", "Cantidad"]
fig1 = px.area(por_anio, x="Ano", y="Cantidad", markers=True)
fig1.update_traces(line_color="#ff9505", fillcolor="rgba(255,149,5,0.2)",
                   marker=dict(size=9, color="#ff9505"))
fig1.update_layout(**PLANTILLA)
st.plotly_chart(fig1, use_container_width=True)

# ----------------- Grafico 2: Top citados -----------------
st.markdown("### \U0001F3C6 Articulos mas citados")
st.caption("Los trabajos mas influyentes segun el numero de citas recibidas.")
top = df_f.nlargest(10, "Cited by")[["Title", "Cited by"]].copy()
top["Corto"] = top["Title"].apply(lambda t: t[:55] + "..." if len(t) > 55 else t)
fig2 = px.bar(top, x="Cited by", y="Corto", orientation="h",
              color="Cited by", color_continuous_scale=["#1b263b", "#2e6da4", "#7cc4f0"],
              hover_data={"Title": True, "Corto": False})
fig2.update_layout(yaxis=dict(autorange="reversed", title=""), **PLANTILLA)
st.plotly_chart(fig2, use_container_width=True)

# ----------------- Grafico 3: Autores -----------------
st.markdown("### \U0001F465 Autores mas productivos")
st.caption("Investigadores con mayor presencia en el conjunto analizado.")
autores = []
for fila in df_f["Authors"].dropna():
    autores.extend([a.strip() for a in str(fila).split(";")])
conteo = Counter(autores).most_common(10)
df_aut = pd.DataFrame(conteo, columns=["Autor", "Publicaciones"])
fig3 = px.bar(df_aut, x="Publicaciones", y="Autor", orientation="h",
              color="Publicaciones", color_continuous_scale=["#1b263b", "#ff9505"])
fig3.update_layout(yaxis=dict(autorange="reversed"), **PLANTILLA)
st.plotly_chart(fig3, use_container_width=True)

# ----------------- Grafico 4: Palabras frecuentes -----------------
st.markdown("### \U0001F524 Temas predominantes en los abstracts")
st.caption("Las palabras mas repetidas en los resumenes revelan los temas centrales de la literatura.")
texto = " ".join(df_f["Abstract"].dropna().astype(str)).lower()
palabras = re.findall(r"[a-z]{4,}", texto)
stop = {"this","that","with","from","were","have","been","their","which","these","such",
        "also","based","using","results","study","paper","data","more","than","other",
        "into","between","however","used","model","models","method","methods","approach",
        "proposed","system","systems","both","each","well","show","shown","high",
        "different","while","they","when","where","could","would","first","case","such",
        "various","through","provide","provides","including","present","application"}
palabras = [p for p in palabras if p not in stop]
top_pal = Counter(palabras).most_common(15)
df_pal = pd.DataFrame(top_pal, columns=["Palabra", "Frecuencia"])
fig4 = px.bar(df_pal, x="Palabra", y="Frecuencia",
              color="Frecuencia", color_continuous_scale=["#2e6da4", "#ff9505"])
fig4.update_layout(**PLANTILLA)
st.plotly_chart(fig4, use_container_width=True)

# ----------------- Tabla -----------------
st.markdown("---")
st.markdown("### \U0001F5C2\uFE0F Explorar el dataset")
st.caption("Tabla interactiva con los articulos analizados. Ordena por cualquier columna.")
cols = [c for c in ["Authors", "Title", "Year", "Source title", "Cited by", "DOI"] if c in df_f.columns]
st.dataframe(df_f[cols], use_container_width=True, height=380)

# ----------------- Pie -----------------
st.markdown("---")
st.markdown("""
<p style='text-align:center; color:#a9c5e0; font-size:13px;'>
Desarrollado con Streamlit \u00b7 Fuente: Scopus (Elsevier) \u00b7 Licencia Apache 2.0<br>
Proyecto academico \u00b7 ISIL \u00b7 Mantenimiento predictivo con Inteligencia Artificial
</p>
""", unsafe_allow_html=True)
