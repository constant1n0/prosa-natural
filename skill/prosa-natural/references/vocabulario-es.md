# Vocabulario español de registro IA

Lista determinista de expresiones que `scripts/scan_tells.py` compara con el
texto y que el modelo puede repasar cuando necesita el detalle léxico. No
sustituye al criterio del modelo: cada aparición se juzga en su contexto antes
de tocar nada.

## Cómo leer esta lista

Cada expresión vive en uno de dos niveles:

- **Fuerte**: una sola aparición ya es una señal clara en su contexto (por
  ejemplo, una apertura de chatbot fuera de un diálogo, o una colocación
  calcada de una fórmula de marketing en inglés).
- **Débil**: es una palabra o frase de uso corriente en español. Sola no
  significa nada; solo pesa cuando se acumula — varias de la misma familia en
  el mismo párrafo, o una densidad alta por cada mil palabras. El corte
  numérico de esa densidad está por calibrar con medición real y no se fija
  en este archivo.

Casi todas las entradas son señales débiles precisamente porque casi todas
son palabras que cualquier persona hispanohablante usa sin pensar en ningún
detector. La mayoría de esta lista **no son errores**: son palabras y frases
correctas del español que aparecen con una frecuencia desproporcionada en
texto generado. Tratarlas como errores universales produciría falsos
positivos constantes; por eso pesan por densidad, no por presencia, y por eso
el modelo comprueba siempre el contexto — una cita textual, un nombre propio,
un INCI, una marca o el propio texto hablando de la palabra no cuentan nunca,
y un claim, una alegación protegida o un intocable técnico tienen prioridad
absoluta sobre cualquier entrada de esta lista.

Esta lista tampoco es una herramienta para evadir detectores. No existe para
que el modelo sustituya una palabra por otra "menos sospechosa", ni para
insertar muletillas, dudas fingidas o imperfecciones que "suenen humanas".
Su único uso es señalar densidad de un registro calcado para que quien
revisa decida si corta, reformula o deja el texto como está.

