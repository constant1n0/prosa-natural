# Capa de discurso

Patrones de estructura y organización del texto, por encima de la frase
suelta. El modelo lee este archivo en textos de más de un párrafo, o
cuando tiene que revisar cómo se organiza el texto completo, no una frase
concreta; en un texto de una sola frase o de un párrafo corto no hace
falta abrirlo. Las dos secciones siguientes, puertas de registro y bandas
de longitud, deciden cuánto de esta capa se aplica en cada caso: en varios
registros no se aplica nada, y en textos muy cortos tampoco. Las reglas
duras del proyecto (cero invención, claims protegidos, intocables
técnicos) tienen prioridad sobre cualquier patrón de este archivo, igual
que en [`patrones.md`](patrones.md).

## Puertas de registro

En texto legal, de cumplimiento normativo, procedimental o técnico, esta
capa no se aplica: esos géneros solo reciben la capa de superficie
(`patrones.md`, `vocabulario-es.md` y los detectores de forma y
tipografía de `scan_tells.py`).

El motivo no es que estos textos estén exentos de revisión, sino que lo
que en un post o una ficha sería un rasgo generado es, en estos cuatro
registros, la propia especificación del género: la explicitud, el cierre
de cada punto y la lógica de un solo hilo argumental son lo que ese texto
tiene que tener, no una señal de texto generado por IA (docs/auditoria.md
§2.2; docs/estudio.md §6, fila "Discurso desactivado por registro"). Un
contrato no debe dejar nada implícito; un procedimiento no debe abrir
hilos que no cierra; una ficha técnica no necesita una apertura de
ambiente. Aplicar aquí los patrones de discurso penalizaría justo la
claridad que el género exige.

Esta puerta ya está en la práctica dentro de `patrones.md`: P38
(enumeración mecánica) es legítima en procedimientos y textos jurídicos
precisamente por esta misma puerta de registro, y no se marca ahí.

## Bandas de longitud

anti-ai-writing fija cuatro bandas por número de palabras: menos de 40,
entre 40 y 200, entre 200 y 800, y más de 800 (docs/estudio.md §6, fila
"Bandas de longitud"; docs/auditoria.md §2.2, misma fila).

- **Menos de 40 palabras:** esta capa no se aplica. Por debajo de ese
  umbral no hay párrafos suficientes para que exista una moraleja, una
  apertura de ambiente o una plantilla de exposición, y ni anti-ai-writing
  ni Aboudjem encuentran una señal fiable a esa longitud (docs/estudio.md
  §6, misma fila).
- **40 palabras o más (40-200, 200-800, más de 800):** se aplica la capa
  completa de este archivo. Las fuentes fijan estas tres bandas como los
  tramos que sí reciben la capa, pero no documentan ninguna diferencia
  adicional de qué patrón pesa más o menos dentro de ellas; no se inventa
  aquí esa graduación. StoryScope trabaja con relatos de una longitud
  media muy superior a estas bandas (unas 5000 palabras: 4753 de media en
  su corpus, 6403 en los relatos humanos) y su propio control de longitud
  solo compara tercios de ese mismo corpus, en un apéndice, sin medir el
  efecto de textos cortos (docs/auditoria.md §2.2, misma fila): sus cifras
  no fijan tampoco un umbral adicional dentro de estas bandas.

## Patrones de discurso

Los ejemplos de estos siete patrones son fragmentos abreviados de textos más
largos, recortados a una o dos frases para mostrar solo dónde aparece el
rasgo; ninguno es el texto completo. La banda de longitud de la sección
anterior se mide siempre sobre el texto completo que se está revisando,
nunca sobre el fragmento recortado del ejemplo: un ejemplo de una frase no
significa que el patrón se aplique a textos de una frase.

### P43 · Moraleja, resumen o epílogo

- **Fuerza:** Fuerte
- **Qué es:** Un último párrafo que explica qué "significaba" el texto, lo
  resume sin necesidad o se despide con una moraleja, sin ningún hecho
  nuevo.
- **Por qué es un rasgo:** No añade ningún dato: recapitula o moraliza
  sobre lo ya dicho. El arreglo alternativo "break the flatness" (añadir
  un detalle concreto al final para que el texto no suene tan cerrado) se
  descartó porque añade un dato que el original no da (docs/auditoria.md
  §2, patrón P43). StoryScope, sobre ficción en inglés, encuentra que el
  narrador comenta el tema del relato en el 77 % de los textos de IA
  frente al 52 % de los humanos; el propio estudio señala que el epílogo
  es solo huella de un modelo concreto (Claude), no un rasgo central. Se
  cita aquí solo con sus cautelas: es una diferencia agregada de
  frecuencia con mucho solapamiento (más de la mitad de los relatos
  humanos también comenta el tema), nunca una regla ni un umbral para un
  texto concreto, y la ficción queda fuera del alcance de esta primera
  versión de la skill (docs/estudio.md §3.4 y §3.9; docs/auditoria.md §5,
  fila sobre la excepción de ficción).
