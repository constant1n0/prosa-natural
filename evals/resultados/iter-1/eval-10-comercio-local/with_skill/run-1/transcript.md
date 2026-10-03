# Transcript — eval-10-comercio-local / with_skill / run-1

## Archivos leídos

- `/Users/dcm/work/prosa-natural/skill/prosa-natural/SKILL.md`
- `/Users/dcm/work/prosa-natural/evals/casos/10-comercio-local.md` (texto del usuario)
- `/Users/dcm/work/prosa-natural/skill/prosa-natural/references/patrones.md`
- `/Users/dcm/work/prosa-natural/skill/prosa-natural/references/discurso.md`
- `/Users/dcm/work/prosa-natural/skill/prosa-natural/references/vocabulario-es.md`

## Comandos ejecutados

- `mkdir -p .../scratchpad` y volcado del texto original a `scratchpad/original.txt` y del borrador a `scratchpad/nueva.txt` (heredocs).
- `python3 /Users/dcm/work/prosa-natural/skill/prosa-natural/scripts/scan_tells.py --original scratchpad/original.txt scratchpad/nueva.txt` — paso 4 del flujo (comprobación determinista de datos y claims). Código de salida 1, por las dos únicas entradas en `comparacion.nombres_propios.faltantes` ("Ubicación", "De"): son palabras comunes que solo aparecían en mayúscula por el Title Case del título original (rasgo P20, corregido a rigor); no son nombres propios reales, así que se descartaron a mano, tal como documenta el propio SKILL.md sobre esta limitación del escáner. El resto de categorías (cifras, precios, fechas, códigos, URL, citas, claims marcados, duraciones/unidades, registro tú/usted) no mostró ninguna diferencia.
- `mkdir -p .../with_skill/run-1/outputs` y `ls` de comprobación.

## Decisiones de la skill aplicadas

- Modo Reescritura (el usuario pidió «pulir»), con la alegación «sin conservantes ni aditivos» (heurística "sin X") dejada literal y señalada, no reformulada (regla dura 2).
- Rasgos corregidos: P20 (Title Case del encabezado), P16 (lenguaje de folleto: "enclavada en el corazón de", "visita obligada"), metadiscurso vacío "cabe destacar que" (vocabulario fuerte), P56 (signo de apertura "¿" que faltaba), y la frase de cierre genérica (P16 + P26 frase portátil + P06 tríada forzada en "artesano, cálido y recién hecho"), cortada por no aportar ningún dato nuevo ni distinguir a Panadería Olmo.
- Datos verificados intactos: dirección, horario, precios, teléfono, plazo de reserva, trato de tú.
