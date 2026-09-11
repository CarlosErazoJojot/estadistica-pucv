# ============================================================
#  pages/02_Poisson.py
#  Distribución Poisson — X ~ Poisson(λ)
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import poisson, binom
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box, prob_box)

st.set_page_config(page_title="Poisson · PUCV", page_icon="⚡", layout="wide")
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
    <h2>⚡ Distribución Poisson</h2>
    <div class="formula">X ~ Poisson(λ) &nbsp;·&nbsp; P(X = k) = e⁻ᵝ · λᵏ / k!</div>
</div>
""", unsafe_allow_html=True)

K_MAX = 45

with st.sidebar:
    st.markdown('<div class="seccion-label">PARÁMETROS · X ~ Poisson(λ)</div>', unsafe_allow_html=True)
    lam = st.slider("λ — tasa media de ocurrencia", 0.1, 20.0, 3.0, 0.1, format="%.1f")

    st.markdown("---")
    st.markdown('<div class="seccion-label">CONSULTA</div>', unsafe_allow_html=True)
    # ✅ Rango fijo: el slider nunca queda fuera de rango al mover λ
    k_query = st.slider("k — valor a consultar", 0, K_MAX, 3, 1)

    st.markdown("---")
    vista = st.radio("Vista del gráfico", ["PMF — P(X = k)", "CDF — P(X ≤ k)"])
    st.markdown("---")
    st.markdown('<div class="seccion-label">IR A</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Inicio", icon="🏠")
    st.page_link("pages/01_Binomial.py", label="Binomial", icon="◀")
    st.page_link("pages/03_Geometrica.py", label="Geométrica", icon="▶")

    st.markdown('<div class="firma">Carlos Erazo Jojot · PUCV</div>',
                unsafe_allow_html=True)

# Ventana visible adaptativa (independiente del rango del slider)
k_vis = int(min(K_MAX, max(k_query + 4, np.ceil(lam + 4*np.sqrt(lam)) + 2)))
ks    = np.arange(0, k_vis + 1)
pmfs  = poisson.pmf(ks, lam)
cdfs  = poisson.cdf(ks, lam)
usar  = pmfs if "PMF" in vista else cdfs

# Moda: floor(λ); si λ es entero hay dos modas (λ−1 y λ)
if abs(lam - round(lam)) < 1e-9 and lam >= 1:
    modas = [int(round(lam)) - 1, int(round(lam))]
else:
    modas = [int(np.floor(lam))]

p_exacta = poisson.pmf(k_query, lam)
p_acum   = poisson.cdf(k_query, lam)
p_cola   = poisson.sf(k_query - 1, lam)

col_g, col_p = st.columns([3, 1], gap="large")

with col_g:
    fig, ax = plt.subplots(figsize=(10, 5))
    colores = [PUCV_GOLD if k == k_query else AZUL_CLARO if k in modas else AZUL_BARRA for k in ks]
    ax.bar(ks, usar, color=colores, edgecolor="#FFFFFF", linewidth=0.6, width=0.65, zorder=3)

    if k_query <= k_vis:
        ax.text(k_query, usar[k_query] + max(usar)*0.025, f"{usar[k_query]:.4f}",
                ha="center", va="bottom", fontsize=9, color=PUCV_GOLD, fontweight="bold")
    ax.axvline(lam, color=PUCV_RED, linestyle="--", linewidth=1.5, alpha=0.8)

    ax.set_xlabel("k  (número de eventos)", fontsize=11, labelpad=8)
    ax.set_ylabel("P(X = k)" if "PMF" in vista else "P(X ≤ k)", fontsize=11, labelpad=8)
    ax.set_xlim(-0.7, k_vis + 0.7)
    ax.grid(axis="y", zorder=0, alpha=0.5)

    moda_txt = ", ".join(str(m) for m in modas)
    ax.legend(handles=[
        Patch(facecolor=PUCV_GOLD,  label=f"k = {k_query}  (seleccionado)"),
        Patch(facecolor=AZUL_CLARO, label=f"k = {moda_txt}  (moda)"),
        Patch(facecolor=AZUL_BARRA, label="resto de valores"),
        Patch(facecolor="none", edgecolor=PUCV_RED, label=f"λ = E[X] = {lam:.1f}"),
    ], fontsize=8.5, loc="upper right", framealpha=0.25, edgecolor=PUCV_GOLD)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(stat_box("E[X] = λ",   f"{lam:.4f}",          PUCV_GOLD),  unsafe_allow_html=True)
    c2.markdown(stat_box("Var(X) = λ", f"{lam:.4f}",          AZUL_CLARO), unsafe_allow_html=True)
    c3.markdown(stat_box("σ = √λ",     f"{np.sqrt(lam):.4f}", AZUL_CLARO), unsafe_allow_html=True)
    c4.markdown(stat_box("Moda",       moda_txt,              AZUL_CLARO),   unsafe_allow_html=True)

with col_p:
    st.markdown(f'<div class="seccion-label">PROBABILIDADES · k = {k_query}</div>', unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X = {k_query})", f"{p_exacta:.6f}", PUCV_GOLD),  unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X ≤ {k_query})", f"{p_acum:.6f}",   AZUL_CLARO), unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X ≥ {k_query})", f"{p_cola:.6f}",   PUCV_RED),   unsafe_allow_html=True)

    st.markdown(f"""
    <div class="formula-box">
        <div class="titulo">DESARROLLO</div>
        <div class="cuerpo">
            P(X = k) = e⁻λ · λᵏ / k!<br><br>
            <span style="color:#A50044;">Para λ = {lam:.1f}, k = {k_query}:</span><br>
            <span style="color:#003087;font-weight:600;padding-left:12px;">
                e^(−{lam:.1f}) · {lam:.1f}^{k_query} / {k_query}!
            </span><br>
            <span style="color:{PUCV_GOLD};font-weight:bold;padding-left:12px;">
                = {p_exacta:.6f}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Comparación con Binomial ──────────────────────────────────
