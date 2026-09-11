# ============================================================
#  utils/calculos.py
#  Paleta, estilos y utilidades compartidas — TEMA CLARO
#  PUCV · Estadística Computacional
# ============================================================

import numpy as np

# ── Paleta institucional PUCV — tema claro ────────────────────
PUCV_BLUE  = "#003087"   # azul institucional — texto y titulares
PUCV_RED   = "#C8102E"   # rojo institucional — acentos, moda, rechazo
PUCV_GOLD  = "#A50044"   # dorado oscurecido para contraste sobre blanco
AZUL_BARRA = "#2E6BB8"   # relleno de barras y áreas
AZUL_CLARO = "#0E7490"   # segundo acento (legible sobre blanco)
MORADO     = "#6B4BA8"   # beta en el módulo de potencia

BG_PAGE    = "#FFFFFF"   # fondo de página
BG_PANEL   = "#F4F7FB"   # fondo de tarjetas y sidebar
BORDE      = "#D4DEEC"   # bordes suaves
TEXTO      = "#003087"   # texto principal (azul PUCV)
TEXTO_SEC  = "#4A688F"   # texto secundario
TEXTO_TENUE= "#5E7391"   # pies de página

# Alias retrocompatibles (los módulos los importan por estos nombres)
BG_DARK    = BG_PAGE
TEXT_LIGHT = TEXTO

# ── Estilo matplotlib — tema claro ────────────────────────────
MATPLOTLIB_STYLE = {
    "figure.facecolor":  BG_PAGE,
    "axes.facecolor":    BG_PAGE,
    "axes.edgecolor":    BORDE,
    "axes.labelcolor":   TEXTO,
    "xtick.color":       TEXTO_SEC,
    "ytick.color":       TEXTO_SEC,
    "text.color":        TEXTO,
    "grid.color":        "#E3EAF4",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.7,
    "font.family":       "monospace",
    "savefig.facecolor": BG_PAGE,
}

# ── CSS compartido — tema claro ───────────────────────────────
CSS_BASE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500;700&family=Playfair+Display:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Mono', monospace; }

.stApp { background: #FFFFFF; }
h1, h2, h3, h4, h5, h6, p, li, label, .stMarkdown { color: #003087; }

.page-header {
    background: linear-gradient(90deg, #003087, #0A47B0);
    border-left: 5px solid #A50044;
    border-radius: 8px;
    padding: 18px 24px;
    margin-bottom: 24px;
}
.page-header h2 {
    font-family: 'Playfair Display', serif;
    color: #FFFFFF !important; margin: 0 0 4px 0; font-size: 1.5rem;
}
.page-header .formula { color: #F5C6D8; font-size: 0.88rem; }

.seccion-label {
    color: #003087; font-size: 0.74rem; letter-spacing: 0.15em; font-weight: 700;
    border-bottom: 2px solid #A50044; padding-bottom: 8px; margin-bottom: 16px;
}

.stat-box {
    background: #F4F7FB; border: 1px solid #D4DEEC;
    border-top: 3px solid #A50044; border-radius: 8px;
    padding: 14px 16px; text-align: center;
}
.stat-box .label { font-size: 0.72rem; color: #4A688F; margin-bottom: 4px; }
.stat-box .value { font-size: 1.3rem; font-weight: 700; }

.prob-box {
    background: #F4F7FB; border: 1px solid #D4DEEC;
    border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;
}
.prob-box .label { color: #4A688F; font-size: 0.8rem; margin-bottom: 4px; }
.prob-box .value { font-size: 1.4rem; font-weight: 700; }

.formula-box {
    background: #F4F7FB; border: 1px solid #D4DEEC;
    border-radius: 8px; padding: 16px; margin-top: 8px;
}
.formula-box .titulo {
    color: #003087; font-size: 0.72rem; letter-spacing: 0.12em;
    font-weight: 700; margin-bottom: 10px;
}
.formula-box .cuerpo { font-size: 0.78rem; color: #34517D; line-height: 2.0; }

.resultado-box {
    border-radius: 10px; padding: 18px 22px; margin: 16px 0; border-left: 5px solid;
}

section[data-testid="stSidebar"] {
    background: #F4F7FB !important; border-right: 1px solid #D4DEEC;
}
section[data-testid="stSidebar"] * { color: #003087; }

.firma {
    font-size: 0.7rem; color: #5E7391; margin-top: 20px; line-height: 1.7;
}
</style>
"""

# ── Helpers de render ─────────────────────────────────────────
def stat_box(label, value, color=PUCV_BLUE):
    return (f'<div class="stat-box" style="border-top-color:{color};">'
            f'<div class="label">{label}</div>'
            f'<div class="value" style="color:{color};">{value}</div></div>')

def prob_box(label, value, color=PUCV_BLUE):
    return (f'<div class="prob-box"><div class="label">{label}</div>'
            f'<div class="value" style="color:{color};">{value}</div></div>')

def clamp(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))
