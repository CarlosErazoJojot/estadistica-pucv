# ============================================================
#  pages/07_Continuas.py
#  Exponencial · Uniforme · t-Student · Chi-cuadrado
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, norm, t as t_dist, chi2
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box, prob_box)

st.set_page_config(page_title="Continuas · PUCV", page_icon="📈", layout="wide")
plt.rcParams.update(MATPLOTLIB_STYLE)
st.markdown(CSS_BASE, unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>📈 Distribuciones Continuas</h2>
    <div class="formula">Exponencial · Uniforme · t-Student · Chi-cuadrado</div>
</div>
""", unsafe_allow_html=True)

def dibujar(D, x_lo, x_hi, a, b, color, titulo, xlabel, extras=None):
    """Curva de densidad con área sombreada entre a y b."""
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.linspace(x_lo, x_hi, 600)
    y = D.pdf(x)
    ax.plot(x, y, color=color, linewidth=2.5, zorder=4)
    ax.fill_between(x, y, alpha=0.08, color=color)

    xs = np.linspace(a, b, 400)
    ax.fill_between(xs, D.pdf(xs), alpha=0.55, color=AZUL_BARRA, zorder=3,
                    label=f"P({a:.2f} ≤ X ≤ {b:.2f}) = {D.cdf(b)-D.cdf(a):.4f}")
    ax.axvline(a, color=PUCV_GOLD,  linestyle=":", linewidth=1.3)
    ax.axvline(b, color=AZUL_CLARO, linestyle=":", linewidth=1.3)

    for val, col, lab in (extras or []):
        ax.axvline(val, color=col, linestyle="--", linewidth=1.4, alpha=0.85, label=lab)

    ax.set_xlabel(xlabel, fontsize=10, labelpad=8)
    ax.set_ylabel("f(x)", fontsize=10)
    ax.set_title(titulo, fontsize=11, color=TEXT_LIGHT)
    ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
    ax.grid(axis="y", alpha=0.4)
    fig.tight_layout()
    return fig

tab1, tab2, tab3, tab4 = st.tabs(["⚡ Exponencial", "▬ Uniforme", "🎓 t-Student", "χ² Chi-cuadrado"])

# ══════════════════════════════════════════════════════════════
# Exponencial
# ══════════════════════════════════════════════════════════════
with tab1:
    c1_, c2_ = st.columns([1, 2], gap="large")
    with c1_:
        st.markdown('<div class="seccion-label">PARÁMETROS · X ~ Exp(λ)</div>', unsafe_allow_html=True)
        lam = st.slider("λ — tasa", 0.1, 5.0, 1.0, 0.1, format="%.1f", key="le")
        st.caption("Los límites se expresan en múltiplos de la media 1/λ, "
                   "así el rango no cambia al mover λ.")
        # ✅ Sliders en múltiplos de la media: rango fijo
        ma = st.slider("a — en múltiplos de 1/λ", 0.0, 5.0, 0.5, 0.05, key="ae")
        mb = st.slider("b — en múltiplos de 1/λ", 0.0, 5.0, 2.0, 0.05, key="be")
        if mb < ma: ma, mb = mb, ma

        D   = expon(scale=1/lam)
        a, b = ma / lam, mb / lam
        mu_e, var_e = 1/lam, 1/lam**2

        st.markdown(prob_box(f"P({a:.3f} ≤ X ≤ {b:.3f})", f"{D.cdf(b)-D.cdf(a):.6f}", PUCV_GOLD),  unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X ≤ {b:.3f})",            f"{D.cdf(b):.6f}",          AZUL_CLARO), unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X > {b:.3f})",            f"{D.sf(b):.6f}",           PUCV_RED),   unsafe_allow_html=True)

    with c2_:
        fig = dibujar(D, 0, 5/lam, a, b, PUCV_GOLD, f"X ~ Exp(λ={lam:.1f})", "x",
                      extras=[(mu_e, PUCV_RED, f"E[X] = 1/λ = {mu_e:.3f}")])
        st.pyplot(fig, use_container_width=True); plt.close(fig)
        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("E[X] = 1/λ",    f"{mu_e:.4f}",            PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Var(X) = 1/λ²", f"{var_e:.4f}",           AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("Mediana",       f"{np.log(2)/lam:.4f}",   PUCV_RED),   unsafe_allow_html=True)

    with st.expander("Falta de memoria — análoga a la Geométrica"):
        cs, ct = st.columns(2)
        s_e = cs.slider("s — tiempo ya transcurrido", 0.1, 5.0, 1.0, 0.1, key="se")
        t_e = ct.slider("t — tiempo adicional",       0.1, 5.0, 0.5, 0.1, key="te")
        cond = D.sf(s_e + t_e) / D.sf(s_e)
        st.markdown(f"""
        > **P(X > s + t | X > s) = P(X > t)**

        | Expresión | Valor |
        |---|---|
        | P(X > {s_e:.1f}) | {D.sf(s_e):.8f} |
        | P(X > {s_e+t_e:.1f}) | {D.sf(s_e+t_e):.8f} |
        | **P(X > {s_e+t_e:.1f} \\| X > {s_e:.1f})** | **{cond:.8f}** |
        | **P(X > {t_e:.1f})** | **{D.sf(t_e):.8f}** |

        La Exponencial es la única distribución continua con esta propiedad.
        """)

# ══════════════════════════════════════════════════════════════
# Uniforme
# ══════════════════════════════════════════════════════════════
with tab2:
    c1_, c2_ = st.columns([1, 2], gap="large")
    with c1_:
        st.markdown('<div class="seccion-label">PARÁMETROS · X ~ U(α, β)</div>', unsafe_allow_html=True)
        al = st.slider("α — límite inferior", -10.0, 10.0, 0.0, 0.5, key="au")
        be = st.slider("β — límite superior", -10.0, 10.0, 1.0, 0.5, key="bu")
        if be <= al:
            be = al + 1.0
            st.info(f"β debe ser mayor que α. Se usa β = {be:.1f}.")
        st.caption("La consulta se expresa como fracción del recorrido [α, β].")
        # ✅ Fracciones del recorrido: rango fijo 0..1
        fa = st.slider("a — fracción del recorrido", 0.0, 1.0, 0.25, 0.01, key="fau")
        fb = st.slider("b — fracción del recorrido", 0.0, 1.0, 0.75, 0.01, key="fbu")
        if fb < fa: fa, fb = fb, fa

        rng_u   = be - al
        a_u, b_u = al + fa*rng_u, al + fb*rng_u
        mu_u, var_u = (al+be)/2, rng_u**2/12
        p_u     = fb - fa    # exacto por construcción

        st.markdown(prob_box(f"P({a_u:.2f} ≤ X ≤ {b_u:.2f})", f"{p_u:.6f}",   PUCV_GOLD),  unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X ≤ {b_u:.2f})",              f"{fb:.6f}",    AZUL_CLARO), unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X > {b_u:.2f})",              f"{1-fb:.6f}",  PUCV_RED),   unsafe_allow_html=True)

    with c2_:
        fig, ax = plt.subplots(figsize=(9, 5))
        pad = rng_u * 0.12
        ax.plot([al-pad, al, al, be, be, be+pad], [0, 0, 1/rng_u, 1/rng_u, 0, 0],
                color=AZUL_CLARO, linewidth=2.5, zorder=4)
        ax.fill_between([a_u, b_u], [1/rng_u]*2, alpha=0.55, color=AZUL_BARRA, zorder=3,
                        label=f"P = {p_u:.4f}")
        ax.axvline(mu_u, color=PUCV_RED, linestyle="--", linewidth=1.4, label=f"E[X] = {mu_u:.3f}")
        ax.set_xlabel("x", fontsize=10); ax.set_ylabel("f(x)", fontsize=10)
        ax.set_title(f"X ~ U({al:.1f}, {be:.1f})   ·   f(x) = 1/{rng_u:.2f} = {1/rng_u:.4f}",
                     fontsize=11, color=TEXT_LIGHT)
        ax.set_ylim(0, 1.35/rng_u)
        ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax.grid(axis="y", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)
        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("E[X] = (α+β)/2",     f"{mu_u:.4f}",          PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Var(X) = (β−α)²/12", f"{var_u:.4f}",         AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("σ",                  f"{np.sqrt(var_u):.4f}",AZUL_CLARO), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# t-Student
# ══════════════════════════════════════════════════════════════
with tab3:
    c1_, c2_ = st.columns([1, 2], gap="large")
    with c1_:
        st.markdown('<div class="seccion-label">PARÁMETROS · X ~ t(ν)</div>', unsafe_allow_html=True)
        nu  = int(st.slider("ν — grados de libertad", 1, 100, 10, key="nut"))
        a_t = st.slider("a", -5.0, 5.0, -1.96, 0.05, format="%.2f", key="at")
        b_t = st.slider("b", -5.0, 5.0,  1.96, 0.05, format="%.2f", key="bt")
        if b_t < a_t: a_t, b_t = b_t, a_t

        D = t_dist(df=nu)
        st.markdown(prob_box(f"P({a_t:.2f} ≤ X ≤ {b_t:.2f})", f"{D.cdf(b_t)-D.cdf(a_t):.6f}", PUCV_GOLD),  unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X < {a_t:.2f})",              f"{D.cdf(a_t):.6f}",            AZUL_CLARO), unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X > {b_t:.2f})",              f"{D.sf(b_t):.6f}",             PUCV_RED),   unsafe_allow_html=True)

    with c2_:
        fig, ax = plt.subplots(figsize=(9, 5))
        x = np.linspace(-5, 5, 600)
        ax.plot(x, D.pdf(x), color=PUCV_GOLD, linewidth=2.5, zorder=4, label=f"t({nu} gl)")
        # ✅ CORREGIDO: norm.pdf directo (antes t con df=1000)
        ax.plot(x, norm.pdf(x), color=AZUL_CLARO, linewidth=1.6, linestyle="--",
                alpha=0.7, label="N(0,1)")
        xs = np.linspace(a_t, b_t, 400)
        ax.fill_between(xs, D.pdf(xs), alpha=0.5, color=AZUL_BARRA, zorder=3,
                        label=f"P = {D.cdf(b_t)-D.cdf(a_t):.4f}")
        ax.axvline(a_t, color=PUCV_GOLD,  linestyle=":", linewidth=1.3)
        ax.axvline(b_t, color=AZUL_CLARO, linestyle=":", linewidth=1.3)
        ax.set_xlabel("t", fontsize=10); ax.set_ylabel("f(t)", fontsize=10)
        ax.set_title(f"X ~ t(ν={nu})  —  colas más pesadas que la Normal", fontsize=11, color=TEXT_LIGHT)
        ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax.grid(axis="y", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

        var_t = nu/(nu-2) if nu > 2 else None
        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("E[X]", "0" if nu > 1 else "no definida", PUCV_GOLD), unsafe_allow_html=True)
        k2.markdown(stat_box("Var(X) = ν/(ν−2)",
                             f"{var_t:.4f}" if var_t else ("∞" if nu == 2 else "no definida"),
                             AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("t₀.₉₇₅", f"{D.ppf(0.975):.4f}", PUCV_RED), unsafe_allow_html=True)
        st.caption(f"Percentil 0.975: t = {D.ppf(0.975):.4f} frente a z = {norm.ppf(0.975):.4f}. "
                   "La diferencia se reduce al aumentar ν.")

# ══════════════════════════════════════════════════════════════
# Chi-cuadrado
# ══════════════════════════════════════════════════════════════
with tab4:
    c1_, c2_ = st.columns([1, 2], gap="large")
    with c1_:
        st.markdown('<div class="seccion-label">PARÁMETROS · X ~ χ²(k)</div>', unsafe_allow_html=True)
        k_chi = int(st.slider("k — grados de libertad", 1, 30, 5, key="kchi"))
        st.caption("La consulta se expresa en percentiles, así el rango "
                   "no cambia al mover k.")
        # ✅ Percentiles: rango fijo 0..1
        pa = st.slider("a — percentil", 0.0, 1.0, 0.0,  0.01, key="pachi")
        pb = st.slider("b — percentil", 0.0, 1.0, 0.95, 0.01, key="pbchi")
        if pb < pa: pa, pb = pb, pa

        D = chi2(df=k_chi)
        a_c = D.ppf(max(pa, 1e-9))
        b_c = D.ppf(min(pb, 1-1e-9))

        st.markdown(prob_box(f"P({a_c:.3f} ≤ X ≤ {b_c:.3f})", f"{pb-pa:.6f}",  PUCV_GOLD),  unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X ≤ {b_c:.3f})",              f"{pb:.6f}",     AZUL_CLARO), unsafe_allow_html=True)
        st.markdown(prob_box(f"P(X > {b_c:.3f})",              f"{1-pb:.6f}",   PUCV_RED),   unsafe_allow_html=True)

    with c2_:
        fig = dibujar(D, 0.001, D.ppf(0.999), a_c, b_c, PUCV_RED,
                      f"X ~ χ²(k={k_chi})", "x",
                      extras=[(k_chi, PUCV_GOLD, f"E[X] = k = {k_chi}")])
        st.pyplot(fig, use_container_width=True); plt.close(fig)
        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("E[X] = k",     f"{k_chi}",              PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Var(X) = 2k",  f"{2*k_chi}",            AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("χ²₀.₉₅",       f"{D.ppf(0.95):.4f}",    PUCV_RED),   unsafe_allow_html=True)
        st.caption("Al crecer k la χ² se vuelve más simétrica y se aproxima a una "
                   "Normal de media k y varianza 2k.")