with st.expander("Poisson como límite de la Binomial"):
    st.markdown(f"""
    Cuando **n → ∞** y **p → 0** manteniendo **n·p = λ** constante, la Binomial
    converge a la Poisson. Compara aquí ambas con λ = {lam:.1f} fijo:
    """)
    n_comp = st.select_slider("n de la Binomial (con p = λ/n)",
                              options=[10, 20, 50, 100, 500, 1000], value=20)
    p_comp = lam / n_comp
    if p_comp >= 1:
        st.warning(f"Con n = {n_comp} y λ = {lam:.1f} resultaría p = {p_comp:.2f} ≥ 1. "
                   "Elige un n mayor.")
    else:
        ks_c   = np.arange(0, k_vis + 1)
        pois_c = poisson.pmf(ks_c, lam)
        bin_c  = binom.pmf(ks_c, n_comp, p_comp)

        fig3, ax3 = plt.subplots(figsize=(9, 4))
        ancho = 0.4
        ax3.bar(ks_c - ancho/2, pois_c, width=ancho, color=PUCV_GOLD,
                label=f"Poisson(λ={lam:.1f})", zorder=3)
        ax3.bar(ks_c + ancho/2, bin_c, width=ancho, color=AZUL_BARRA,
                label=f"Binomial(n={n_comp}, p={p_comp:.4f})", zorder=3)
        ax3.set_xlabel("k", fontsize=10)
        ax3.set_ylabel("P(X = k)", fontsize=10)
        ax3.legend(fontsize=9, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax3.grid(axis="y", alpha=0.4)
        fig3.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

        dif_max = np.max(np.abs(pois_c - bin_c))
        st.markdown(f"""
        Diferencia máxima entre ambas: **{dif_max:.6f}**

        Sube `n` y observa cómo la diferencia disminuye. La regla práctica habitual
        es que la aproximación es aceptable cuando **n ≥ 20 y p ≤ 0.05**, o
        **n ≥ 100 y n·p ≤ 10**. Con los valores actuales: n = {n_comp}, p = {p_comp:.4f}.
        """)

with st.expander("¿Cuándo usar la distribución Poisson?"):
    st.markdown(f"""
    Modela el **número de eventos** en un intervalo fijo de tiempo, espacio o
    volumen, cuando ocurren de forma independiente a tasa constante λ.

    **Condiciones (proceso de Poisson):**
    - Eventos independientes entre sí
    - Tasa media λ constante en el intervalo
    - Dos eventos no ocurren simultáneamente
    - El número de eventos en intervalos disjuntos es independiente

    **Ejemplos:**
    - Llamadas a un call center por hora
    - Errores por cada mil líneas de código
    - Accidentes en un tramo de carretera por mes
    - Clientes que llegan a una caja por minuto

    **Propiedad distintiva:** E[X] = Var(X) = λ. Si en datos reales la varianza
    supera mucho a la media (**sobredispersión**), Poisson no es adecuada y
    conviene revisar alternativas como la Binomial Negativa.
    """)
