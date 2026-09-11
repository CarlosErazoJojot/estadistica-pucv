# ============================================================
#  pages/03_Normal.py
#  Distribución Normal — X ~ N(μ, σ²)
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box, prob_box)

st.set_page_config(page_title="Normal · PUCV", page_icon="🔔", layout="wide")
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
    <h2>🔔 Distribución Normal</h2>
    <div class="formula">X ~ N(μ, σ²) &nbsp;·&nbsp; f(x) = (1/σ√2π) · e^(−(x−μ)²/2σ²)</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="seccion-label">PARÁMETROS · X ~ N(μ, σ²)</div>', unsafe_allow_html=True)
    mu    = st.slider("μ — media", -10.0, 10.0, 0.0, 0.5, format="%.1f")
    sigma = st.slider("σ — desviación estándar", 0.1, 5.0, 1.0, 0.1, format="%.1f")

    st.markdown("---")
    st.markdown('<div class="seccion-label">CONSULTA P(a ≤ X ≤ b)</div>', unsafe_allow_html=True)
    st.caption("Los límites se definen en unidades de σ desde μ, "
               "así el rango no cambia al mover los parámetros.")

    # ✅ CORREGIDO: sliders en unidades de σ (rango fijo −4..4).
    # Antes dependían de mu/sigma y podían quedar fuera de rango.
    za = st.slider("a — en unidades de σ desde μ", -4.0, 4.0, -1.0, 0.05, format="%.2f")
    zb = st.slider("b — en unidades de σ desde μ", -4.0, 4.0,  1.0, 0.05, format="%.2f")
    if zb < za:
        za, zb = zb, za

    a = mu + za * sigma
    b = mu + zb * sigma

    st.markdown("---")
    mostrar_z = st.checkbox("Mostrar escala Z estandarizada", value=True)
    st.markdown("---")
    st.markdown('<div class="seccion-label">IR A</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Inicio", icon=":material/home:")
    st.page_link("pages/03_Geometrica.py", label="Geométrica", icon=":material/arrow_back:")
    st.page_link("pages/05_Continuas.py", label="Continuas", icon=":material/arrow_forward:")

    st.markdown('<div class="firma">Carlos Erazo Jojot · PUCV</div>',
                unsafe_allow_html=True)

# ── Cálculos ──────────────────────────────────────────────────
x     = np.linspace(mu - 4.5 * sigma, mu + 4.5 * sigma, 500)
y     = norm.pdf(x, mu, sigma)
x_ab  = np.linspace(a, b, 300)
y_ab  = norm.pdf(x_ab, mu, sigma)

p_ab    = norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)
p_left  = norm.cdf(a, mu, sigma)
p_right = norm.sf(b, mu, sigma)

col_g, col_p = st.columns([3, 1], gap="large")

