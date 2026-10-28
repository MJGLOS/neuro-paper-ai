"""Ejecutar: .venv/bin/python backend/test_analyze.py"""

from analyze import Analysis, cost, validate


def sample(**over):
    base = {
        'summary': [{'text': 't', 'pages': [1]}] * 4,
        'simple': 's',
        'concepts': [{'term': 'c', 'definition': 'd', 'pages': [2]}] * 5,
        'quiz': [{'question': 'q', 'options': ['a', 'b', 'c', 'd'], 'correct': 0, 'explanation': 'e', 'pages': [3]}] * 3,
        'debate': ['d'] * 5,
    }
    return Analysis.model_validate(base | over)


assert validate(sample(), page_count=10) == []
assert validate(sample(), page_count=2)  # quiz cita la página 3 de un PDF de 2
assert validate(sample(summary=[{'text': 't', 'pages': []}] * 4), 10)  # afirmación sin página
assert validate(sample(quiz=[{'question': 'q', 'options': ['a', 'b', 'c', 'd'], 'correct': 4, 'explanation': 'e', 'pages': [1]}] * 3), 10)
assert validate(sample(debate=['d'] * 4), 10)
assert abs(cost('claude-haiku-5-5', 50_000, 5_000) - 0.0075) < 1e-9
assert abs(cost('claude-haiku-5-5', 200_000, 5_000) - 0.1125) < 1e-9  # tramo largo
assert abs(cost('claude-sonnet-5-5', 50_000, 5_000) - 0.15) < 1e-9
print('ok')
