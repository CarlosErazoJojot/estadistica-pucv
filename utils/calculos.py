# ============================================================
#  utils/calculos.py
#  Paleta, estilos y utilidades compartidas
#  PUCV · Estadística Computacional
# ============================================================

import numpy as np

# ── Paleta institucional PUCV ─────────────────────────────────
PUCV_BLUE  = "#003087"
PUCV_RED   = "#C8102E"
PUCV_GOLD  = "#B8963E"
AZUL_BARRA = "#1A5CB0"
AZUL_CLARO = "#7EBAFF"
BG_DARK    = "#0A1628"
BG_PANEL   = "#0F1E38"
TEXT_LIGHT = "#D0DCF0"

# ── Estilo matplotlib ─────────────────────────────────────────
MATPLOTLIB_STYLE = {
    "figure.facecolor":  BG_DARK,
    "axes.facecolor":    BG_PANEL,
    "axes.edgecolor":    "#1E3A5F",
    "axes.labelcolor":   TEXT_LIGHT,
    "xtick.color":       TEXT_LIGHT,
    "ytick.color":       TEXT_LIGHT,
    "text.color":        TEXT_LIGHT,
    "grid.color":        "#1E3A5F",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.6,
    "font.family":       "monospace",
}

# ── CSS compartido (evita duplicarlo en cada página) ──────────
CSS_BASE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500;700&family=Playfair+Display:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Mono', monospace; }

.page-header {
    background: linear-gradient(90deg, #003087, #001A50);
    border-left: 5px solid #B8963E;
    border-radius: 8px;
    padding: 18px 24px;
    margin-bottom: 24px;
}
.page-header h2 {
    font-family: 'Playfair Display', serif;
    color: #fff; margin: 0 0 4px 0; font-size: 1.5rem;
}
.page-header .formula { color: #B8963E; font-size: 0.88rem; }

.seccion-label {
    color: #B8963E; font-size: 0.72rem; letter-spacing: 0.15em;
    border-bottom: 1px solid #1E3A5F; padding-bottom: 8px; margin-bottom: 16px;
}

.stat-box {
    background: #0F1E38; border: 1px solid #1E3A5F;
    border-top: 3px solid #B8963E; border-radius: 8px;
    padding: 14px 16px; text-align: center;
}
.stat-box .label { font-size: 0.72rem; color: #9BB5D8; margin-bottom: 4px; }
.stat-box .value { font-size: 1.3rem; font-weight: 700; }

.prob-box {
    background: #0F1E38; border: 1px solid #1E3A5F;
    border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;
}
.prob-box .label { color: #9BB5D8; font-size: 0.8rem; margin-bottom: 4px; }
.prob-box .value { font-size: 1.4rem; font-weight: 700; }

.formula-box {
    background: #0F1E38; border: 1px solid #1E3A5F;
    border-radius: 8px; padding: 16px; margin-top: 8px;
}
.formula-box .titulo {
    color: #B8963E; font-size: 0.7rem; letter-spacing: 0.12em; margin-bottom: 10px;
}
.formula-box .cuerpo { font-size: 0.78rem; color: #9BB5D8; line-height: 2.0; }

.resultado-box {
    border-radius: 10px; padding: 18px 22px; margin: 16px 0; border-left: 5px solid;
}

section[data-testid="stSidebar"] {
    background: #060E1C !important; border-right: 1px solid #1E3A5F;
}
</style>
"""

# ── Helpers de render ─────────────────────────────────────────
def stat_box(label, value, color=PUCV_GOLD):
    """Devuelve el HTML de una tarjeta de estadístico."""
    return (f'<div class="stat-box" style="border-top-color:{color};">'
            f'<div class="label">{label}</div>'
            f'<div class="value" style="color:{color};">{value}</div></div>')

def prob_box(label, value, color=PUCV_GOLD):
    """Devuelve el HTML de una tarjeta de probabilidad."""
    return (f'<div class="prob-box"><div class="label">{label}</div>'
            f'<div class="value" style="color:{color};">{value}</div></div>')

def clamp(valor, minimo, maximo):
    """Acota un valor al rango [minimo, maximo]."""
    return max(minimo, min(valor, maximo))
