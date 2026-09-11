# ============================================================
#  app.py — Landing principal
#  Estadística y Probabilidad · PUCV
#  Carlos Erazo Jojot
# ============================================================

import streamlit as st

st.set_page_config(
    page_title="Estadística · PUCV",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
html, body, [class*="css"] { font-family: 'DM Mono', monospace; }
.stApp { background: #FFFFFF; }
h1, h2, h3, p, li, .stMarkdown { color: #003087; }

.pucv-header {
    background: linear-gradient(90deg, #003087 0%, #0A47B0 70%, #1B5FD0 100%);
    border-bottom: 4px solid #A50044;
    border-radius: 10px;
    padding: 30px 36px;
    margin-bottom: 30px;
}
.pucv-header h1 {
    font-family:'Playfair Display',serif; font-size:2.2rem;
    color:#FFFFFF !important; margin:0 0 8px 0;
}
.pucv-header .sub { font-size:0.82rem; color:#F5C6D8; letter-spacing:0.15em; }
.pucv-header .autor { font-size:0.8rem; color:#FFFFFF; margin-top:10px; opacity:0.94; }

.seccion {
    color:#003087; font-size:0.74rem; letter-spacing:0.2em; text-transform:uppercase;
    font-weight:700; border-bottom:2px solid #A50044;
    padding-bottom:8px; margin:26px 0 14px 0;
}
.modulo-card {
    background:#F4F7FB;
    border:1px solid #D4DEEC; border-left:4px solid #A50044;
    border-radius:10px; padding:18px 20px 10px 20px; margin-bottom:6px;
}
.modulo-card h3 {
    font-family:'Playfair Display',serif; color:#003087 !important;
    margin:0 0 6px 0; font-size:1rem;
}
.modulo-card p { color:#34517D !important; font-size:0.8rem; margin:0; line-height:1.6; }

/* Enlaces de página: apariencia de botón discreto */
div[data-testid="stPageLink"] a {
    background:#FFFFFF !important; border:1px solid #A50044 !important;
    border-radius:20px !important; padding:3px 14px !important;
    margin:0 0 16px 0 !important;
}
div[data-testid="stPageLink"] a p {
    color:#A50044 !important; font-size:0.72rem !important; font-weight:600 !important;
    margin:0 !important;
}
div[data-testid="stPageLink"] a:hover { background:#A50044 !important; }
div[data-testid="stPageLink"] a:hover p { color:#FFFFFF !important; }

section[data-testid="stSidebar"] { background:#F4F7FB !important; border-right:1px solid #D4DEEC; }
section[data-testid="stSidebar"] * { color:#003087; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pucv-header">
    <h1>📊 Estadística y Probabilidad</h1>
    <div class="sub">PONTIFICIA UNIVERSIDAD CATÓLICA DE VALPARAÍSO</div>
    <div class="autor">Carlos Erazo Jojot</div>
</div>
<p style="color:#4A688F; font-size:0.88rem;">
Plataforma interactiva de apoyo a la docencia en probabilidad y estadística.
Cada módulo incluye visualizaciones en tiempo real, calculadoras y contexto conceptual.
Navega desde el menú lateral o con los enlaces de cada tarjeta.
</p>
""", unsafe_allow_html=True)

# ── Catálogo de módulos en el orden del menú ──────────────────
def tarjeta(icon, titulo, desc, ruta, etiqueta):
    st.markdown(f'<div class="modulo-card"><h3>{icon} {titulo}</h3><p>{desc}</p></div>',
                unsafe_allow_html=True)
    st.page_link(ruta, label=etiqueta, icon=":material/arrow_forward:")

st.markdown('<div class="seccion">Variables Aleatorias Discretas</div>', unsafe_allow_html=True)
d1, d2, d3 = st.columns(3, gap="medium")
with d1:
    tarjeta("📦", "Binomial",
            "X ~ B(n,p). PMF y CDF, probabilidades exactas y acumuladas, desarrollo de la fórmula.",
            "pages/01_Binomial.py", "Abrir Binomial")
with d2:
    tarjeta("⚡", "Poisson",
            "X ~ Poisson(λ). Eventos por intervalo y comparación directa con el límite de la Binomial.",
            "pages/02_Poisson.py", "Abrir Poisson")
with d3:
    tarjeta("🔁", "Geométrica e Hipergeométrica",
            "Ensayos hasta el primer éxito, falta de memoria y extracción sin reposición.",
            "pages/03_Geometrica.py", "Abrir Geométrica")

st.markdown('<div class="seccion">Variables Aleatorias Continuas</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    tarjeta("🔔", "Normal",
            "X ~ N(μ,σ²). Áreas bajo la curva, estandarización Z y regla 68–95–99.7.",
            "pages/04_Normal.py", "Abrir Normal")
with c2:
    tarjeta("📈", "Continuas: Exp · U · t · χ²",
            "Exponencial, Uniforme, t-Student y Chi-cuadrado con consulta por percentiles.",
            "pages/05_Continuas.py", "Abrir Continuas")
with c3:
    tarjeta("📐", "Teorema Central del Límite",
            "Simulación con cinco distribuciones base. Convergencia a Normal al crecer n.",
            "pages/06_TCL.py", "Abrir TCL")

st.markdown('<div class="seccion">Inferencia Estadística</div>', unsafe_allow_html=True)
i1, i2 = st.columns(2, gap="medium")
with i1:
    tarjeta("🎲", "Distribuciones Muestrales",
            "X̄, p̂ y S². Error estándar y la relación (n−1)S²/σ² ~ χ².",
            "pages/07_Distribuciones_Muestrales.py", "Abrir Distribuciones Muestrales")
    tarjeta("🔬", "Error tipo II y Potencia",
            "H₀ y H₁ superpuestas con α, β y potencia como áreas. Curvas de potencia.",
            "pages/09_Potencia.py", "Abrir Potencia")
with i2:
    tarjeta("🎯", "Inferencia para μ y otras pruebas",
            "IC y prueba para la media, más pruebas de proporción, varianza y dos muestras.",
            "pages/08_Inferencia.py", "Abrir Inferencia")
    tarjeta("📏", "IC para p, σ² y μ₁−μ₂",
            "Wald vs Wilson, IC asimétrico para varianza, Welch vs pooled y el efecto de n.",
            "pages/10_IC_Avanzados.py", "Abrir IC avanzados")

st.divider()
st.markdown("""
<div style="text-align:center;font-size:0.72rem;color:#5E7391;font-family:'DM Mono',monospace;">
    Carlos Erazo Jojot &nbsp;·&nbsp; Pontificia Universidad Católica de Valparaíso
</div>
""", unsafe_allow_html=True)
