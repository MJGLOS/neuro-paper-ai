/* ═══════════════════════════════════════════
   NeuroPaper AI — app.js
   ═══════════════════════════════════════════ */

'use strict';

// ── State ──────────────────────────────────────────────────────
let quizScore    = 0;
let quizAnswered = 0;
let quizTotal    = 0;

// ── Drag & Drop ────────────────────────────────────────────────
function handleDragOver(e) {
  e.preventDefault();
  document.getElementById('uploadZone').classList.add('drag-over');
}

function handleDragLeave() {
  document.getElementById('uploadZone').classList.remove('drag-over');
}

function handleDrop(e) {
  e.preventDefault();
  document.getElementById('uploadZone').classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file && file.type === 'application/pdf') {
    processFile(file);
  } else {
    showToast('⚠️ Por favor sube un archivo PDF');
  }
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) processFile(file);
}

// ── File Processing ────────────────────────────────────────────
function processFile(file) {
  if (file.size > 20 * 1024 * 1024) {
    showToast('⚠️ El archivo supera los 20MB');
    return;
  }

  // Show processing, hide upload
  document.getElementById('uploadWrap').style.display = 'none';
  document.getElementById('processingPanel').classList.add('active');
  document.getElementById('paperName').textContent = file.name;

  // Animate progress steps
  const stepIds  = ['ps1', 'ps2', 'ps3', 'ps4', 'ps5'];
  const progPcts = [15, 35, 55, 75, 92];
  let stepIndex  = 0;

  const tick = setInterval(() => {
    // Mark previous step as done
    if (stepIndex > 0) {
      const prev = document.getElementById(stepIds[stepIndex - 1]);
      prev.className = 'proc-step done';
      prev.querySelector('.ps-icon').textContent = '✓';
    }
    // Activate next step
    if (stepIndex < stepIds.length) {
      document.getElementById(stepIds[stepIndex]).className = 'proc-step active';
      document.getElementById('progFill').style.width = progPcts[stepIndex] + '%';
      stepIndex++;
    } else {
      clearInterval(tick);
    }
  }, 650);

  // Read file and call API
  const reader = new FileReader();
  reader.onerror = () => {
    clearInterval(tick);
    showToast('❌ Error al leer el archivo');
    resetApp();
  };
  reader.onload = async (e) => {
    const base64 = e.target.result.split(',')[1];
    await callAPI(base64);
  };
  reader.readAsDataURL(file);
}

// ── Claude API ─────────────────────────────────────────────────
async function callAPI(base64PDF) {
  const prompt = `Analiza este paper de neurociencia. Responde ÚNICAMENTE con JSON válido, sin markdown, sin texto extra:
{
  "summary": "Resumen técnico de 4-6 oraciones con terminología científica precisa",
  "simple": "Explicación de 3-4 oraciones para no-científicos usando analogías cotidianas",
  "concepts": ["concepto1","concepto2","concepto3","concepto4","concepto5","concepto6","concepto7","concepto8"],
  "ai_connection": "3-4 oraciones relacionando el paper con IA, machine learning o neurociencia computacional",
  "quiz": [
    {
      "question": "Primera pregunta de comprensión",
      "options": ["A) opción uno","B) opción dos","C) opción tres","D) opción cuatro"],
      "correct": 0,
      "explanation": "Razón por la que esta respuesta es correcta"
    },
    {
      "question": "Segunda pregunta de comprensión",
      "options": ["A) opción uno","B) opción dos","C) opción tres","D) opción cuatro"],
      "correct": 2,
      "explanation": "Razón por la que esta respuesta es correcta"
    },
    {
      "question": "Tercera pregunta de comprensión",
      "options": ["A) opción uno","B) opción dos","C) opción tres","D) opción cuatro"],
      "correct": 1,
      "explanation": "Razón por la que esta respuesta es correcta"
    }
  ],
  "debate": [
    "Pregunta 1: implicaciones del hallazgo principal",
    "Pregunta 2: sobre la metodología del estudio",
    "Pregunta 3: implicaciones éticas o futuras",
    "Pregunta 4: conexión con otras áreas de neurociencia",
    "Pregunta 5: limitaciones o controversias del estudio"
  ]
}`;

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-opus-4-6',          // ← modelo correcto y actualizado
        max_tokens: 2000,                   // ← aumentado para respuestas completas
        messages: [{
          role: 'user',
          content: [
            {
              type: 'document',
              source: { type: 'base64', media_type: 'application/pdf', data: base64PDF }
            },
            { type: 'text', text: prompt }
          ]
        }]
      })
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      console.error('API error:', err);
      throw new Error(`API ${response.status}: ${err?.error?.message || 'Error desconocido'}`);
    }

    const data  = await response.json();
    const raw   = (data.content || []).map(b => b.text || '').join('');
    // Strip any accidental markdown fences
    const clean = raw.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();
    const result = JSON.parse(clean);

    renderResults(result);

  } catch (err) {
    console.error('callAPI error:', err);
    showToast('❌ Error al analizar el paper. Revisa la consola.');
    resetApp();
  }
}

