# ============================================================
#  pages/01_Binomial.py
#  Distribución Binomial — X ~ B(n, p)
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import binom
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box, prob_box)

st.set_page_config(page_title="Binomial · PUCV", page_icon="📦", layout="wide")
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
    <h2>📦 Distribución Binomial</h2>
    <div class="formula">X ~ B(n, p) &nbsp;·&nbsp; P(X = k) = C(n,k) · pᵏ · (1−p)ⁿ⁻ᵏ</div>
</div>
""", unsafe_allow_html=True)

N_MAX = 40

with st.sidebar:
    st.markdown('<div class="seccion-label">PARÁMETROS · X ~ B(n, p)</div>', unsafe_allow_html=True)
    n = st.slider("n — número de ensayos", 1, N_MAX, 10, 1)
    p = st.slider("p — probabilidad de éxito", 0.01, 0.99, 0.40, 0.01, format="%.2f")

    st.markdown("---")
    st.markdown('<div class="seccion-label">CONSULTA</div>', unsafe_allow_html=True)
    # ✅ CORREGIDO: rango fijo 0..N_MAX + clamp. Antes max_value=n hacía que el
    # valor guardado quedara fuera de rango al bajar n.
    k_raw   = st.slider("k — valor a consultar", 0, N_MAX, 4, 1)
    k_query = min(k_raw, n)
    if k_raw > n:
        st.info(f"k no puede exceder n = {n}. Se usa k = {k_query}.")

    st.markdown("---")
    vista = st.radio("Vista del gráfico", ["PMF — P(X = k)", "CDF — P(X ≤ k)"], index=0)
    st.markdown("---")
    st.markdown('<div class="seccion-label">IR A</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Inicio", icon=":material/home:")
    st.page_link("pages/02_Poisson.py", label="Poisson", icon=":material/arrow_forward:")

    st.markdown('<div class="firma">Carlos Erazo Jojot · PUCV</div>',
                unsafe_allow_html=True)

# ── Cálculos ──────────────────────────────────────────────────
ks    = np.arange(0, n + 1)
pmfs  = binom.pmf(ks, n, p)
cdfs  = binom.cdf(ks, n, p)
usar  = pmfs if "PMF" in vista else cdfs

media = n * p
var   = n * p * (1 - p)
std   = np.sqrt(var)

# Moda: floor((n+1)p); si (n+1)p es entero hay dos modas
mp    = (n + 1) * p
if abs(mp - round(mp)) < 1e-12 and 0 < round(mp) <= n:
    modas = [int(round(mp)) - 1, int(round(mp))]
else:
    modas = [int(np.floor(mp))]

p_exacta = binom.pmf(k_query, n, p)
p_acum   = binom.cdf(k_query, n, p)
p_cola   = binom.sf(k_query - 1, n, p)      # P(X ≥ k), estable numéricamente

col_g, col_p = st.columns([3, 1], gap="large")

with col_g:
    fig, ax = plt.subplots(figsize=(10, 5))
    colores = [PUCV_GOLD if k == k_query else AZUL_CLARO if k in modas else AZUL_BARRA for k in ks]
    ax.bar(ks, usar, color=colores, edgecolor="#FFFFFF", linewidth=0.6, width=0.65, zorder=3)

    ax.text(k_query, usar[k_query] + max(usar)*0.025, f"{usar[k_query]:.4f}",
            ha="center", va="bottom", fontsize=9, color=PUCV_GOLD, fontweight="bold")
    ax.axvline(media, color=PUCV_RED, linestyle="--", linewidth=1.5, alpha=0.8)

    ax.set_xlabel("k  (número de éxitos)", fontsize=11, labelpad=8)
    ax.set_ylabel("P(X = k)" if "PMF" in vista else "P(X ≤ k)", fontsize=11, labelpad=8)
    ax.set_xlim(-0.7, n + 0.7)
    ax.grid(axis="y", zorder=0, alpha=0.5)
    ax.set_xticks(ks if n <= 25 else np.arange(0, n + 1, max(1, n // 15)))

    moda_txt = ", ".join(str(m) for m in modas)
    ax.legend(handles=[
        Patch(facecolor=PUCV_GOLD,  label=f"k = {k_query}  (seleccionado)"),
        Patch(facecolor=AZUL_CLARO, label=f"k = {moda_txt}  (moda)"),
        Patch(facecolor=AZUL_BARRA, label="resto de valores"),
        Patch(facecolor="none", edgecolor=PUCV_RED, label=f"E[X] = {media:.3f}"),
    ], fontsize=8.5, loc="upper right", framealpha=0.25, edgecolor=PUCV_GOLD)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(stat_box("E[X] = n·p",        f"{media:.4f}", PUCV_GOLD),  unsafe_allow_html=True)
    c2.markdown(stat_box("Var(X) = n·p·(1−p)", f"{var:.4f}",  AZUL_CLARO), unsafe_allow_html=True)
    c3.markdown(stat_box("σ",                  f"{std:.4f}",  AZUL_CLARO), unsafe_allow_html=True)
    c4.markdown(stat_box("Moda",               moda_txt,      AZUL_CLARO),   unsafe_allow_html=True)

with col_p:
    st.markdown(f'<div class="seccion-label">PROBABILIDADES · k = {k_query}</div>', unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X = {k_query})", f"{p_exacta:.6f}", PUCV_GOLD),  unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X ≤ {k_query})", f"{p_acum:.6f}",   AZUL_CLARO), unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X ≥ {k_query})", f"{p_cola:.6f}",   PUCV_RED),   unsafe_allow_html=True)

    st.markdown(f"""
    <div class="formula-box">
        <div class="titulo">DESARROLLO</div>
        <div class="cuerpo">
            P(X = k) = C(n,k) · pᵏ · (1−p)ⁿ⁻ᵏ<br><br>
            <span style="color:#A50044;">Para n = {n}, p = {p:.2f}, k = {k_query}:</span><br>
            <span style="color:#003087;font-weight:600;padding-left:12px;">
                C({n},{k_query}) · {p:.2f}^{k_query} · {1-p:.2f}^{n-k_query}
            </span><br>
            <span style="color:#003087;font-weight:600;padding-left:12px;">
                = {binom.pmf(k_query, n, p) / (p**k_query * (1-p)**(n-k_query)):.0f}
                · {p**k_query:.6g} · {(1-p)**(n-k_query):.6g}
            </span><br>
            <span style="color:{PUCV_GOLD};font-weight:bold;padding-left:12px;">
                = {p_exacta:.6f}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("¿Cuándo usar la distribución Binomial?"):
    st.markdown(f"""
    Modela el **número de éxitos** en `n` ensayos independientes, cada uno con
    probabilidad `p` de éxito.

    **Condiciones (ensayos de Bernoulli):**
    - Número fijo de ensayos `n`
    - Ensayos independientes entre sí
    - Solo dos resultados: éxito / fracaso
    - `p` constante en todos los ensayos

    **Ejemplos:**
    - Piezas defectuosas en un lote de {n} unidades
    - Respuestas correctas en una prueba de {n} preguntas de alternativas
    - Clientes que compran de {n} visitantes

    **Cuándo NO usarla:** si el muestreo es **sin reposición** desde una población
    finita pequeña, los ensayos dejan de ser independientes y corresponde la
    **Hipergeométrica**. Si `n` es muy grande y `p` muy pequeño, la **Poisson**
    con λ = n·p = {n*p:.2f} es una buena aproximación.
    """)
