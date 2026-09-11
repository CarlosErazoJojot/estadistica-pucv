# ============================================================
#  pages/05_Inferencia.py
#  Intervalos de Confianza y Pruebas de Hipótesis
#  PUCV · Estadística Computacional
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2, t as t_dist
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.calculos import (PUCV_RED, PUCV_GOLD, AZUL_BARRA, AZUL_CLARO,
                            TEXT_LIGHT, MATPLOTLIB_STYLE, CSS_BASE, stat_box)

st.set_page_config(page_title="Inferencia · PUCV", page_icon="🎯", layout="wide")
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
    <h2>🎯 Inferencia Estadística</h2>
    <div class="formula">Intervalos de Confianza &nbsp;·&nbsp; Pruebas de Hipótesis &nbsp;·&nbsp; Error tipo I y II</div>
</div>
""", unsafe_allow_html=True)

# ✅ CORREGIDO: el criterio Z/t ya no está fijo en el código.
# Antes usaba "σ conocida O n≥30", una postura que no todos los textos comparten.
with st.sidebar:
    st.markdown('<div class="seccion-label">CRITERIO Z / t</div>', unsafe_allow_html=True)
    criterio = st.radio(
        "Con σ desconocida, usar:",
        ["t siempre (criterio estricto)", "Z si n ≥ 30 (aproximación)"],
        help="Con σ desconocida, el estadístico exacto es t. La aproximación "
             "por Z con n grande es común en varios textos introductorios. "
             "Elige el criterio que enseñas."
    )
    estricto = criterio.startswith("t siempre")
    st.caption("Con σ **conocida** siempre corresponde Z, en ambos criterios.")
    st.markdown("---")
    st.markdown('<div class="seccion-label">IR A</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Inicio", icon="🏠")
    st.page_link("pages/07_Distribuciones_Muestrales.py", label="Distribuciones Muestrales", icon="◀")
    st.page_link("pages/09_Potencia.py", label="Potencia", icon="▶")

    st.markdown('<div class="firma">Carlos Erazo Jojot · PUCV</div>',
                unsafe_allow_html=True)

def elegir_dist(sigma_conocida, n, estricto):
    """Devuelve (usar_z, gl, etiqueta)."""
    if sigma_conocida:
        return True, None, "Z ~ N(0,1)  (σ conocida)"
    if estricto:
        return False, n - 1, f"t({n-1} gl)  (σ desconocida)"
    if n >= 30:
        return True, None, "Z ~ N(0,1)  (aprox., n ≥ 30)"
    return False, n - 1, f"t({n-1} gl)  (σ desconocida, n < 30)"

tab1, tab2, tab3 = st.tabs(["📏 IC para μ", "⚖️ Prueba para μ", "🧪 Otras pruebas"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — Intervalo de Confianza
# ══════════════════════════════════════════════════════════════
with tab1:
    col_c, col_v = st.columns([1, 2], gap="large")

    with col_c:
        st.markdown('<div class="seccion-label">DATOS DE LA MUESTRA</div>', unsafe_allow_html=True)
        x_bar = st.number_input("X̄ — media muestral", value=105.0, step=0.5)
        n     = int(st.number_input("n — tamaño de muestra", value=30, step=1, min_value=2))
        sigma_conocida = st.checkbox("σ poblacional conocida", value=False)
        if sigma_conocida:
            sigma_p = st.number_input("σ — desviación poblacional", value=15.0, step=0.5, min_value=0.01)
            desv, simbolo = sigma_p, "σ"
        else:
            s       = st.number_input("s — desviación muestral", value=15.0, step=0.5, min_value=0.01)
            desv, simbolo = s, "s"
        conf  = st.slider("Nivel de confianza (1 − α)", 0.80, 0.99, 0.95, 0.01, format="%.2f")
        alpha = 1 - conf

        usar_z, gl, dist_txt = elegir_dist(sigma_conocida, n, estricto)
        crit  = norm.ppf(1 - alpha/2) if usar_z else t_dist.ppf(1 - alpha/2, df=gl)
        error = crit * desv / np.sqrt(n)
        ic_lo, ic_hi = x_bar - error, x_bar + error

    with col_v:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        xr = np.linspace(-4.5, 4.5, 500)
        yr = norm.pdf(xr) if usar_z else t_dist.pdf(xr, df=gl)

        ax.plot(xr, yr, color=PUCV_GOLD, linewidth=2.5, zorder=4)
        ax.fill_between(xr, yr, alpha=0.07, color=PUCV_GOLD)

        for xs in [np.linspace(-4.5, -crit, 200), np.linspace(crit, 4.5, 200)]:
            ys = norm.pdf(xs) if usar_z else t_dist.pdf(xs, df=gl)
            ax.fill_between(xs, ys, alpha=0.55, color=PUCV_RED, zorder=3)

        xm = np.linspace(-crit, crit, 300)
        ym = norm.pdf(xm) if usar_z else t_dist.pdf(xm, df=gl)
        ax.fill_between(xm, ym, alpha=0.3, color=AZUL_BARRA, zorder=2,
                        label=f"{conf*100:.0f}% confianza")
        ax.plot([], [], color=PUCV_RED, linewidth=6, alpha=0.55,
                label=f"α/2 = {alpha/2:.4f} por cola")

        ax.axvline(-crit, color=PUCV_GOLD, linestyle="--", linewidth=1.3)
        ax.axvline( crit, color=PUCV_GOLD, linestyle="--", linewidth=1.3)
        ax.text(-crit, max(yr)*0.55, f"−{crit:.3f}", ha="center", fontsize=8.5, color=PUCV_GOLD)
        ax.text( crit, max(yr)*0.55, f"+{crit:.3f}", ha="center", fontsize=8.5, color=PUCV_GOLD)

        ax.set_xlabel("Valor crítico", fontsize=10)
        ax.set_ylabel("Densidad", fontsize=10)
        ax.set_title(dist_txt, fontsize=10.5, color=TEXT_LIGHT)
        ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax.grid(axis="y", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown(f"""
        <div class="resultado-box" style="background:rgba(184,150,62,0.1);border-color:{PUCV_GOLD};">
            <div style="color:#A50044;font-size:0.7rem;letter-spacing:.15em;margin-bottom:10px;">
                INTERVALO DE CONFIANZA AL {conf*100:.0f}%
            </div>
            <div style="font-size:1.5rem;font-weight:700;color:#003087;text-align:center;">
                [ {ic_lo:.4f} &nbsp;,&nbsp; {ic_hi:.4f} ]
            </div>
            <div style="text-align:center;color:#4A688F;font-size:0.8rem;margin-top:8px;">
                X̄ ± {crit:.4f} · {simbolo}/√n &nbsp;=&nbsp; {x_bar:.2f} ± {error:.4f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown(stat_box("Margen de error", f"±{error:.4f}",   PUCV_GOLD),  unsafe_allow_html=True)
        c2.markdown(stat_box("Amplitud del IC", f"{2*error:.4f}",  AZUL_CLARO), unsafe_allow_html=True)
        c3.markdown(stat_box("Distribución",    "Z" if usar_z else f"t({gl})", PUCV_RED), unsafe_allow_html=True)

        st.caption("Interpretación: si repitiéramos el muestreo muchas veces, "
                   f"aproximadamente {conf*100:.0f}% de los intervalos construidos así "
                   "contendrían el verdadero μ. No es la probabilidad de que μ esté "
                   "en *este* intervalo.")

# ══════════════════════════════════════════════════════════════
# TAB 2 — Prueba de Hipótesis
# ══════════════════════════════════════════════════════════════
with tab2:
    col_c2, col_v2 = st.columns([1, 2], gap="large")

    with col_c2:
        st.markdown('<div class="seccion-label">HIPÓTESIS Y DATOS</div>', unsafe_allow_html=True)
        mu0    = st.number_input("μ₀ — valor bajo H₀", value=100.0, step=0.5)
        x_bar2 = st.number_input("X̄ — media muestral ", value=105.0, step=0.5)
        n2     = int(st.number_input("n — tamaño de muestra ", value=30, step=1, min_value=2))
        sig_con2 = st.checkbox("σ poblacional conocida ", value=False)
        desv2  = st.number_input(("σ" if sig_con2 else "s") + " — desviación",
                                 value=15.0, step=0.5, min_value=0.01)
        alpha2 = st.slider("α — nivel de significancia", 0.01, 0.20, 0.05, 0.01, format="%.2f")
        cola   = st.radio("Tipo de prueba", ["Bilateral (≠)", "Cola izquierda (<)", "Cola derecha (>)"])

        usar_z2, gl2, dist_txt2 = elegir_dist(sig_con2, n2, estricto)
        est_obs = (x_bar2 - mu0) / (desv2 / np.sqrt(n2))
        D       = norm if usar_z2 else t_dist(df=gl2)

        if "Bilateral" in cola:
            crit2    = D.ppf(1 - alpha2/2)
            p_val    = 2 * D.sf(abs(est_obs))
            rechazar = abs(est_obs) > crit2
            h1_txt   = f"H₁: μ ≠ {mu0:.2f}"
        elif "izquierda" in cola:
            crit2    = D.ppf(alpha2)
            p_val    = D.cdf(est_obs)
            rechazar = est_obs < crit2
            h1_txt   = f"H₁: μ < {mu0:.2f}"
        else:
            crit2    = D.ppf(1 - alpha2)
            p_val    = D.sf(est_obs)
            rechazar = est_obs > crit2
            h1_txt   = f"H₁: μ > {mu0:.2f}"

        st.markdown(f"""
        <div class="formula-box">
            <div class="titulo">HIPÓTESIS</div>
            <div class="cuerpo">
                H₀: μ = {mu0:.2f}<br>
                <span style="color:{PUCV_GOLD};">{h1_txt}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_v2:
        fig2, ax2 = plt.subplots(figsize=(8, 4.5))
        xr2 = np.linspace(-4.5, 4.5, 500)
        yr2 = D.pdf(xr2)

        ax2.plot(xr2, yr2, color=PUCV_GOLD, linewidth=2.5, zorder=4)
        ax2.fill_between(xr2, yr2, alpha=0.07, color=PUCV_GOLD)

        if "Bilateral" in cola:
            for xs in [np.linspace(-4.5, -abs(crit2), 200), np.linspace(abs(crit2), 4.5, 200)]:
                ax2.fill_between(xs, D.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            ax2.axvline(-abs(crit2), color=PUCV_RED, linestyle="--", linewidth=1.3)
            ax2.axvline( abs(crit2), color=PUCV_RED, linestyle="--", linewidth=1.3)
        elif "izquierda" in cola:
            xs = np.linspace(-4.5, crit2, 200)
            ax2.fill_between(xs, D.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            ax2.axvline(crit2, color=PUCV_RED, linestyle="--", linewidth=1.3)
        else:
            xs = np.linspace(crit2, 4.5, 200)
            ax2.fill_between(xs, D.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            ax2.axvline(crit2, color=PUCV_RED, linestyle="--", linewidth=1.3)

        color_obs = PUCV_RED if rechazar else AZUL_CLARO
        ax2.axvline(est_obs, color=color_obs, linewidth=2.5, zorder=5,
                    label=f"{'Z' if usar_z2 else 't'}_obs = {est_obs:.4f}")
        ax2.plot([], [], color=PUCV_RED, linewidth=6, alpha=0.55, label="Región de rechazo")

        ax2.set_xlabel("Estadístico de prueba", fontsize=10)
        ax2.set_ylabel("Densidad", fontsize=10)
        ax2.set_title(f"{dist_txt2}  ·  α = {alpha2:.2f}  ·  {cola}", fontsize=10.5, color=TEXT_LIGHT)
        ax2.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD)
        ax2.grid(axis="y", alpha=0.4)
        fig2.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

        color_res = PUCV_RED if rechazar else PUCV_GOLD
        texto_res = "Se rechaza H₀" if rechazar else "No se rechaza H₀"
        rgb       = "200,16,46" if rechazar else "184,150,62"
        st.markdown(f"""
        <div class="resultado-box" style="background:rgba({rgb},0.1);border-color:{color_res};">
            <div style="color:{color_res};font-size:0.7rem;letter-spacing:.15em;margin-bottom:10px;">
                RESULTADO
            </div>
            <div style="font-size:1.4rem;font-weight:700;color:{color_res};text-align:center;">
                {texto_res}
            </div>
            <div style="text-align:center;color:#4A688F;font-size:0.8rem;margin-top:8px;">
                p-valor = {p_val:.6f} &nbsp;{'<' if rechazar else '≥'}&nbsp; α = {alpha2:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown(stat_box("Estadístico obs.", f"{est_obs:.4f}", color_obs), unsafe_allow_html=True)
        c2.markdown(stat_box("Valor crítico",    f"{crit2:.4f}",   PUCV_RED),  unsafe_allow_html=True)
        c3.markdown(stat_box("p-valor",          f"{p_val:.6f}",   PUCV_GOLD), unsafe_allow_html=True)

        st.caption("No rechazar H₀ no significa que H₀ sea verdadera: "
                   "significa que los datos no aportan evidencia suficiente en su contra.")


# ══════════════════════════════════════════════════════════════
# TAB 3 — Otras pruebas: proporción, varianza, dos muestras
# ══════════════════════════════════════════════════════════════
with tab3:
    sub = st.radio("Tipo de prueba", 
                   ["Proporción (una muestra)", "Varianza (una muestra)",
                    "Diferencia de medias (dos muestras)", "Diferencia de proporciones"],
                   horizontal=False)

    # ── Proporción ────────────────────────────────────────────
    if sub.startswith("Proporción"):
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown('<div class="seccion-label">DATOS</div>', unsafe_allow_html=True)
            p0   = st.slider("p₀ — proporción bajo H₀", 0.01, 0.99, 0.30, 0.01, format="%.2f")
            n_pp = int(st.number_input("n — tamaño de muestra", value=200, step=10, min_value=2))
            x_pp = int(st.number_input("x — éxitos observados", value=75, step=1,
                                       min_value=0, max_value=n_pp))
            a_pp = st.slider("α", 0.01, 0.20, 0.05, 0.01, format="%.2f", key="app")
            cola_pp = st.radio("Cola", ["Bilateral (≠)", "Izquierda (<)", "Derecha (>)"], key="cpp")

            p_hat = x_pp / n_pp
            ee0   = np.sqrt(p0*(1-p0)/n_pp)     # EE bajo H0, no con p̂
            z_obs = (p_hat - p0) / ee0

            np0, nq0 = n_pp*p0, n_pp*(1-p0)
            if np0 < 10 or nq0 < 10:
                st.warning(f"np₀ = {np0:.1f}, n(1−p₀) = {nq0:.1f}. "
                           "Bajo 10 la aproximación Normal es poco fiable.")

            if cola_pp.startswith("Bilateral"):
                crit = norm.ppf(1-a_pp/2); pv = 2*norm.sf(abs(z_obs)); rech = abs(z_obs) > crit
            elif cola_pp.startswith("Izquierda"):
                crit = norm.ppf(a_pp);     pv = norm.cdf(z_obs);       rech = z_obs < crit
            else:
                crit = norm.ppf(1-a_pp);   pv = norm.sf(z_obs);        rech = z_obs > crit

            st.caption("El error estándar se calcula con p₀, no con p̂: bajo H₀ "
                       "la proporción verdadera se supone igual a p₀.")

        with c2:
            fig, ax = plt.subplots(figsize=(9, 4.4))
            xr = np.linspace(-4.5, 4.5, 600)
            ax.plot(xr, norm.pdf(xr), color=PUCV_GOLD, linewidth=2.5, zorder=4)
            ax.fill_between(xr, norm.pdf(xr), alpha=0.07, color=PUCV_GOLD)
            if cola_pp.startswith("Bilateral"):
                for xs in [np.linspace(-4.5,-abs(crit),200), np.linspace(abs(crit),4.5,200)]:
                    ax.fill_between(xs, norm.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            elif cola_pp.startswith("Izquierda"):
                xs = np.linspace(-4.5, crit, 200)
                ax.fill_between(xs, norm.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            else:
                xs = np.linspace(crit, 4.5, 200)
                ax.fill_between(xs, norm.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            col_o = PUCV_RED if rech else AZUL_CLARO
            ax.axvline(z_obs, color=col_o, linewidth=2.5, zorder=5, label=f"Z_obs = {z_obs:.4f}")
            ax.set_xlabel("Z", fontsize=10); ax.set_ylabel("densidad", fontsize=10)
            ax.set_title(f"H₀: p = {p0:.2f}   ·   p̂ = {p_hat:.4f}   ·   α = {a_pp:.2f}",
                         fontsize=10.5, color=TEXT_LIGHT)
            ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(axis="y", alpha=0.4)
            fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

            cr, tx = (PUCV_RED, "Se rechaza H₀") if rech else (PUCV_GOLD, "No se rechaza H₀")
            rgb = "200,16,46" if rech else "184,150,62"
            st.markdown(f"""
            <div class="resultado-box" style="background:rgba({rgb},0.1);border-color:{cr};">
                <div style="font-size:1.3rem;font-weight:700;color:{cr};text-align:center;">{tx}</div>
                <div style="text-align:center;color:#4A688F;font-size:0.8rem;margin-top:8px;">
                    p-valor = {pv:.6f} &nbsp;{'<' if rech else '≥'}&nbsp; α = {a_pp:.2f}
                </div>
            </div>""", unsafe_allow_html=True)
            k1,k2,k3 = st.columns(3)
            k1.markdown(stat_box("p̂", f"{p_hat:.5f}", PUCV_GOLD), unsafe_allow_html=True)
            k2.markdown(stat_box("Z observado", f"{z_obs:.4f}", col_o), unsafe_allow_html=True)
            k3.markdown(stat_box("p-valor", f"{pv:.6f}", PUCV_RED), unsafe_allow_html=True)

    # ── Varianza ──────────────────────────────────────────────
    elif sub.startswith("Varianza"):
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown('<div class="seccion-label">DATOS</div>', unsafe_allow_html=True)
            sig0 = st.number_input("σ₀ — desviación bajo H₀", value=10.0, step=0.5, min_value=0.01)
            s_vv = st.number_input("s — desviación muestral",  value=12.5, step=0.5, min_value=0.01)
            n_vv = int(st.number_input("n — tamaño de muestra", value=25, step=1, min_value=2))
            a_vv = st.slider("α", 0.01, 0.20, 0.05, 0.01, format="%.2f", key="avv")
            cola_vv = st.radio("Cola", ["Bilateral (≠)", "Izquierda (<)", "Derecha (>)"], key="cvv")

            gl_v  = n_vv - 1
            chi_obs = gl_v * s_vv**2 / sig0**2
            Dv = chi2(df=gl_v)

            if cola_vv.startswith("Bilateral"):
                c_lo, c_hi = Dv.ppf(a_vv/2), Dv.ppf(1-a_vv/2)
                pv = 2*min(Dv.cdf(chi_obs), Dv.sf(chi_obs))
                rech = chi_obs < c_lo or chi_obs > c_hi
            elif cola_vv.startswith("Izquierda"):
                c_lo, c_hi = Dv.ppf(a_vv), None
                pv = Dv.cdf(chi_obs); rech = chi_obs < c_lo
            else:
                c_lo, c_hi = None, Dv.ppf(1-a_vv)
                pv = Dv.sf(chi_obs);  rech = chi_obs > c_hi

            st.markdown(f"""
            <div class="formula-box">
                <div class="titulo">ESTADÍSTICO</div>
                <div class="cuerpo">
                    χ² = (n−1)s²/σ₀²<br>
                    = {gl_v}·{s_vv**2:.3f}/{sig0**2:.3f}<br>
                    <span style="color:{PUCV_GOLD};font-weight:bold;">= {chi_obs:.4f}</span>
                    &nbsp;con {gl_v} gl
                </div>
            </div>""", unsafe_allow_html=True)
            st.caption("Esta prueba es muy sensible al supuesto de normalidad, "
                       "bastante más que las pruebas sobre medias.")

        with c2:
            fig, ax = plt.subplots(figsize=(9, 4.4))
            xr = np.linspace(0.01, max(Dv.ppf(0.999), chi_obs*1.1), 600)
            ax.plot(xr, Dv.pdf(xr), color=PUCV_GOLD, linewidth=2.5, zorder=4)
            ax.fill_between(xr, Dv.pdf(xr), alpha=0.08, color=PUCV_GOLD)
            if c_lo is not None:
                xs = np.linspace(0.01, c_lo, 200)
                ax.fill_between(xs, Dv.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
                ax.axvline(c_lo, color=PUCV_RED, linestyle="--", linewidth=1.3)
            if c_hi is not None:
                xs = np.linspace(c_hi, xr[-1], 200)
                ax.fill_between(xs, Dv.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
                ax.axvline(c_hi, color=PUCV_RED, linestyle="--", linewidth=1.3)
            col_o = PUCV_RED if rech else AZUL_CLARO
            ax.axvline(chi_obs, color=col_o, linewidth=2.5, zorder=5, label=f"χ²_obs = {chi_obs:.4f}")
            ax.set_xlabel("χ²", fontsize=10); ax.set_ylabel("densidad", fontsize=10)
            ax.set_title(f"χ²({gl_v})   ·   H₀: σ = {sig0:.2f}   ·   α = {a_vv:.2f}",
                         fontsize=10.5, color=TEXT_LIGHT)
            ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(axis="y", alpha=0.4)
            fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

            cr, tx = (PUCV_RED, "Se rechaza H₀") if rech else (PUCV_GOLD, "No se rechaza H₀")
            rgb = "200,16,46" if rech else "184,150,62"
            st.markdown(f"""
            <div class="resultado-box" style="background:rgba({rgb},0.1);border-color:{cr};">
                <div style="font-size:1.3rem;font-weight:700;color:{cr};text-align:center;">{tx}</div>
                <div style="text-align:center;color:#4A688F;font-size:0.8rem;margin-top:8px;">
                    p-valor = {pv:.6f} &nbsp;{'<' if rech else '≥'}&nbsp; α = {a_vv:.2f}
                </div>
            </div>""", unsafe_allow_html=True)
            k1,k2,k3 = st.columns(3)
            k1.markdown(stat_box("s² / σ₀²", f"{s_vv**2/sig0**2:.4f}", PUCV_GOLD), unsafe_allow_html=True)
            k2.markdown(stat_box("χ² observado", f"{chi_obs:.4f}", col_o), unsafe_allow_html=True)
            k3.markdown(stat_box("p-valor", f"{pv:.6f}", PUCV_RED), unsafe_allow_html=True)

    # ── Dos muestras: medias ──────────────────────────────────
    elif sub.startswith("Diferencia de medias"):
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown('<div class="seccion-label">MUESTRA 1</div>', unsafe_allow_html=True)
            xa1 = st.number_input("X̄₁", value=105.0, step=0.5, key="ha1")
            sa1 = st.number_input("s₁",  value=15.0, step=0.5, min_value=0.01, key="hs1")
            na1 = int(st.number_input("n₁", value=30, step=1, min_value=2, key="hn1"))
            st.markdown('<div class="seccion-label">MUESTRA 2</div>', unsafe_allow_html=True)
            xa2 = st.number_input("X̄₂", value=98.0, step=0.5, key="ha2")
            sa2 = st.number_input("s₂",  value=18.0, step=0.5, min_value=0.01, key="hs2")
            na2 = int(st.number_input("n₂", value=35, step=1, min_value=2, key="hn2"))
            a_dm = st.slider("α", 0.01, 0.20, 0.05, 0.01, format="%.2f", key="adm")
            cola_dm = st.radio("Cola", ["Bilateral (≠)", "Izquierda (<)", "Derecha (>)"], key="cdm")
            pooled = st.checkbox("Asumir varianzas iguales (pooled)", value=False, key="pdm")

            dif = xa1 - xa2
            if pooled:
                gl_dm = na1 + na2 - 2
                sp2   = ((na1-1)*sa1**2 + (na2-1)*sa2**2)/gl_dm
                ee_dm = np.sqrt(sp2*(1/na1 + 1/na2))
                met   = f"pooled · gl = {gl_dm}"
            else:
                v1, v2 = sa1**2/na1, sa2**2/na2
                ee_dm  = np.sqrt(v1+v2)
                gl_dm  = (v1+v2)**2/(v1**2/(na1-1) + v2**2/(na2-1))
                met    = f"Welch · gl ≈ {gl_dm:.2f}"
            t_obs = dif / ee_dm
            Dt = t_dist(df=gl_dm)
            if cola_dm.startswith("Bilateral"):
                crit = Dt.ppf(1-a_dm/2); pv = 2*Dt.sf(abs(t_obs)); rech = abs(t_obs) > crit
            elif cola_dm.startswith("Izquierda"):
                crit = Dt.ppf(a_dm);     pv = Dt.cdf(t_obs);       rech = t_obs < crit
            else:
                crit = Dt.ppf(1-a_dm);   pv = Dt.sf(t_obs);        rech = t_obs > crit

        with c2:
            fig, ax = plt.subplots(figsize=(9, 4.4))
            xr = np.linspace(-4.5, 4.5, 600)
            ax.plot(xr, Dt.pdf(xr), color=PUCV_GOLD, linewidth=2.5, zorder=4)
            ax.fill_between(xr, Dt.pdf(xr), alpha=0.07, color=PUCV_GOLD)
            if cola_dm.startswith("Bilateral"):
                for xs in [np.linspace(-4.5,-abs(crit),200), np.linspace(abs(crit),4.5,200)]:
                    ax.fill_between(xs, Dt.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            elif cola_dm.startswith("Izquierda"):
                xs = np.linspace(-4.5, crit, 200); ax.fill_between(xs, Dt.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            else:
                xs = np.linspace(crit, 4.5, 200);  ax.fill_between(xs, Dt.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            col_o = PUCV_RED if rech else AZUL_CLARO
            ax.axvline(t_obs, color=col_o, linewidth=2.5, zorder=5, label=f"t_obs = {t_obs:.4f}")
            ax.set_xlabel("t", fontsize=10); ax.set_ylabel("densidad", fontsize=10)
            ax.set_title(f"H₀: μ₁ = μ₂   ·   {met}   ·   α = {a_dm:.2f}", fontsize=10.5, color=TEXT_LIGHT)
            ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(axis="y", alpha=0.4)
            fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

            cr, tx = (PUCV_RED, "Se rechaza H₀") if rech else (PUCV_GOLD, "No se rechaza H₀")
            rgb = "200,16,46" if rech else "184,150,62"
            st.markdown(f"""
            <div class="resultado-box" style="background:rgba({rgb},0.1);border-color:{cr};">
                <div style="font-size:1.3rem;font-weight:700;color:{cr};text-align:center;">{tx}</div>
                <div style="text-align:center;color:#4A688F;font-size:0.8rem;margin-top:8px;">
                    p-valor = {pv:.6f} &nbsp;{'<' if rech else '≥'}&nbsp; α = {a_dm:.2f}
                </div>
            </div>""", unsafe_allow_html=True)
            k1,k2,k3 = st.columns(3)
            k1.markdown(stat_box("X̄₁ − X̄₂", f"{dif:.4f}", PUCV_GOLD), unsafe_allow_html=True)
            k2.markdown(stat_box("Error estándar", f"{ee_dm:.4f}", AZUL_CLARO), unsafe_allow_html=True)
            k3.markdown(stat_box("t observado", f"{t_obs:.4f}", col_o), unsafe_allow_html=True)
            st.caption("Welch no requiere varianzas iguales y funciona bien aun cuando lo son. "
                       "Es la opción por defecto en la mayoría de los textos actuales.")

    # ── Dos proporciones ──────────────────────────────────────
    else:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown('<div class="seccion-label">GRUPO 1</div>', unsafe_allow_html=True)
            xg1 = int(st.number_input("x₁ — éxitos", value=45, step=1, min_value=0, key="xg1"))
            ng1 = int(st.number_input("n₁", value=120, step=5, min_value=1, key="ng1"))
            st.markdown('<div class="seccion-label">GRUPO 2</div>', unsafe_allow_html=True)
            xg2 = int(st.number_input("x₂ — éxitos", value=30, step=1, min_value=0, key="xg2"))
            ng2 = int(st.number_input("n₂", value=130, step=5, min_value=1, key="ng2"))
            a_dp = st.slider("α", 0.01, 0.20, 0.05, 0.01, format="%.2f", key="adp")
            cola_dp = st.radio("Cola", ["Bilateral (≠)", "Izquierda (<)", "Derecha (>)"], key="cdp")

            xg1, xg2 = min(xg1, ng1), min(xg2, ng2)
            ph1, ph2 = xg1/ng1, xg2/ng2
            p_pool   = (xg1 + xg2)/(ng1 + ng2)
            ee_dp    = np.sqrt(p_pool*(1-p_pool)*(1/ng1 + 1/ng2))
            z_dp     = (ph1 - ph2)/ee_dp

            if cola_dp.startswith("Bilateral"):
                crit = norm.ppf(1-a_dp/2); pv = 2*norm.sf(abs(z_dp)); rech = abs(z_dp) > crit
            elif cola_dp.startswith("Izquierda"):
                crit = norm.ppf(a_dp);     pv = norm.cdf(z_dp);       rech = z_dp < crit
            else:
                crit = norm.ppf(1-a_dp);   pv = norm.sf(z_dp);        rech = z_dp > crit

            st.markdown(f"""
            <div class="formula-box">
                <div class="titulo">PROPORCIÓN COMBINADA</div>
                <div class="cuerpo">
                    p̄ = (x₁+x₂)/(n₁+n₂) = ({xg1}+{xg2})/({ng1}+{ng2})<br>
                    <span style="color:{PUCV_GOLD};font-weight:bold;">= {p_pool:.5f}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            st.caption("Bajo H₀ ambas proporciones son iguales, así que el error estándar "
                       "se estima con la proporción combinada, no con cada p̂ por separado.")

        with c2:
            fig, ax = plt.subplots(figsize=(9, 4.4))
            xr = np.linspace(-4.5, 4.5, 600)
            ax.plot(xr, norm.pdf(xr), color=PUCV_GOLD, linewidth=2.5, zorder=4)
            ax.fill_between(xr, norm.pdf(xr), alpha=0.07, color=PUCV_GOLD)
            if cola_dp.startswith("Bilateral"):
                for xs in [np.linspace(-4.5,-abs(crit),200), np.linspace(abs(crit),4.5,200)]:
                    ax.fill_between(xs, norm.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            elif cola_dp.startswith("Izquierda"):
                xs = np.linspace(-4.5, crit, 200); ax.fill_between(xs, norm.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            else:
                xs = np.linspace(crit, 4.5, 200);  ax.fill_between(xs, norm.pdf(xs), alpha=0.55, color=PUCV_RED, zorder=3)
            col_o = PUCV_RED if rech else AZUL_CLARO
            ax.axvline(z_dp, color=col_o, linewidth=2.5, zorder=5, label=f"Z_obs = {z_dp:.4f}")
            ax.set_xlabel("Z", fontsize=10); ax.set_ylabel("densidad", fontsize=10)
            ax.set_title(f"H₀: p₁ = p₂   ·   p̂₁ = {ph1:.4f}, p̂₂ = {ph2:.4f}   ·   α = {a_dp:.2f}",
                         fontsize=10.5, color=TEXT_LIGHT)
            ax.legend(fontsize=8.5, framealpha=0.25, edgecolor=PUCV_GOLD); ax.grid(axis="y", alpha=0.4)
            fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

            cr, tx = (PUCV_RED, "Se rechaza H₀") if rech else (PUCV_GOLD, "No se rechaza H₀")
            rgb = "200,16,46" if rech else "184,150,62"
            st.markdown(f"""
            <div class="resultado-box" style="background:rgba({rgb},0.1);border-color:{cr};">
                <div style="font-size:1.3rem;font-weight:700;color:{cr};text-align:center;">{tx}</div>
                <div style="text-align:center;color:#4A688F;font-size:0.8rem;margin-top:8px;">
                    p-valor = {pv:.6f} &nbsp;{'<' if rech else '≥'}&nbsp; α = {a_dp:.2f}
                </div>
            </div>""", unsafe_allow_html=True)
            k1,k2,k3 = st.columns(3)
            k1.markdown(stat_box("p̂₁ − p̂₂", f"{ph1-ph2:.5f}", PUCV_GOLD), unsafe_allow_html=True)
            k2.markdown(stat_box("Error estándar", f"{ee_dp:.5f}", AZUL_CLARO), unsafe_allow_html=True)
            k3.markdown(stat_box("Z observado", f"{z_dp:.4f}", col_o), unsafe_allow_html=True)

with st.expander("Errores tipo I y II"):
    st.markdown(f"""
    | | H₀ verdadera | H₀ falsa |
    |---|---|---|
    | **No rechazar H₀** | Decisión correcta (1−α = {1-alpha2:.2f}) | Error tipo II (β) |
    | **Rechazar H₀** | Error tipo I (α = {alpha2:.2f}) | Decisión correcta (potencia = 1−β) |

    - **Error tipo I (α):** rechazar H₀ siendo verdadera. Lo fijas tú con el nivel de significancia.
    - **Error tipo II (β):** no rechazar H₀ siendo falsa. Depende de n, de α y del tamaño real del efecto.
    - **Potencia (1−β):** probabilidad de detectar un efecto que sí existe. Crece con n.

    Reducir α sin aumentar n aumenta β. Es un intercambio, no una mejora gratuita.

    Para **ver** α, β y la potencia como áreas sobre las curvas de H₀ y H₁, abre el módulo **Error tipo II y Potencia** en el menú lateral.
    """)
