import pandas as pd
import plotly_express as px
import seaborn as sns
import matplotlib as plt

# =========================================================
# PREPARAÇÃO DE DADOS
# =========================================================

def criar_faixas_uso(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 2, 4, 6, 8, 10]
    labels = ["0-2h", "2-4h", "4-6h", "6-8h", "8h+"]

    df["FAIXA_USO"] = pd.cut(
        df["MÉDIA_HORAS_USO_DIÁRIO"],
        bins=bins,
        labels=labels
    )

    return df


def criar_faixas_sono(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 4, 6, 8, 10]
    labels = ["<4h", "4-6h", "6-8h", "8h+"]

    df["FAIXA_SONO"] = pd.cut(
        df["HORAS_SONO_POR_NOITE"],
        bins=bins,
        labels=labels
    )

    return df


def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = criar_faixas_uso(df)
    df = criar_faixas_sono(df)
    return df


# =========================================================
# INSIGHT 1 — Uso vs Saúde Mental
# =========================================================

def uso_vs_saude(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby("FAIXA_USO")["PONTUAÇÃO_SAÚDE_MENTAL"]
        .agg(["mean", "median"])
        .reset_index()
        .round(2)
    )
    return df_grouped


# =========================================================
# INSIGHT 2 — Sono vs Saúde Mental
# =========================================================

def sono_vs_saude(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby("FAIXA_SONO")["PONTUAÇÃO_SAÚDE_MENTAL"]
        .median()
        .reset_index()
        .round(2)
    )
    return df_grouped


# =========================================================
# INSIGHT 3 — Uso + Sono (combinado)
# =========================================================

def uso_sono_vs_saude(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby(["FAIXA_USO", "FAIXA_SONO"])["PONTUAÇÃO_SAÚDE_MENTAL"]
        .median()
        .reset_index()
        .round(2)
    )
    return df_grouped


def uso_sono_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = uso_sono_vs_saude(df)

    df_pivot = df_grouped.pivot(
        index="FAIXA_SONO",
        columns="FAIXA_USO",
        values="PONTUAÇÃO_SAÚDE_MENTAL"
    )

    return df_pivot


# =========================================================
# INSIGHT 4 — Desempenho Acadêmico
# =========================================================

def impacto_academico_vs_saude(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby("AFETA_DESEMPENHO_ACADÊMICO")["PONTUAÇÃO_SAÚDE_MENTAL"]
        .mean()
        .reset_index()
        .round(2)
    )
    return df_grouped


def impacto_academico_vs_uso(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby("AFETA_DESEMPENHO_ACADÊMICO")["MÉDIA_HORAS_USO_DIÁRIO"]
        .mean()
        .reset_index()
        .round(2)
    )
    return df_grouped


def impacto_academico_percentual(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby(["FAIXA_USO", "AFETA_DESEMPENHO_ACADÊMICO"])
        .size()
        .groupby(level=0)
        .apply(lambda x: x / x.sum())
        .reset_index(name="PERCENTUAL")
    )
    return df_grouped


# =========================================================
# INSIGHT 5 — Plataforma
# =========================================================

def plataforma_vs_saude(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby("PLATAFORMA_MAIS_UTILIZADA")["PONTUAÇÃO_SAÚDE_MENTAL"]
        .mean()
        .reset_index()
        .sort_values(by="PONTUAÇÃO_SAÚDE_MENTAL", ascending=True)
    )
    return df_grouped


def plataforma_vs_uso(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby("PLATAFORMA_MAIS_UTILIZADA")["MÉDIA_HORAS_USO_DIÁRIO"]
        .mean()
        .reset_index()
        .round(2)
    )
    return df_grouped


# =========================================================
# MÉTRICAS GERAIS (para dashboard)
# =========================================================

def metricas_gerais(df: pd.DataFrame) -> dict:
    return {
        "media_saude_mental": df["PONTUAÇÃO_SAÚDE_MENTAL"].mean(),
        "mediana_saude_mental": df["PONTUAÇÃO_SAÚDE_MENTAL"].median(),
        "media_uso": df["MÉDIA_HORAS_USO_DIÁRIO"].mean(),
        "media_sono": df["HORAS_SONO_POR_NOITE"].mean(),
        "total_registros": len(df),
    }