# 📊 Estadística Computacional · PUCV
### Carlos Erazo Jojot · Plataforma interactiva de apoyo a la docencia

Aplicación Streamlit con diez módulos interactivos de probabilidad y
estadística. Cálculo exacto con `scipy` — sin APIs externas, sin costos
de servicio, sin dependencia de servicios de terceros en tiempo de ejecución.

---

## Estructura

```
estadistica-pucv/
├── app.py                    ← Landing / menú principal
├── pages/
│   ├── 01_Binomial.py        X ~ B(n,p)
│   ├── 02_Poisson.py         X ~ Poisson(λ) + límite de la Binomial
│   ├── 03_Geometrica.py      Geométrica e Hipergeométrica
│   ├── 04_Normal.py          X ~ N(μ,σ²) + escala Z
│   ├── 05_Continuas.py       Exponencial · Uniforme · t · χ²
│   ├── 06_TCL.py             Simulación del Teorema Central del Límite
│   ├── 07_Distribuciones_Muestrales.py   X̄ · p̂ · S²
│   ├── 08_Inferencia.py      IC + pruebas (μ, p, σ², dos muestras)
│   ├── 09_Potencia.py        α, β, potencia y curvas de potencia
│   └── 10_IC_Avanzados.py    IC para p, σ², μ₁−μ₂ y efecto de n
├── utils/
│   └── calculos.py           Paleta PUCV, CSS y helpers compartidos
├── .streamlit/
│   └── config.toml           Tema institucional
├── requirements.txt
└── README.md
```

---

## Correr localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre en `http://localhost:8501`.

---

## Desplegar en Streamlit Community Cloud

**Requisito:** el repositorio de GitHub debe ser **público** en el plan gratuito.

### 1. Subir a GitHub

```bash
git init
git add .
git commit -m "versión inicial"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/estadistica-pucv.git
git push -u origin main
```

### 2. Desplegar

1. Entrar a https://share.streamlit.io con la cuenta de GitHub
2. **New app**
3. Repository: `TU_USUARIO/estadistica-pucv` · Branch: `main` · Main file: `app.py`
4. **Deploy**

### 3. Actualizar

```bash
git add . && git commit -m "descripción" && git push
```

El redespliegue es automático.

---

## Límites del plan gratuito (verificar antes de decidir)

| Aspecto | Streamlit Community Cloud |
|---|---|
| Memoria | ~1 GB por app |
| Apps públicas | Ilimitadas |
| Apps privadas | 1 |
| Repositorio | Debe ser público |
| Inactividad | Duerme tras ~12 h sin tráfico |
| Dominio propio | No disponible |

**Alternativa:** Hugging Face Spaces ofrece más memoria en su tier gratuito
(las fuentes discrepan entre 8 y 16 GB) y soporta Streamlit directamente.
Conviene revisar su documentación vigente antes de elegir.

---

## Notas sobre decisiones de implementación

**Criterio Z / t configurable.** El módulo de Inferencia permite elegir en la
barra lateral entre *t siempre con σ desconocida* (criterio estricto) y
*Z si n ≥ 30* (aproximación frecuente en textos introductorios). La app no
impone una postura.

**Sliders con rango fijo.** Los límites de consulta se expresan en unidades
relativas —múltiplos de σ, fracciones del recorrido, percentiles— en lugar de
unidades absolutas dependientes de los parámetros. Esto evita que un slider
quede fuera de rango al mover el parámetro del que dependía.

**Caché en la simulación del TCL.** `@st.cache_data` con semilla explícita:
reproducible en clases y sin recalcular en cada interacción, lo que importa
con el límite de 1 GB.

**Colas con `sf()`.** Se usa `dist.sf(k-1)` en lugar de `1 - dist.cdf(k-1)`
para P(X ≥ k): en colas extremas la segunda forma pierde precisión.

**Modas dobles.** Binomial con (n+1)p entero y Poisson con λ entero tienen
dos modas. La app las detecta y muestra ambas.

---

## Paleta institucional

| Color | Hex | Uso |
|---|---|---|
| Azul PUCV | `#003087` | Texto, encabezados, degradados |
| Burdeo | `#A50044` | Títulos de sección, valor seleccionado, enlaces |
| Rojo PUCV | `#C8102E` | Líneas de referencia, región de rechazo |
| Azul medio | `#2E6BB8` | Relleno de barras y áreas |
| Teal | `#0E7490` | Moda, segundo acento |
| Morado | `#6B4BA8` | β en el módulo de potencia |

Tema claro: fondo blanco `#FFFFFF`, paneles `#F4F7FB`. Todos los colores de texto
superan el mínimo WCAG AA de 4.5:1 sobre blanco.

---

*Pontificia Universidad Católica de Valparaíso · *


---

## Cobertura del bloque de inferencia

| Tema | Módulo |
|---|---|
| Distribución muestral de X̄, p̂, S² | 07 |
| Teorema Central del Límite | 06 |
| IC para μ | 08 |
| IC para p (Wald y Wilson) | 10 |
| IC para σ² y σ | 10 |
| IC para μ₁ − μ₂ (Welch y pooled) | 10 |
| Efecto de n sobre la amplitud del IC | 10 |
| Prueba para μ (una muestra) | 08 |
| Prueba para p (una muestra) | 08 |
| Prueba para σ² | 08 |
| Prueba para μ₁ − μ₂ | 08 |
| Prueba para p₁ − p₂ | 08 |
| Error tipo I, error tipo II, potencia | 09 |
| Curva de potencia y cálculo de n | 09 |

## Validación numérica

Los estadísticos se verificaron contra `scipy` y `statsmodels`:

| Cálculo | Referencia | Estado |
|---|---|---|
| Welch y pooled | `scipy.stats.ttest_ind_from_stats` | Coincide |
| IC Wilson y Wald | `statsmodels.proportion_confint` | Coincide |
| Prueba de dos proporciones | `statsmodels.proportions_ztest` | Coincide |
| Potencia | Fórmula cerrada con d de Cohen | Coincide |
| Falta de memoria (Geométrica) | Identidad (1−p)^k | Diferencia < 1e-15 |
| Cobertura del IC para σ² | Integral de la χ² | Exacta al nivel nominal |

## Detalles de implementación con relevancia estadística

- **Test de proporción:** el error estándar se calcula con p₀, no con p̂. Bajo H₀
  la proporción verdadera se supone igual a p₀.
- **Test de dos proporciones:** error estándar con la proporción combinada p̄.
- **IC para σ²:** el cuantil superior de la χ² genera el límite inferior. Van
  cruzados porque σ² está en el denominador del estadístico.
- **Welch por defecto:** no exige varianzas iguales y se comporta bien incluso
  cuando lo son.
- **Wilson disponible junto a Wald:** Wald puede producir límites fuera de [0,1]
  y su cobertura real suele quedar bajo el nivel nominal.
