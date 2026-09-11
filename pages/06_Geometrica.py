# ============================================================
#  pages/06_Geometrica.py
#  Distribución Geométrica e Hipergeométrica
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import geom, hypergeom
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import PUCV_RED, PUCV_GOLD, TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE

st.set_page_config(page_title="Geométrica · PUCV", page_icon="🔁", layout="wide")
plt.rcParams.update(MATPLOTLIB_STYLE)
st.markdown(CSS_BASE, unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>🔁 Distribuciones Geométrica e Hipergeométrica</h2>
    <div class="formula">Geométrica: P(X=k) = (1−p)^(k−1)·p &nbsp;·&nbsp; Hipergeométrica: extracción sin reposición</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📍 Geométrica", "🎲 Hipergeométrica"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — Geométrica
# ══════════════════════════════════════════════════════════════
with tab1:
    col_ctrl, col_viz = st.columns([1, 2], gap="large")

    with col_ctrl:
        st.markdown('<div class="seccion-label">PARÁMETROS · X ~ Geom(p)</div>', unsafe_allow_html=True)
        p_g     = st.slider("p — probabilidad de éxito", 0.01, 0.99, 0.30, 0.01, format="%.2f", key="pg")
        # Rango fijo: evita que el slider de k quede fuera de rango al mover p
        k_max_g = 50
        k_q_g   = st.slider("k — ensayo a consultar", 1, k_max_g, 3, key="kqg")
        vista_g = st.radio("Vista", ["PMF", "CDF"], key="vg", horizontal=True)

        mu_g    = 1 / p_g
        var_g   = (1 - p_g) / p_g**2
        std_g   = np.sqrt(var_g)

        # Ventana de graficación adaptativa (el slider no depende de ella)
        k_vis   = min(k_max_g, max(k_q_g + 5, int(np.ceil(8 / p_g))))
        ks_g    = np.arange(1, k_vis + 1)
        pmfs_g  = geom.pmf(ks_g, p_g)
        cdfs_g  = geom.cdf(ks_g, p_g)
        usar_g  = pmfs_g if vista_g == "PMF" else cdfs_g

        p_ex_g  = geom.pmf(k_q_g, p_g)
        p_ac_g  = geom.cdf(k_q_g, p_g)
        p_cs_g  = geom.sf(k_q_g - 1, p_g)

        for label, val, color in [
            (f"P(X = {k_q_g})", f"{p_ex_g:.6f}", PUCV_GOLD),
            (f"P(X ≤ {k_q_g})", f"{p_ac_g:.6f}", "#0E7490"),
            (f"P(X ≥ {k_q_g})", f"{p_cs_g:.6f}", PUCV_RED),
        ]:
            st.markdown(f'<div class="prob-box"><div class="label">{label}</div><div class="value" style="color:{color};">{val}</div></div>', unsafe_allow_html=True)

    with col_viz:
        fig, ax = plt.subplots(figsize=(9, 5))
        colores = [PUCV_GOLD if k == k_q_g else "#2E6BB8" for k in ks_g]
        ax.bar(ks_g, usar_g, color=colores, edgecolor="#FFFFFF", linewidth=0.5, width=0.7, zorder=3)
        ax.axvline(mu_g, color=PUCV_RED, linestyle="--", linewidth=1.4, label=f"E[X] = 1/p = {mu_g:.2f}")
        ax.set_xlabel("k  (ensayos hasta el primer éxito)", fontsize=10, labelpad=8)
        ax.set_ylabel("P(X = k)" if vista_g == "PMF" else "P(X ≤ k)", fontsize=10)
        ax.set_title(f"X ~ Geom(p={p_g:.2f})", fontsize=11, color=TEXT_LIGHT)
        ax.legend(fontsize=9, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax.grid(axis="y", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        c1, c2, c3 = st.columns(3)
        for col, label, val, color in [
            (c1, "E[X] = 1/p",  f"{mu_g:.4f}",  PUCV_GOLD),
            (c2, "Var(X)",      f"{var_g:.4f}",  "#0E7490"),
            (c3, "σ",           f"{std_g:.4f}",  "#0E7490"),
        ]:
            col.markdown(f'<div class="stat-box" style="border-top-color:{color};"><div class="label">{label}</div><div class="value" style="color:{color};">{val}</div></div>', unsafe_allow_html=True)

    # ── Falta de memoria — CORREGIDO ──────────────────────────
    with st.expander("Propiedad de falta de memoria (sin memoria)"):
        st.markdown("""
        La propiedad se enuncia **sobre colas**, no sobre valores puntuales:

        > **P(X > s + t | X > s) = P(X > t)**

        Es decir: si ya realizaste `s` ensayos sin éxito, la probabilidad de
        necesitar más de `t` ensayos **adicionales** es la misma que al inicio.
        """)
        cs, ct = st.columns(2)
        k_s = cs.slider("s — ensayos ya realizados sin éxito", 1, 15, 3, key="gs")
        k_t = ct.slider("t — ensayos adicionales", 1, 15, 2, key="gt")

        # P(X > s+t | X > s) = P(X > s+t) / P(X > s)
        sf_s   = geom.sf(k_s, p_g)          # P(X > s)
        sf_st  = geom.sf(k_s + k_t, p_g)    # P(X > s+t)
        cond   = sf_st / sf_s
        sf_t   = geom.sf(k_t, p_g)          # P(X > t)
        dif    = abs(cond - sf_t)

        st.markdown(f"""
        | Expresión | Valor |
        |---|---|
        | P(X > {k_s}) | {sf_s:.8f} |
        | P(X > {k_s + k_t}) | {sf_st:.8f} |
        | **P(X > {k_s + k_t} \\| X > {k_s})** = {sf_st:.6f} / {sf_s:.6f} | **{cond:.8f}** |
        | **P(X > {k_t})** | **{sf_t:.8f}** |
        | Diferencia absoluta | {dif:.2e} |

        Ambas coinciden (la diferencia es error de punto flotante). La Geométrica
        es la **única** distribución discreta con esta propiedad; su análoga continua
        es la Exponencial.
        """)

        st.caption(f"Comprobación algebraica: P(X > k) = (1−p)^k, entonces "
                   f"(1−p)^{k_s + k_t} / (1−p)^{k_s} = (1−p)^{k_t}")

# ══════════════════════════════════════════════════════════════
# TAB 2 — Hipergeométrica
# ══════════════════════════════════════════════════════════════
with tab2:
    col_ctrl2, col_viz2 = st.columns([1, 2], gap="large")

    with col_ctrl2:
        st.markdown('<div class="seccion-label">PARÁMETROS · X ~ HG(N, K, n)</div>', unsafe_allow_html=True)
        # Rangos fijos + clamp explícito: los sliders nunca quedan fuera de rango
        N_h    = int(st.slider("N — tamaño de la población", 10, 200, 50, 5, key="Nh"))
        K_raw  = int(st.slider("K — éxitos en la población", 1, 200, 15, 1, key="Kh"))
        n_raw  = int(st.slider("n — tamaño de la muestra",   1, 200, 10, 1, key="nh"))

        K_h = min(K_raw, N_h)
        n_h = min(n_raw, N_h)
        if K_raw > N_h or n_raw > N_h:
            st.info(f"K y n no pueden exceder N. Se usan K = {K_h}, n = {n_h}.")

        k_lo   = max(0, n_h - (N_h - K_h))
        k_hi   = min(n_h, K_h)
        k_q_h  = int(st.slider("k — valor a consultar", int(k_lo), int(max(k_hi, k_lo + 1)),
                               int(min(3, k_hi)), key="kqh"))

        mu_h   = n_h * K_h / N_h
        var_h  = n_h * (K_h/N_h) * (1 - K_h/N_h) * (N_h - n_h)/(N_h - 1)
        std_h  = np.sqrt(var_h)

        ks_h   = np.arange(k_lo, k_hi + 1)
        pmfs_h = hypergeom.pmf(ks_h, N_h, K_h, n_h)
        cdfs_h = hypergeom.cdf(ks_h, N_h, K_h, n_h)
        vista_h = st.radio("Vista ", ["PMF", "CDF"], key="vh", horizontal=True)
        usar_h = pmfs_h if vista_h == "PMF" else cdfs_h

        p_ex_h = hypergeom.pmf(k_q_h, N_h, K_h, n_h)
        p_ac_h = hypergeom.cdf(k_q_h, N_h, K_h, n_h)
        p_cs_h = hypergeom.sf(k_q_h - 1, N_h, K_h, n_h)

        for label, val, color in [
            (f"P(X = {k_q_h})", f"{p_ex_h:.6f}", PUCV_GOLD),
            (f"P(X ≤ {k_q_h})", f"{p_ac_h:.6f}", "#0E7490"),
            (f"P(X ≥ {k_q_h})", f"{p_cs_h:.6f}", PUCV_RED),
        ]:
            st.markdown(f'<div class="prob-box"><div class="label">{label}</div><div class="value" style="color:{color};">{val}</div></div>', unsafe_allow_html=True)

    with col_viz2:
        fig2, ax2 = plt.subplots(figsize=(9, 5))
        colores2 = [PUCV_GOLD if k == k_q_h else "#2E6BB8" for k in ks_h]
        ax2.bar(ks_h, usar_h, color=colores2, edgecolor="#FFFFFF", linewidth=0.5, width=0.6, zorder=3)
        ax2.axvline(mu_h, color=PUCV_RED, linestyle="--", linewidth=1.4, label=f"E[X] = {mu_h:.3f}")
        ax2.set_xlabel("k  (éxitos en la muestra)", fontsize=10, labelpad=8)
        ax2.set_ylabel("P(X = k)" if vista_h == "PMF" else "P(X ≤ k)", fontsize=10)
        ax2.set_title(f"X ~ HG(N={N_h}, K={K_h}, n={n_h})", fontsize=11, color=TEXT_LIGHT)
        ax2.legend(fontsize=9, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax2.grid(axis="y", alpha=0.4)
        fig2.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

        c1, c2, c3 = st.columns(3)
        for col, label, val, color in [
            (c1, "E[X] = n·K/N", f"{mu_h:.4f}",  PUCV_GOLD),
            (c2, "Var(X)",        f"{var_h:.4f}",  "#0E7490"),
            (c3, "σ",             f"{std_h:.4f}",  "#0E7490"),
        ]:
            col.markdown(f'<div class="stat-box" style="border-top-color:{color};"><div class="label">{label}</div><div class="value" style="color:{color};">{val}</div></div>', unsafe_allow_html=True)

    with st.expander("Diferencia con Binomial"):
        st.markdown(f"""
        | Característica | Binomial | Hipergeométrica |
        |---|---|---|
        | Extracción | **Con** reposición | **Sin** reposición |
        | Ensayos | Independientes | Dependientes |
        | p | Constante | Cambia en cada extracción |
        | Parámetros | n, p | N, K, n |
        | E[X] | n·p | n·K/N |
        | Var(X) | n·p·(1−p) | n·p·(1−p)·(N−n)/(N−1) |

        Con los valores actuales (N={N_h}, K={K_h}, n={n_h}, p = K/N = {K_h/N_h:.4f}):

        - **Hipergeométrica:** Var(X) = {var_h:.4f}
        - **Binomial equivalente:** Var(X) = {n_h * (K_h/N_h) * (1 - K_h/N_h):.4f}

        El factor **(N−n)/(N−1) = {(N_h-n_h)/(N_h-1):.4f}** se llama *corrección por
        población finita*. Cuando N ≫ n tiende a 1 y ambas distribuciones convergen.
        """)
