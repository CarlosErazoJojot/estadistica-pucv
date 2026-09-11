# ============================================================
#  pages/04_TCL.py
#  Teorema Central del Límite — Simulación
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box)

st.set_page_config(page_title="TCL · PUCV", page_icon="📐", layout="wide")
plt.rcParams.update(MATPLOTLIB_STYLE)
st.markdown(CSS_BASE, unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stPageLink"] a {
    background:#FFFFFF !important; border:1px solid #A50044 !important;
    border-radius:20px !important; padding:3px 12px !important;
}
div[data-testid="stPageLink"] a p {
    color:#A50044 !important; font-size:0.7rem !important; font-weight:600 !important; margin:0 !important;
}
div[data-testid="stPageLink"] a:hover { background:#A50044 !important; }
div[data-testid="stPageLink"] a:hover p { color:#FFFFFF !important; }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="page-header">
    <h2>📐 Teorema Central del Límite</h2>
    <div class="formula">X̄ ~ N(μ, σ²/n) &nbsp;·&nbsp; conforme n crece, cualquier distribución base converge</div>
</div>
""", unsafe_allow_html=True)

# ── Parámetros teóricos de cada distribución base ─────────────
DIST_PARAMS = {
    "Uniforme [0, 1]":          {"mu": 0.5, "sigma": np.sqrt(1/12)},
    "Exponencial (λ=1)":        {"mu": 1.0, "sigma": 1.0},
    "Binomial (n=10, p=0.3)":   {"mu": 3.0, "sigma": np.sqrt(10*0.3*0.7)},
    "Bernoulli (p=0.2)":        {"mu": 0.2, "sigma": np.sqrt(0.2*0.8)},
    "Chi² (df=2) — sesgada":    {"mu": 2.0, "sigma": 2.0},
}

def _muestrear(nombre, M, n, rng):
    if nombre == "Uniforme [0, 1]":         return rng.uniform(0, 1, (M, n))
    if nombre == "Exponencial (λ=1)":       return rng.exponential(1, (M, n))
    if nombre == "Binomial (n=10, p=0.3)":  return rng.binomial(10, 0.3, (M, n))
    if nombre == "Bernoulli (p=0.2)":       return rng.binomial(1, 0.2, (M, n))
    return rng.chisquare(2, (M, n))

# ✅ CORREGIDO: caché + una sola simulación por (dist, n, M, semilla).
# Antes se regeneraban las muestras dos veces (gráfico y tabla) sin caché.
@st.cache_data(show_spinner=False)
def medias_muestrales(nombre, M, n, semilla):
    rng = np.random.default_rng(semilla + n)   # semilla distinta por n, reproducible
    return _muestrear(nombre, M, n, rng).mean(axis=1)

with st.sidebar:
    st.markdown('<div class="seccion-label">CONFIGURACIÓN</div>', unsafe_allow_html=True)
    dist_nombre = st.selectbox("Distribución base", list(DIST_PARAMS.keys()))
    M           = st.select_slider("Número de muestras (M)",
                                   options=[200, 500, 1000, 2000, 5000], value=1000)
    st.markdown("---")
    st.markdown('<div class="seccion-label">TAMAÑOS DE MUESTRA</div>', unsafe_allow_html=True)
    ns_sel = st.multiselect("Mostrar n =", [1, 2, 5, 10, 30, 50], default=[1, 5, 10, 30])
    if not ns_sel:
        ns_sel = [1, 30]
    ns_sel = sorted(ns_sel)
    st.markdown("---")
    semilla = int(st.number_input("Semilla aleatoria", value=42, step=1))
    st.caption("Misma semilla ⇒ mismos resultados. Útil para reproducir en clases.")
    st.markdown("---")
    st.markdown('<div class="seccion-label">IR A</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Inicio", icon=":material/home:")
    st.page_link("pages/05_Continuas.py", label="Continuas", icon=":material/arrow_back:")
    st.page_link("pages/07_Distribuciones_Muestrales.py", label="Distribuciones Muestrales", icon=":material/arrow_forward:")

    st.markdown('<div class="firma">Carlos Erazo Jojot · PUCV</div>',
                unsafe_allow_html=True)

mu_pob    = DIST_PARAMS[dist_nombre]["mu"]
sigma_pob = DIST_PARAMS[dist_nombre]["sigma"]

# Simular una sola vez por n; el resultado se reutiliza en gráfico y tabla
resultados = {n: medias_muestrales(dist_nombre, M, n, semilla) for n in ns_sel}

n_cols = min(len(ns_sel), 4)
n_rows = int(np.ceil(len(ns_sel) / n_cols))

fig, axes = plt.subplots(n_rows, n_cols, figsize=(4.5*n_cols, 4.2*n_rows), squeeze=False)
fig.suptitle(f"Base: {dist_nombre}   |   μ = {mu_pob:.3f}, σ = {sigma_pob:.3f}   |   M = {M}",
             fontsize=11.5, color=PUCV_GOLD, y=1.01)

for idx, n in enumerate(ns_sel):
    r, c    = divmod(idx, n_cols)
    ax      = axes[r][c]
    medias  = resultados[n]
    sig_teo = sigma_pob / np.sqrt(n)

    ax.hist(medias, bins=40, density=True, color=AZUL_BARRA,
            edgecolor="#FFFFFF", linewidth=0.4, alpha=0.75, zorder=3)

    xr = np.linspace(medias.min(), medias.max(), 300)
    ax.plot(xr, norm.pdf(xr, mu_pob, sig_teo), color=PUCV_GOLD, linewidth=2.2,
            zorder=5, label=f"N({mu_pob:.2f}, {sig_teo:.3f}²)")
    ax.axvline(medias.mean(), color=PUCV_RED, linestyle="--", linewidth=1.3,
               alpha=0.9, label=f"X̄ obs = {medias.mean():.3f}")

    ax.set_title(f"n = {n}", fontsize=11, color=PUCV_GOLD if n >= 30 else TEXT_LIGHT, pad=6)
    ax.set_xlabel("X̄", fontsize=9)
    ax.set_ylabel("Densidad", fontsize=9)
    ax.legend(fontsize=7.5, loc="upper right", framealpha=0.25, edgecolor=PUCV_GOLD)
    ax.grid(axis="y", alpha=0.4)

for idx in range(len(ns_sel), n_rows * n_cols):
    r, c = divmod(idx, n_cols)
    axes[r][c].set_visible(False)

fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="seccion-label">DESVIACIÓN ESTÁNDAR OBSERVADA vs TEÓRICA (σ/√n)</div>',
            unsafe_allow_html=True)

cols = st.columns(len(ns_sel))
for i, n in enumerate(ns_sel):
    medias  = resultados[n]          # ← reutiliza, no re-simula
    sig_teo = sigma_pob / np.sqrt(n)
    color   = PUCV_GOLD if n >= 30 else AZUL_CLARO
    cols[i].markdown(f"""
    <div class="stat-box" style="border-top-color:{color};">
        <div class="label">n = {n}</div>
        <div class="value" style="color:{color};">{medias.std(ddof=1):.4f}</div>
        <div style="font-size:0.65rem;color:#4A688F;margin-top:4px;">teórica: {sig_teo:.4f}</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("¿Qué muestra esta simulación?"):
    st.markdown(f"""
    Cada panel toma **{M} muestras** de tamaño n desde una distribución
    **{dist_nombre}** (μ = {mu_pob:.3f}, σ = {sigma_pob:.3f}) y grafica el
    histograma de las **medias muestrales** X̄.

    La curva dorada es la Normal que predice el TCL:

    > X̄ ~ N(μ, σ²/n)

    **Qué observar:**
    - **n = 1:** la distribución de X̄ coincide con la distribución original.
      Con base Bernoulli o Chi² el histograma no se parece en nada a una Normal.
    - **n creciente:** el histograma se va simetrizando y concentrando.
    - **n ≥ 30 (título dorado):** el ajuste a la Normal es bueno sin importar
      la forma de la distribución base.
    - La desviación observada converge a σ/√n, no a σ.

    **Advertencia pedagógica:** el umbral n ≥ 30 es una regla práctica, no un
    teorema. Con distribuciones muy asimétricas (Chi² df=2) puede requerirse
    un n mayor; compara n = 30 y n = 50 con esa base para verlo.
    """)
