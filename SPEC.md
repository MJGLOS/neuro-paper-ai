# Spec: NeuroPaper AI — MVP de validación

Estado: **borrador, pendiente de aprobación** · 2026-10-27

> ⚠️ **Desactualizado (ver ESTADO.md):** Supabase quedó descartado (será Azure o AWS), el límite sube a 300 páginas, el modelo candidato es Haiku 5.5 y el precio de Pro sigue abierto. Reescribir antes de aprobar.
Fuentes: intención confirmada en la entrevista, `docs/CONTEXTO.md` y `docs/AUDITORIA-2026-10-27.md`.

## Objetivo

Lograr que un estudiante suba un PDF real y reciba una ayuda que funcione para *entender* el paper: resumen, explicación sencilla, conceptos clave, quiz y preguntas de debate, con **el número de página donde se apoya cada afirmación**. Todo dentro de una cuenta que guarda su historial.

**Por qué ahora:** la fundadora quiere lanzar NeuroPaper como startup, y el sitio publicado no funciona (`app.js` da 404 y no hay backend ni clave).

**Usuarios de esta etapa**
- **Pruebas (gratis):** de 5 a 10 compañeros de ingeniería de sistemas de la fundadora que leen papers de IA.
- **Validación de pago:** de 1 a 3 estudiantes de medicina, contactadas a través de amigas de la fundadora.
- La visión de largo plazo son los universitarios en general, pero no se diseña para ellos todavía.

**Historias de usuario**
1. Como estudiante, entro con mi correo (enlace mágico, sin contraseña) y veo mi historial.
2. Subo un PDF de hasta 20 MB y, en menos de 2 minutos, veo el resumen, la explicación sencilla, los conceptos, un quiz de 3 preguntas y 5 preguntas de debate.
3. Cada punto del resumen y cada explicación del quiz muestra la página o páginas de donde sale (ej.: "p. 4").
4. Si el PDF no se puede analizar (escaneado ilegible, demasiado largo, error de la IA), veo un mensaje claro y el intento no se descuenta de mi cuota.
5. Vuelvo otro día y abro un análisis anterior sin pagar otra llamada a la IA.
6. Con el plan gratis tengo **3 análisis al mes**. Al llegar al límite, veo cómo pasar a Pro (pago manual por Nequi o transferencia) y la fundadora activa mi cuenta a mano.
7. Puedo borrar un análisis o mi cuenta completa.

## Mapa de capacidades

Un solo spec. Los módulos están demasiado acoplados para justificar specs separados en un MVP de 2 a 3 semanas.

| Módulo | Responsabilidad | Depende de |
|---|---|---|
| `cuentas` | Login con enlace mágico, perfil con `plan` (`free` o `pro`) | — |
| `analisis` | Recibir el PDF, llamar a Claude, validar el JSON y guardar el resultado | `cuentas` |
| `historial` | Listar, abrir y borrar análisis | `analisis` |
| `cuota` | 3 por mes en `free`, ilimitado en `pro`, activación manual | `cuentas`, `analisis` |

Orden de construcción: `analisis` (primero sin login, para probar con PDFs reales) → `cuentas` → `historial` → `cuota`.

## Stack técnico

"Backend completo" significa autenticación, base de datos y lógica en el servidor, sin mantener servidores propios:

- **Frontend:** el HTML, CSS y JS sin framework que ya existe, servido en GitHub Pages. Sin paso de build.
- **Backend:** Supabase (plan gratis): Auth (enlace mágico), Postgres con Row Level Security y **una Edge Function** (`analyze`, TypeScript/Deno) que guarda la clave de Anthropic.
- **IA:** API de Claude. El PDF se envía como bloque `document`, así Claude lee texto, tablas y páginas escaneadas sin PyPDF2. El modelo se define en el secreto `CLAUDE_MODEL` y se elige según el costo medido (ver Preguntas abiertas).
- **Cliente Supabase en el navegador:** `@supabase/supabase-js` desde CDN con la versión fija.
- **Se elimina:** `app.py` (Streamlit) y `app (1).js`, que se renombra a `app.js`.