Una entrada puede llevar el campo `pendiente` (ver [Formato](#formato)).
Marca que la base normativa de esa entrada —una censura o recomendación de
la RAE o Fundéu— está pendiente de comprobar en fuente primaria. Mientras
siga pendiente, esa entrada no autoriza ninguna corrección automática ni se
presenta como una regla ya establecida: se señala como posible uso a
revisar, igual que el resto de entradas débiles, nunca como un error
confirmado.

Los patrones estructurales —el contraste "no solo… sino" (P01), la tríada
forzada y la acumulación de epítetos antepuestos (P06, P41), los conectores
apilados (P37) y el gerundio de posterioridad (P15)— no están en este
archivo porque no son presencia léxica: dependen de la construcción de la
frase. Viven en `patrones.md` y en los detectores estructurales de
`scan_tells.py`.

## Formato

Este archivo se parsea con la biblioteca estándar de Python (sin YAML ni
CSV de terceros), así que el formato es estricto. `scan_tells.py` sigue
exactamente estas reglas y su docstring las repite.

- Solo se parsean los encabezados `## Fuerte` y `## Débil`, escritos tal
  cual. Cualquier otro encabezado `##` termina la región de nivel que esté
  abierta en ese momento —por ejemplo, `## Excluidas y variantes` cierra la
  región `## Débil` que lo precede—; el texto que quede fuera de esas dos
  regiones nunca se lee, incluido este mismo `## Formato`, que va antes de
  `## Fuerte` y por tanto es preámbulo, no una región que cerrar.
- Dentro de un nivel, cada familia es un encabezado `### <nombre de
  familia>`. Puede ir seguida de una o dos líneas de motivo que empiezan por
  `> ` (el porqué de la familia); esas líneas no son entradas.
- Cada línea de contenido no vacía que no empiece por `#` ni por `> ` es una
  entrada con el formato `expresión | AAAA-MM-DD | origen`, con un cuarto
  campo opcional `pendiente`. Los campos van separados por ` | ` (espacio,
  barra vertical, espacio).
  - `expresión`: en minúsculas, con tildes normales y con la puntuación
    propia de la expresión cuando forma parte de ella (por ejemplo,
    `¡por supuesto!`).
  - `AAAA-MM-DD`: fecha de alta de la entrada.
  - `origen`: identificador de patrón de `docs/auditoria.md` (uno o varios,
    separados por coma) y el nombre corto de la fuente citada en esa
    auditoría (por ejemplo, `P31 · anti-ai-writing`, `P44 · humanamente`,
    `P22 · semilla`).
  - `pendiente`: presente solo si la base normativa de la entrada está sin
    verificar en fuente primaria (ver [Cómo leer esta lista](#cómo-leer-esta-lista)).
- El asterisco `*` solo se admite al final de una palabra, como comodín de
  letras (por ejemplo, `optimiz*` para cubrir "optimizar", "optimizando",
  "optimización"). Se usa solo donde no genera coincidencias con palabras no
  relacionadas; si el comodín ampliaría la búsqueda a una palabra distinta
  (por ejemplo, la familia de "potencial", que se trata aparte por
  colocación), se listan las formas concretas en vez de un comodín.
- Las colocaciones (expresiones que solo son señal en combinación, nunca en
  la palabra suelta) se listan como la colocación completa —por ejemplo,
  `desbloquear el potencial`, `aprovechar al máximo`— y nunca como la
  palabra aislada.
- Se permiten líneas en blanco entre entradas y entre bloques.
- Comparación: `scan_tells.py` normaliza con Unicode NFD y compara sin
  distinguir mayúsculas ni tildes, y solo en límites de palabra. Esta
  normalización afecta a cómo busca el script, nunca a cómo se escribe la
  entrada en este archivo (aquí siempre en minúsculas y con tildes
  normales). El modelo, en cualquier caso, siempre valora el contexto antes
  de actuar sobre un hallazgo.

## Fuerte

### Restos de chatbot

> Un saludo o una despedida de asistente conversacional fuera de un diálogo
> o de una carta real delata, con una sola aparición, que el texto no pasó
> por una revisión de voz propia.

¡claro! | 2026-09-27 | P22 · semilla
¡por supuesto! | 2026-09-27 | P22 · semilla
espero que te sea útil | 2026-09-27 | P22, P63 · semilla

### Preámbulo escenificado

> Invitaciones del tipo "vamos a explorar esto juntos" imitan la voz de un
> asistente que presenta un tema a quien no lo conoce, no la de quien ya
> domina lo que cuenta.

profundicemos en | 2026-09-27 | P04 · ADS
descubramos juntos | 2026-09-27 | P04 · ADS
vamos a sumergirnos en | 2026-09-27 | P04 · semilla

### Límite de conocimiento y conjeturas

> Presentar una suposición con la cautela de un modelo con fecha de corte,
> en vez de con la duda propia de quien escribe, delata el origen del
> texto y además presenta una conjetura como si fuera un hecho.

hasta donde alcanza mi información | 2026-09-27 | P23 · blader

### Metadiscurso vacío

> Anuncian que algo es relevante sin añadir el hecho que lo demuestre.
> Convergen en siete fuentes españolas distintas y en la familia
> "destacar, subrayar" descrita por Juzek (2026).

cabe destacar que | 2026-09-27 | P31 · anti-ai-writing, semilla
cabe mencionar que | 2026-09-27 | P31 · semilla
vale la pena mencionar que | 2026-09-27 | P31 · anti-ai-writing
vale la pena señalar | 2026-09-27 | P31 · semilla
es importante mencionar | 2026-09-27 | P31 · ADS
es importante destacar que | 2026-09-27 | P31 · semilla

### Apertura temporal o panorámica vacía

> Abren con una época o un panorama sin ningún dato concreto del texto que
> sigue. Se cortan porque no aportan nada, no porque la fórmula "suene a
> IA" en abstracto; "en los últimos años" con un dato real detrás no
> cuenta.

en el mundo actual | 2026-09-27 | P44 · anti-ai-writing
en el competitivo mundo de | 2026-09-27 | P44 · anti-ai-writing
hoy en día más que nunca | 2026-09-27 | P44 · anti-ai-writing
en la era de | 2026-09-27 | P44 · ADS
en el panorama actual | 2026-09-27 | P44 · semilla
en un mundo cada vez más | 2026-09-27 | P44 · semilla

### Significado inflado: colocaciones calcadas

> Calcos de fórmulas inglesas de marketing que inflan un hecho corriente
> hasta la grandilocuencia. La señal es la colocación exacta, no las
> palabras sueltas que la forman.

constituye un testimonio de | 2026-09-27 | P13 · PR#151
liberar el potencial de | 2026-09-27 | P12 · anti-ai-writing
desbloquear el potencial | 2026-09-27 | P12 · anti-ai-writing, semilla, PR#151
navegar por los retos | 2026-09-27 | P12 · PR#151
por último, pero no menos importante | 2026-09-27 | P13 · PR#151
llevar al siguiente nivel | 2026-09-27 | P12 · anti-ai-writing

### Evitar "ser" y "tener": excepciones fuertes

> Perífrasis que sustituyen sistemáticamente a "es" o "tiene" para sonar
> más corporativo. El resto de la familia (patrón P18, en
> [Verbos comodín y perífrasis](#verbos-comodín-y-perífrasis)) solo pesa
> acumulada; estas dos formas bastan solas.

se erige como | 2026-09-27 | P18 · PR#151
se posiciona como | 2026-09-27 | P18 · ADS

### Promesa de revelación

> Anuncia un secreto que después no llega: el contenido que sigue es
> información corriente presentada como si fuera un hallazgo exclusivo,
> calco de titulares de marketing y de LinkedIn.

lo que nadie te cuenta | 2026-09-28 | P27 · kjm

## Débil

### Apertura y cierre suave

> Fórmulas de apertura o de resumen corrientes en prensa y ensayo español.
> Solo pesan cuando abren o cierran un texto breve sin aportar ningún dato
> nuevo; un resumen legítimo de un documento largo no cuenta.

en la actualidad | 2026-09-27 | P44 · anti-ai-writing
en resumen, | 2026-09-27 | P43 · semilla
en definitiva, | 2026-09-27 | P43 · semilla
en conclusión | 2026-09-27 | P43 · humanamente
en síntesis | 2026-09-27 | P43 · humanamente
en última instancia | 2026-09-27 | P43 · humanamente
como hemos visto | 2026-09-27 | P43 · humanamente

### Metadiscurso de relleno

> Anuncian que algo importa sin llegar al nivel de las fórmulas calcadas de
> "Metadiscurso vacío". Son frecuentes también en la prosa académica
> humana, así que solo cuentan por acumulación.

en este sentido | 2026-09-27 | P31 · semilla
es evidente que | 2026-09-27 | P31 · NTE
como se puede ver | 2026-09-27 | P31 · NTE
es menester | 2026-09-27 | P31 · ADS
resulta imperativo | 2026-09-27 | P31 · ADS
cobra especial relevancia | 2026-09-27 | P31 · ADS
me complace compartir | 2026-09-27 | P31 · anti-ai-writing

### Transición de relleno

> Otras guías de naturalización en español (NTE) recomiendan "dicho esto"
> como marcador de transición natural. No se veta suelto ni se inserta
> nunca para simular un "toque humano"; solo cuenta si se repite en el
> mismo texto.

dicho esto | 2026-09-27 | P65 · NTE

### Sentencia que suena profunda

> Cierres reflexivos sin ningún contenido nuevo. Son frecuentes también en
> la prosa humana ("en el fondo, tiene razón" es una frase corriente), así
> que solo pesan si se acumulan o si sustituyen a lo que el original
> afirma en vez de decirlo.

en el fondo | 2026-09-27 | P03 · blader
lo que de verdad importa | 2026-09-27 | P03 · blader

### Significado inflado y modificadores huecos

> Frases hechas de inflación que la prensa española usa con normalidad. El
> rasgo es el abuso o la acumulación, no la existencia de la frase.

un antes y un después | 2026-09-27 | P13 · semilla
marca un hito | 2026-09-27 | P13 · semilla, PR#151
sin lugar a dudas | 2026-09-27 | P13 · semilla, humanamente
indudablemente | 2026-09-27 | P12 · humanamente
un verdadero referente | 2026-09-27 | P32 · semilla
revolucionario | 2026-09-27 | P12 · anti-ai-writing, semilla
pilar fundamental | 2026-09-27 | P13 · PR#151
piedra angular | 2026-09-27 | P13 · PR#151
rico tapiz de | 2026-09-27 | P13 · PR#151
de vital importancia | 2026-09-27 | P13 · PR#151

### Lenguaje de folleto

> Calcos de folleto turístico o comercial. Son legítimos cuando describen
> un lugar o un producto con un dato concreto detrás; pesan cuando
> sustituyen a ese dato.

enclavado en | 2026-09-27 | P16 · HES
en el corazón de | 2026-09-27 | P16 · HES
visita obligada | 2026-09-27 | P16 · HES

### Vocabulario de registro IA

> Palabras de uso humano corriente que aparecen con una frecuencia
> desproporcionada en texto generado, según la lista española de
> anti-ai-writing. Una aparición no prueba nada; la acumulación en el mismo
> párrafo, sí. "Subrayar" e "innovador" cuentan además con apoyo empírico
> de Juzek (2026). "Panorama" y "navegar" solo pesan en sentido figurado
> ("navegar por internet" en sentido literal no cuenta).

crucial | 2026-09-27 | P12 · anti-ai-writing
fundamental | 2026-09-27 | P12 · anti-ai-writing
esencial | 2026-09-27 | P12 · anti-ai-writing
imprescindible | 2026-09-27 | P12 · anti-ai-writing
potenciar | 2026-09-27 | P12 · anti-ai-writing, semilla
fomentar | 2026-09-27 | P12 · anti-ai-writing, semilla
optimiz* | 2026-09-27 | P12 · anti-ai-writing, semilla
maximizar | 2026-09-27 | P12 · anti-ai-writing
holístico | 2026-09-27 | P12 · anti-ai-writing
multifacético | 2026-09-27 | P12 · anti-ai-writing
paradigma | 2026-09-27 | P12 · anti-ai-writing
sinergia | 2026-09-27 | P12 · anti-ai-writing
robusto | 2026-09-27 | P12 · anti-ai-writing
innovador | 2026-09-27 | P12 · anti-ai-writing
empoderar | 2026-09-27 | P12 · anti-ai-writing
brindar | 2026-09-27 | P12 · anti-ai-writing
subrayar | 2026-09-27 | P12 · anti-ai-writing
panorama | 2026-09-27 | P12 · anti-ai-writing
navegar | 2026-09-27 | P12 · anti-ai-writing
adentrarse en | 2026-09-27 | P12 · anti-ai-writing

### Verbos comodín y perífrasis

> Verbos y perífrasis que sustituyen a un verbo simple sin añadir
> información ("cuenta con" por "tiene", "el ámbito de" por el tema
> mismo). Son corrientes en español; solo pesan cuando se repiten.

impulsar | 2026-09-27 | P12 · semilla
aprovechar al máximo | 2026-09-27 | P12 · anti-ai-writing, semilla
aprovechar el poder de | 2026-09-27 | P12 · anti-ai-writing
se presenta como | 2026-09-27 | P18 · ADS
se consolida como | 2026-09-27 | P18 · ADS
recalcar | 2026-09-27 | P12 · humanamente
poner de relieve | 2026-09-27 | P12 · humanamente
el ámbito | 2026-09-27 | P12 · humanamente
el universo de | 2026-09-27 | P12 · humanamente
el reino de | 2026-09-27 | P12 · humanamente
un sinfín de | 2026-09-27 | P12 · humanamente
una miríada de | 2026-09-27 | P12 · humanamente
un abanico de | 2026-09-27 | P12 · humanamente
clave | 2026-09-27 | P13 · humanamente
vital | 2026-09-27 | P13 · humanamente
primordial | 2026-09-27 | P13 · humanamente
integral | 2026-09-27 | P12 · humanamente
sinérgico | 2026-09-27 | P12 · humanamente
disruptivo | 2026-09-27 | P12 · humanamente
vanguardista | 2026-09-27 | P12 · humanamente

### Calcos y construcciones importadas

> La norma que censuraría estas construcciones (DPD, Fundéu) está pendiente
> de comprobar en fuente primaria porque la descarga automática de esas
> fuentes está bloqueada. Mientras siga pendiente, ninguna de estas
> entradas autoriza una corrección automática ni se presenta como regla
> establecida: se señalan igual que el resto de entradas débiles, para que
> decida quien revisa. Según la auditoría, "en base a" es admisible
> aunque menos recomendable y "jugar un papel" no es incorrecto; esas
> lecturas del DPD también están pendientes de comprobar. Se listan por su
> frecuencia en texto calcado, no como error.

a nivel de | 2026-09-27 | P33 · semilla | pendiente
hacer sentido | 2026-09-27 | P33 · semilla | pendiente
en base a | 2026-09-27 | P34 · semilla | pendiente
de cara a | 2026-09-27 | P34 · semilla | pendiente
jugar un papel clave | 2026-09-27 | P34 · semilla | pendiente
jugar un rol clave | 2026-09-27 | P34 · semilla | pendiente
tomar lugar | 2026-09-27 | P36 · semilla | pendiente

## Excluidas y variantes

Estas palabras y variantes no se listan como entradas activas. No las lee
`scan_tells.py`; están aquí solo como nota para quien mantenga esta lista.

**Excluidas por falso positivo alto** (`docs/auditoria.md`, §3.1): desarrollar,
diversa, diversos, dinámico, enriquecer, estimular, excepcional, explorar,
fortalecer, integrar, interactuar, notable, permitirá, relevante, sólido,
transformar, aprovechemos. Son palabras demasiado corrientes en español para
servir de señal por sí solas, y varias ya quedan cubiertas indirectamente
por otros patrones: "excepcional" en una ficha de producto entra por
lenguaje de folleto (P16); "diversos estudios" sin cita, por autoridad
prestada (P17); "exploraremos" como anuncio de estructura, por metadiscurso
que anuncia (P49, en `patrones.md`).

**Locuciones prepositivas frecuentes en prosa peninsular** (P80, descartado,
`docs/auditoria.md`, §2): "en aras de", "de la mano de", "a la hora de", "en
pos de". Se descartaron del catálogo entero, no solo de este archivo: son
demasiado frecuentes en prosa humana española para funcionar como señal.

**Anglicismos y calcos admitidos sin censura localizada** (`docs/estudio.md`, §4.5):
"empoderar", "asumir" (en el sentido de "dar por sentado"), "impactar",
"remarcar", "evento", "sinergia". Ninguno se trata como calco-error en la
familia "Calcos y construcciones importadas"; la fuente primaria que los
admitiría sin reservas también está pendiente de comprobar, pero mientras
tanto no hay indicio de que estén censurados. "Empoderar" y "sinergia" sí
aparecen arriba, en "Vocabulario de registro IA", por un motivo distinto:
ahí no se juzga si son calcos, sino si se repiten como vocabulario típico
de texto generado.

**Variante ES-LatAm** (P64, `docs/auditoria.md`, §2; `docs/estudio.md`, §4.10):
"computadora" frente a "ordenador", y "ustedes" cuando convive en el mismo
texto con "vosotros" o con el tuteo de confianza. Nunca se cambian ni se
tratan como error: solo se avisa de la mezcla, y solo si el texto declara
o mantiene la variante española. "Ustedes" como plural formal, solo, en un
texto de España es correcto y no se señala.

**Patrones estructurales, no vocabulario**: el contraste "no solo… sino"
(P01), la tríada forzada y la acumulación de epítetos antepuestos (P06,
P41), los conectores apilados (P37) y el gerundio de posterioridad (P15)
dependen de la construcción de la frase, no de una expresión fija. Se
documentan en `references/patrones.md` y los detecta el motor de
expresiones regulares de `scripts/scan_tells.py`, no esta lista.
