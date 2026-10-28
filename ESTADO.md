# Estado de NeuroPaper AI — dónde quedamos

Última sesión: **2026-10-27** · Rama: `eval/modelo` (commit local, **sin push** al repo de la fundadora)

## Hecho
- Auditoría del repo y del sitio: `docs/AUDITORIA-2026-10-27.md`. El sitio publicado no funciona (`app.js` da 404, sin backend ni clave).
- Intención confirmada (entrevista):
  - **Usuarios:** compañeros de sistemas de la fundadora que leen papers de IA (pruebas gratis) y estudiantes de medicina, a través de sus amigas (validar el pago).
  - **Éxito en ~6 semanas:** de 5 a 10 usuarios, la mitad vuelve por su cuenta, y de 1 a 3 pagos.
  - **Límites:** ~US$20 al mes y 5–10 h por semana por persona.
- Primer borrador de `SPEC.md`, desactualizado: hay que reescribirlo con las decisiones de abajo.
- Núcleo de análisis: `backend/analyze.py` (prompt, esquema, `validate`, `cost`) y `backend/test_analyze.py`, que pasa.
- Evaluación de modelos: `eval/run.py` y resultados en `docs/evaluacion.md`. Con 5 PDFs ficticios costó US$1,76. Haiku 5.5 y Sonnet 5.5 tuvieron 100 % de cifras en la página citada. Haiku es entre 15 y 20 veces más barato.

## Decisiones tomadas
- **Backend completo, en Azure o AWS. NO Supabase.**
- Repo de la fundadora (MJGLOS/neuro-paper-ai). El usuario es colaborador: trabajar con ramas y PRs.
- Límite de **300 páginas** por documento.
- Modelo candidato: **Haiku 5.5**. Sonnet 5.5 queda como opción "análisis profundo".
- Se quita la pestaña "Conexión con IA". Cada afirmación lleva su número de página.

## Pendiente (en este orden)
1. Repetir `eval/run.py` con 3 o 4 papers **reales** (arXiv o PubMed Central, con dos columnas, figuras y un escaneo) y fijar el modelo.
2. Agregar a `analyze.py` un reintento si `validate()` falla y el barajado de las opciones del quiz (Haiku puso todas las correctas en B).
3. Decidir la **nube**: Azure (Azure for Students, a nombre de ella, sin tarjeta) o AWS (la cuenta del usuario aparece **cerrada**). Solicitar créditos de startup (Microsoft for Startups, AWS Activate, Anthropic).
4. Decidir el **precio de Pro**: la fundadora propone US$15.99. Yo propuse COP 24.900 / US$9.99. Con Haiku hay margen para cualquiera de los dos.
5. Reescribir `SPEC.md`, aprobarlo, hacer push de la rama y abrir el PR. Después vienen `planning-and-task-breakdown` y la construcción.

## Cómo correr
```bash
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python backend/test_analyze.py   # pruebas
.venv/bin/python eval/run.py               # estimación gratis
.venv/bin/python eval/run.py --run         # análisis real (gasta créditos)
```
`.env` tiene `ANTHROPIC_API_KEY` (no versionado). El script ignora a propósito el proxy local OmniRoute (`ANTHROPIC_BASE_URL`).
