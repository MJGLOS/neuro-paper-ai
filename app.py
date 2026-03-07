# ═══════════════════════════════════════════════════════════════
#  NeuroPaper AI — app.py
#  Backend en Python/Streamlit (opcional si usas el HTML puro)
# ═══════════════════════════════════════════════════════════════

import json
import streamlit as st
import anthropic
import PyPDF2

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroPaper AI",
    page_icon="🧠",
    layout="centered",
)

# ── Header ─────────────────────────────────────────────────────
st.markdown("# 🧠 NeuroPaper AI")
st.markdown("*Analiza papers de neurociencia con inteligencia artificial*")
st.divider()

# ── Upload ─────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Sube un paper de neurociencia en PDF",
    type=["pdf"],
    help="Máximo 20 MB",
)

# ── Extract PDF text ───────────────────────────────────────────
def extract_pdf_text(file) -> str:
    """Extrae todo el texto del PDF página a página."""
    reader = PyPDF2.PdfReader(file)
    pages  = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)

# ── Call Claude API ────────────────────────────────────────────
def analyze_paper(text: str) -> dict:
    """Envía el texto a Claude y devuelve el análisis como dict."""
    client = anthropic.Anthropic()   # Lee ANTHROPIC_API_KEY del entorno

    prompt = f"""Analiza el siguiente paper de neurociencia.
Responde ÚNICAMENTE con JSON válido, sin markdown, sin texto extra.

Estructura exacta requerida:
{{
  "summary": "Resumen técnico de 4-6 oraciones con terminología científica",
  "simple": "Explicación de 3-4 oraciones para no-científicos usando analogías",
  "concepts": ["c1","c2","c3","c4","c5","c6","c7","c8"],
  "ai_connection": "3-4 oraciones sobre relación con IA/ML/neurociencia computacional",
  "quiz": [
    {{"question":"Pregunta 1","options":["A) ...","B) ...","C) ...","D) ..."],"correct":0,"explanation":"Razón"}},
    {{"question":"Pregunta 2","options":["A) ...","B) ...","C) ...","D) ..."],"correct":2,"explanation":"Razón"}},
    {{"question":"Pregunta 3","options":["A) ...","B) ...","C) ...","D) ..."],"correct":1,"explanation":"Razón"}}
  ],
  "debate": [
    "Pregunta 1 sobre implicaciones del hallazgo",
    "Pregunta 2 sobre metodología",
    "Pregunta 3 sobre ética o futuro",
    "Pregunta 4 conectando con neurociencia",
    "Pregunta 5 sobre limitaciones"
  ]
}}

TEXTO DEL PAPER:
{text[:12000]}"""          # Limitamos a ~12k chars para no superar el contexto

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw   = message.content[0].text.strip()
    clean = raw.lstrip("```json").lstrip("```").rstrip("```").strip()
    return json.loads(clean)

# ── Main logic ─────────────────────────────────────────────────
if uploaded_file is not None:

    with st.spinner("Extrayendo texto del PDF…"):
        paper_text = extract_pdf_text(uploaded_file)

    if not paper_text.strip():
        st.error("No se pudo extraer texto del PDF. Puede estar escaneado (imagen).")
        st.stop()

    with st.spinner("La IA está analizando tu paper… ⏳"):
        try:
            result = analyze_paper(paper_text)
        except json.JSONDecodeError:
            st.error("La IA no devolvió JSON válido. Intenta de nuevo.")
            st.stop()
        except Exception as e:
            st.error(f"Error al llamar a la API: {e}")
            st.stop()

    st.success("¡Análisis completado! ✅")

    # ── Tabs ──
    tab_summary, tab_simple, tab_concepts, tab_ai, tab_quiz, tab_debate = st.tabs([
        "📋 Resumen", "💡 Simple", "🔑 Conceptos", "🤖 IA", "🧩 Quiz", "💬 Debate"
    ])

    with tab_summary:
        st.subheader("Resumen Técnico")
        st.write(result.get("summary", "—"))

    with tab_simple:
        st.subheader("Explicación Simple")
        st.write(result.get("simple", "—"))

    with tab_concepts:
        st.subheader("Conceptos Clave")
        concepts = result.get("concepts", [])
        cols = st.columns(4)
        for i, concept in enumerate(concepts):
            cols[i % 4].markdown(f"`{concept}`")

    with tab_ai:
        st.subheader("Conexión con Inteligencia Artificial")
        st.write(result.get("ai_connection", "—"))

    with tab_quiz:
        st.subheader("Quiz de Comprensión")
        score = 0
        quiz  = result.get("quiz", [])

        for i, q in enumerate(quiz):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            answer = st.radio(
                label=f"Pregunta {i+1}",
                options=q["options"],
                index=None,
                key=f"q_{i}",
                label_visibility="collapsed",
            )
            if answer is not None:
                chosen_index = q["options"].index(answer)
                if chosen_index == q["correct"]:
                    st.success(f"✓ ¡Correcto! {q.get('explanation','')}")
                    score += 1
                else:
                    st.error(f"✗ Incorrecto. {q.get('explanation','')}")
                    st.info(f"La respuesta correcta era: {q['options'][q['correct']]}")
            st.divider()

        answered = sum(1 for i in range(len(quiz)) if st.session_state.get(f"q_{i}") is not None)
        if answered > 0:
            st.metric("Puntuación", f"{score} / {answered}")

    with tab_debate:
        st.subheader("Preguntas para Debate Científico")
        for i, question in enumerate(result.get("debate", []), 1):
            st.markdown(f"**{i}.** {question}")
