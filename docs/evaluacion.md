# Evaluación de modelos — 2026-10-27

Costo total: $1.76. Resultados completos en eval/out/ (no versionado).

| PDF | Págs | Modelo | Estado | Tiempo | Tokens entrada / salida | Costo |
|---|---|---|---|---|---|---|
| paper_IA_1_atencion_dispersa.pdf | 5 | claude-haiku-5-5 | válido | 11 s | 15,997 / 2,096 | $0.003 |
| paper_IA_1_atencion_dispersa.pdf | 5 | claude-sonnet-5-5 | válido | 17 s | 15,997 / 2,303 | $0.055 |
| paper_IA_2_refuerzo_robotica.pdf | 4 | claude-haiku-5-5 | válido | 8 s | 13,409 / 1,862 | $0.002 |
| paper_IA_2_refuerzo_robotica.pdf | 4 | claude-sonnet-5-5 | válido | 14 s | 13,409 / 2,102 | $0.048 |
| paper_LARGO_tesis_neurociencia_computacional.pdf | 190 | claude-haiku-5-5 | inválido: quiz tiene 4 preguntas | 43 s | 612,798 / 2,105 | $0.312 |
| paper_LARGO_tesis_neurociencia_computacional.pdf | 190 | claude-sonnet-5-5 | válido | 47 s | 612,798 / 2,060 | $1.246 |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | 4 | claude-haiku-5-5 | válido | 16 s | 12,575 / 3,309 | $0.003 |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | 4 | claude-sonnet-5-5 | válido | 16 s | 12,575 / 2,296 | $0.048 |
| paper_MED_2_microbiota_sueno.pdf | 3 | claude-haiku-5-5 | válido | 9 s | 10,607 / 1,962 | $0.002 |
| paper_MED_2_microbiota_sueno.pdf | 3 | claude-sonnet-5-5 | válido | 13 s | 10,607 / 1,923 | $0.040 |

## Verificación manual de fidelidad

Abre el PDF en la página indicada y marca [x] si la afirmación está ahí y es correcta.