// ── Render Results ─────────────────────────────────────────────
function renderResults(data) {
  // Complete the progress bar
  document.getElementById('progFill').style.width = '100%';

  setTimeout(() => {
    document.getElementById('processingPanel').classList.remove('active');
    document.getElementById('resultsPanel').classList.add('active');

    // -- Text sections
    document.getElementById('summaryText').textContent = data.summary       || '(sin datos)';
    document.getElementById('simpleText').textContent  = data.simple        || '(sin datos)';
    document.getElementById('aiText').textContent      = data.ai_connection || '(sin datos)';

    // -- Concepts cloud
    const cloud = document.getElementById('conceptsCloud');
    cloud.innerHTML = '';
    (data.concepts || []).forEach((concept, i) => {
      const tag = document.createElement('span');
      tag.className = 'concept-item';
      tag.textContent = concept;
      tag.style.animationDelay = (i * 0.06) + 's';
      cloud.appendChild(tag);
    });

    // -- Quiz
    quizScore    = 0;
    quizAnswered = 0;
    quizTotal    = (data.quiz || []).length;

    const quizList = document.getElementById('quizList');
    quizList.innerHTML = '';

    (data.quiz || []).forEach((q, qi) => {
      // Safely escape explanation for use in onclick attribute
      const explanation = (q.explanation || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '&quot;');

      const item = document.createElement('div');
      item.className = 'quiz-item';
      item.innerHTML = `
        <div class="quiz-q-text">
          <span class="q-num">Q${qi + 1}</span>
          ${escapeHTML(q.question)}
        </div>
        <div class="quiz-opts" id="qo-${qi}">
          ${(q.options || []).map((opt, oi) => `
            <button class="quiz-opt"
              onclick="pickAnswer(${qi}, ${oi}, ${q.correct}, '${explanation}')">
              ${escapeHTML(opt)}
            </button>
          `).join('')}
        </div>
        <div class="quiz-fb" id="qf-${qi}"></div>
      `;
      quizList.appendChild(item);
    });

    refreshScore();

    // -- Debate
    const debateList = document.getElementById('debateList');
    debateList.innerHTML = '';

    (data.debate || []).forEach((question, i) => {
      const item = document.createElement('div');
      item.className = 'debate-item';
      item.innerHTML = `
        <div class="debate-badge">${i + 1}</div>
        <div>
          <div class="debate-text">${escapeHTML(question)}</div>
          <div class="debate-hint">Clic para copiar</div>
        </div>
      `;
      item.addEventListener('click', () => {
        navigator.clipboard.writeText(question)
          .then(() => showToast('📋 Pregunta copiada'))
          .catch(() => showToast('⚠️ No se pudo copiar'));
      });
      debateList.appendChild(item);
    });

    // Scroll & notify
    document.getElementById('resultsPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
    showToast('✅ ¡Análisis completado!');

  }, 400);
}

// ── Quiz ───────────────────────────────────────────────────────
function pickAnswer(questionIndex, selectedIndex, correctIndex, explanation) {
  const opts = document.querySelectorAll(`#qo-${questionIndex} .quiz-opt`);
  const fb   = document.getElementById(`qf-${questionIndex}`);

  // Disable all options
  opts.forEach(opt => { opt.disabled = true; });

  // Mark correct / wrong
  opts[correctIndex].classList.add('correct');
  if (selectedIndex !== correctIndex) {
    opts[selectedIndex].classList.add('wrong');
  }

  const isCorrect = selectedIndex === correctIndex;

  // Show feedback
  fb.textContent = isCorrect
    ? `✓ ¡Correcto! ${explanation}`
    : `✗ Incorrecto. ${explanation}`;
  fb.className = 'quiz-fb ' + (isCorrect ? 'ok' : 'bad');

  if (isCorrect) quizScore++;
  quizAnswered++;
  refreshScore();
}

function refreshScore() {
  const display = `${quizScore} / ${quizAnswered > 0 ? quizAnswered : quizTotal}`;
  document.getElementById('quizScore').textContent  = display;
  document.getElementById('scoreText').textContent  = display;

  if (quizAnswered > 0) {
    document.getElementById('scorePill').classList.add('visible');
  }
}

// ── Tabs ───────────────────────────────────────────────────────
function switchTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));

  document.querySelector(`.tab-btn[data-tab="${tabName}"]`).classList.add('active');
  document.getElementById(`tab-${tabName}`).classList.add('active');
}

// ── Reset ──────────────────────────────────────────────────────
function resetApp() {
  document.getElementById('uploadWrap').style.display       = 'block';
  document.getElementById('processingPanel').classList.remove('active');
  document.getElementById('resultsPanel').classList.remove('active');
  document.getElementById('fileInput').value                = '';
  document.getElementById('progFill').style.width           = '0%';
  document.getElementById('scorePill').classList.remove('visible');

  // Reset step indicators
  ['ps1', 'ps2', 'ps3', 'ps4', 'ps5'].forEach((id, i) => {
    const el = document.getElementById(id);
    el.className = i === 0 ? 'proc-step active' : 'proc-step';
    el.querySelector('.ps-icon').textContent = '●';
  });

  switchTab('summary');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── Navigation ─────────────────────────────────────────────────
function scrollToPricing() {
  document.getElementById('pricingSection').scrollIntoView({ behavior: 'smooth' });
}

// ── Toast ──────────────────────────────────────────────────────
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

// ── Helpers ────────────────────────────────────────────────────
function escapeHTML(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