with col_g:
    ncols = 2 if mostrar_z else 1
    fig, axes = plt.subplots(1, ncols, figsize=(12 if mostrar_z else 9, 5), squeeze=False)
    ax = axes[0][0]

    ax.plot(x, y, color=PUCV_GOLD, linewidth=2.5, zorder=4)
    ax.fill_between(x, y, alpha=0.08, color=PUCV_GOLD)
    ax.fill_between(x_ab, y_ab, alpha=0.55, color=AZUL_BARRA, zorder=3,
                    label=f"P(a ≤ X ≤ b) = {p_ab:.4f}")

    ax.axvline(mu, color=PUCV_RED,  linestyle="--", linewidth=1.4, alpha=0.85, label=f"μ = {mu:.1f}")
    ax.axvline(a,  color=PUCV_GOLD, linestyle=":",  linewidth=1.3, alpha=0.9,  label=f"a = {a:.3f}")
    ax.axvline(b,  color=AZUL_CLARO,linestyle=":",  linewidth=1.3, alpha=0.9,  label=f"b = {b:.3f}")

    for k, al in [(1, 0.06), (2, 0.04), (3, 0.02)]:
        ax.axvspan(mu - k*sigma, mu + k*sigma, alpha=al, color=PUCV_GOLD)

    ax.set_xlabel("x", fontsize=11, labelpad=8)
    ax.set_ylabel("f(x)", fontsize=11, labelpad=8)
    ax.set_title(f"X ~ N(μ={mu:.1f}, σ={sigma:.1f})", fontsize=11, color=TEXT_LIGHT)
    ax.grid(axis="y", alpha=0.4)
    ax.legend(fontsize=8.5, loc="upper right", framealpha=0.25, edgecolor=PUCV_GOLD)

    if mostrar_z:
        ax2 = axes[0][1]
        zr  = np.linspace(-4.5, 4.5, 500)
        # ✅ CORREGIDO: usa norm.pdf directamente (antes t con df=1000)
        ax2.plot(zr, norm.pdf(zr), color=AZUL_CLARO, linewidth=2.5, zorder=4)
        ax2.fill_between(zr, norm.pdf(zr), alpha=0.08, color=AZUL_CLARO)
        zf = np.linspace(za, zb, 300)
        ax2.fill_between(zf, norm.pdf(zf), alpha=0.55, color=AZUL_BARRA, zorder=3,
                         label=f"P = {p_ab:.4f}")
        ax2.axvline(0,  color=PUCV_RED,  linestyle="--", linewidth=1.4, alpha=0.85, label="μ = 0")
        ax2.axvline(za, color=PUCV_GOLD, linestyle=":",  linewidth=1.3, label=f"z_a = {za:.2f}")
        ax2.axvline(zb, color=AZUL_CLARO,linestyle=":",  linewidth=1.3, label=f"z_b = {zb:.2f}")
        ax2.set_xlabel("z", fontsize=11, labelpad=8)
        ax2.set_ylabel("φ(z)", fontsize=11)
        ax2.set_title("Z ~ N(0, 1) — forma estándar", fontsize=11, color=TEXT_LIGHT)
        ax2.grid(axis="y", alpha=0.4)
        ax2.legend(fontsize=8.5, loc="upper right", framealpha=0.25, edgecolor=AZUL_CLARO)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(stat_box("μ (media)",        f"{mu:.2f}",        PUCV_GOLD),  unsafe_allow_html=True)
    c2.markdown(stat_box("σ² (varianza)",    f"{sigma**2:.4f}",  AZUL_CLARO), unsafe_allow_html=True)
    c3.markdown(stat_box("σ",                f"{sigma:.2f}",     AZUL_CLARO), unsafe_allow_html=True)
    c4.markdown(stat_box("Moda = Mediana",   f"{mu:.2f}",        PUCV_RED),   unsafe_allow_html=True)

with col_p:
    st.markdown('<div class="seccion-label">PROBABILIDADES</div>', unsafe_allow_html=True)
    st.markdown(prob_box(f"P({a:.2f} ≤ X ≤ {b:.2f})", f"{p_ab:.6f}",    PUCV_GOLD),  unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X < {a:.2f})",            f"{p_left:.6f}",  AZUL_CLARO), unsafe_allow_html=True)
    st.markdown(prob_box(f"P(X > {b:.2f})",            f"{p_right:.6f}", PUCV_RED),   unsafe_allow_html=True)

    st.markdown(f"""
    <div class="formula-box">
        <div class="titulo">ESTANDARIZACIÓN</div>
        <div class="cuerpo">
            Z = (X − μ) / σ<br>
            <span style="color:#A50044;">z_a = ({a:.3f} − {mu:.1f}) / {sigma:.1f}</span><br>
            <span style="color:{PUCV_GOLD};font-weight:bold;padding-left:12px;">= {za:.4f}</span><br>
            <span style="color:{AZUL_CLARO};">z_b = ({b:.3f} − {mu:.1f}) / {sigma:.1f}</span><br>
            <span style="color:{PUCV_GOLD};font-weight:bold;padding-left:12px;">= {zb:.4f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("Regla empírica 68–95–99.7"):
    p1 = norm.cdf(1) - norm.cdf(-1)
    p2 = norm.cdf(2) - norm.cdf(-2)
    p3 = norm.cdf(3) - norm.cdf(-3)
    st.markdown(f"""
    Con μ = {mu:.1f} y σ = {sigma:.1f}:

    | Intervalo | Aproximación usual | Valor exacto |
    |---|---|---|
    | μ ± 1σ = [{mu-sigma:.2f}, {mu+sigma:.2f}] | ≈ 68% | **{p1*100:.4f}%** |
    | μ ± 2σ = [{mu-2*sigma:.2f}, {mu+2*sigma:.2f}] | ≈ 95% | **{p2*100:.4f}%** |
    | μ ± 3σ = [{mu-3*sigma:.2f}, {mu+3*sigma:.2f}] | ≈ 99.7% | **{p3*100:.4f}%** |

    Los porcentajes no dependen de μ ni σ: son propiedades de la forma de la
    Normal, no de su ubicación o escala.
    """)
