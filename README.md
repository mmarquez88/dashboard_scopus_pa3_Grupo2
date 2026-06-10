# Dashboard Bibliometrico - Scopus

## Mantenimiento predictivo y deteccion de fallas con Inteligencia Artificial

Aplicacion web interactiva desarrollada con **Streamlit** que analiza articulos
cientificos extraidos de la base de datos **Scopus**.

### Pregunta de investigacion

Como contribuye el machine learning al mantenimiento predictivo y la deteccion
de fallas de equipos industriales?

### Palabras clave

`predictive maintenance` - `machine learning` - `fault detection` - `industry`

### Que muestra el dashboard

La aplicacion presenta cuatro visualizaciones interactivas:

1. **Evolucion de publicaciones por anio** - muestra el crecimiento del interes
   academico en el tema entre 2019 y 2026.
2. **Top 10 articulos mas citados** - identifica los trabajos mas influyentes.
3. **Autores mas productivos** - destaca a los investigadores con mayor presencia.
4. **Temas predominantes** - analiza las palabras mas frecuentes en los abstracts.

Ademas incluye metricas resumen y una tabla interactiva para explorar el dataset.

### Como ejecutar la aplicacion

**Opcion 1 - En linea (Streamlit Cloud):**
La aplicacion esta desplegada y disponible publicamente. Solo abre el enlace.

**Opcion 2 - De forma local:**

```bash
pip install -r requirements.txt
streamlit run app.py
```

Luego abre tu navegador en http://localhost:8501

### Datos

El archivo `scopus.csv` contiene 20 articulos cientificos vigentes (2019-2026)
con sus metadatos: autores, titulo, anio, revista, citas y abstract.

### Tecnologias utilizadas

- Python
- Streamlit (interfaz web)
- Pandas (procesamiento de datos)
- Plotly (visualizaciones interactivas)

### Licencia

Este proyecto esta bajo la licencia Apache 2.0. Ver el archivo `LICENSE`.

---

*Proyecto academico - ISIL - Curso de Data Mining Basico / IA*