## Comandos

```bash
# Frontend local
python3 -m http.server 8000                      # http://localhost:8000

# Backend local (requiere Supabase CLI y Docker)
supabase start
supabase db reset                                # aplica supabase/migrations/
supabase functions serve analyze --env-file supabase/.env.local

# Pruebas
deno test supabase/functions/analyze/

# Despliegue
supabase db push
supabase secrets set ANTHROPIC_API_KEY=... CLAUDE_MODEL=...
supabase functions deploy analyze
git push                                         # GitHub Pages publica el frontend
```

## Estructura del proyecto

```
index.html, styles.css, app.js     → frontend (lo actual, corregido)
supabase/migrations/0001_init.sql  → tablas profiles y analyses, más las políticas RLS
supabase/functions/analyze/
  index.ts                         → auth, cuota, llamada a Claude, guardado
  validate.ts                      → validación pura del JSON del modelo
  validate_test.ts                 → pruebas de validate.ts
docs/                              → contexto, auditoría, ADRs
SPEC.md                            → este documento
```

## Modelo de datos

```sql
profiles (id uuid PK → auth.users, plan text default 'free' check (plan in ('free','pro')), created_at)
analyses (id uuid PK, user_id uuid → auth.users on delete cascade,
          file_name text, page_count int, result jsonb, model text,
          input_tokens int, output_tokens int, created_at timestamptz)
```

- RLS: cada usuario solo lee y borra sus propios `analyses`. Solo la Edge Function (con la service role key) inserta registros y cambia el `plan`.
- **El PDF no se guarda.** Se procesa en memoria y se descarta. Solo se guarda el JSON del resultado.
- Los tokens se guardan para calcular el costo real por análisis.

## Contrato de la Edge Function `analyze`

`POST /functions/v1/analyze` con el JWT del usuario y el PDF en base64.

| Respuesta | Cuándo |
|---|---|
| `200 { id, result }` | Análisis válido y guardado |
| `401` | Sin sesión |
| `402 { error: "quota" }` | `free` con 3 análisis o más en el mes actual |
| `413` | PDF de más de 20 MB o de más páginas que el límite (ver Preguntas abiertas) |
| `422 { error: "invalid_output" }` | El modelo devolvió algo que no pasa la validación tras 1 reintento. No cuenta en la cuota |
| `502` | Falló la API de Claude. No cuenta en la cuota |

Forma del `result` (validada en `validate.ts`):

```json
{
  "summary":  [{ "text": "…", "pages": [3, 4] }],
  "simple":   "…",
  "concepts": [{ "term": "…", "definition": "…", "pages": [2] }],
  "quiz":     [{ "question": "…", "options": ["…","…","…","…"], "correct": 0,
                 "explanation": "…", "pages": [5] }],
  "debate":   ["…", "…", "…", "…", "…"]
}
```

Reglas de validación: `quiz` tiene exactamente 3 preguntas, cada una con 4 opciones y `correct` entre 0 y 3. `debate` tiene 5 preguntas. `concepts` tiene entre 5 y 8. Cada número de `pages` está entre 1 y `page_count`. Lo que no cumpla se rechaza, no se repara a medias.

Cambios al prompt: dejar de suponer que el paper es "de neurociencia", **quitar "Conexión con IA"** (no le sirve a medicina y empuja al modelo a inventar) y pedir que todo salga solo del documento.

## Estilo de código

Seguir el idioma del `app.js` actual: `'use strict'`, funciones pequeñas con nombre, comentarios de sección `// ── X ──` e interfaz en español.

```ts
// ── Validación ─────────────────────────────────────
export function validate(r: unknown, pageCount: number): Result {
  const ok = (p: unknown) => Array.isArray(p) && p.every(n => Number.isInteger(n) && n >= 1 && n <= pageCount);
  if (!Array.isArray(r?.quiz) || r.quiz.length !== 3) throw new Error('quiz');
  // …
  return r as Result;
}
```

