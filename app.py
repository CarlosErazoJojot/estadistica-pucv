# ============================================================
#  app.py — Landing principal
#  Estadística y Probabilidad · PUCV
#  Carlos Erazo
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
    border-bottom: 4px solid #7D6220;
    border-radius: 10px;
    padding: 30px 36px;
    margin-bottom: 30px;
}
.pucv-header h1 {
    font-family:'Playfair Display',serif; font-size:2.2rem;
    color:#FFFFFF !important; margin:0 0 8px 0;
}
.pucv-header .sub {
    font-size:0.82rem; color:#E8D9A8; letter-spacing:0.15em;
}
.pucv-header .autor {
    font-size:0.78rem; color:#FFFFFF; margin-top:10px; opacity:0.92;
}

.seccion {
    color:#003087; font-size:0.74rem; letter-spacing:0.2em; text-transform:uppercase;
    font-weight:700; border-bottom:2px solid #7D6220;
    padding-bottom:8px; margin:26px 0 16px 0;
}
.modulo-card {
    background:#F4F7FB;
    border:1px solid #D4DEEC; border-left:4px solid #7D6220;
    border-radius:10px; padding:20px 22px; margin-bottom:12px;
}
.modulo-card h3 {
    font-family:'Playfair Display',serif; color:#003087 !important;
    margin:0 0 6px 0; font-size:1rem;
}
.modulo-card p  { color:#34517D !important; font-size:0.8rem; margin:0; line-height:1.6; }
.badge-ok  { display:inline-block; font-size:0.68rem; padding:2px 10px; border-radius:20px; margin-top:10px;
             background:#FFFFFF; color:#7D6220; border:1px solid #7D6220; }
.badge-wip { display:inline-block; font-size:0.68rem; padding:2px 10px; border-radius:20px; margin-top:10px;
             background:#FFFFFF; color:#2E6BB8; border:1px solid #2E6BB8; }
section[data-testid="stSidebar"] { background:#F4F7FB !important; border-right:1px solid #D4DEEC; }
section[data-testid="stSidebar"] * { color:#003087; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pucv-header">
    <h1>📊 Estadística y Probabilidad</h1>
    <div class="sub">PONTIFICIA UNIVERSIDAD CATÓLICA DE VALPARAÍSO</div>
    <div class="autor">Carlos Erazo &nbsp;·&nbsp; Escuela de Ingeniería Civil Informática</div>
</div>
<p style="color:#4A688F; font-size:0.88rem;">
Plataforma interactiva de apoyo a la docencia en probabilidad y estadística.
Cada módulo incluye visualizaciones en tiempo real, calculadoras y contexto conceptual.
Usa el menú lateral para navegar.
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
<div style="text-align:center;font-size:0.72rem;color:#5E7391;font-family:'DM Mono',monospace;">
    Carlos Erazo &nbsp;·&nbsp; Pontificia Universidad Católica de Valparaíso &nbsp;·&nbsp;
    Escuela de Ingeniería Civil Informática
</div>
""", unsafe_allow_html=True)
