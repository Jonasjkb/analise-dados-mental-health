import streamlit as st
import pandas as pd
import plotly.express as px

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analise import (
    preparar_dados,
    uso_vs_saude,
    sono_vs_saude,
    uso_sono_heatmap,
    impacto_academico_vs_saude,
    plataforma_vs_saude,
    metricas_gerais
)

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Análise de Saúde Mental",
    layout="wide"
)

st.title("📊 Análise de Saúde Mental e Redes Sociais")

# =========================================================
# CARREGAMENTO DE DADOS
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/Jonasjkb/analise-dados-mental-health/refs/heads/main/data/raw_mental_health.csv")
    df = preparar_dados(df)
    return df

df = load_data()

# =========================================================
# FILTROS
# =========================================================

st.sidebar.header("🔎 Filtros")

genero = st.sidebar.multiselect(
    "Gênero",
    options=df["GÊNERO"].unique(),
    default=df["GÊNERO"].unique()
)

nivel = st.sidebar.multiselect(
    "Nível Acadêmico",
    options=df["NÍVEL_ACADÊMICO"].unique(),
    default=df["NÍVEL_ACADÊMICO"].unique()
)

df_filtrado = df[
    (df["GÊNERO"].isin(genero)) &
    (df["NÍVEL_ACADÊMICO"].isin(nivel))
]

# =========================================================
# KPIs
# =========================================================

st.subheader("📌 Métricas Gerais")

metrics = metricas_gerais(df_filtrado)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Saúde Mental (Média)", f"{metrics['media_saude_mental']:.2f}")
col2.metric("Uso Médio (h/dia)", f"{metrics['media_uso']:.2f}")
col3.metric("Sono Médio (h/noite)", f"{metrics['media_sono']:.2f}")
col4.metric("Total de Registros", metrics["total_registros"])

# =========================================================
# GRÁFICOS
# =========================================================

st.subheader("📈 Análises")

# 🔹 Uso vs Saúde
df_uso = uso_vs_saude(df_filtrado)

fig_uso = px.bar(
    df_uso.melt(id_vars="FAIXA_USO"),
    x="FAIXA_USO",
    y="value",
    color="variable",
    barmode="group",
    title="Uso de Redes Sociais vs Saúde Mental"
)

st.plotly_chart(fig_uso, use_container_width=True)

# 🔹 Sono vs Saúde
df_sono = sono_vs_saude(df_filtrado)

fig_sono = px.bar(
    df_sono,
    x="FAIXA_SONO",
    y="PONTUAÇÃO_SAÚDE_MENTAL",
    color="PONTUAÇÃO_SAÚDE_MENTAL",
    color_continuous_scale="RdYlGn",
    title="Sono vs Saúde Mental"
)

st.plotly_chart(fig_sono, use_container_width=True)

# 🔹 Heatmap (Uso + Sono)
df_heatmap = uso_sono_heatmap(df_filtrado)

fig_heatmap = px.imshow(
    df_heatmap,
    text_auto=".2f",
    color_continuous_scale="RdYlGn",
    title="Uso + Sono vs Saúde Mental"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# 🔹 Impacto Acadêmico
df_academico = impacto_academico_vs_saude(df_filtrado)

fig_academico = px.bar(
    df_academico,
    x="AFETA_DESEMPENHO_ACADÊMICO",
    y="PONTUAÇÃO_SAÚDE_MENTAL",
    color="AFETA_DESEMPENHO_ACADÊMICO",
    text="PONTUAÇÃO_SAÚDE_MENTAL",
    title="Impacto Acadêmico vs Saúde Mental"
)

st.plotly_chart(fig_academico, use_container_width=True)

# 🔹 Plataforma
df_plataforma = plataforma_vs_saude(df_filtrado)

fig_plataforma = px.bar(
    df_plataforma,
    x="PONTUAÇÃO_SAÚDE_MENTAL",
    y="PLATAFORMA_MAIS_UTILIZADA",
    orientation="h",
    color="PONTUAÇÃO_SAÚDE_MENTAL",
    color_continuous_scale="RdYlGn",
    title="Saúde Mental por Plataforma"
)

st.plotly_chart(fig_plataforma, use_container_width=True)