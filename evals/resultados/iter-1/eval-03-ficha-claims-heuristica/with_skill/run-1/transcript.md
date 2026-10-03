## Archivos leídos

- /Users/dcm/work/prosa-natural/skill/prosa-natural/SKILL.md
- /Users/dcm/work/prosa-natural/evals/casos/03-ficha-claims-heuristica.md
- /Users/dcm/work/prosa-natural/skill/prosa-natural/references/revision.md
- /Users/dcm/work/prosa-natural/skill/prosa-natural/references/claims.md
- /Users/dcm/work/prosa-natural/skill/prosa-natural/references/patrones.md
- /Users/dcm/work/prosa-natural/skill/prosa-natural/references/discurso.md
- /Users/dcm/work/prosa-natural/skill/prosa-natural/references/vocabulario-es.md (offset 100-150, tras rg)

## Comandos ejecutados

- `mkdir -p ".../with_skill/run-1/outputs" && ls -la ".../with_skill/run-1"` — crear estructura de salida
- `python3 scripts/scan_tells.py /Users/dcm/work/prosa-natural/evals/casos/03-ficha-claims-heuristica.md` (desde `/Users/dcm/work/prosa-natural/skill/prosa-natural`) — pasada del escáner opcional (paso 4 del flujo) sobre el texto de entrada, sin `--original` porque no se generó una versión reescrita (modo Revisión)
- `rg -n "P31|cabe destacar|Metadiscurso vacío" references/vocabulario-es.md` (desde la carpeta de la skill) — localizar la entrada de vocabulario para el hallazgo de "cabe destacar que"

## Notas del proceso

- El texto tiene claims heurísticos (duración con unidad, "dermatológicamente testado", "sin X", "no testado en animales", porcentaje, referencia a estudios) y el usuario no eligió modo, así que la skill entró en modo Revisión por su cuenta (regla de SKILL.md §Claims).
- No se creó `version_final.md`: la respuesta es una revisión/auditoría, no entrega una versión final reescrita.