| PDF | Modelo | Afirmación | Páginas | ¿Correcta? |
|---|---|---|---|---|
| paper_IA_1_atencion_dispersa.pdf | claude-haiku-5-5 | En la Tabla 1, ADA (k = 512) obtiene 70,8 en LongQA frente a 71,4 de la atención completa, y reduce la memoria de 21,3 GB a 9,6 GB; la ventana deslizante es más barata pero con menor exactitud en LongQA (62,1). | [3] | [ ] |
| paper_IA_1_atencion_dispersa.pdf | claude-haiku-5-5 | El análisis de ablación indica que el selector aprendido es el componente más importante: sustituirlo por selección aleatoria baja LongQA de 70,8 a 58,2 (−12,6 puntos). | [4, 5] | [ ] |
| paper_IA_1_atencion_dispersa.pdf | claude-haiku-5-5 | El artículo presenta ADA (Atención Dispersa Adaptativa), un mecanismo que selecciona dinámicamente un subconjunto de tokens relevantes para cada consulta, con el objetivo de reducir el costo de la atención de O(n²) a O(n·k). | [1] | [ ] |
| paper_IA_1_atencion_dispersa.pdf | claude-sonnet-5-5 | Entre las limitaciones se menciona el uso exclusivo de corpus en inglés y español, que las métricas automáticas no siempre reflejan la percepción humana de calidad, y que se proponen como trabajo futuro modalidades como audio o video. | [1, 2, 4] | [ ] |
| paper_IA_1_atencion_dispersa.pdf | claude-sonnet-5-5 | El método usa un selector ligero que calcula una puntuación de relevancia r_ij = σ(wᵀ[q_i; k_j]) para cada clave; solo los k tokens con mayor puntuación participan en la atención, y durante el entrenamiento se usa una relajación Gumbel-Softmax para mantener la diferenciabilidad. | [2] | [ ] |
| paper_IA_1_atencion_dispersa.pdf | claude-sonnet-5-5 | El objetivo del artículo es presentar ADA (Atención Dispersa Adaptativa), un mecanismo que selecciona dinámicamente un subconjunto de tokens relevantes para cada consulta, reduciendo el costo de la atención de O(n²) a O(n·k). | [1] | [ ] |
| paper_IA_2_refuerzo_robotica.pdf | claude-haiku-5-5 | Limitaciones: la variabilidad entre semillas fue considerable en las tareas de mayor dificultad, y la transferencia de simulación a realidad sigue siendo un desafío del área; el documento se describe como ficticio y para pruebas. | [2, 3, 1] | [ ] |
| paper_IA_2_refuerzo_robotica.pdf | claude-haiku-5-5 | Resultados en simulación: en seis tareas, CURRIC-HF alcanza una tasa de éxito media del 83 % frente al 61 % del entrenamiento sin currículo, y reduce un 54 % los pasos para converger. | [1, 3] | [ ] |
| paper_IA_2_refuerzo_robotica.pdf | claude-haiku-5-5 | Objetivo: proponer CURRIC-HF, un método que construye automáticamente un currículo de tareas de manipulación a partir de preferencias humanas. | [1] | [ ] |
| paper_IA_2_refuerzo_robotica.pdf | claude-sonnet-5-5 | Limitaciones señaladas: la variabilidad entre semillas fue considerable en las tareas más difíciles, y se observaron comportamientos indeseados cuando el modelo de recompensa estaba poco entrenado. | [1, 3] | [ ] |
| paper_IA_2_refuerzo_robotica.pdf | claude-sonnet-5-5 | Los autores proponen CURRIC-HF, un método que construye automáticamente un currículo de tareas de manipulación robótica a partir de preferencias humanas. | [1] | [ ] |
| paper_IA_2_refuerzo_robotica.pdf | claude-sonnet-5-5 | En un robot físico, la política transferida logra un 67 % de éxito al apilar bloques; los resultados reales fueron inferiores a los de simulación, y la transferencia de simulación a realidad sigue siendo un desafío. | [1, 2] | [ ] |
| paper_LARGO_tesis_neurociencia_computacional.pdf | claude-haiku-5-5 | La tesis presenta una revisión integradora de los vínculos entre la neurociencia computacional y el aprendizaje automático, recorriendo doce capítulos. | [2] | [ ] |
| paper_LARGO_tesis_neurociencia_computacional.pdf | claude-haiku-5-5 | El texto de los capítulos es en gran parte repetitivo: las mismas frases genéricas se repiten sobre cada tema, sin desarrollar definiciones, datos o resultados concretos. | [5, 6, 7] | [ ] |
| paper_LARGO_tesis_neurociencia_computacional.pdf | claude-haiku-5-5 | Las referencias bibliográficas listadas no permiten verificar las afirmaciones del texto, y el documento no reporta un método empírico propio. | [188, 189, 190] | [ ] |
| paper_LARGO_tesis_neurociencia_computacional.pdf | claude-sonnet-5-5 | La tesis presenta una revisión integradora de los vínculos entre neurociencia computacional y aprendizaje automático, a lo largo de doce capítulos. | [2] | [ ] |
| paper_LARGO_tesis_neurociencia_computacional.pdf | claude-sonnet-5-5 | El documento es una revisión sin método experimental propio ni resultados cuantitativos; gran parte de cada capítulo repite afirmaciones generales sin detalle técnico. | [2, 20, 35] | [ ] |
| paper_LARGO_tesis_neurociencia_computacional.pdf | claude-sonnet-5-5 | Como limitaciones se señalan repetidamente que la analogía entre modelos biológicos y artificiales debe tomarse con cautela, que los modelos no explican todas las observaciones empíricas y que los datos provienen sobre todo de roedores y primates. | [5, 6, 19] | [ ] |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | claude-haiku-5-5 | Objetivo: evaluar el efecto de un programa de 12 semanas de ejercicio aeróbico moderado sobre la presión arterial sistólica (PAS). | [1] | [ ] |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | claude-haiku-5-5 | Conclusión de los autores: el ejercicio aeróbico moderado reduce de forma clínicamente relevante la presión arterial, con buena tolerancia. | [1, 4] | [ ] |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | claude-haiku-5-5 | Otros desenlaces: la presión arterial diastólica, la frecuencia cardiaca y el VO2máx mejoraron más en el grupo de intervención; el cambio en colesterol LDL no fue estadísticamente significativo (p = 0,098). | [3] | [ ] |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | claude-sonnet-5-5 | Método: ensayo aleatorizado, paralelo y con evaluador cegado. Se aleatorizaron 184 personas (92 por grupo) con bloques permutados de tamaño variable. La intervención fue de tres sesiones semanales de caminata rápida o cicloergómetro al 50–70 % de la frecuencia cardiaca de reserva, y el control recibió recomendaciones generales de estilo de vida. | [1, 2] | [ ] |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | claude-sonnet-5-5 | Seguridad: no hubo eventos adversos graves. En el grupo de intervención hubo más dolor musculoesquelético leve (15,2 % frente a 3,3 %), esguinces de tobillo, mareos durante la sesión y un caso de hipotensión sintomática. | [3, 4] | [ ] |
| paper_MED_1_ejercicio_hipertension_TABLAS.pdf | claude-sonnet-5-5 | El efecto fue consistente según sexo y edad, y mayor en participantes con IMC ≥ 30 (−8,7 mmHg frente a −5,1 mmHg), aunque la p de interacción fue 0,08. | [3] | [ ] |
| paper_MED_2_microbiota_sueno.pdf | claude-haiku-5-5 | Limitación: el diseño transversal no permite inferir causalidad ni establecer la dirección de la asociación; el propio texto indica que se necesitan estudios longitudinales e intervenciones controladas. | [1, 2, 3] | [ ] |
| paper_MED_2_microbiota_sueno.pdf | claude-haiku-5-5 | Los resultados de la Tabla 1 muestran también menos horas de sueño por noche (5,9 vs. 7,1; p < 0,001) y menor consumo de fibra (17 vs. 21 g/día; p = 0,011) en el grupo de mala calidad. | [2] | [ ] |
| paper_MED_2_microbiota_sueno.pdf | claude-haiku-5-5 | Resultados: los participantes con mala calidad de sueño (58 %) presentaron menor diversidad alfa (Shannon 3,41 vs. 3,78; p = 0,002) y menor abundancia de géneros productores de butirato. | [1, 2] | [ ] |
| paper_MED_2_microbiota_sueno.pdf | claude-sonnet-5-5 | El estudio analiza la relación entre la composición de la microbiota intestinal y la calidad del sueño en 212 estudiantes universitarios de pregrado de 18 a 26 años. | [1, 2] | [ ] |
| paper_MED_2_microbiota_sueno.pdf | claude-sonnet-5-5 | Por su diseño transversal, no se puede establecer la dirección de la asociación ni la causalidad; el estrés académico y la dieta podrían confundir, y se requieren estudios longitudinales e intervenciones controladas. | [1, 2, 3] | [ ] |
| paper_MED_2_microbiota_sueno.pdf | claude-sonnet-5-5 | El grupo con mala calidad de sueño durmió menos horas por noche (5,9 vs. 7,1; p < 0,001) y consumió menos fibra dietaria (17 vs. 21 g/día; p = 0,011). | [2] | [ ] |

