# ============================================================
#  pages/10_Potencia.py
#  Error tipo I y II · Potencia de una prueba
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

st.set_page_config(page_title="Potencia · PUCV", page_icon="🔬", layout="wide")
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
    <h2>🔬 Error tipo II y Potencia</h2>
    <div class="formula">α · β · 1−β &nbsp;—&nbsp; las dos distribuciones que conviven en toda prueba</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Una prueba de hipótesis compara **dos mundos posibles**. Bajo H₀ la media es μ₀;
bajo H₁ es μ₁. La región de rechazo se fija mirando solo H₀ — pero β y la potencia
solo se pueden ver mirando **ambas** curvas a la vez.
""")

with st.sidebar:
    st.markdown('<div class="seccion-label">ESCENARIO</div>', unsafe_allow_html=True)
    mu0    = st.number_input("μ₀ — bajo H₀", value=100.0, step=1.0)
    mu1    = st.number_input("μ₁ — valor real (bajo H₁)", value=105.0, step=1.0)
    sigma  = st.number_input("σ — desviación", value=15.0, step=0.5, min_value=0.01)
    n      = int(st.slider("n — tamaño de muestra", 2, 300, 30))
    alpha  = st.slider("α — significancia", 0.01, 0.20, 0.05, 0.01, format="%.2f")
    cola   = st.radio("Tipo de prueba", ["Cola derecha (>)", "Cola izquierda (<)", "Bilateral (≠)"])
    st.markdown("---")
    st.markdown('<div class="seccion-label">IR A</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Inicio", icon=":material/home:")
    st.page_link("pages/08_Inferencia.py", label="Inferencia", icon=":material/arrow_back:")
    st.page_link("pages/10_IC_Avanzados.py", label="IC avanzados", icon=":material/arrow_forward:")

    st.markdown('<div class="firma">Carlos Erazo Jojot · PUCV</div>',
                unsafe_allow_html=True)

ee    = sigma / np.sqrt(n)          # error estándar
D0    = norm(loc=mu0, scale=ee)     # distribución de X̄ bajo H0
D1    = norm(loc=mu1, scale=ee)     # distribución de X̄ bajo H1
delta = abs(mu1 - mu0)
d     = delta / sigma               # tamaño del efecto (d de Cohen)

# Valores críticos en la escala de X̄ y cálculo de β
if cola.startswith("Cola derecha"):
    xc      = D0.ppf(1 - alpha)
    beta    = D1.cdf(xc)
    regiones = [(xc, np.inf)]
elif cola.startswith("Cola izquierda"):
    xc      = D0.ppf(alpha)
    beta    = D1.sf(xc)
    regiones = [(-np.inf, xc)]
else:
    xc_lo   = D0.ppf(alpha/2)
    xc_hi   = D0.ppf(1 - alpha/2)
    beta    = D1.cdf(xc_hi) - D1.cdf(xc_lo)
    regiones = [(-np.inf, xc_lo), (xc_hi, np.inf)]

potencia = 1 - beta

# ── Gráfico principal ─────────────────────────────────────────
lo = min(mu0, mu1) - 4.2*ee
hi = max(mu0, mu1) + 4.2*ee
x  = np.linspace(lo, hi, 900)

fig, ax = plt.subplots(figsize=(11, 5.2))

ax.plot(x, D0.pdf(x), color=AZUL_CLARO, linewidth=2.4, zorder=5, label=f"H₀: μ = {mu0:.1f}")
ax.plot(x, D1.pdf(x), color=PUCV_GOLD,  linewidth=2.4, zorder=5, label=f"H₁: μ = {mu1:.1f}")

# α — área bajo H0 en la región de rechazo
for lo_r, hi_r in regiones:
    xs = x[(x >= (lo_r if np.isfinite(lo_r) else lo)) & (x <= (hi_r if np.isfinite(hi_r) else hi))]
    if len(xs):
        ax.fill_between(xs, D0.pdf(xs), alpha=0.6, color=PUCV_RED, zorder=3)

# β — área bajo H1 FUERA de la región de rechazo
if cola.startswith("Cola derecha"):
    xs_b = x[x <= xc]
elif cola.startswith("Cola izquierda"):
    xs_b = x[x >= xc]
else:
    xs_b = x[(x >= xc_lo) & (x <= xc_hi)]
if len(xs_b):
    ax.fill_between(xs_b, D1.pdf(xs_b), alpha=0.45, color="#6B4BA8", zorder=2)

# potencia — área bajo H1 DENTRO de la región de rechazo
for lo_r, hi_r in regiones:
    xs = x[(x >= (lo_r if np.isfinite(lo_r) else lo)) & (x <= (hi_r if np.isfinite(hi_r) else hi))]
    if len(xs):
        ax.fill_between(xs, D1.pdf(xs), alpha=0.4, color=AZUL_BARRA, zorder=4,
                        hatch="///", edgecolor=AZUL_CLARO, linewidth=0)

for lo_r, hi_r in regiones:
    for v in (lo_r, hi_r):
        if np.isfinite(v):
            ax.axvline(v, color=PUCV_RED, linestyle="--", linewidth=1.5, zorder=6)

ax.plot([], [], color=PUCV_RED,  linewidth=7, alpha=0.6,  label=f"α = {alpha:.3f}  (error tipo I)")
ax.plot([], [], color="#6B4BA8", linewidth=7, alpha=0.45, label=f"β = {beta:.4f}  (error tipo II)")
ax.plot([], [], color=AZUL_BARRA,linewidth=7, alpha=0.4,  label=f"potencia = {potencia:.4f}")

ax.set_xlabel("X̄  (media muestral)", fontsize=10.5, labelpad=8)
ax.set_ylabel("densidad", fontsize=10.5)
ax.set_title(f"n = {n}  ·  error estándar = {ee:.3f}  ·  distancia |μ₁−μ₀| = {delta:.2f}",
             fontsize=11, color=TEXT_LIGHT)
ax.legend(fontsize=9, framealpha=0.25, edgecolor=PUCV_GOLD, loc="upper right")
ax.grid(axis="y", alpha=0.35)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(stat_box("α — error tipo I",  f"{alpha:.4f}",    PUCV_RED),   unsafe_allow_html=True)
c2.markdown(stat_box("β — error tipo II", f"{beta:.4f}",     "#6B4BA8"),  unsafe_allow_html=True)
c3.markdown(stat_box("Potencia (1−β)",    f"{potencia:.4f}", PUCV_GOLD),  unsafe_allow_html=True)
c4.markdown(stat_box("d de Cohen",        f"{d:.4f}",        AZUL_CLARO), unsafe_allow_html=True)

if potencia < 0.80 and delta > 0:
    # n necesario para potencia 0.80 (aproximación de una cola / bilateral)
    z_a = norm.ppf(1 - alpha) if not cola.startswith("Bilateral") else norm.ppf(1 - alpha/2)
    n_req = int(np.ceil(((z_a + norm.ppf(0.80)) * sigma / delta)**2))
    st.warning(f"Potencia = {potencia:.3f}, bajo el 0.80 habitual. "
               f"Para alcanzar 0.80 con este efecto se requiere aproximadamente **n = {n_req}** "
               f"(actualmente n = {n}).")
elif delta == 0:
    st.info("Con μ₁ = μ₀ no hay efecto que detectar: la «potencia» calculada coincide con α.")
else:
    st.success(f"Potencia = {potencia:.3f}, igual o superior al 0.80 habitual.")

st.divider()

# ── Curva de potencia ─────────────────────────────────────────
st.markdown('<div class="seccion-label">CURVA DE POTENCIA</div>', unsafe_allow_html=True)

cc1, cc2 = st.columns(2, gap="large")

with cc1:
    st.caption("Potencia en función del valor real de μ, con n fijo.")
    mus = np.linspace(mu0 - 4*sigma/np.sqrt(n)*1.6, mu0 + 4*sigma/np.sqrt(n)*1.6, 300)
    if cola.startswith("Cola derecha"):
        pot = norm.sf(xc, loc=mus, scale=ee)
    elif cola.startswith("Cola izquierda"):
        pot = norm.cdf(xc, loc=mus, scale=ee)
    else:
        pot = norm.cdf(xc_lo, loc=mus, scale=ee) + norm.sf(xc_hi, loc=mus, scale=ee)

    fig2, ax2 = plt.subplots(figsize=(6, 4.2))
    ax2.plot(mus, pot, color=PUCV_GOLD, linewidth=2.5, zorder=4)
    ax2.axhline(alpha, color=PUCV_RED, linestyle=":", linewidth=1.4, label=f"α = {alpha:.2f}")
    ax2.axhline(0.80, color=AZUL_CLARO, linestyle="--", linewidth=1.3, label="0.80 de referencia")
    ax2.axvline(mu0, color=PUCV_RED, linestyle="--", linewidth=1.3, alpha=0.7, label=f"μ₀ = {mu0:.1f}")
    ax2.plot([mu1], [potencia], "o", color=PUCV_GOLD, markersize=9,
             markeredgecolor="#FFFFFF", zorder=6, label=f"μ₁ = {mu1:.1f}")
    ax2.set_xlabel("valor real de μ", fontsize=9.5)
    ax2.set_ylabel("potencia", fontsize=9.5)
    ax2.set_ylim(-0.03, 1.03)
    ax2.legend(fontsize=8, framealpha=0.25, edgecolor=PUCV_GOLD)
    ax2.grid(alpha=0.35)
    fig2.tight_layout(); st.pyplot(fig2, use_container_width=True); plt.close(fig2)
    st.caption("En μ = μ₀ la potencia vale exactamente α: rechazar cuando H₀ es cierta "
               "es, por definición, el error tipo I.")

with cc2:
    st.caption("Potencia en función de n, con el efecto |μ₁−μ₀| fijo.")
    ns  = np.arange(2, 301)
    ees = sigma / np.sqrt(ns)
    if cola.startswith("Cola derecha"):
        xcs = norm.ppf(1-alpha, loc=mu0, scale=ees); potn = norm.sf(xcs, loc=mu1, scale=ees)
    elif cola.startswith("Cola izquierda"):
        xcs = norm.ppf(alpha, loc=mu0, scale=ees);   potn = norm.cdf(xcs, loc=mu1, scale=ees)
    else:
        lo_s = norm.ppf(alpha/2, loc=mu0, scale=ees); hi_s = norm.ppf(1-alpha/2, loc=mu0, scale=ees)
        potn = norm.cdf(lo_s, loc=mu1, scale=ees) + norm.sf(hi_s, loc=mu1, scale=ees)

    fig3, ax3 = plt.subplots(figsize=(6, 4.2))
    ax3.plot(ns, potn, color=AZUL_CLARO, linewidth=2.5, zorder=4)
    ax3.axhline(0.80, color=PUCV_GOLD, linestyle="--", linewidth=1.3, label="0.80 de referencia")
    ax3.plot([n], [potencia], "o", color=PUCV_GOLD, markersize=9,
             markeredgecolor="#FFFFFF", zorder=6, label=f"n = {n} → {potencia:.3f}")
    ax3.set_xlabel("tamaño de muestra n", fontsize=9.5)
    ax3.set_ylabel("potencia", fontsize=9.5)
    ax3.set_ylim(-0.03, 1.03)
    ax3.legend(fontsize=8, framealpha=0.25, edgecolor=PUCV_GOLD)
    ax3.grid(alpha=0.35)
    fig3.tight_layout(); st.pyplot(fig3, use_container_width=True); plt.close(fig3)
    st.caption("La potencia crece con n pero con rendimientos decrecientes: "
               "duplicar n no duplica la potencia.")

with st.expander("Cómo leer el gráfico principal"):
    st.markdown(f"""
    | Zona | Qué representa | Valor actual |
    |---|---|---|
    | 🔴 Roja | α — probabilidad de rechazar H₀ siendo verdadera | {alpha:.4f} |
    | 🟣 Morada | β — probabilidad de NO rechazar H₀ siendo falsa | {beta:.4f} |
    | 🔵 Rayada | Potencia — probabilidad de detectar el efecto real | {potencia:.4f} |

    **Las tres relaciones que conviene que los estudiantes descubran moviendo los controles:**

    1. **α y β se oponen.** Baja α de {alpha:.2f} a 0.01 con n fijo y observa cómo β sube.
       Ser más exigente para rechazar implica dejar pasar más efectos reales.
    2. **n los mejora a ambos.** Sube n y las dos curvas se estrechan: β cae sin tocar α.
       Es la única forma de mejorar ambos errores a la vez, y cuesta datos.
    3. **El tamaño del efecto manda.** Acerca μ₁ a μ₀: las curvas se solapan y la potencia
       se desploma hacia α. Efectos pequeños exigen muestras grandes.

    **Sobre el 0.80:** es una convención, no un requisito matemático. El valor apropiado
    depende del costo relativo de cada tipo de error en el problema concreto.
    """)
