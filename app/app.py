import sys
import os

# Corrige path para importar src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px

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
# ⚙️ CONFIG
# =========================================================

st.set_page_config(
    page_title="Análise de Saúde Mental",
    layout="wide"
)

st.title("📊 Análise de Saúde Mental e Redes Sociais")

st.markdown("""
Este dashboard explora a relação entre o uso de redes sociais, sono e desempenho acadêmico,
e seus impactos na saúde mental de estudantes.
""")

st.markdown("---")

# =========================================================
# 📂 LOAD DATA
# =========================================================

@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/Jonasjkb/analise-dados-mental-health/refs/heads/main/data/processed_mental_health.csv")
    df = preparar_dados(df)
    return df

df = load_data()

# =========================================================
# 🎛️ FILTROS
# =========================================================

# --- BOTÃO PARA ATUALIZAR DADOS MANUALMENTE ---
if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()

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

st.sidebar.markdown("---")
st.sidebar.info("💡 Ajuste os filtros para explorar diferentes perfis de estudantes.")

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# =========================================================
# 📊 MÉTRICAS
# =========================================================

metrics = metricas_gerais(df_filtrado)

# =========================================================
# 📊 GRÁFICOS (pré-carregados)
# =========================================================

df_uso = uso_vs_saude(df_filtrado)
df_sono = sono_vs_saude(df_filtrado)
df_heatmap = uso_sono_heatmap(df_filtrado)
df_academico = impacto_academico_vs_saude(df_filtrado)
df_plataforma = plataforma_vs_saude(df_filtrado)

fig_uso = px.bar(
    df_uso.melt(id_vars="FAIXA_USO"),
    x="FAIXA_USO",
    y="value",
    color="variable",
    barmode="group",
    title="Uso de Redes Sociais vs Saúde Mental"
)

fig_sono = px.bar(
    df_sono,
    x="FAIXA_SONO",
    y="PONTUAÇÃO_SAÚDE_MENTAL",
    color="PONTUAÇÃO_SAÚDE_MENTAL",
    color_continuous_scale="RdYlGn",
    title="Sono vs Saúde Mental"
)

fig_heatmap = px.imshow(
    df_heatmap,
    text_auto=".2f",
    color_continuous_scale="RdYlGn",
    title="Uso + Sono vs Saúde Mental"
)

fig_academico = px.bar(
    df_academico,
    x="AFETA_DESEMPENHO_ACADÊMICO",
    y="PONTUAÇÃO_SAÚDE_MENTAL",
    color="AFETA_DESEMPENHO_ACADÊMICO",
    text="PONTUAÇÃO_SAÚDE_MENTAL",
    title="Impacto Acadêmico vs Saúde Mental"
)

fig_plataforma = px.bar(
    df_plataforma,
    x="PONTUAÇÃO_SAÚDE_MENTAL",
    y="PLATAFORMA_MAIS_UTILIZADA",
    orientation="h",
    color="PONTUAÇÃO_SAÚDE_MENTAL",
    color_continuous_scale="RdYlGn",
    title="Saúde Mental por Plataforma"
)

# =========================================================
# 🧭 ABAS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Visão Geral",
    "📱 Uso de Redes",
    "😴 Sono",
    "🔥 Uso + Sono",
    "🎓 Desempenho",
    "📱 Plataformas"
])

# =========================================================
# 📊 VISÃO GERAL
# =========================================================

with tab1:
    st.subheader("📊 Visão Geral")

    st.markdown("""
    Este projeto analisa como o uso de redes sociais impacta a saúde mental,
    considerando também fatores como sono e desempenho acadêmico.
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Saúde Mental", f"{metrics['media_saude_mental']:.2f}")
    col2.metric("Uso (h/dia)", f"{metrics['media_uso']:.2f}")
    col3.metric("Sono (h/noite)", f"{metrics['media_sono']:.2f}")
    col4.metric("Registros", metrics["total_registros"])

# =========================================================
# 📱 USO
# =========================================================

with tab2:
    st.subheader("📱 Uso de Redes Sociais")

    st.markdown("""
    🔍 **Insight:** Quanto maior o uso, menor a saúde mental.
    """)

    st.plotly_chart(fig_uso, use_container_width=True)

# =========================================================
# 😴 SONO
# =========================================================

with tab3:
    st.subheader("😴 Sono")

    st.markdown("""
    🧠 **Insight:** Dormir entre 6–8h melhora significativamente a saúde mental.
    """)

    st.plotly_chart(fig_sono, use_container_width=True)

# =========================================================
# 🔥 USO + SONO
# =========================================================

with tab4:
    st.subheader("🔥 Uso + Sono")

    st.markdown("""
    💡 **Insight avançado:** Alto uso + pouco sono = pior cenário.
    """)

    st.plotly_chart(fig_heatmap, use_container_width=True)

# =========================================================
# 🎓 DESEMPENHO
# =========================================================

with tab5:
    st.subheader("🎓 Desempenho Acadêmico")

    st.markdown("""
    📉 Estudantes impactados academicamente apresentam pior saúde mental.
    """)

    st.plotly_chart(fig_academico, use_container_width=True)

# =========================================================
# 📱 PLATAFORMAS
# =========================================================

with tab6:
    st.subheader("📱 Plataformas")

    st.markdown("""
    📊 O tipo de plataforma também influencia o bem-estar.
    """)

    st.plotly_chart(fig_plataforma, use_container_width=True)

# =========================================================
# 🧠 CONCLUSÃO
# =========================================================

st.markdown("---")

st.subheader("🧠 Conclusões Gerais")

st.markdown("""
- 📉 Uso excessivo impacta negativamente a saúde mental  
- 😴 Sono adequado é essencial  
- 🔥 Uso + pouco sono = pior cenário  
- 🎓 Impacto acadêmico está relacionado ao bem-estar  
- 📱 Plataforma também influencia  

👉 O equilíbrio é o fator mais importante.
""")

# --- SIDEBAR INFO ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Registros filtrados:** {len(df_filtrado)}")