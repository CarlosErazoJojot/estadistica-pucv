# ============================================================
#  pages/08_Distribuciones_Muestrales.py
#  Distribuciones muestrales de X̄, p̂ y S²
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box, prob_box)

st.set_page_config(page_title="Distribuciones Muestrales · PUCV", page_icon="🎲", layout="wide")
plt.rcParams.update(MATPLOTLIB_STYLE)
st.markdown(CSS_BASE, unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>🎲 Distribuciones Muestrales</h2>
    <div class="formula">X̄ · p̂ · S² &nbsp;—&nbsp; qué ocurre cuando el estadístico es la variable aleatoria</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Un **estadístico** calculado sobre una muestra es una variable aleatoria: cambia
de muestra en muestra. Su distribución se llama **distribución muestral**, y es
lo que permite construir intervalos y pruebas.
""")

tab1, tab2, tab3 = st.tabs(["X̄ — media muestral", "p̂ — proporción muestral", "S² — varianza muestral"])

# ══════════════════════════════════════════════════════════════
# X̄
# ══════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown('<div class="seccion-label">POBLACIÓN Y MUESTRA</div>', unsafe_allow_html=True)
        mu_p  = st.number_input("μ — media poblacional", value=100.0, step=1.0, key="mux")
        sig_p = st.number_input("σ — desviación poblacional", value=15.0, step=0.5,
                                min_value=0.01, key="sigx")
        n_x   = int(st.slider("n — tamaño de muestra", 1, 200, 25, key="nx"))
        sigma_conocida = st.checkbox("σ conocida", value=True, key="sckx")

        ee = sig_p / np.sqrt(n_x)      # error estándar

        st.markdown(f"""
        <div class="formula-box">
            <div class="titulo">RESULTADO</div>
            <div class="cuerpo">
                E[X̄] = μ = <span style="color:{PUCV_GOLD};">{mu_p:.4f}</span><br>
                Var(X̄) = σ²/n = <span style="color:{AZUL_CLARO};">{sig_p**2/n_x:.4f}</span><br>
                <b>Error estándar</b> = σ/√n =
                <span style="color:{PUCV_GOLD};font-weight:bold;">{ee:.4f}</span><br><br>
                <span style="color:#4A688F;font-size:0.72rem;">
                {'X̄ ~ N(μ, σ²/n) exacta si la población es Normal; aproximada por TCL si n es grande.'
                 if sigma_conocida else
                 '(X̄−μ)/(S/√n) ~ t(n−1) cuando σ se estima con S.'}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.caption("El error estándar NO es la desviación de la población: "
                   "mide cuánto varía la *media muestral*, no un dato individual.")

    with c2:
        fig, ax = plt.subplots(figsize=(9, 5))
        x = np.linspace(mu_p - 4*sig_p, mu_p + 4*sig_p, 600)
        ax.plot(x, norm.pdf(x, mu_p, sig_p), color=AZUL_CLARO, linewidth=1.8,
                linestyle="--", alpha=0.75, label=f"Población: σ = {sig_p:.2f}")
        ax.plot(x, norm.pdf(x, mu_p, ee), color=PUCV_GOLD, linewidth=2.6,
                zorder=4, label=f"X̄ con n = {n_x}: σ/√n = {ee:.3f}")
        ax.fill_between(x, norm.pdf(x, mu_p, ee), alpha=0.15, color=PUCV_GOLD)
        ax.axvline(mu_p, color=PUCV_RED, linestyle="--", linewidth=1.4, label=f"μ = {mu_p:.1f}")
        ax.set_xlabel("valor", fontsize=10); ax.set_ylabel("densidad", fontsize=10)
        ax.set_title("La distribución de X̄ es más concentrada que la de la población",
                     fontsize=11, color=TEXT_LIGHT)
        ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax.grid(axis="y", alpha=0.4)
        fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("E[X̄] = μ",      f"{mu_p:.4f}",        PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Error estándar", f"{ee:.4f}",          AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("Reducción",      f"÷ {np.sqrt(n_x):.2f}", PUCV_RED), unsafe_allow_html=True)

        st.caption(f"Para reducir el error estándar a la mitad hay que cuadruplicar n: "
                   f"de n = {n_x} a n = {4*n_x}. La precisión crece con √n, no con n.")

# ══════════════════════════════════════════════════════════════
# p̂
# ══════════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown('<div class="seccion-label">PROPORCIÓN POBLACIONAL</div>', unsafe_allow_html=True)
        p_pob = st.slider("p — proporción poblacional", 0.01, 0.99, 0.30, 0.01,
                          format="%.2f", key="ppob")
        n_p   = int(st.slider("n — tamaño de muestra", 5, 500, 100, key="np_"))

        ee_p  = np.sqrt(p_pob*(1-p_pob)/n_p)
        np_, nq_ = n_p*p_pob, n_p*(1-p_pob)
        valida = np_ >= 10 and nq_ >= 10

        st.markdown(f"""
        <div class="formula-box">
            <div class="titulo">RESULTADO</div>
            <div class="cuerpo">
                E[p̂] = p = <span style="color:{PUCV_GOLD};">{p_pob:.4f}</span><br>
                Var(p̂) = p(1−p)/n = <span style="color:{AZUL_CLARO};">{ee_p**2:.6f}</span><br>
                <b>Error estándar</b> = √(p(1−p)/n) =
                <span style="color:{PUCV_GOLD};font-weight:bold;">{ee_p:.5f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if valida:
            st.success(f"Aproximación Normal válida: np = {np_:.1f} ≥ 10 y n(1−p) = {nq_:.1f} ≥ 10")
        else:
            st.warning(f"Aproximación Normal cuestionable: np = {np_:.1f}, n(1−p) = {nq_:.1f}. "
                       "Se recomienda np ≥ 10 y n(1−p) ≥ 10. Con estos valores conviene "
                       "usar la Binomial exacta.")

    with c2:
        fig, ax = plt.subplots(figsize=(9, 5))
        lo, hi = max(0, p_pob-4*ee_p), min(1, p_pob+4*ee_p)
        x = np.linspace(lo, hi, 600)
        col = PUCV_GOLD if valida else PUCV_RED
        ax.plot(x, norm.pdf(x, p_pob, ee_p), color=col, linewidth=2.6, zorder=4,
                label=f"p̂ ≈ N({p_pob:.2f}, {ee_p:.4f}²)")
        ax.fill_between(x, norm.pdf(x, p_pob, ee_p), alpha=0.18, color=col)
        ax.axvline(p_pob, color=PUCV_RED, linestyle="--", linewidth=1.4, label=f"p = {p_pob:.2f}")
        for k in (1, 2):
            ax.axvspan(p_pob-k*ee_p, p_pob+k*ee_p, alpha=0.05, color=PUCV_GOLD)
        ax.set_xlabel("p̂", fontsize=10); ax.set_ylabel("densidad", fontsize=10)
        ax.set_title(f"Distribución muestral de p̂  (n = {n_p})", fontsize=11, color=TEXT_LIGHT)
        ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax.grid(axis="y", alpha=0.4)
        fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("E[p̂] = p",       f"{p_pob:.4f}",  PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Error estándar",  f"{ee_p:.5f}",   AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("np / n(1−p)",     f"{np_:.0f} / {nq_:.0f}",
                             PUCV_GOLD if valida else PUCV_RED), unsafe_allow_html=True)

        st.caption("El error estándar de p̂ es máximo cuando p = 0.5. "
                   "Por eso las encuestas asumen p = 0.5 al calcular el tamaño de muestra: "
                   "es el escenario más exigente.")

# ══════════════════════════════════════════════════════════════
# S²
# ══════════════════════════════════════════════════════════════
with tab3:
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown('<div class="seccion-label">VARIANZA MUESTRAL</div>', unsafe_allow_html=True)
        sig2_p = st.number_input("σ² — varianza poblacional", value=100.0, step=5.0,
                                 min_value=0.01, key="sig2p")
        n_s    = int(st.slider("n — tamaño de muestra", 2, 100, 20, key="ns"))
        gl     = n_s - 1

        st.markdown(f"""
        <div class="formula-box">
            <div class="titulo">RESULTADO CLAVE</div>
            <div class="cuerpo">
                <span style="color:{PUCV_GOLD};font-weight:bold;">
                (n−1)·S² / σ²  ~  χ²(n−1)
                </span><br><br>
                E[S²] = σ² = <span style="color:{AZUL_CLARO};">{sig2_p:.4f}</span><br>
                Var(S²) = 2σ⁴/(n−1) =
                <span style="color:{AZUL_CLARO};">{2*sig2_p**2/gl:.4f}</span><br>
                gl = n − 1 = <span style="color:{PUCV_GOLD};">{gl}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.caption("Aquí conecta la distribución χ² del módulo de continuas: "
                   "no es una curva suelta, es la distribución de la varianza muestral "
                   "reescalada. De aquí salen los IC y tests para σ².")

    with c2:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

        # χ² del estadístico
        ax = axes[0]
        D  = chi2(df=gl)
        xr = np.linspace(0.01, D.ppf(0.999), 600)
        ax.plot(xr, D.pdf(xr), color=PUCV_RED, linewidth=2.5, zorder=4)
        ax.fill_between(xr, D.pdf(xr), alpha=0.12, color=PUCV_RED)
        lo_c, hi_c = D.ppf(0.025), D.ppf(0.975)
        xm = np.linspace(lo_c, hi_c, 400)
        ax.fill_between(xm, D.pdf(xm), alpha=0.5, color=AZUL_BARRA, zorder=3,
                        label="95% central")
        ax.axvline(gl, color=PUCV_GOLD, linestyle="--", linewidth=1.4, label=f"E = gl = {gl}")
        ax.set_title(f"(n−1)S²/σ²  ~  χ²({gl})", fontsize=10.5, color=TEXT_LIGHT)
        ax.set_xlabel("valor", fontsize=9); ax.set_ylabel("densidad", fontsize=9)
        ax.legend(fontsize=8, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(axis="y", alpha=0.4)

        # Distribución implicada de S²
        ax2 = axes[1]
        s2  = xr * sig2_p / gl
        ax2.plot(s2, D.pdf(xr) * gl / sig2_p, color=PUCV_GOLD, linewidth=2.5, zorder=4)
        ax2.fill_between(s2, D.pdf(xr) * gl / sig2_p, alpha=0.15, color=PUCV_GOLD)
        ax2.axvline(sig2_p, color=PUCV_RED, linestyle="--", linewidth=1.4,
                    label=f"E[S²] = σ² = {sig2_p:.1f}")
        ax2.set_title("Distribución implicada de S²  (asimétrica)", fontsize=10.5, color=TEXT_LIGHT)
        ax2.set_xlabel("S²", fontsize=9); ax2.set_ylabel("densidad", fontsize=9)
        ax2.legend(fontsize=8, framealpha=0.25, edgecolor=PUCV_GOLD); ax2.grid(axis="y", alpha=0.4)

        fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("E[S²] = σ²",  f"{sig2_p:.3f}",            PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Var(S²)",     f"{2*sig2_p**2/gl:.3f}",    AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("gl = n−1",    f"{gl}",                    PUCV_RED),   unsafe_allow_html=True)

        st.caption("A diferencia de X̄, la distribución de S² es asimétrica: "
                   "por eso el IC para σ² no tiene la forma «estimador ± margen». "
                   "Se simetriza al crecer n.")

with st.expander("Resumen — los tres estadísticos"):
    st.markdown("""
    | Estadístico | Valor esperado | Error estándar | Distribución |
    |---|---|---|---|
    | X̄ | μ | σ/√n | Normal (exacta o por TCL); t si σ se estima |
    | p̂ | p | √(p(1−p)/n) | Normal aproximada si np ≥ 10 y n(1−p) ≥ 10 |
    | S² | σ² | √(2σ⁴/(n−1)) | (n−1)S²/σ² ~ χ²(n−1), asimétrica |

    Los tres comparten la misma idea: el estadístico es **insesgado** (su valor
    esperado es el parámetro) y su dispersión **disminuye al crecer n**. Esa es
    toda la base de la inferencia estadística.
    """)