- Nunca se meten datos del modelo en HTML con `innerHTML` ni en atributos `onclick`. Se usa `textContent` y `addEventListener`, lo que corrige el hallazgo 9 de la auditoría.
- Sin dependencias nuevas sin preguntar. Las únicas previstas son `supabase-js` y el SDK de Anthropic (o `fetch` directo) en la función.

## Estrategia de pruebas

- **Unitarias (`deno test`):** `validate.ts` con salidas buenas, salidas con un campo faltante, `correct` fuera de rango, páginas inexistentes y número equivocado de preguntas. Es la lógica con más ramas, así que se prueba primero.
- **Set de papers reales (manual, antes de cada despliegue):** 5 PDFs en una carpeta local fuera del repo, por derechos de autor. Dos papers de IA (uno de más de 30 páginas), dos de medicina (un ensayo clínico con tablas) y uno escaneado. Para cada uno se anota en `docs/evaluacion.md`: si salió bien, cuánto tardó, los tokens, el costo, y si 3 afirmaciones elegidas al azar existen de verdad en la página citada.
- **RLS:** verificar a mano con dos cuentas que A no ve los análisis de B.

## Fronteras

- **Siempre:** ramas y PRs (el repo es de la fundadora; nunca hacer push directo a `main`). Correr `deno test` antes de cada commit. Validar en el servidor el tamaño, el tipo y la salida del modelo. Registrar los tokens de cada análisis.
- **Preguntar antes:** cambios al esquema de la base de datos, dependencias nuevas, cambiar de modelo, cambiar precios o límites, cualquier cosa que guarde el PDF.
- **Nunca:** poner la clave de API o la service role key en el frontend o en git. Anunciar en la página una función que no exista. Mostrar afirmaciones sin página como si estuvieran respaldadas.

## Criterios de éxito

**Técnicos (al cerrar las 2 o 3 semanas)**
- [ ] El sitio público carga sin errores 404 ni errores en la consola.
- [ ] Al menos 4 de los 5 PDFs del set se analizan bien en menos de 120 s.
- [ ] Al menos el 80 % de las afirmaciones revisadas aparecen de verdad en la página citada.
- [ ] La clave no aparece en ningún archivo del frontend ni del historial de git.
- [ ] La cuota bloquea el 4.º análisis del mes en `free` y no lo bloquea en `pro`.
- [ ] El costo medio medido por análisis cabe en US$20 al mes con el uso esperado (unos 10 usuarios × 3 análisis).

**De producto (unas 6 semanas, medidos con SQL sobre `analyses`)**
- [ ] De 5 a 10 compañeros completan al menos 1 análisis.
- [ ] Al menos la mitad hace un 2.º análisis otro día, sin que nadie se lo pida.
- [ ] De 1 a 3 estudiantes de medicina pagan entre US$3 y US$5 (registro manual).

## Fuera de alcance

Pasarela de pagos automática, plan Institución, chatbot, comparación de papers, exportaciones, app móvil, adaptación por carrera, seguimiento de errores del quiz y repaso espaciado (P2). En la sección de precios queda solo "Gratis: 3/mes" y "Pro: acceso anticipado, escríbenos". El resto se quita.

## Preguntas abiertas

1. **Modelo y costo:** el costo real por paper se mide con el set de 5 PDFs antes de elegir el modelo. La regla de decisión: el modelo más barato que pase los criterios de fidelidad.
2. **Límite de páginas:** los PDFs largos cuestan más y pueden pasarse del tiempo máximo de la Edge Function. Propuesta: rechazar más de 40 páginas en el MVP. Hay que confirmar los límites actuales de Supabase (tiempo máximo y tamaño de petición) en su documentación.
3. **Citas:** comparar la API de Citations de Claude (citas verificadas por página) con pedir `pages` dentro del JSON. Se decide con una prueba corta en la tarea 1 y se documenta en un ADR.
4. **Aviso de privacidad:** el texto exacto (qué se guarda, que el PDF se envía a Anthropic, cómo borrar los datos) lo revisa la fundadora.
5. **Precio Pro:** ¿US$3 o US$5 al mes? Lo decide la fundadora y no bloquea el desarrollo.
