# Auditoría inicial — 2026-10-27

Base: commit `ea1a616` de https://github.com/MJGLOS/neuro-paper-ai y el sitio publicado.
Convención: **Hecho** = verificado en código o en el sitio. **Hipótesis** = no verificado.

## Hechos

| # | Hallazgo | Evidencia | Gravedad |
|---|----------|-----------|----------|
| 1 | **El sitio publicado no funciona.** `index.html` carga `app.js`, pero el archivo se llama `app (1).js`. Ningún botón ni la subida de PDF hacen nada. | `index.html:237`; `app.js` → 404, `app%20(1).js` → 200 | P0 |
| 2 | Aunque se arregle el nombre, la llamada a Anthropic fallaría: no hay `x-api-key`, ni `anthropic-version`, ni permiso CORS desde el navegador. | `app (1).js` `callAPI()` | P0 |
| 3 | Poner la clave en el navegador la expondría a cualquier visitante. Hace falta un backend mínimo. | Arquitectura actual: sitio estático en GitHub Pages | P0 (seguridad) |
| 4 | No hay backend desplegado ligado al sitio. `app.py` (Streamlit) es una app aparte y nada indica que esté desplegada. | Solo GitHub Pages, sin config de despliegue | Hecho |
| 5 | Los planes (Free/Pro/Institución) son decorativos: los botones no tienen handler, no hay pagos, cuentas ni límites. | `index.html:191,208,223` | Hecho |
| 6 | No hay persistencia, historial ni chatbot. | No existe ningún código de almacenamiento | Hecho |
| 7 | `app.py` pierde las páginas (concatena el texto), corta en 12.000 caracteres (en un paper típico es solo la introducción) y PyPDF2 falla con PDFs escaneados. | `extract_pdf_text`, `text[:12000]` | P1 |
| 8 | El JSON se parsea sin validarse; si falta un campo o `correct` está fuera de rango, el quiz se rompe. | `JSON.parse(clean)` → `renderResults` | P1 |
| 9 | La explicación del quiz se inyecta en un atributo `onclick` con un escape manual (vector de XSS si el modelo devuelve texto raro). | `renderResults`, `pickAnswer(..., '${explanation}')` | P1 |
| 10 | El prompt pide "paper de neurociencia" y una "conexión con IA" fija, aunque el paper no trate de eso, lo que invita a inventar. | prompt en ambos archivos | P1 (fidelidad) |
| 11 | No hay pruebas ni README (0 bytes). | repo | Hecho |

## Respuestas a las incertidumbres del contexto (§14)

- ¿Funciona el análisis en el sitio? **No** (hallazgos 1 y 2).
- ¿Hay backend desplegado? **No** (4).
- ¿Hay persistencia? **No** (6).
- ¿Hay chatbot? **No** (6).
- ¿Qué modelo/credenciales? El código pide `claude-opus-4-6` y **no envía credenciales**.
- ¿Qué funciones comerciales existen? **Ninguna** (5).
- Público, costos y evidencia de aprendizaje: **sin datos**, requieren validación.
