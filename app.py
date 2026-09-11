# ============================================================
#  app.py — Landing principal
#  Estadística Computacional · PUCV · ICI 3170
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
.pucv-header {
    background: linear-gradient(90deg, #003087 0%, #001A50 70%, rgba(200,16,46,0.2) 100%);
    border-bottom: 3px solid #B8963E;
    border-radius: 10px;
    padding: 28px 36px;
    margin-bottom: 32px;
}
.pucv-header h1 { font-family:'Playfair Display',serif; font-size:2.2rem; color:#fff; margin:0 0 6px 0; }
.pucv-header .sub { font-size:0.82rem; color:#B8963E; letter-spacing:0.15em; }
.seccion { color:#B8963E; font-size:0.72rem; letter-spacing:0.2em; text-transform:uppercase;
           border-bottom:1px solid #1E3A5F; padding-bottom:8px; margin:24px 0 16px 0; }
.modulo-card {
    background:linear-gradient(135deg,#0F1E38 0%,#0A1628 100%);
    border:1px solid #1E3A5F; border-left:4px solid #B8963E;
    border-radius:10px; padding:20px 22px; margin-bottom:12px;
}
.modulo-card h3 { font-family:'Playfair Display',serif; color:#B8963E; margin:0 0 6px 0; font-size:1rem; }
.modulo-card p  { color:#9BB5D8; font-size:0.8rem; margin:0; line-height:1.6; }
.badge-ok  { display:inline-block; font-size:0.68rem; padding:2px 10px; border-radius:20px; margin-top:10px;
             background:rgba(184,150,62,0.15); color:#B8963E; border:1px solid #B8963E; }
.badge-wip { display:inline-block; font-size:0.68rem; padding:2px 10px; border-radius:20px; margin-top:10px;
             background:rgba(0,48,135,0.3); color:#7EBAFF; border:1px solid #3A6AB0; }
section[data-testid="stSidebar"] { background:#060E1C !important; border-right:1px solid #1E3A5F; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pucv-header">
    <h1>📊 Estadística Computacional</h1>
    <div class="sub">PONTIFICIA UNIVERSIDAD CATÓLICA DE VALPARAÍSO &nbsp;·&nbsp; ICI 3170</div>
</div>
<p style="color:#9BB5D8; font-size:0.88rem;">
Plataforma interactiva de apoyo al curso. Cada módulo incluye visualizaciones en tiempo real,
calculadoras de probabilidades y contexto pedagógico. Usa el menú lateral para navegar.
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="seccion">Variables Aleatorias Discretas</div>', unsafe_allow_html=True)
    for icon, title, desc, badge, badge_class in [
        ("📦", "Distribución Binomial",      "X ~ B(n,p). PMF, CDF, probabilidades exactas y acumuladas con sliders interactivos.", "✓ Disponible", "badge-ok"),
        ("⚡", "Distribución Poisson",        "X ~ Poisson(λ). Modela eventos raros. Visualiza cómo λ controla la forma.", "✓ Disponible", "badge-ok"),
        ("🔁", "Geométrica e Hipergeométrica","Ensayos hasta el primer éxito y extracción sin reposición. Propiedad de falta de memoria.", "✓ Disponible", "badge-ok"),
    ]:
        st.markdown(f'<div class="modulo-card"><h3>{icon} {title}</h3><p>{desc}</p><span class="{badge_class}">{badge}</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="seccion">Variables Aleatorias Continuas</div>', unsafe_allow_html=True)
    for icon, title, desc, badge, badge_class in [
        ("🔔", "Distribución Normal",         "X ~ N(μ,σ²). Áreas bajo la curva, estandarización Z y regla 68-95-99.7.", "✓ Disponible", "badge-ok"),
        ("📈", "Continuas: Exp · U · t · χ²", "Exponencial, Uniforme, t-Student y Chi-cuadrado. Cuatro distribuciones en un módulo.", "✓ Disponible", "badge-ok"),
        ("📐", "Teorema Central del Límite",   "Simulación con cualquier distribución base. Observa la convergencia a Normal con n creciente.", "✓ Disponible", "badge-ok"),
    ]:
        st.markdown(f'<div class="modulo-card"><h3>{icon} {title}</h3><p>{desc}</p><span class="{badge_class}">{badge}</span></div>', unsafe_allow_html=True)

st.markdown('<div class="seccion">Inferencia Estadística</div>', unsafe_allow_html=True)

ci1, ci2 = st.columns(2, gap="large")
with ci1:
    for icon, title, desc in [
        ("🎲", "Distribuciones Muestrales",
         "X̄, p̂ y S². Error estándar, la conexión (n−1)S²/σ² ~ χ² y por qué la precisión crece con √n."),
        ("🎯", "IC y Pruebas para μ",
         "Intervalo de confianza y prueba de hipótesis sobre la media. Criterio Z/t configurable. "
         "Incluye pruebas de proporción, varianza y dos muestras."),
    ]:
        st.markdown(f'<div class="modulo-card"><h3>{icon} {title}</h3><p>{desc}</p>'
                    f'<span class="badge-ok">✓ Disponible</span></div>', unsafe_allow_html=True)

with ci2:
    for icon, title, desc in [
        ("📏", "IC para p, σ² y μ₁−μ₂",
         "Wald vs Wilson para proporciones, IC asimétrico para varianza, Welch vs pooled, "
         "y el efecto del tamaño de muestra sobre la amplitud."),
        ("🔬", "Error tipo II y Potencia",
         "H₀ y H₁ superpuestas con α, β y potencia como áreas. Curva de potencia frente a μ y frente a n."),
    ]:
        st.markdown(f'<div class="modulo-card"><h3>{icon} {title}</h3><p>{desc}</p>'
                    f'<span class="badge-ok">✓ Disponible</span></div>', unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style="text-align:center;font-size:0.72rem;color:#3A5070;font-family:'DM Mono',monospace;">
    Pontificia Universidad Católica de Valparaíso &nbsp;·&nbsp;
    Escuela de Ingeniería Civil Informática &nbsp;·&nbsp;
    Estadística Computacional ICI 3170
</div>
""", unsafe_allow_html=True)
