# ============================================================
#  pages/09_IC_Avanzados.py
#  IC para proporción, varianza y diferencia de medias
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2, t as t_dist
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_BLUE, PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box)

st.set_page_config(page_title="IC avanzados · PUCV", page_icon="📏", layout="wide")
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
    <h2>📏 Intervalos de Confianza — proporción, varianza y diferencia</h2>
    <div class="formula">IC para p &nbsp;·&nbsp; σ² &nbsp;·&nbsp; μ₁ − μ₂ &nbsp;·&nbsp; efecto del tamaño de muestra</div>
</div>
""", unsafe_allow_html=True)

# ── Navegación ────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="seccion-label">IR A</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Inicio", icon=":material/home:")
    st.page_link("pages/09_Potencia.py", label="Potencia", icon=":material/arrow_back:")
    st.markdown("---")
    st.markdown('<div class="firma">Carlos Erazo Jojot · PUCV</div>',
                unsafe_allow_html=True)


def caja_ic(titulo, lo, hi, detalle, color=PUCV_GOLD):
    rgb = "184,150,62" if color == PUCV_GOLD else "126,186,255"
    return f"""
    <div class="resultado-box" style="background:rgba({rgb},0.1);border-color:{color};">
        <div style="color:{color};font-size:0.7rem;letter-spacing:.15em;margin-bottom:10px;">{titulo}</div>
        <div style="font-size:1.5rem;font-weight:700;color:#003087;text-align:center;">
            [ {lo:.5f} &nbsp;,&nbsp; {hi:.5f} ]
        </div>
        <div style="text-align:center;color:#4A688F;font-size:0.78rem;margin-top:8px;">{detalle}</div>
    </div>"""

tab1, tab2, tab3, tab4 = st.tabs(["IC para p", "IC para σ²", "IC para μ₁ − μ₂", "Efecto de n"])

# ══════════════════════════════════════════════════════════════
# IC para proporción
# ══════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown('<div class="seccion-label">DATOS</div>', unsafe_allow_html=True)
        n_p   = int(st.number_input("n — tamaño de muestra", value=200, step=10, min_value=2, key="npic"))
        x_ex  = int(st.number_input("x — número de éxitos", value=68, step=1, min_value=0,
                                    max_value=n_p, key="xic"))
        conf  = st.slider("Nivel de confianza", 0.80, 0.99, 0.95, 0.01, format="%.2f", key="cic")
        metodo = st.radio("Método", ["Wald (clásico)", "Wilson (recomendado)"])

        p_hat = x_ex / n_p
        alpha = 1 - conf
        z     = norm.ppf(1 - alpha/2)
        ee    = np.sqrt(p_hat*(1-p_hat)/n_p)

        if metodo.startswith("Wald"):
            lo, hi = p_hat - z*ee, p_hat + z*ee
            detalle = f"p̂ ± z·√(p̂(1−p̂)/n) = {p_hat:.4f} ± {z*ee:.5f}"
        else:
            den   = 1 + z**2/n_p
            centro = (p_hat + z**2/(2*n_p)) / den
            margen = z*np.sqrt(p_hat*(1-p_hat)/n_p + z**2/(4*n_p**2)) / den
            lo, hi = centro - margen, centro + margen
            detalle = f"centro corregido = {centro:.5f}, margen = {margen:.5f}"

        np_, nq_ = n_p*p_hat, n_p*(1-p_hat)
        if np_ < 10 or nq_ < 10:
            st.warning(f"np̂ = {np_:.1f}, n(1−p̂) = {nq_:.1f}. Con valores bajo 10 el método "
                       "de Wald es poco fiable; Wilson se comporta mucho mejor.")

    with c2:
        st.markdown(caja_ic(f"IC AL {conf*100:.0f}% PARA p", max(lo,0), min(hi,1), detalle),
                    unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("p̂",              f"{p_hat:.5f}",    PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Error estándar", f"{ee:.5f}",       AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("Amplitud",       f"{hi-lo:.5f}",    PUCV_RED),   unsafe_allow_html=True)

        # Comparación de ambos métodos
        lo_w, hi_w = p_hat - z*ee, p_hat + z*ee
        den = 1 + z**2/n_p
        cen = (p_hat + z**2/(2*n_p))/den
        mar = z*np.sqrt(p_hat*(1-p_hat)/n_p + z**2/(4*n_p**2))/den
        fig, ax = plt.subplots(figsize=(9, 2.8))
        for i, (nom, l, h, col) in enumerate([("Wald", lo_w, hi_w, AZUL_CLARO),
                                               ("Wilson", cen-mar, cen+mar, PUCV_GOLD)]):
            ax.plot([l, h], [i, i], color=col, linewidth=7, solid_capstyle="round", alpha=0.85)
            ax.plot([(l+h)/2], [i], "o", color="#fff", markersize=6, zorder=5)
            ax.text(h, i+0.22, f"{nom}: [{l:.4f}, {h:.4f}]", fontsize=8.5, color=col, ha="right")
        ax.axvline(p_hat, color=PUCV_RED, linestyle="--", linewidth=1.3, label=f"p̂ = {p_hat:.4f}")
        ax.set_yticks([0, 1]); ax.set_yticklabels(["Wald", "Wilson"], fontsize=9)
        ax.set_ylim(-0.6, 1.7); ax.set_xlabel("p", fontsize=9.5)
        ax.set_title("Comparación de métodos", fontsize=10, color=TEXT_LIGHT)
        ax.legend(fontsize=8, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(axis="x", alpha=0.3)
        fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

        st.caption("Wald puede producir límites fuera de [0,1] y su cobertura real "
                   "suele quedar por debajo del nivel nominal. Wilson corrige ambos problemas "
                   "y es el método que recomienda la literatura actual.")

# ══════════════════════════════════════════════════════════════
# IC para varianza
# ══════════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown('<div class="seccion-label">DATOS</div>', unsafe_allow_html=True)
        n_v  = int(st.number_input("n — tamaño de muestra", value=25, step=1, min_value=2, key="nv"))
        s_v  = st.number_input("s — desviación muestral", value=12.0, step=0.5,
                               min_value=0.01, key="sv")
        conf_v = st.slider("Nivel de confianza", 0.80, 0.99, 0.95, 0.01, format="%.2f", key="cv")

        gl    = n_v - 1
        a_v   = 1 - conf_v
        chi_lo = chi2.ppf(a_v/2,     df=gl)     # cuantil inferior
        chi_hi = chi2.ppf(1 - a_v/2, df=gl)     # cuantil superior
        var_lo = gl * s_v**2 / chi_hi           # ojo: cuantil superior va al DENOMINADOR del límite inferior
        var_hi = gl * s_v**2 / chi_lo

        st.markdown(f"""
        <div class="formula-box">
            <div class="titulo">CONSTRUCCIÓN</div>
            <div class="cuerpo">
                (n−1)S²/σ² ~ χ²({gl})<br><br>
                χ²<sub>{a_v/2:.3f}</sub> = <span style="color:{AZUL_CLARO};">{chi_lo:.4f}</span><br>
                χ²<sub>{1-a_v/2:.3f}</sub> = <span style="color:{AZUL_CLARO};">{chi_hi:.4f}</span><br><br>
                <span style="color:{PUCV_GOLD};">
                límite inf = (n−1)s²/χ²<sub>sup</sub><br>
                límite sup = (n−1)s²/χ²<sub>inf</sub></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("El cuantil superior genera el límite INFERIOR: van cruzados "
                   "porque σ² está en el denominador del estadístico.")

    with c2:
        st.markdown(caja_ic(f"IC AL {conf_v*100:.0f}% PARA σ²", var_lo, var_hi,
                            f"s² = {s_v**2:.4f}   ·   gl = {gl}"), unsafe_allow_html=True)
        st.markdown(caja_ic(f"IC AL {conf_v*100:.0f}% PARA σ", np.sqrt(var_lo), np.sqrt(var_hi),
                            f"s = {s_v:.4f}   (raíz de los límites anteriores)", AZUL_CLARO),
                    unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(9, 4.2))
        D  = chi2(df=gl)
        xr = np.linspace(0.01, D.ppf(0.999), 600)
        ax.plot(xr, D.pdf(xr), color=PUCV_RED, linewidth=2.5, zorder=4)
        ax.fill_between(xr, D.pdf(xr), alpha=0.1, color=PUCV_RED)
        xm = np.linspace(chi_lo, chi_hi, 400)
        ax.fill_between(xm, D.pdf(xm), alpha=0.5, color=AZUL_BARRA, zorder=3,
                        label=f"{conf_v*100:.0f}% central")
        for xs in [np.linspace(0.01, chi_lo, 200), np.linspace(chi_hi, D.ppf(0.999), 200)]:
            ax.fill_between(xs, D.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
        ax.axvline(chi_lo, color=PUCV_GOLD, linestyle="--", linewidth=1.3)
        ax.axvline(chi_hi, color=PUCV_GOLD, linestyle="--", linewidth=1.3)
        ax.set_xlabel("χ²", fontsize=9.5); ax.set_ylabel("densidad", fontsize=9.5)
        ax.set_title(f"χ²({gl})  —  el IC para σ² NO es simétrico", fontsize=10.5, color=TEXT_LIGHT)
        ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(axis="y", alpha=0.4)
        fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

        dist_lo = s_v**2 - var_lo
        dist_hi = var_hi - s_v**2
        st.caption(f"Distancia de s² al límite inferior: {dist_lo:.4f}. Al superior: {dist_hi:.4f}. "
                   "No coinciden — el intervalo es asimétrico y no tiene la forma «estimador ± margen».")

# ══════════════════════════════════════════════════════════════
# IC para diferencia de medias
# ══════════════════════════════════════════════════════════════
with tab3:
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown('<div class="seccion-label">MUESTRA 1</div>', unsafe_allow_html=True)
        xb1 = st.number_input("X̄₁", value=105.0, step=0.5, key="xb1")
        s1  = st.number_input("s₁",  value=15.0,  step=0.5, min_value=0.01, key="s1")
        n1  = int(st.number_input("n₁", value=30, step=1, min_value=2, key="n1"))
        st.markdown('<div class="seccion-label">MUESTRA 2</div>', unsafe_allow_html=True)
        xb2 = st.number_input("X̄₂", value=98.0,  step=0.5, key="xb2")
        s2  = st.number_input("s₂",  value=18.0,  step=0.5, min_value=0.01, key="s2")
        n2  = int(st.number_input("n₂", value=35, step=1, min_value=2, key="n2"))
        conf_d = st.slider("Nivel de confianza", 0.80, 0.99, 0.95, 0.01, format="%.2f", key="cd")
        var_ig = st.checkbox("Asumir varianzas iguales (pooled)", value=False)

        a_d  = 1 - conf_d
        dif  = xb1 - xb2

        if var_ig:
            gl_d  = n1 + n2 - 2
            sp2   = ((n1-1)*s1**2 + (n2-1)*s2**2) / gl_d
            ee_d  = np.sqrt(sp2*(1/n1 + 1/n2))
            met   = f"pooled · s²ₚ = {sp2:.4f} · gl = {gl_d}"
        else:
            # Welch-Satterthwaite
            v1, v2 = s1**2/n1, s2**2/n2
            ee_d   = np.sqrt(v1 + v2)
            gl_d   = (v1+v2)**2 / (v1**2/(n1-1) + v2**2/(n2-1))
            met    = f"Welch · gl ≈ {gl_d:.2f}"

        t_c   = t_dist.ppf(1 - a_d/2, df=gl_d)
        margen = t_c * ee_d
        lo_d, hi_d = dif - margen, dif + margen

    with c2:
        st.markdown(caja_ic(f"IC AL {conf_d*100:.0f}% PARA μ₁ − μ₂", lo_d, hi_d,
                            f"({xb1:.2f} − {xb2:.2f}) ± {t_c:.4f}·{ee_d:.4f}   ·   {met}"),
                    unsafe_allow_html=True)

        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box("Diferencia X̄₁−X̄₂", f"{dif:.4f}",    PUCV_GOLD),  unsafe_allow_html=True)
        k2.markdown(stat_box("Error estándar",    f"{ee_d:.4f}",   AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("t crítico",         f"{t_c:.4f}",    PUCV_RED),   unsafe_allow_html=True)

        contiene_cero = lo_d <= 0 <= hi_d
        if contiene_cero:
            st.info("El intervalo **contiene el 0**: con este nivel de confianza los datos son "
                    "compatibles con μ₁ = μ₂. Equivale a no rechazar H₀ en una prueba bilateral "
                    f"con α = {a_d:.2f}.")
        else:
            st.success("El intervalo **no contiene el 0**: hay evidencia de diferencia entre las "
                       f"medias al nivel α = {a_d:.2f}.")

        fig, ax = plt.subplots(figsize=(9, 3.2))
        ax.plot([lo_d, hi_d], [0, 0], color=PUCV_GOLD, linewidth=8,
                solid_capstyle="round", alpha=0.85)
        ax.plot([dif], [0], "o", color=PUCV_BLUE, markersize=9, zorder=5)
        ax.axvline(0, color=PUCV_RED, linestyle="--", linewidth=1.6,
                   label="μ₁ − μ₂ = 0  (sin diferencia)")
        ax.text(dif, 0.22, f"{dif:.3f}", ha="center", fontsize=9.5, color=PUCV_GOLD, fontweight="bold")
        ax.text(lo_d, -0.3, f"{lo_d:.3f}", ha="center", fontsize=8.5, color=AZUL_CLARO)
        ax.text(hi_d, -0.3, f"{hi_d:.3f}", ha="center", fontsize=8.5, color=AZUL_CLARO)
        ax.set_ylim(-0.6, 0.6); ax.set_yticks([])
        ax.set_xlabel("μ₁ − μ₂", fontsize=10)
        ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax.grid(axis="x", alpha=0.3)
        fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

        st.caption("Welch no exige varianzas iguales y se comporta bien incluso cuando lo son; "
                   "por eso muchos textos actuales lo recomiendan por defecto sobre el pooled.")

# ══════════════════════════════════════════════════════════════
# Efecto de n
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("Cómo cambia la amplitud del intervalo al aumentar el tamaño de muestra.")
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown('<div class="seccion-label">ESCENARIO</div>', unsafe_allow_html=True)
        xb_e   = st.number_input("X̄ — media muestral", value=100.0, step=1.0, key="xbe")
        s_e    = st.number_input("s — desviación", value=15.0, step=0.5, min_value=0.01, key="se2")
        conf_e = st.slider("Nivel de confianza", 0.80, 0.99, 0.95, 0.01, format="%.2f", key="ce")
        n_ref  = int(st.slider("n de referencia", 2, 500, 30, key="nref"))
        a_e    = 1 - conf_e

    with c2:
        ns   = np.arange(2, 501)
        tcs  = t_dist.ppf(1 - a_e/2, df=ns-1)
        mars = tcs * s_e / np.sqrt(ns)

        fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))

        ax = axes[0]
        ax.fill_between(ns, xb_e - mars, xb_e + mars, alpha=0.3, color=AZUL_BARRA,
                        label=f"IC al {conf_e*100:.0f}%")
        ax.plot(ns, xb_e + mars, color=PUCV_GOLD, linewidth=1.8)
        ax.plot(ns, xb_e - mars, color=PUCV_GOLD, linewidth=1.8)
        ax.axhline(xb_e, color=PUCV_RED, linestyle="--", linewidth=1.3, label=f"X̄ = {xb_e:.1f}")
        m_ref = t_dist.ppf(1-a_e/2, df=n_ref-1) * s_e/np.sqrt(n_ref)
        ax.axvline(n_ref, color=AZUL_CLARO, linestyle=":", linewidth=1.5,
                   label=f"n = {n_ref} → ±{m_ref:.3f}")
        ax.set_xlabel("n", fontsize=9.5); ax.set_ylabel("valor", fontsize=9.5)
        ax.set_title("El intervalo se estrecha con n", fontsize=10.5, color=TEXT_LIGHT)
        ax.legend(fontsize=8, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(alpha=0.35)

        ax2 = axes[1]
        ax2.plot(ns, 2*mars, color=PUCV_GOLD, linewidth=2.4, zorder=4)
        ax2.plot([n_ref], [2*m_ref], "o", color=PUCV_GOLD, markersize=9,
                 markeredgecolor="#FFFFFF", zorder=6)
        for nn in (n_ref, 4*n_ref):
            if nn <= 500:
                mm = t_dist.ppf(1-a_e/2, df=nn-1)*s_e/np.sqrt(nn)
                ax2.annotate(f"n={nn}\n{2*mm:.3f}", xy=(nn, 2*mm), xytext=(nn+25, 2*mm+0.6),
                             fontsize=8, color=AZUL_CLARO,
                             arrowprops=dict(arrowstyle="->", color=AZUL_CLARO, lw=1))
        ax2.set_xlabel("n", fontsize=9.5); ax2.set_ylabel("amplitud del IC", fontsize=9.5)
        ax2.set_title("Rendimientos decrecientes: amplitud ∝ 1/√n", fontsize=10.5, color=TEXT_LIGHT)
        ax2.grid(alpha=0.35)

        fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

        m4 = t_dist.ppf(1-a_e/2, df=4*n_ref-1)*s_e/np.sqrt(4*n_ref) if 4*n_ref <= 500 else None
        k1, k2, k3 = st.columns(3)
        k1.markdown(stat_box(f"Margen con n={n_ref}", f"±{m_ref:.4f}", PUCV_GOLD), unsafe_allow_html=True)
        k2.markdown(stat_box(f"Margen con n={4*n_ref}",
                             f"±{m4:.4f}" if m4 else "—", AZUL_CLARO), unsafe_allow_html=True)
        k3.markdown(stat_box("Razón", f"{m_ref/m4:.3f}" if m4 else "—", PUCV_RED), unsafe_allow_html=True)

        st.caption("Cuadruplicar n reduce el margen aproximadamente a la mitad. "
                   "Esa razón cercana a 2 es la consecuencia directa del √n en el denominador.")

with st.expander("Resumen de los tres intervalos"):
    st.markdown("""
    | Parámetro | Forma del IC | Distribución | ¿Simétrico? |
    |---|---|---|---|
    | μ | X̄ ± t·s/√n | t(n−1) | Sí |
    | p | p̂ ± z·√(p̂(1−p̂)/n) — Wald<br>o versión de Wilson | Normal aprox. | Wald sí, Wilson no |
    | σ² | [(n−1)s²/χ²_sup , (n−1)s²/χ²_inf] | χ²(n−1) | **No** |
    | μ₁−μ₂ | (X̄₁−X̄₂) ± t·EE | t (Welch o pooled) | Sí |

    **La idea que unifica todo:** un IC se construye despejando el parámetro desde
    la distribución muestral del estadístico. Cuando esa distribución es simétrica
    (Normal, t) el intervalo toma la forma «estimador ± margen». Cuando es asimétrica
    (χ²) no puede tomarla, y por eso el IC para σ² se ve distinto.
    """)
