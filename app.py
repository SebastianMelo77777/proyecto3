import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

st.set_page_config(
    page_title="Proyecto 3 - Homicidios en Colombia 2024",
    page_icon="🕊️",
    layout="wide"
)


st.title(" Proyecto 3 - Análisis de Homicidios en Colombia")
st.markdown("### Datos del año 2024 · Visualización interactiva por municipio y departamento")

data = pd.read_csv("base3pro.csv")
gdf  = gpd.read_parquet('proy3.parquet')
# SELECTBOX JERÁRQUICO

departamentos = sorted(data["departamento"].unique().tolist())
departamento = st.selectbox("Seleccione un departamento:", departamentos)

municipios = sorted(data[data["departamento"] == departamento]["municipio"].unique().tolist())
municipio = st.selectbox("Seleccione un municipio:", municipios)

# FILTROS

filtro = data[(data["departamento"] == departamento) & (data["municipio"] == municipio)]

# =====================
# PUNTO 1: TASA DE HOMICIDIOS (MÉTRICA + CONTEXTO)
# =====================
tasa_mun = filtro["tasa_homicidios"].values[0]
tasa_dep = data[data["departamento"] == departamento]["tasa_homicidios"].mean()
tasa_nal = data["tasa_homicidios"].mean()

# --- Métrica principal ---
st.metric(
    label=f"Tasa de homicidios 2024 en {municipio} (por 100.000 hab.)",
    value=f"{tasa_mun:.2f}"
)

# --- Comparativo con Dept y Nacional ---
comparativo = pd.DataFrame({
    "Nivel": ["Municipio", "Departamento", "Nacional"],
    "Tasa": [tasa_mun, tasa_dep, tasa_nal]
})

fig = px.bar(
    comparativo,
    x="Nivel",
    y="Tasa",
    color="Nivel",
    text="Tasa",
    title="Comparación de la tasa de homicidios (x 100.000 hab.)",
    color_discrete_sequence=["#1D2783", "#3a4a52", "#b11738"]  # 👈 colores personalizados
)

fig.update_traces(texttemplate='%{text:.2f}', textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# PUNTO 2: TOP 10 MUNICIPIOS CON MÁS Y MENOS HOMICIDIOS

st.subheader(" Municipios con más y menos homicidios en 2024")

# Ordenamos por homicidios absolutos
ordenados = data.sort_values(by="homicidios", ascending=False)

top10_mas = ordenados.head(10)
top10_menos = ordenados.tail(10)

# --- TOP 10 MÁS HOMICIDIOS ---
fig_mas = px.bar(
    top10_mas.sort_values("homicidios"),  # invertimos para que más esté arriba
    x="homicidios",
    y="municipio",
    orientation="h",
    title="🔴 TOP 10 municipios con MÁS homicidios absolutos",
    text="homicidios",
    color_discrete_sequence=["#b11738"]  # rojo intenso
)
fig_mas.update_traces(textposition="outside")
st.plotly_chart(fig_mas, use_container_width=True)

# --- TOP 10 MENOS HOMICIDIOS ---
fig_menos = px.bar(
    top10_menos.sort_values("homicidios"),
    x="homicidios",
    y="municipio",
    orientation="h",
    title="🟢 TOP 10 municipios con MENOS homicidios absolutos",
    text="homicidios",
    color_discrete_sequence=["#1D2783"]  # azul profundo
)
fig_menos.update_traces(textposition="outside")
st.plotly_chart(fig_menos, use_container_width=True)


st.subheader("Distribución de homicidios en 2024")


# AGREGACIÓN POR DEPARTAMENTO

dep_data = (
    data.groupby("departamento")[["homicidios", "poblacion"]]
    .sum()
    .reset_index()
)

# Calculamos tasa departamental promedio
dep_data["tasa_homicidios"] = (dep_data["homicidios"] / dep_data["poblacion"] * 100000).round(2)

# =====================
# GRÁFICO DE BARRAS - POR DEPARTAMENTO
# =====================
fig_dep = px.bar(
    dep_data.sort_values("homicidios", ascending=False),
    x="homicidios",
    y="departamento",
    orientation="h",
    title="Total de homicidios por departamento (2024)",
    text="homicidios",
    color_discrete_sequence=["#1D2783"]
)
fig_dep.update_traces(textposition="outside")
st.plotly_chart(fig_dep, use_container_width=True)

fig,ax = plt.subplots(1,1, figsize = (10, 8))

gdf.plot(column = 'tasa_homicidios', ax = ax, missing_kwds={
        "color": "lightgrey",
        "edgecolor": "white",
      
    })
ax.set_axis_off()

st.pyplot(fig)


