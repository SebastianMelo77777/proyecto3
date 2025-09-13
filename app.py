import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, PowerNorm 

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

import plotly.graph_objects as go

tasa_mun = filtro["tasa_homicidios"].values[0]

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=tasa_mun,
    title={'text': f"Tasa de homicidios en {municipio} (x 100.000 hab.)"},
    gauge={
        'axis': {'range': [0, max(100, tasa_mun*1.5)]},  # escala automática
        'bar': {'color': "#D72638"},
        'steps': [
            {'range': [0, tasa_mun/2], 'color': "#90BE6D"},
            {'range': [tasa_mun/2, tasa_mun], 'color': "#F9C74F"},
            {'range': [tasa_mun, max(100, tasa_mun*1.5)], 'color': "#F94144"}
        ],
    }
))

st.plotly_chart(fig, use_container_width=True)


import plotly.express as px

# --- TOP 10 en número de homicidios ---
top_homicidios = data.sort_values("homicidios", ascending=False).head(10)

fig1 = px.bar(
    top_homicidios,
    x="municipio",
    y="homicidios",
    text="homicidios",
    color="homicidios",
    color_continuous_scale="Reds",
    title="🔴 TOP 10 municipios con MÁS homicidios absolutos"
)
fig1.update_traces(texttemplate='%{text}', textposition="outside")
fig1.update_layout(
    xaxis_title="Municipio",
    yaxis_title="Número de homicidios",
    showlegend=False
)

st.plotly_chart(fig1, use_container_width=True)


# --- TOP 10 en tasa de homicidios ---
top_tasa = data.sort_values("tasa_homicidios", ascending=False).head(10)

fig2 = px.bar(
    top_tasa,
    x="municipio",
    y="tasa_homicidios",
    text="tasa_homicidios",
    color="tasa_homicidios",
    color_continuous_scale="Reds",
    title="🔴 TOP 10 municipios con MAYOR tasa de homicidios (x 100.000 hab.)"
)
fig2.update_traces(texttemplate='%{text:.2f}', textposition="outside")
fig2.update_layout(
    xaxis_title="Municipio",
    yaxis_title="Tasa de homicidios (x 100.000 hab.)",
    showlegend=False
)

st.plotly_chart(fig2, use_container_width=True)

# --- TOP 10 municipios con MENOS homicidios ---
bottom_homicidios = data.sort_values("homicidios", ascending=True).head(10)

fig3 = px.bar(
    bottom_homicidios,
    x="municipio",
    y="homicidios",
    text="homicidios",
    color="homicidios",
    color_continuous_scale="Blues",
    title="🔵 TOP 10 municipios con MENOS homicidios absolutos"
)
fig3.update_traces(texttemplate='%{text}', textposition="outside")
fig3.update_layout(
    xaxis_title="Municipio",
    yaxis_title="Número de homicidios",
    showlegend=False
)

st.plotly_chart(fig3, use_container_width=True)


# --- TOP 10 municipios con MENOR tasa de homicidios ---
bottom_tasa = data.sort_values("tasa_homicidios", ascending=True).head(10)

fig4 = px.bar(
    bottom_tasa,
    x="municipio",
    y="tasa_homicidios",
    text="tasa_homicidios",
    color="tasa_homicidios",
    color_continuous_scale="Blues",
    title="🔵 TOP 10 municipios con MENOR tasa de homicidios (x 100.000 hab.)"
)
fig4.update_traces(texttemplate='%{text:.2f}', textposition="outside")
fig4.update_layout(
    xaxis_title="Municipio",
    yaxis_title="Tasa de homicidios (x 100.000 hab.)",
    showlegend=False
)

st.plotly_chart(fig4, use_container_width=True)



import plotly.express as px
import pandas as pd

# Asegurar agregación correcta por departamento (homicidios absolutos)
dep_data = (
    data.groupby("departamento", as_index=False)["homicidios"]
        .sum()
        .sort_values("homicidios", ascending=False)
)

# Si hay espacios/casos raros, normaliza nombres para evitar pérdidas por duplicados invisibles
dep_data["departamento"] = dep_data["departamento"].str.strip()

# Gráfico de barras VERTICAL (homicidios absolutos)
fig_dep = px.bar(
    dep_data,
    x="departamento",
    y="homicidios",
    text="homicidios",
    title=" Homicidios por departamento (2024)",
    color_discrete_sequence=["#4F46E5"],  # azul violeta legible en dark
)

# Estilo y legibilidad
fig_dep.update_traces(
    texttemplate="%{text:,}",
    textposition="outside",
    marker_line_color="#BD3009",
    marker_line_width=0.6,
)

# Eje X: departamentos legibles y completos (incluye Valle y Cundinamarca)
fig_dep.update_layout(
    xaxis_title="Departamento",
    yaxis_title="Homicidios (absolutos)",
    xaxis=dict(
        tickangle=-45,
        categoryorder="array",
        categoryarray=dep_data["departamento"].tolist(),  # respeta orden por valor
        tickfont=dict(size=11),
    ),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.10)", zeroline=False),
    margin=dict(l=10, r=10, t=60, b=80),
    font=dict(size=13),
)

# Para muchos departamentos, usar scroll horizontal o barras delgadas
fig_dep.update_layout(bargap=0.2)

st.plotly_chart(fig_dep, use_container_width=True)


# Mapa choropleth con normalización no lineal (Opción 2)
# Usa PowerNorm (gamma < 1) para realzar valores medios sin perder los altos.
# Alternativamente, puedes probar LogNorm para distribuciones muy sesgadas.

 # (o LogNorm)

# 1) Paleta pensada para fondo oscuro (bajo=gris claro → alto=rojo)
neutral_red = [
    "#F2F2F2",  # casi blanco
    "#E8E6E6",  # gris muy claro
    "#F5D6D6",  # rosa muy claro
    "#F2A7A7",  # salmón
    "#E35C5C",  # rojo medio
    "#C62828",  # rojo fuerte
    "#8B0000"   # rojo oscuro
]
cmap_neutral_red = LinearSegmentedColormap.from_list("NeutralRed", neutral_red)

# 2) Normalización no lineal
vals = gdf["tasa_homicidios"].astype(float).to_numpy()
vmin = max(0, np.nanmin(vals))
vmax = np.nanmax(vals)

# PowerNorm: gamma < 1 realza medios; prueba 0.5–0.8
norm = PowerNorm(gamma=0.6, vmin=vmin, vmax=vmax)

# (Alternativa) LogNorm si hay muchos ceros evita; usa un mínimo positivo:
# from matplotlib.colors import LogNorm
# norm = LogNorm(vmin=max(0.1, np.nanmin(vals[vals > 0])), vmax=vmax)

# 3) Crear figura y dibujar
fig, ax = plt.subplots(1, 1, figsize=(4, 4), dpi=220)

gdf.plot(
    column="tasa_homicidios",
    ax=ax,
    cmap=cmap_neutral_red,
    norm=norm,                      # << usamos 'norm' en lugar de vmin/vmax
    legend=True,
    edgecolor="#4A4A4A", linewidth=0.15,
    missing_kwds={
        "color": "#BDBDBD",
        "edgecolor": "#4A4A4A",
        "hatch": "///",
        "label": "Sin datos"
    }
)

# 4) Estética para fondo oscuro
ax.set_facecolor("none")
fig.patch.set_alpha(0)
ax.axis("off")

# 5) Colorbar legible
cb = ax.get_figure().axes[-1]
cb.tick_params(colors="#E6E6E6", labelsize=8)
cb.set_ylabel("tasa x 100k (escala no lineal)", color="#E6E6E6")
st.pyplot(fig)



