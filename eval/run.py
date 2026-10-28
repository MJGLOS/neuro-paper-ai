"""Evaluación de modelos con PDFs reales.

  .venv/bin/python eval/run.py          # solo estima el costo (gratis)
  .venv/bin/python eval/run.py --run    # analiza y gasta créditos

Lee ANTHROPIC_API_KEY de .env. Los PDFs van en eval/papers/ (ignorado por git).
"""

import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'backend'))

import anthropic  # noqa: E402
from pypdf import PdfReader  # noqa: E402

from analyze import PRICES, analyze, cost, count_tokens, validate  # noqa: E402

MAX_BYTES = 23 * 1024 * 1024  # ponytail: base64 infla ~33% y la petición tope es 32 MB; más grande → Files API
OUTPUT_ESTIMATE = 6_000  # tokens de salida supuestos para la estimación

env = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines() if '=' in line)
# Explícito: ignora ANTHROPIC_BASE_URL/AUTH_TOKEN del shell (p. ej. un proxy local) y usa solo la clave del proyecto.
client = anthropic.Anthropic(api_key=env['ANTHROPIC_API_KEY'].strip(), auth_token=None, base_url='https://api.anthropic.com')
pdfs = sorted((ROOT / 'eval' / 'papers').glob('*.pdf'))
if not pdfs:
    sys.exit('No hay PDFs en eval/papers/')
run = '--run' in sys.argv
out_dir = ROOT / 'eval' / 'out'
out_dir.mkdir(exist_ok=True)

rows, checks, total = [], [], 0.0
for pdf in pdfs:
    data = pdf.read_bytes()
    pages = len(PdfReader(pdf).pages)
    if len(data) > MAX_BYTES:
        rows.append(f'| {pdf.name} | {pages} | — | demasiado grande ({len(data) // 2**20} MB), necesita Files API | | | |')
        continue
    for model in PRICES:
        tokens = count_tokens(client, model, data)
        if not run:
            est = cost(model, tokens, OUTPUT_ESTIMATE)
            total += est
            print(f'{pdf.name:40} {pages:4} págs  {model:18} {tokens:>9,} tokens  ~${est:.3f}')
            continue
        t0 = time.time()
        try:
            result, resp = analyze(client, model, data)
        except anthropic.APIError as e:
            rows.append(f'| {pdf.name} | {pages} | {model} | error API: {e} | | | |')
            continue
        secs = time.time() - t0
        u = resp.usage
        usd = cost(model, u.input_tokens, u.output_tokens)
        total += usd
        if result is None:
            status = f'sin resultado ({resp.stop_reason})'
        else:
            problems = validate(result, pages)
            status = 'válido' if not problems else 'inválido: ' + '; '.join(problems)
            (out_dir / f'{pdf.stem}.{model}.json').write_text(result.model_dump_json(indent=2))
            for c in random.sample(result.summary, min(3, len(result.summary))):
                checks.append(f'| {pdf.name} | {model} | {c.text} | {c.pages} | [ ] |')
        rows.append(f'| {pdf.name} | {pages} | {model} | {status} | {secs:.0f} s | {u.input_tokens:,} / {u.output_tokens:,} | ${usd:.3f} |')
        print(rows[-1])

if not run:
    print(f'\nCosto estimado total: ~${total:.2f}  (supone {OUTPUT_ESTIMATE:,} tokens de salida por análisis)')
    print('Para ejecutar de verdad: .venv/bin/python eval/run.py --run')
    sys.exit()

report = ROOT / 'docs' / 'evaluacion.md'
report.write_text(
    f'# Evaluación de modelos — {time.strftime("%Y-%m-%d")}\n\n'
    f'Costo total: ${total:.2f}. Resultados completos en eval/out/ (no versionado).\n\n'
    '| PDF | Págs | Modelo | Estado | Tiempo | Tokens entrada / salida | Costo |\n|---|---|---|---|---|---|---|\n'
    + '\n'.join(rows)
    + '\n\n## Verificación manual de fidelidad\n\n'
    'Abre el PDF en la página indicada y marca [x] si la afirmación está ahí y es correcta.\n\n'
    '| PDF | Modelo | Afirmación | Páginas | ¿Correcta? |\n|---|---|---|---|---|\n'
    + '\n'.join(checks) + '\n'
)
print(f'\nCosto total: ${total:.2f}. Informe: {report.relative_to(ROOT)}')