## Conclusiones (2026-10-27, PDFs ficticios)

- **Validez:** Sonnet, 5 de 5. Haiku, 4 de 5: en la tesis de 190 páginas devolvió 4 preguntas de quiz en vez de 3. `validate()` lo detectó, que es justo para lo que sirve.
- **Fidelidad numérica (automática):** toda cifra que aparece en el resumen o en las explicaciones del quiz está en la página citada. Haiku, 60 de 60; Sonnet, 93 de 93. Las páginas impresas coinciden con las físicas en estos PDFs.
- **Detalle:** Sonnet da resúmenes más ricos (93 cifras frente a 60, efectos por subgrupo, seguridad). Haiku es correcto pero más escueto.
- **Costo:** Haiku cuesta entre US$0,002 y US$0,003 por paper corto y US$0,31 por 190 páginas. Sonnet, entre US$0,04 y US$0,06 y US$1,25. Unos 3.200 tokens por página.
- **Tiempo:** de 8 a 17 s por paper corto y de 43 a 47 s por 190 páginas.
- **Sesgo:** en un quiz de Haiku las 3 respuestas correctas eran la opción B. Solución: barajar las opciones en el código, no en el prompt.
- **Pendiente:** repetir con 3 o 4 papers reales (arXiv o PubMed Central) con dos columnas, figuras y escaneos antes de fijar el modelo.
