"""NeuroPaper AI — análisis de un PDF con Claude (núcleo reutilizable por el backend)."""

import base64

import anthropic
from pydantic import BaseModel

# USD por millón de tokens (entrada, salida). Haiku 5.5 cobra más si la entrada pasa de 100K tokens.
PRICES = {
    'claude-haiku-5-5': {'base': (0.10, 0.50), 'long': (0.50, 2.50)},
    'claude-sonnet-5-5': {'base': (2.00, 10.00)},
}

PROMPT = """Eres un tutor que ayuda a estudiantes universitarios a comprender el documento adjunto.
Responde en español aunque el documento esté en otro idioma.

Reglas:
- Usa SOLO información del documento. No añadas datos, cifras ni conclusiones que no estén en él.
- En cada campo "pages" pon el número de página del PDF donde se apoya la afirmación
  (la primera página del archivo es 1; NO uses el número impreso en la página).
- Si el documento no es un artículo científico, analízalo igual con lo que contenga.

Devuelve:
- summary: 4 a 6 afirmaciones clave (objetivo, método, resultados, limitaciones), cada una con sus páginas.
- simple: explicación de 3 a 4 oraciones para alguien sin formación en el área, con una analogía cotidiana.
- concepts: 5 a 8 conceptos clave con una definición breve según el documento.
- quiz: exactamente 3 preguntas de comprensión, 4 opciones cada una, "correct" = índice 0-3 de la correcta,
  y una explicación que cite el documento. Varía la posición de la respuesta correcta.
- debate: exactamente 5 preguntas abiertas de pensamiento crítico (metodología, limitaciones, implicaciones)."""


class Claim(BaseModel):
    text: str
    pages: list[int]


class Concept(BaseModel):
    term: str
    definition: str
    pages: list[int]


class Question(BaseModel):
    question: str
    options: list[str]
    correct: int
    explanation: str
    pages: list[int]


class Analysis(BaseModel):
    summary: list[Claim]
    simple: str
    concepts: list[Concept]
    quiz: list[Question]
    debate: list[str]


def _messages(pdf_bytes: bytes) -> list:
    data = base64.standard_b64encode(pdf_bytes).decode()
    return [{'role': 'user', 'content': [
        {'type': 'document', 'source': {'type': 'base64', 'media_type': 'application/pdf', 'data': data}},
        {'type': 'text', 'text': PROMPT},
    ]}]


def cost(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICES[model]
    inp, out = p['long'] if 'long' in p and input_tokens > 100_000 else p['base']
    return (input_tokens * inp + output_tokens * out) / 1_000_000


def count_tokens(client: anthropic.Anthropic, model: str, pdf_bytes: bytes) -> int:
    """Gratis: cuenta los tokens de entrada sin generar nada."""
    return client.messages.count_tokens(model=model, messages=_messages(pdf_bytes)).input_tokens


def analyze(client: anthropic.Anthropic, model: str, pdf_bytes: bytes):
    """Devuelve (Analysis | None, response). None si el modelo se negó o se cortó."""
    response = client.messages.parse(
        model=model,
        max_tokens=16000,
        output_config={'effort': 'medium'},
        messages=_messages(pdf_bytes),
        output_format=Analysis,
    )
    if response.stop_reason in ('refusal', 'max_tokens'):
        return None, response
    return response.parsed_output, response


def validate(a: Analysis, page_count: int) -> list[str]:
    """Problemas que impiden mostrar el análisis. Lista vacía = válido."""
    problems = []
    ok_pages = lambda ps: bool(ps) and all(1 <= p <= page_count for p in ps)
    if not 4 <= len(a.summary) <= 6:
        problems.append(f'summary tiene {len(a.summary)} afirmaciones')
    problems += [f'summary[{i}] páginas inválidas {c.pages}' for i, c in enumerate(a.summary) if not ok_pages(c.pages)]
    if not 5 <= len(a.concepts) <= 8:
        problems.append(f'concepts tiene {len(a.concepts)}')
    problems += [f'concepts[{i}] páginas inválidas {c.pages}' for i, c in enumerate(a.concepts) if not ok_pages(c.pages)]
    if len(a.quiz) != 3:
        problems.append(f'quiz tiene {len(a.quiz)} preguntas')
    for i, q in enumerate(a.quiz):
        if len(q.options) != 4 or not 0 <= q.correct <= 3:
            problems.append(f'quiz[{i}] opciones/correct inválidos')
        if not ok_pages(q.pages):
            problems.append(f'quiz[{i}] páginas inválidas {q.pages}')
    if len(a.debate) != 5:
        problems.append(f'debate tiene {len(a.debate)} preguntas')
    return problems