- **Cuándo no tocarlo:** Un resumen real de un documento largo, que
  recoge de verdad su contenido, es legítimo y no es este patrón. Se
  respeta también si el cierre reflexivo es la voz deliberada del autor.
- **Qué hacer:** Cortar el párrafo final si no aporta ningún hecho nuevo;
  nunca sustituirlo por un detalle concreto inventado para que suene menos
  cerrado.
- **Ejemplo:** «Ferretería Robledo repara herramientas desde 1990. En
  definitiva, cuidar las herramientas es cuidar el oficio.» → «Ferretería
  Robledo repara herramientas desde 1990.»
- **Escáner:** `vocabulario.hallazgos` cubre parcialmente la familia
  "Apertura y cierre suave" (débil) de
  [`vocabulario-es.md`](vocabulario-es.md): solo las fórmulas fijas ("en
  resumen,", "en definitiva,", "en conclusión", "en síntesis", "en última
  instancia", "como hemos visto"). El molde completo —un párrafo entero
  que recapitula o moraliza sin fórmula fija— no lo detecta: juicio del
  modelo.

### P44 · Apertura temporal o panorámica vacía

- **Fuerza:** Fuerte
- **Qué es:** Situar el texto en "el mundo actual", "el panorama actual" o
  "los últimos años" antes de entrar en el contenido, sin ningún dato
  concreto en esa apertura.
- **Por qué es un rasgo:** Ocupa la primera frase con una ambientación
  genérica que no dice nada del sujeto real del texto; cualquier tema
  admitiría la misma apertura sin cambiar una palabra.
- **Cuándo no tocarlo:** Si la apertura temporal va acompañada de un dato
  concreto ("en los últimos tres años, la plantilla se ha duplicado"), el
  dato hace que la frase ya no sea vacía y no es este patrón.
- **Qué hacer:** Cortar la apertura y empezar directamente por el
  contenido, sin perder ningún dato que la frase sí diera.
- **Ejemplo:** «En el panorama actual, cada vez más vecinos compran en
  Panadería Olmo por su cercanía.» → «Cada vez más vecinos compran en
  Panadería Olmo por su cercanía.»
- **Escáner:** `vocabulario.hallazgos` cubre la familia "Apertura temporal
  o panorámica vacía" (fuerte) de [`vocabulario-es.md`](vocabulario-es.md)
  ("en el mundo actual", "en el panorama actual", "en un mundo cada vez
  más", "en la era de", entre otras). Otras aperturas equivalentes que no
  estén en esa lista no las detecta: juicio del modelo.

### P45 · Apertura de ambiente o pregunta retórica

- **Fuerza:** Débil
- **Qué es:** Una escena ambientada (un lugar, un momento, una sensación)
  o una pregunta retórica antes de entrar en el contenido real.
- **Por qué es un rasgo:** Retrasa el contenido con un recurso narrativo
  que no aporta ningún hecho, imitando la apertura de un artículo de
  revista o un listículo antes de decir lo que el texto realmente afirma.
- **Cuándo no tocarlo:** Solo cuenta en acumulación con otros rasgos; si
  la pregunta retórica es la voz deliberada del autor o el género admite
  ese arranque (una columna de opinión, por ejemplo), no se toca.
- **Qué hacer:** Cortar la escena o la pregunta y empezar por el
  contenido, conservando el hecho que la frase siguiente ya daba.
- **Ejemplo:** «¿Alguna vez te has preguntado por qué el pan de ayer sabe
  distinto? En Panadería Olmo dejamos fermentar la masa toda la noche.» →
  «En Panadería Olmo dejamos fermentar la masa toda la noche.»
- **Escáner:** no lo detecta: juicio del modelo.

### P46 · Contexto ya conocido

- **Fuerza:** Débil
- **Qué es:** Reexplicar al lector una historia, una decisión o una
  relación que ya comparte de verdad con quien escribe.
- **Por qué es un rasgo:** Es propio de un texto genérico dirigido a nadie
  en particular: reintroduce un contexto que un destinatario real y
  concreto ya conoce, como si el texto no supiera a quién se dirige.
- **Cuándo no tocarlo:** En un correo o un mensaje a una persona real que
  de verdad comparte ese contexto ("como ya sabes, quedamos el jueves"),
  la fórmula es legítima y no es este patrón.
- **Qué hacer:** Cortar la reexplicación cuando el texto no tiene un
  destinatario real que ya conozca ese contexto, sin sustituirla por
  contenido nuevo.
- **Ejemplo:** en una entrada de blog, sin destinatario real: «Como ya
  sabes, decidimos ampliar el horario de Ferretería Robledo el mes
  pasado. Ahora abrimos también los sábados por la tarde.» → «Ferretería
  Robledo amplió su horario el mes pasado: ahora también abre los sábados
  por la tarde.»
- **Escáner:** no lo detecta: juicio del modelo (saber si el destinatario
  es real y comparte ese contexto es un dato que el script no tiene).

### P47 · Párrafos sin relación

- **Fuerza:** Débil
- **Qué es:** Párrafos intercambiables entre sí, que no preparan el
  siguiente ni dependen del anterior: se podrían reordenar sin que nada
  del texto dejara de tener sentido.
- **Por qué es un rasgo:** Un texto con progresión real necesita leerse en
  orden; la ausencia de esa progresión es la señal, no la longitud ni el
  número de párrafos.
- **Cuándo no tocarlo:** Se nombra una relación entre párrafos solo si el
  propio original ya la da en algún punto (aunque esté en otro lugar del
  texto); si el original no relaciona los párrafos en ningún sitio, no se
  inventa una relación nueva para "arreglarlo".
- **Qué hacer:** Señalar la falta de progresión; si el original ya
  relaciona esos datos en otra parte, recuperar esa relación al fusionar o
  reordenar; si no la da en ningún sitio, dejar los párrafos como una
  sucesión de datos y limitarse a señalarlo.
- **Ejemplo:** «Panadería Olmo abre de martes a domingo. El horno es de
  leña. La sala tiene mesas para tomar café.» Estos tres datos son
  intercambiables: ningún párrafo prepara el siguiente. Si el original no
  los relaciona en ningún otro punto, se dejan tal cual y solo se señala
  la falta de progresión, sin unirlos con un conector que sugiera una
  relación que el texto no da.
- **Escáner:** no lo detecta: juicio del modelo.

### P48 · Plantilla de exposición

- **Fuerza:** Débil
- **Qué es:** Aplicar siempre el mismo armazón —qué es, por qué importa,
  qué tipos hay, conclusión— sea cual sea el tema real del texto.
- **Por qué es un rasgo:** Impone una estructura fija en lugar de una que
  responda al contenido concreto; es reconocible porque se repite igual
  con cualquier tema, divulgativo o no.
- **Cuándo no tocarlo:** En un documento de referencia realmente largo que
  sí necesita ese desglose para que se pueda consultar por partes, la
  estructura es legítima y no se fuerza a prosa corrida.
- **Qué hacer:** Fuera de un documento de referencia largo, fusionar el
  armazón en prosa corrida que siga lo que el contenido necesita, sin
  perder ningún dato ni forzar la fusión cuando el documento sí necesita
  esa estructura.
- **Ejemplo:** en un post breve, no en un documento de referencia: «##
  ¿Qué es el pan de masa madre? Es un pan fermentado con masa madre
  natural. ## Tipos Panadería Olmo elabora dos: de trigo y de centeno. ##
  Conclusión En definitiva, cada cliente elige el que prefiere.» → «El pan
  de masa madre de Panadería Olmo se fermenta con masa madre natural; hay
  de trigo y de centeno.»
- **Escáner:** no aplica un veredicto directo; los datos brutos de
  `encabezados.resumen` (total de encabezados, vacíos, saltos de nivel)
  pueden apoyar el juicio, pero decidir si la estructura es una plantilla
  forzada para ese contenido concreto es del modelo.

### P50 · Emoción contada en el cuerpo

- **Fuerza:** Débil
- **Qué es:** Contar una emoción como una sensación física del cuerpo (un
  nudo en el estómago, un peso en el pecho) en lugar de nombrarla o
  dejarla implícita.
- **Por qué es un rasgo:** Es el modo predominante de expresar emoción en
  la ficción de IA estudiada por StoryScope (81 % de los relatos frente al
  38 % de los humanos, con las mismas cautelas de agregación y solapamiento
  que P43; docs/estudio.md §3.4). No es lo mismo que "nombrar la emoción",
  que es justo lo contrario: los humanos etiquetan la emoción de forma
  explícita más, no menos, que los textos de IA (29 % frente a 8 %), así
  que exigir nombrarla sería reintroducir un rasgo distinto y descartado
  (docs/auditoria.md §2, patrón P75).
- **Cuándo no tocarlo:** Solo se aplica en textos personales (un diario,
  una carta, un relato en primera persona sobre algo vivido); fuera de un
  texto personal, este patrón no se marca. Se conserva también si es la
  voz deliberada del autor.
- **Qué hacer:** Solo se señala, nunca se reescribe ni se sustituye la
  sensación por el nombre de una emoción concreta: decidir qué emoción es
  en realidad sería una interpretación que el texto original no da.
- **Ejemplo:** en una entrada personal de diario: «Se me hizo un nudo en
  el estómago al leer el correo del despido.» En un texto personal, la
  skill señala que la emoción se cuenta como sensación física, sin
  proponer qué emoción es ni reescribir la frase: nombrarla ("sentí
  miedo", "sentí rabia") sería una interpretación que el original no da.
- **Escáner:** no lo detecta: juicio del modelo.

## Fuera de alcance

La ficción queda fuera del alcance de esta primera versión de la skill.
Varios de los hallazgos de StoryScope citados arriba (moraleja explícita,
emoción como sensación física, hilo narrativo único, resolución por
decisión del protagonista, señales humanas a restaurar) son propios de
relatos de ficción en inglés y se citan aquí solo como respaldo de la
fuerza de P43 y P50; no se traducen a nuevas reglas de discurso para
ficción en español en esta fase (docs/auditoria.md §5, fila sobre la
excepción de ficción de blader; docs/estudio.md §3.9).
