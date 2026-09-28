# Patrones de escritura generada

Catálogo de patrones estructurales y de contenido que delatan un texto
generado, con su motivo, su salvaguarda y un ejemplo propio. El modelo lee
este archivo cuando `SKILL.md` lo remite aquí: siempre que tenga que juzgar
o corregir un párrafo, para decidir si un giro concreto es un rasgo o una
forma corriente del español, y qué hacer si lo es.

## Orden de precedencia

Ante cualquier conflicto entre lo que dice una entrada de este archivo y
otra fuente, el orden es (`docs/auditoria.md`, §1):

1. Las reglas duras del proyecto: cero invención, claims protegidos e
   intocables técnicos. Ningún patrón de este archivo se aplica dentro de
   una frase con un claim o un intocable técnico (INCI, marca, precio,
   código, URL, cita textual): esas frases se dejan literales, pase lo que
   pase con el patrón.
2. La norma lingüística vigente, con su edición y fecha.
3. La evidencia empírica.
4. La convergencia de varias fuentes independientes.
5. El criterio propio, solo cuando ninguna de las anteriores decide.

Cuando una entrada cita una norma (DPD, NGLE, Fundéu) cuya verificación en
fuente primaria sigue pendiente, lo dice explícitamente. Mientras siga
pendiente, esa norma no autoriza tratar la entrada como una regla
establecida ni corregirla de forma automática: se señala igual que
cualquier otra entrada, para que decida quien revisa.

## Señales fuertes y débiles

Cada patrón lleva una fuerza:

- **Fuerte**: una sola aparición ya justifica editar, porque no tiene un uso
  corriente legítimo fuera del contexto que delata.
- **Media**: una fuente normativa la admite en unos casos y la censura o
  desaconseja en otros. La skill señala el caso y propone una alternativa,
  pero no lo trata como error ni lo corrige de forma automática; decide
  siempre quien revisa.
- **Débil**: es una construcción que también aparece en prosa humana
  corriente. Sola no significa nada; solo pesa por acumulación, cuando se
  repite varias veces en el mismo texto o convive con otras señales.

## Esto no es un tribunal

Cada entrada explica el motivo del patrón, no una orden a cumplir sin
matices. Si el autor conoce la regla y decide mantener su redacción
original, esa decisión se acepta: la skill señala y explica, no impone
(`docs/auditoria.md`, §2.2).

## Los arreglos solo cortan, fusionan o reordenan

Ningún arreglo de este archivo añade una cifra, un nombre, una fecha o una
cita que no esté ya en el original. Si la frase mejoraría con un dato
concreto que el original no da, el arreglo es preguntar al autor ese dato,
nunca inventarlo. Este archivo tampoco es un evasor de detectores: ningún
arreglo inserta una muletilla, un error deliberado o un "toque humano" para
parecer menos generado; el objetivo es siempre la calidad del texto.

## Índice de familias

1. [Contenido](#contenido)
2. [Sintaxis y construcción](#sintaxis-y-construcción)
3. [Formato y tipografía](#formato-y-tipografía)
4. [Comunicación con el lector](#comunicación-con-el-lector)
5. [Patrones descartados](#patrones-descartados)

## Contenido

### P02 · Cierre de una línea y fragmentos

- **Fuerza:** Fuerte
- **Qué es:** Una frase final que repite lo ya dicho, un fragmento suelto o
  el mismo cierre repetido tras cada sección.
- **Por qué es un rasgo:** No añade ningún hecho nuevo: es un cierre
  retórico que imita el ritmo de una diapositiva o un titular sin aportar
  contenido distinto del resto del párrafo.
- **Cuándo no tocarlo:** Una frase corta vale si aporta un hecho nuevo que
  el resto del párrafo no daba.
- **Qué hacer:** Cortar el fragmento vacío o fusionarlo con la frase
  anterior si no añade nada; nunca sustituirlo por un cierre distinto
  inventado.
- **Ejemplo:** «Ferretería Robledo lleva treinta años en el mismo local.
  Treinta años atendiendo al barrio. Así de sencillo.» → «Ferretería
  Robledo lleva treinta años en el mismo local, atendiendo al barrio.»
- **Escáner:** no lo detecta: juicio del modelo.

### P03 · Sentencia que suena profunda

- **Fuerza:** Fuerte
- **Qué es:** Un aforismo o una metáfora en lugar del enunciado concreto que
  el original afirma.
- **Por qué es un rasgo:** Sustituye un hecho o una afirmación concreta por
  una frase reflexiva grandilocuente que no añade contenido nuevo.
- **Cuándo no tocarlo:** Si el registro reflexivo es la voz deliberada del
  autor, o si la sentencia añade un matiz real que el original confirma, no
  se toca.
- **Qué hacer:** Cortar la sentencia o decir directamente lo que el
  original afirma; nunca reinterpretar ni añadir contenido.
- **Ejemplo:** «Panadería Olmo hornea el pan a las seis de la mañana. En el
  fondo, hacer pan es escuchar al barrio.» → «Panadería Olmo hornea el pan a
  las seis de la mañana.»
- **Escáner:** `vocabulario.hallazgos` detecta las expresiones fijas de la
  familia "Sentencia que suena profunda" (débil) de
  [`vocabulario-es.md`](vocabulario-es.md); el molde retórico completo no
  lo detecta — juicio del modelo.

### P05 · Discutir con nadie

- **Fuerza:** Fuerte
- **Qué es:** Refutar una objeción que nadie ha planteado, para simular un
  debate donde no lo hay.
- **Por qué es un rasgo:** La objeción "refutada" es una fabricación: el
  contenido que la introduce no está en el original ni responde a nada que
  el lector haya dicho.
- **Cuándo no tocarlo:** Se conservan las objeciones atribuidas a alguien
  real o respondidas de verdad en el original.
- **Qué hacer:** Cortar la objeción inventada y dejar la afirmación
  directa.
- **Ejemplo:** «No digo que el horno de leña esté pasado de moda, pero en
  Panadería Olmo seguimos usándolo cada día.» → «En Panadería Olmo seguimos
  usando el horno de leña cada día.»
- **Escáner:** no lo detecta: juicio del modelo.

### P13 · Significado inflado

- **Fuerza:** Fuerte
- **Qué es:** Atribuir trascendencia o legado a un hecho corriente.
- **Por qué es un rasgo:** Infla un hecho neutro con vocabulario de hito
  histórico sin ningún dato que lo sustente.
- **Cuándo no tocarlo:** Si el original de verdad reporta un hito objetivo
  con un dato concreto detrás (un premio, un aniversario documentado), ese
  hecho se conserva; solo se retira la grandilocuencia añadida. Si la
  inflación forma parte de una alegación de eficacia, salud o seguridad, es
  un claim: se deja literal y se señala en `claims.md`, nunca se corrige
  aquí.
- **Qué hacer:** Cortar la frase de trascendencia y terminar en el último
  hecho concreto que dé el original.
- **Ejemplo:** «La apertura de la segunda tienda de Arcilla marca un hito
  en la vida del barrio.» → «Arcilla abre su segunda tienda.»
- **Escáner:** `vocabulario.hallazgos` cubre las familias "Significado
  inflado: colocaciones calcadas" (fuerte) y "Significado inflado y
  modificadores huecos" (débil) de [`vocabulario-es.md`](vocabulario-es.md).

### P14 · Relación vaga

- **Fuerza:** Débil
- **Qué es:** "Vinculado a", "asociado a" donde el original tiene un dato
  concreto sobre la relación, o donde no lo tiene.
- **Por qué es un rasgo:** Sustituye una relación concreta y comprobable
  por una vaguedad que suena a dato sin serlo.
- **Cuándo no tocarlo:** "Vinculado a" es una expresión corriente en
  español y legítima cuando el original no da más detalle o cuando la
  vaguedad es justo lo que el autor quiere comunicar. Nunca se inventa la
  relación exacta si el original no la da.
- **Qué hacer:** Si el dato concreto ya está en otra parte del texto,
  fusionarlo aquí; si no está, dejar la vaguedad o preguntar al autor, sin
  inventar la relación.
- **Ejemplo:** «La marca está vinculada al mundo del ciclismo. Patrocina la
  vuelta local desde 2019.» → «La marca patrocina la vuelta local desde
  2019.»
- **Escáner:** no lo detecta: juicio del modelo.

### P16 · Lenguaje de folleto

- **Fuerza:** Fuerte
- **Qué es:** Fórmulas promocionales de folleto turístico o comercial en
  lugar de decir qué es la cosa.
- **Por qué es un rasgo:** Sustituye la descripción factual por
  adjetivación calcada de marketing; es frecuente en fichas de producto,
  donde a menudo coincide con un claim.
- **Cuándo no tocarlo:** "Decir qué es la cosa" solo se aplica fuera de una
  frase con claim. Si la fórmula forma parte de una alegación protegida, se
  deja literal y se señala en `claims.md`, nunca se reformula.
- **Qué hacer:** Sustituir la fórmula de folleto por lo que la cosa
  realmente es, usando solo los datos que ya da el original.
- **Ejemplo:** «Enclavado en pleno corazón del casco antiguo, el Hostal
  Lumbre presume de unas vistas de ensueño.» → «El Hostal Lumbre está en el
  casco antiguo y tiene vistas.»
- **Escáner:** `vocabulario.hallazgos` cubre la familia "Lenguaje de
  folleto" (débil) de [`vocabulario-es.md`](vocabulario-es.md).

### P17 · Autoridad prestada y atribución vaga

- **Fuerza:** Fuerte
- **Qué es:** Citar "los expertos" o "estudios" sin nombrar la fuente, o
  generalizar a partir de una sola fuente.
- **Por qué es un rasgo:** Presenta como autoridad general algo sin
  verificar. Dentro de una alegación de eficacia, salud o seguridad es
  además un claim regulado (Reglamento 655/2013): "clínicamente probado" o
  "según estudios" dentro de un claim son claim, no vocabulario, y no se
  cortan ni se reformulan nunca — ver [`claims.md`](claims.md).
- **Cuándo no tocarlo:** Fuera de un claim, una cita ausente no es por sí
  sola un rasgo que haya que "restaurar" inventando una fuente; como mucho
  se pregunta al autor cuál era la fuente real.
- **Qué hacer:** Fuera de un claim, preguntar la fuente real o mantener lo
  vago si el original no la da. Dentro de un claim, dejar la frase literal
  y marcarla; nunca reformularla.
- **Ejemplo:** «Los expertos coinciden en que el pan de masa madre es más
  digestivo.» → pregunta al autor: «¿qué fuente da el original para "los
  expertos"? Sin ella, la frase se deja como está.»
- **Escáner:** `candidatos_claim` marca la frase como candidata solo si
  incluye además un marcador de estudios o eficacia; fuera de eso, no lo
  detecta — juicio del modelo.

### P23 · Límite de conocimiento y conjeturas

- **Fuerza:** Fuerte
- **Qué es:** Fórmulas de fecha de corte de un modelo ("hasta donde alcanza
  mi información"), o presentar una suposición como si fuera un hecho.
- **Por qué es un rasgo:** Refuerza la regla de cero invención: presentar
  una conjetura como hecho verificado es justo lo que esa regla prohíbe, y
  la fórmula de fecha de corte delata además que el texto no pasó por una
  revisión de voz propia.
- **Cuándo no tocarlo:** No hay uso legítimo de la fórmula de fecha de
  corte fuera de un chatbot hablando en primera persona; es señal fuerte
  sin excepción.
- **Qué hacer:** Cortar la fórmula de fecha de corte; si la conjetura es
  necesaria, dejarla con la duda propia del autor humano ("probablemente",
  "creo que") en vez de presentarla como hecho, o preguntar el dato real.
- **Ejemplo:** «Hasta donde alcanza mi información, el Museo Robledo
  probablemente cierra los lunes.» → «El Museo Robledo probablemente
  cierra los lunes.»
- **Escáner:** `vocabulario.hallazgos` cubre la familia "Límite de
  conocimiento y conjeturas" (fuerte) de
  [`vocabulario-es.md`](vocabulario-es.md).

### P25 · Escribir sobre la versión anterior

- **Fuerza:** Débil
- **Qué es:** Describir lo sustituido fuera de un registro de cambios.
- **Por qué es un rasgo:** Mezcla información sobre el propio proceso de
  edición con el contenido, propio de un asistente que explica su cambio,
  no de un texto final.
- **Cuándo no tocarlo:** Es legítimo en registros de cambios (changelog) y
  en ayuda de producto que explica qué cambió; poco frecuente y por tanto
  más señal en fichas de producto o posts.
- **Qué hacer:** Cortar la comparación con la versión anterior si el género
  del texto no es un registro de cambios; dejarla si lo es.
- **Ejemplo:** en la ayuda de una web, no en un registro de cambios: «Antes
  el formulario de contacto pedía el DNI; ahora ya no lo pide.» → «El
  formulario de contacto ya no pide el DNI.»
- **Escáner:** no lo detecta: juicio del modelo.

### P26 · Frase portátil

- **Fuerza:** Débil
- **Qué es:** Una frase que podría pasar sin cambios a cualquier otra marca
  o persona.
- **Por qué es un rasgo:** No aporta ningún dato específico del sujeto del
  texto: si al cambiar el nombre de la marca la frase sigue siendo
  igual de cierta, no dice nada propio de ella.
- **Cuándo no tocarlo:** El arreglo necesita un dato del autor que el
  original no da; ese dato nunca se inventa.
- **Qué hacer:** Preguntar al autor un dato concreto que distinga la frase,
  o cortarla si no hay dato disponible.
- **Ejemplo:** «En Panadería Olmo trabajamos cada día para ofrecerte la
  mejor calidad.» → pregunta al autor: «¿qué hace distinta a Panadería
  Olmo? Sin un dato concreto, esta frase se corta.»
- **Escáner:** no lo detecta: juicio del modelo.

### P27 · Promesa de revelación

- **Fuerza:** Fuerte
- **Qué es:** Anunciar un secreto antes de decir algo corriente, o
  presentar lo ya sabido como un hallazgo.
- **Por qué es un rasgo:** Crea la expectativa de una revelación que
  después no llega: el contenido que sigue es información ordinaria, no un
  secreto.
- **Cuándo no tocarlo:** Si el original de verdad entrega un dato poco
  conocido, la fórmula de apertura puede quedarse si coincide con la voz
  del autor; el rasgo es la promesa vacía, no la existencia de una fórmula
  de apertura.
- **Qué hacer:** Cortar el anuncio y dejar solo el contenido que el
  original entrega.
- **Ejemplo:** «Lo que nadie te cuenta sobre regar las plantas en verano:
  hazlo al anochecer.» → «Riega las plantas al anochecer en verano.»
- **Escáner:** `vocabulario.hallazgos` cubre la familia "Promesa de
  revelación" (fuerte) de [`vocabulario-es.md`](vocabulario-es.md); otras
  fórmulas equivalentes que no estén en esa lista no las detecta — juicio
  del modelo.

### P28 · Declarativa vaga

- **Fuerza:** Débil
- **Qué es:** Afirmar una magnitud o una importancia sin contenido que la
  sustente.
- **Por qué es un rasgo:** "Las consecuencias son enormes" no dice nada
  verificable: infla sin aportar la magnitud real.
- **Cuándo no tocarlo:** Nunca se corrige inventando la magnitud que falta.
- **Qué hacer:** Cortar la declarativa vacía, o preguntar al autor la
  magnitud real.
- **Ejemplo:** «El cierre de la fábrica tendrá consecuencias enormes para
  el pueblo.» → pregunta al autor: «¿qué consecuencia concreta tiene el
  cierre? Sin el dato, se corta la frase.»
- **Escáner:** no lo detecta: juicio del modelo.

### P29 · Agencia falsa

- **Fuerza:** Débil
- **Qué es:** Abstracciones con verbos de persona ("los datos nos dicen
  que…").
- **Por qué es un rasgo:** Atribuye acción o voluntad a una abstracción
  (los datos, el mercado, la tendencia) para sonar más autorial; en español
  es menos frecuente porque el idioma recurre más a la impersonal con "se".
- **Cuándo no tocarlo:** Solo cuenta en acumulación; una única aparición no
  es un rasgo por sí sola, y muchas expresiones de este tipo son normales
  en prosa analítica española.
- **Qué hacer:** Sustituir por una construcción impersonal con "se" o
  nombrar al sujeto real de la acción, sin añadir ningún dato nuevo.
- **Ejemplo:** «Los datos nos dicen que el cliente busca cercanía.» → «Se
  observa en los datos que el cliente busca cercanía.»
- **Escáner:** no lo detecta: juicio del modelo.

## Sintaxis y construcción

### P01 · Contraste "no X, sino Y"

- **Fuerza:** Fuerte
- **Qué es:** "No es X, es Y", "no solo X, sino también Y", "no se trata de
  X, se trata de Y", "más que X, Y", o el mismo contraste partido en dos
  frases.
- **Por qué es un rasgo:** Es una correlación correcta en español —el DPD
  (*sino*, 2.4) la valida con coma delante de "sino"— pero se repite como
  molde retórico automático incluso cuando la mitad negativa no corrige
  ninguna creencia real; se marca el molde, nunca la construcción en sí.
- **Cuándo no tocarlo:** Se conserva si corrige una creencia real que el
  lector podría tener, o si las dos mitades informan (cada una aporta un
  dato distinto). No se corrige partiendo el contraste en dos frases
  separadas ("No es X. Es Y."): eso reproduce el mismo rasgo con otra
  forma.
- **Qué hacer:** Si la mitad negativa no corrige ninguna creencia real,
  cortarla y decir directamente lo que afirma la mitad positiva.
- **Ejemplo:** «No es solo una crema: es un ritual diario para Marta.» →
  «Para Marta, la crema es un ritual diario.»
- **Escáner:** `estructuras.no_solo_sino`, `estructuras.no_se_trata_de`,
  `estructuras.no_es_es`.

### P06 · Tríada forzada

- **Fuerza:** Fuerte
- **Qué es:** Grupos de tres por costumbre —adjetivos, ejemplos, frases
  paralelas— sin que el contenido necesite tres elementos.
- **Por qué es un rasgo:** Es un molde retórico calcado del inglés de
  marketing; la anteposición de un solo epíteto es gramatical en español,
  pero la acumulación en grupos de tres sin necesidad de significado es el
  rasgo.
- **Cuándo no tocarlo:** Las listas reales (ingredientes, INCI, pasos de
  una receta, especificaciones técnicas) no cuentan aunque tengan tres
  elementos, porque ahí los tres son datos, no relleno retórico. Nunca se
  añade un cuarto elemento para "arreglar" una tríada: solo se quita o se
  fusiona.
- **Qué hacer:** Quitar el elemento sobrante o fusionar los tres si dicen
  lo mismo; nunca añadir un cuarto.
- **Ejemplo:** «Un espacio acogedor, moderno y funcional.» → «Un espacio
  acogedor y funcional.»
- **Escáner:** `estructuras.triadas_adjetivos` (siempre etiquetada
  "probable": un escáner determinista no puede confirmar la categoría
  gramatical).

### P07 · Arranques repetidos

- **Fuerza:** Débil
- **Qué es:** Frases seguidas con el mismo arranque, sobre todo el mismo
  sujeto explícito repetido.
- **Por qué es un rasgo:** El español omite el sujeto por defecto; el
  rasgo no es "empezar igual" en abstracto, sino el pronombre o sujeto
  explícito innecesario que se repite, o el mismo arranque literal frase
  tras frase, algo ajeno al uso corriente del idioma.
- **Cuándo no tocarlo:** Se respeta la anáfora deliberada (repetir el
  arranque a propósito, como recurso consciente del autor) y el sujeto
  explícito cuando desambigua a quién se refiere la frase.
- **Qué hacer:** Quitar el sujeto explícito redundante o variar el
  arranque de alguna frase, sin cambiar lo que cada una afirma.
- **Ejemplo:** «Este taller enseña a hacer pan. Este taller ofrece
  ingredientes ecológicos. Este taller cuenta con horno de leña.» → «Este
  taller enseña a hacer pan con ingredientes ecológicos y horno de leña.»
- **Escáner:** no lo detecta: juicio del modelo.

### P09 · Matices apilados

- **Fuerza:** Débil
- **Qué es:** Varias cautelas seguidas, matización en sube y baja
  ("podría, en cierta medida, ayudar potencialmente a…").
- **Por qué es un rasgo:** Acumula coberturas retóricas que diluyen la
  afirmación sin que ninguna aporte información nueva; cada matiz por
  separado puede ser legítimo, la acumulación es el rasgo.
- **Cuándo no tocarlo:** Nunca se quita un matiz dentro de una frase con
  claim ("ayuda a reducir"): cambiaría el alcance de la alegación. Se
  conservan también los avisos legales y de seguridad, aunque acumulen
  varias cautelas.
- **Qué hacer:** Quitar las cautelas redundantes y dejar una sola, la que
  el original necesite para no afirmar de más.
- **Ejemplo:** «Podría, en cierta medida, ayudar potencialmente a mejorar
  el ánimo.» → «Podría ayudar a mejorar el ánimo.»
- **Escáner:** no lo detecta: juicio del modelo.

### P11 · Pasiva perifrástica e impersonal de relleno

- **Fuerza:** Débil
- **Qué es:** "Fue + participio + por" sin necesidad real, o impersonales
  de relleno como "se hace necesario señalar", "se podría decir que".
- **Por qué es un rasgo:** En el español actual, la pasiva refleja es más
  frecuente que la perifrástica tanto en la lengua oral como en la escrita
  (NGLE, *la pasiva refleja (I)*, 41.11l); el tic real en castellano no es
  tanto la pasiva inglesa como el impersonal de relleno.
- **Cuándo no tocarlo:** La pasiva refleja ("se lanzó la campaña en
  marzo") nunca se marca, tenga o no complemento agente. En el registro
  jurídico y administrativo esto pesa más: aunque en general la refleja
  opone más resistencia a llevar un complemento agente, la NGLE señala que
  ahí "se aceptan a menudo en el código restrictivo del lenguaje jurídico"
  (NGLE, *la pasiva refleja (I)*, 41.11h). No hay fuente que respalde que
  en ese registro se prefiera además la perifrástica: se descarta esa
  lectura anterior.
- **Qué hacer:** Sustituir la perifrástica innecesaria por activa y cortar
  el impersonal de relleno, sin cambiar quién hace qué.
- **Ejemplo:** «La campaña fue lanzada por el equipo de Arcilla en marzo.»
  → «El equipo de Arcilla lanzó la campaña en marzo.»
- **Escáner:** no lo detecta: juicio del modelo.

### P15 · Gerundio ilativo o de posterioridad

- **Fuerza:** Media (posterioridad pura); Débil (consecuencia sin apoyo)
- **Qué es:** Un gerundio que expresa una mera sucesión temporal posterior
  al verbo principal, o uno que cuelga una interpretación sin apoyo en el
  original.
- **Por qué es un rasgo:** La NGLE considera hoy incorrecto el gerundio que
  introduce una mera sucesión temporal; el DPD matiza esa censura y lo da
  por "admisible cuando puede inferirse una sucesión o una relación
  lógicas" (DPD, *gerundio*, 5; `docs/auditoria.md` §7.5). Por eso la skill
  señala el gerundio de posterioridad pura y propone una alternativa, pero
  no lo trata como error ni lo corrige sola: decide quien revisa. El
  gerundio de consecuencia es gramatical y solo se convierte en rasgo
  cuando cuelga una interpretación que el original no respalda; ahí sí se
  corrige, porque el problema no es la norma, sino que añade un dato que no
  está en el original.
- **Cuándo no tocarlo:** El gerundio de consecuencia inmediata o casi
  simultánea, con apoyo en el original, es correcto y no se toca. Tampoco
  se corrige de oficio la posterioridad pura: se señala y se propone una
  alternativa, y decide el autor si la aplica.
- **Qué hacer:** Ante la posterioridad pura, señalar el gerundio y proponer
  como alternativa separarlo en dos frases, sin aplicarla de forma
  automática. Ante una interpretación de consecuencia sin apoyo en el
  original, cortarla y dejar el hecho tal cual.
- **Ejemplo:** «El taller abrió en 2019, mudándose después a un local más
  grande.» — Gerundio de posterioridad pura: se señala y se propone la
  alternativa «El taller abrió en 2019. Después se mudó a un local más
  grande.», sin aplicarla de oficio.
- **Escáner:** no lo detecta: juicio del modelo (el escáner no analiza
  gramática; requiere criterio sobre si el gerundio expresa posterioridad
  o consecuencia).

### P18 · Evitar "ser" y "tener"

- **Fuerza:** Débil, salvo "se erige como" / "se posiciona como" (Fuerte)
- **Qué es:** Perífrasis que sustituyen sistemáticamente a "es" o "tiene"
  para sonar más corporativo.
- **Por qué es un rasgo:** Sustituye la cópula simple por una perífrasis
  calcada de un registro corporativo; "se erige como" y "se posiciona
  como" son señal fuerte por sí solas por ser colocaciones casi exclusivas
  de ese registro, mientras que "cuenta con" y "ofrece" son corrientes en
  español y solo pesan acumuladas.
- **Cuándo no tocarlo:** "Cuenta con" y "ofrece" no se tocan si aparecen
  una sola vez.
- **Qué hacer:** Sustituir por "es" o "tiene" cuando la perífrasis no
  añada matiz real; con "se erige/posiciona como" basta una aparición para
  simplificar.
- **Ejemplo:** «La biblioteca de Marta se erige como un punto de encuentro
  vecinal.» → «La biblioteca de Marta es un punto de encuentro vecinal.»
- **Escáner:** `vocabulario.hallazgos` cubre las familias "Evitar 'ser' y
  'tener': excepciones fuertes" y "Verbos comodín y perífrasis" de
  [`vocabulario-es.md`](vocabulario-es.md); "cuenta con"/"ofrece" sueltos
  no están en el vocabulario y no los detecta — juicio del modelo.

### P37 · Conectores apilados

- **Fuerza:** Débil
- **Qué es:** "Además", "asimismo", "por otro lado" abriendo párrafo tras
  párrafo.
- **Por qué es un rasgo:** Un conector suelto es normal ("un 'sin embargo'
  no es un tic"); el rasgo es la cadena de varios párrafos seguidos que
  empiezan todos por un conector.
- **Cuándo no tocarlo:** Un conector aislado al inicio de un párrafo nunca
  se marca; la coma tras el conector es norma y no se toca.
- **Qué hacer:** Variar el arranque de los párrafos de la cadena o
  fusionar alguno, sin cambiar lo que cada párrafo afirma.
- **Ejemplo:** «Además, el taller abre los sábados. Asimismo, ofrece
  clases para niños. Por otro lado, tiene aparcamiento gratuito.» → «El
  taller abre los sábados, ofrece clases para niños y tiene aparcamiento
  gratuito.»
- **Escáner:** `estructuras.conectores_parrafo`.

### P38 · Enumeración mecánica

- **Fuerza:** Débil
- **Qué es:** "En primer lugar… en segundo lugar… por último" fuera de un
  procedimiento.
- **Por qué es un rasgo:** Convierte cualquier lista de ideas en una
  secuencia numerada aunque el contenido no sea un procedimiento, imitando
  la estructura de una guía paso a paso sin que el género lo pida.
- **Cuándo no tocarlo:** Legítima en procedimientos y textos jurídicos
  (puerta de registro): si el texto es de verdad una lista de pasos a
  seguir en orden, la enumeración no es un rasgo.
- **Qué hacer:** Fuera de un procedimiento, sustituir por prosa corrida o
  por una lista sin la fórmula numerada, sin perder ningún elemento.
- **Ejemplo:** en un post de blog, no en un procedimiento: «En primer
  lugar, el pan reposa doce horas. En segundo lugar, se hornea a fuego
  lento. Por último, se deja enfriar.» → «El pan reposa doce horas, se
  hornea a fuego lento y se deja enfriar.»
- **Escáner:** `estructuras.enumeracion_mecanica`.

### P39 · Simetría cautelosa

- **Fuerza:** Débil
- **Qué es:** Plantillas que se dirigen a todos los lectores a la vez
  ("tanto si eres principiante como si llevas años cocinando…", "ya
  seas… o…").
- **Por qué es un rasgo:** Es una fórmula que evita comprometerse con un
  lector concreto, cubriendo todos los casos a la vez sin aportar ningún
  dato específico.
- **Cuándo no tocarlo:** Se conserva si nombra una bifurcación real que el
  original necesita distinguir (dos procedimientos distintos según el caso
  del lector), no una simetría vacía.
- **Qué hacer:** Cortar la fórmula y dirigirse directamente al contenido,
  o mantenerla solo si distingue una bifurcación real.
- **Ejemplo:** «Tanto si eres principiante como si llevas años cocinando,
  esta receta de pan de Panadería Olmo lleva solo tres ingredientes.» →
  «Esta receta de pan de Panadería Olmo lleva solo tres ingredientes.»
- **Escáner:** `estructuras.tanto_si_como_si`, `estructuras.ya_seas_o`.

### P40 · Revelación tras dos puntos

- **Fuerza:** Débil
- **Qué es:** Una pausa dramática con dos puntos antes de una respuesta
  breve ("La clave: la constancia.").
- **Por qué es un rasgo:** Imita el ritmo de una diapositiva o un titular,
  deteniendo la frase para dar efecto a una palabra que podría decirse sin
  la pausa forzada.
- **Cuándo no tocarlo:** Solo cuenta si se repite varias veces en el mismo
  texto; una sola aparición no es rasgo.
- **Qué hacer:** Fusionar en una frase corrida cuando se acumule, sin
  perder la palabra revelada.
- **Ejemplo:** «La clave: la constancia. El secreto: no rendirse. La
  fórmula: practicar cada día.» → «La clave está en la constancia, en no
  rendirse y en practicar cada día.»
- **Escáner:** no lo detecta directamente: el escáner no distingue una
  revelación retórica de un uso normativo de los dos puntos — juicio del
  modelo.

### P41 · Acumulación de epítetos

- **Fuerza:** Débil
- **Qué es:** Un epíteto antepuesto más adjetivos pospuestos en serie ("un
  exquisito aroma intenso, envolvente y sofisticado").
- **Por qué es un rasgo:** La anteposición de un epíteto es un rasgo
  gramatical normal en español: la Gramática básica dice que el epíteto
  "admite con mayor facilidad la anteposición" (Gramática básica, 7.4.1), y
  la NGLE explica que "el adjetivo antepuesto se convirtió pronto en un
  rasgo característico de la lengua literaria" (NGLE, *posición del
  adjetivo*, 13.13b); el rasgo no es anteponer un adjetivo, sino acumular
  varios hasta saturar el sustantivo.
- **Cuándo no tocarlo:** Nunca se marca un solo epíteto antepuesto; solo la
  acumulación de varios adjetivos alrededor del mismo sustantivo.
- **Qué hacer:** Quitar los adjetivos que no añadan información distinta,
  dejando como mucho uno o dos.
- **Ejemplo:** «Un exquisito aroma intenso, envolvente y sofisticado.» →
  «Un aroma intenso.»
- **Escáner:** `estructuras.triadas_adjetivos` cubre parcialmente la tríada
  pospuesta (siempre "probable"); el epíteto antepuesto en sí no lo
  detecta — juicio del modelo.

### P42 · Aposición explicativa de manual

- **Fuerza:** Débil
- **Qué es:** Una aposición que explica al lector algo que ya sabe ("el
  turrón, ese dulce emblemático de nuestras Navidades, …").
- **Por qué es un rasgo:** Se detiene a aclarar algo obvio para el público
  al que se dirige el texto, como si necesitara la explicación; solo una
  fuente documenta este patrón, así que la fuerza es débil.
- **Cuándo no tocarlo:** Solo se marca si de verdad explica algo obvio
  para la audiencia declarada del texto; si el lector real puede no
  conocer el término (por ejemplo, un texto para público extranjero), la
  aposición es información legítima.
- **Qué hacer:** Cortar la aposición cuando sea redundante para la
  audiencia del texto.
- **Ejemplo:** «El turrón, ese dulce emblemático de nuestras Navidades, se
  vende ya en Ferretería Robledo.» → «El turrón se vende ya en Ferretería
  Robledo.»
- **Escáner:** no lo detecta: juicio del modelo.

## Formato y tipografía

### P08 · Raya a la inglesa

- **Fuerza:** Débil; fuerte si va espaciada por los dos lados sin aislar un
  inciso, pegada a las dos palabras que separa, o sustituye a los dos
  puntos en un encabezado.
- **Qué es:** Una raya (—) usada como calco del inglés: suelta entre
  espacios sin función de inciso, en vez de los dos puntos para anunciar
  una conclusión, o en vez del paréntesis para una sigla.
- **Por qué es un rasgo:** La Wikilengua recoge estos usos como «impropios
  de la raya…, la mayoría calcos del inglés»; en un encabezado, sustituir
  los dos puntos por una raya es además anglicismo de titulación, también
  según la Wikilengua (sin copia guardada, verificación pendiente).
- **Cuándo no tocarlo:** El diálogo, el inciso cerrado y el inciso del
  narrador cuya raya de cierre se omite legítimamente al terminar la frase
  o el párrafo («—Ya voy —dijo Marta.») son usos normativos del español,
  nunca este patrón; tampoco lo es el guion o la semirraya de un intervalo
  numérico ("1990-2000"), que es un carácter distinto. Se descartó prohibir
  la raya por completo ("cero rayas en la versión final"): manda la
  muestra de voz del autor, si existe.
- **Qué hacer:** Cerrar la raya si de verdad aísla un inciso y le falta el
  cierre, sustituirla por los dos puntos o el paréntesis si hacía esa
  función, o quitarla si no cumple ninguna; nunca prohibirla en bloque.
- **Ejemplo:** «Dos años de pruebas — ese fue el precio de Ferretería
  Robledo.» → «Dos años de pruebas: ese fue el precio de Ferretería
  Robledo.»
- **Escáner:** `rayas.hallazgos` clasifica cada raya en `dialogo`,
  `inciso_cerrado`, `inciso_sin_cierre`, `raya_inglesa` o `en_encabezado`.
  Los tres primeros son uso normativo del español y nunca son este patrón;
  `raya_inglesa` sí lo es siempre, y `en_encabezado` marca cualquier raya
  dentro de un encabezado, sea cual sea su función, porque ahí calca a los
  dos puntos.

### P19 · Negrita decorativa

- **Fuerza:** Fuerte
- **Qué es:** Negrita sin ninguna función de localización: viñetas del
  tipo «- **Término:** explicación» repetidas como si fueran una
  plantilla.
- **Por qué es un rasgo:** El Libro de estilo reserva la negrita para
  localizar elementos (un término que se busca después, una referencia
  cruzada), no para decorar cada línea de una lista (verificación
  pendiente en fuente primaria, `docs/auditoria.md` §7.5).
- **Cuándo no tocarlo:** La negrita que de verdad marca algo que se va a
  localizar después (un término de un glosario, el nombre de un elemento
  de interfaz) es legítima; la negrita que ya viene del original como
  intocable técnico (código, frontmatter) tampoco se toca.
- **Qué hacer:** Quitar la negrita decorativa, dejando el texto tal cual;
  nunca añadir negrita nueva.
- **Ejemplo:** «- **Cercanía:** conocemos a cada cliente de Panadería
  Olmo. - **Calidad:** solo trabajamos con harina de proximidad.» →
  «Conocemos a cada cliente de Panadería Olmo y solo trabajamos con harina
  de proximidad.»
- **Escáner:** no lo detecta: juicio del modelo.

### P20 · Encabezados decorativos y Title Case

- **Fuerza:** Fuerte
- **Qué es:** Mayúscula inicial en cada palabra del encabezado (Title Case
  calcado del inglés), en vez de solo en la primera.
- **Por qué es un rasgo:** El Libro de estilo dice que "solo se escribe con
  mayúscula inicial la primera palabra de los elementos de titulación,
  además de aquellas que lo requieran por su naturaleza" (Libro de estilo,
  *elementos de titulación*); la Wikilengua, sin copia guardada, considera
  además anglicismo la mayúscula sistemática, incluso en nombres comunes.
- **Cuándo no tocarlo:** Se excluyen las marcas, los nombres propios, las
  siglas y los títulos de obra citados en su idioma original; esas
  palabras conservan su mayúscula aunque no sean la primera del
  encabezado.
- **Qué hacer:** Bajar a minúscula las palabras que no sean la primera ni
  una excepción; nunca tocar el contenido del encabezado.
- **Ejemplo:** «## Nuestra Historia Y Nuestros Valores En Ferretería
  Robledo» → «## Nuestra historia y nuestros valores en Ferretería
  Robledo»
- **Escáner:** `encabezados.hallazgos[].title_case.ratio` da la proporción
  de palabras con mayúscula no inicial sobre las palabras elegibles (se
  excluyen la primera palabra, las funcionales y las siglas en mayúscula);
  no aplica ningún corte. Limitación documentada en el propio script: no
  excluye nombres propios ni marcas, así que un encabezado con varias
  marcas en mayúscula puede dar una ratio alta sin ser este patrón — el
  modelo debe descartar esos casos al revisar cada hallazgo.

### P24 · Encabezado repetido en la primera frase

- **Fuerza:** Fuerte
- **Qué es:** La primera frase tras un encabezado se limita a repetir sus
  mismas palabras, sin añadir ningún hecho nuevo.
- **Por qué es un rasgo:** Es relleno puro: ocupa una frase entera sin
  decir nada que el propio encabezado no dijera ya.
- **Cuándo no tocarlo:** Si esa primera frase añade un dato que el
  encabezado no daba, no es este patrón, aunque repita alguna palabra.
- **Qué hacer:** Cortar la frase que solo repite el encabezado, o
  fusionarla con la frase siguiente que sí aporta el hecho.
- **Ejemplo:** «## Horarios» seguido de «Los horarios de Ferretería
  Robledo son muy importantes. Abre de martes a sábado.» → «## Horarios»
  seguido de «Ferretería Robledo abre de martes a sábado.»
- **Escáner:** `encabezados.hallazgos[].texto` da el texto de cada
  encabezado, pero comparar su contenido con el de la frase siguiente
  exige entender el significado — no lo detecta, juicio del modelo.

### P52 · Markdown fuera de contexto

- **Fuerza:** Fuerte
- **Qué es:** Asteriscos, almohadillas o guiones de lista en un canal que
  no interpreta Markdown, de modo que el lector ve los propios símbolos en
  vez del formato que debían producir.
- **Por qué es un rasgo:** Delata que el texto se generó pensando en un
  formato genérico de salida, sin adaptarlo al canal real donde se va a
  leer.
- **Cuándo no tocarlo:** Es decidible por el canal declarado: en un
  README, una entrada de blog o un chat que sí interpreta Markdown, la
  misma sintaxis es legítima.
- **Qué hacer:** Quitar la sintaxis de Markdown que el canal no va a
  interpretar, dejando la puntuación normal que corresponda; nunca añadir
  contenido nuevo al simplificar.
- **Ejemplo:** en un mensaje de WhatsApp (no interpreta Markdown):
  «**Oferta:** 2x1 en pan de Panadería Olmo, solo hoy.» → «Oferta: 2x1 en
  pan de Panadería Olmo, solo hoy.»
- **Escáner:** no lo detecta: depende del canal de publicación, un dato
  que el escáner no tiene — juicio del modelo.

### P53 · Estructura donde bastaba prosa

- **Fuerza:** Débil
- **Qué es:** Viñetas, tablas diminutas, encabezados vacíos o saltos de
  nivel para decir algo que una frase corrida diría igual de bien.
- **Por qué es un rasgo:** "La prosa es la opción por defecto"
  (anti-ai-writing): fragmentar en estructura un contenido que no la
  necesita imita una plantilla o una diapositiva, no la escritura natural.
- **Cuándo no tocarlo:** Las listas reales con varios elementos distintos
  (ingredientes, pasos, especificaciones) sí necesitan estructura y no son
  este patrón; los documentos de referencia largos pueden necesitar
  encabezados.
- **Qué hacer:** Fusionar la estructura en prosa corrida, conservando
  todos los hechos; nunca añadir una frase de conexión que invente algo no
  dado.
- **Ejemplo:** una tabla de dos filas — «Apertura: 9:00. Cierre: 14:00.» —
  seguida de «Estos son los horarios de Ferretería Robledo.» → «Ferretería
  Robledo abre de 9:00 a 14:00.»
- **Escáner:** no aplica un veredicto directo; los datos brutos de
  `encabezados.resumen` (total de encabezados, vacíos, saltos de nivel)
  pueden apoyar el juicio, pero decidir si sobra estructura es del modelo.

### P54 · Encabezado en pregunta

- **Fuerza:** Débil
- **Qué es:** Un título de sección formulado como pregunta («## ¿Por qué
  elegir nuestra academia?») fuera de un apartado real de preguntas
  frecuentes.
- **Por qué es un rasgo:** Imita el ritmo de una FAQ o un listicle de
  marketing aunque el texto no lo sea; repetirlo en todos los encabezados
  de un documento delata una plantilla, no una organización orgánica del
  contenido.
- **Cuándo no tocarlo:** Es legítimo en un apartado real de preguntas
  frecuentes.
- **Qué hacer:** Convertir el encabezado en una afirmación con las mismas
  palabras cuando el texto no sea una FAQ; dejarlo si lo es.
- **Ejemplo:** «## ¿Por qué elegir la Academia Arcilla?» (en una página de
  "quiénes somos", no en una FAQ) → «## Por qué elegir la Academia
  Arcilla»
- **Escáner:** `encabezados.hallazgos[].es_pregunta` marca cada encabezado
  que termina en "?"; no distingue si el texto es de verdad una FAQ —
  juicio del modelo.

### P55 · Comillas incoherentes

- **Fuerza:** Débil
- **Qué es:** Mezclar «», ""/“” y '' en el mismo nivel dentro del mismo
  texto, o anidarlas al revés de lo que marca la norma.
- **Por qué es un rasgo:** La Wikilengua es explícita: "No hay diferencia
  ortográfica alguna entre las comillas españolas y las inglesas […] es
  una elección esencialmente tipográfica" (sin copia guardada) — las
  curvas o las rectas por sí solas no prueban nada. El DPD y la Ortografía
  sí recomiendan las angulares en primer lugar en textos impresos, y esa
  lectura ya está comprobada en fuente primaria. Lo que delata falta de
  revisión es cambiar de tipo sin criterio dentro del mismo texto, o
  invertir el orden de anidamiento recomendado.
- **Cuándo no tocarlo:** Usar un solo tipo de comillas de forma constante
  en todo el texto es correcto, sea cual sea el tipo elegido; nunca se
  convierte de un tipo a otro sin que el autor lo confirme o sin una guía
  de estilo del proyecto que lo pida.
- **Qué hacer:** Señalar la mezcla o el anidamiento invertido; unificar al
  tipo predominante del propio texto solo si el autor lo confirma o hay
  guía de estilo, nunca por sistema.
- **Ejemplo:** con la guía de estilo del proyecto ya confirmada (comillas
  angulares): «La ficha de Arcilla destaca "calidad", "servicio" y
  «precio» en la misma frase.» → «La ficha de Arcilla destaca «calidad»,
  «servicio» y «precio» en la misma frase.»
- **Escáner:** `comillas.mezcla_de_tipos` y `comillas.anidamiento_invertido`.

### P56 · Signos de apertura omitidos

- **Fuerza:** Fuerte
- **Qué es:** Una interrogación o una exclamación sin su signo de apertura
  («Qué te ha parecido la nueva carta?» en vez de «¿Qué te ha parecido la
  nueva carta?»).
- **Por qué es un rasgo:** Los signos de apertura "son característicos del
  español y no deben suprimirse por imitación de otras lenguas" (DPD,
  *signos de interrogación y exclamación*, 2.1); el estudio del proyecto lo
  trata como error objetivo.
- **Cuándo no tocarlo:** No hay excepción legítima: la omisión es siempre
  un calco, nunca una elección de estilo.
- **Qué hacer:** Añadir el signo de apertura que falta, sin cambiar
  ninguna otra palabra.
- **Ejemplo:** «Qué te ha parecido la nueva carta de Panadería Olmo?» →
  «¿Qué te ha parecido la nueva carta de Panadería Olmo?»
- **Escáner:** `tipografia.signos_sin_apertura` registra cada `?` o `!` de
  un párrafo que no tiene su `¿` o `¡` correspondiente.

### P57 · Mayúscula tras dos puntos

- **Fuerza:** Débil
- **Qué es:** Una mayúscula justo después de dos puntos, fuera de las
  excepciones normativas.
- **Por qué es un rasgo:** El DPD no formula una regla general sobre la
  mayúscula tras los dos puntos: pide minúscula tras un conector como
  "pues bien" ("La oración que los sigue se inicia con minúscula", DPD,
  *dos puntos*, 2.6), mayúscula tras el saludo de una carta y tras el verbo
  que abre ciertos textos jurídicos y administrativos, y muestra la cita
  textual con mayúscula en su propio ejemplo; para el resto remite a
  *mayúsculas* (sin copia guardada). Por eso este patrón solo señala el
  uso: una mayúscula sistemática fuera de esos casos puede ser puntuación
  descuidada o calcada, pero no hay una regla general que lo confirme
  siempre.
- **Cuándo no tocarlo:** El saludo de una carta («Querida Marta:» seguido
  de mayúscula), una cita textual introducida por los dos puntos, y las
  fórmulas jurídicas o administrativas nunca se tocan.
- **Qué hacer:** Señalar la mayúscula que sigue a los dos puntos cuando no
  encaje en ninguna de esas excepciones, para que decida quien revisa; no
  se corrige de oficio, porque no hay una regla general que lo respalde en
  todos los casos.
- **Ejemplo:** «Nota: El horario cambia en agosto en Ferretería Robledo.»
  — Se señala la mayúscula tras los dos puntos, porque no es un saludo, una
  cita ni una fórmula jurídica; decide quien revisa si la baja a
  minúscula.
- **Escáner:** `tipografia.mayuscula_tras_dos_puntos`, con las mismas
  excepciones ya incorporadas al detector (no informa ante una cita, un
  elemento de lista, un encabezado ni una región enmascarada pegada a los
  dos puntos). El exceso de exclamaciones (P58, sin entrada propia en este
  archivo) vive en el mismo bloque, en `tipografia.exclamaciones`: da el
  recuento por mil palabras sin aplicar ningún umbral, porque el de su
  fuente original es arbitrario.

### P60 · Marcadores de posición

- **Fuerza:** Fuerte
- **Qué es:** Un hueco de plantilla sin rellenar que queda en el texto que
  se entrega como definitivo («Firma: [Tu nombre]»).
- **Por qué es un rasgo:** Determinista: un marcador sin rellenar
  demuestra que el texto no pasó por una revisión final, sin necesidad de
  interpretar nada más.
- **Cuándo no tocarlo:** No hay excepción: si el texto se presenta como
  terminado, ningún marcador debería quedar sin rellenar.
- **Qué hacer:** Nunca rellenarlo con un dato inventado; preguntar al
  autor el valor que falta.
- **Ejemplo:** «Firma: [Tu nombre]» → pregunta al autor: «¿qué nombre va
  en la firma? Sin el dato, el marcador se deja tal cual.»
- **Escáner:** `deterministas.marcadores_de_posicion`.

### P61 · Marcado de chatbot filtrado

- **Fuerza:** Fuerte
- **Qué es:** Restos técnicos de la interfaz de un modelo que se han
  colado en el texto final («…según el informe.contentReference[oaicite:0]»).
- **Por qué es un rasgo:** Determinista: es un resto de copiar y pegar
  directamente desde una conversación con un asistente, sin limpieza
  posterior.
- **Cuándo no tocarlo:** No hay excepción.
- **Qué hacer:** Quitar el marcado filtrado, dejando intacta la frase que
  lo rodea.
- **Ejemplo:** «El horario aparece confirmado en la web oficial.contentReference[oaicite:0].»
  → «El horario aparece confirmado en la web oficial.»
- **Escáner:** `deterministas.marcado_filtrado`.

## Comunicación con el lector

### P04 · Preámbulo escenificado

- **Fuerza:** Fuerte
- **Qué es:** Anunciar que se va a decir algo, con el gancho de una
  presentación teatral o de teletienda, antes de entrar en el contenido
  («Vamos a sumergirnos en el mundo del café. ¿El secreto? El tueste.»).
- **Por qué es un rasgo:** Imita la voz de un asistente que presenta un
  tema a quien no lo conoce, no la de alguien que ya domina lo que cuenta
  y lo dice directamente.
- **Cuándo no tocarlo:** Un "mira" suelto dentro de una frase coloquial es
  normal en español y no es este patrón; estos arranques solo se quitan,
  nunca se añaden para simular cercanía.
- **Qué hacer:** Cortar el preámbulo escenificado y empezar directamente
  por el contenido.
- **Ejemplo:** «Vamos a sumergirnos en el proceso de horneado de Panadería
  Olmo. El secreto: la fermentación lenta.» → «El secreto del horneado de
  Panadería Olmo es la fermentación lenta.»
- **Escáner:** `vocabulario.hallazgos` cubre la familia "Preámbulo
  escenificado" (fuerte) de [`vocabulario-es.md`](vocabulario-es.md)
  ("profundicemos en", "descubramos juntos", "vamos a sumergirnos en"); el
  molde retórico completo, fuera de esas fórmulas fijas, no lo detecta —
  juicio del modelo.

### P22 · Restos de chatbot

- **Fuerza:** Fuerte
- **Qué es:** Saludo servil, eco de la petición del usuario, oferta de
  seguir ayudando, o pasos de razonamiento expuestos («¡Claro! Aquí tienes
  una versión más breve. ¿Quieres que la adapte a Instagram?»).
- **Por qué es un rasgo:** Es el rasgo más seguro de todo el catálogo:
  esta forma de hablar solo existe en la interfaz de un asistente
  conversacional, nunca en un texto final que se sostiene solo.
- **Cuándo no tocarlo:** Los saludos y despedidas propios de una carta o
  un correo real no cuentan (P63); una réplica real de diálogo donde
  alguien dice de verdad "¡Claro!" tampoco es este patrón.
- **Qué hacer:** Cortar el saludo servil, el eco de la petición y la
  oferta de seguir ayudando; dejar solo el contenido entregado.
- **Ejemplo:** «¡Claro! Aquí tienes la nueva descripción de Ferretería
  Robledo: lleva treinta años en el mismo local. ¿Quieres que la acorte
  más?» → «Ferretería Robledo lleva treinta años en el mismo local.»
- **Escáner:** `vocabulario.hallazgos` cubre la familia "Restos de
  chatbot" (fuerte) de [`vocabulario-es.md`](vocabulario-es.md)
  ("¡claro!", "¡por supuesto!", "espero que te sea útil"); el resto de
  fórmulas de eco o de oferta de continuar no están en la lista y no las
  detecta — juicio del modelo.

### P49 · Metadiscurso que anuncia

- **Fuerza:** Débil
- **Qué es:** Anunciar la estructura o "los factores a tener en cuenta" en
  vez de exponerlos directamente («En las siguientes líneas veremos los
  factores clave…»).
- **Por qué es un rasgo:** Es frecuente también en la prosa académica
  humana, así que solo cuenta por acumulación; pero anunciar lo que viene
  en vez de decirlo aplaza el contenido sin aportar nada por sí mismo.
- **Cuándo no tocarlo:** Una sola aparición en un documento largo, o un
  anuncio que de verdad ayuda a navegar una estructura compleja, no es
  este patrón.
- **Qué hacer:** Cortar el anuncio y dejar directamente el contenido que
  anunciaba.
- **Ejemplo:** «En las siguientes líneas veremos los factores clave del
  crecimiento de Arcilla: la cercanía con el cliente y la calidad del
  producto.» → «Arcilla ha crecido por la cercanía con el cliente y la
  calidad del producto.»
- **Escáner:** no lo detecta todavía: [`vocabulario-es.md`](vocabulario-es.md)
  no tiene ninguna familia etiquetada con P49 (solo lo menciona como nota
  de exclusión para "exploraremos") — juicio del modelo.

### P63 · Fórmulas epistolares fuera de lugar

- **Fuerza:** Débil
- **Qué es:** Un saludo o una despedida propios de una carta o un correo,
  en un texto que no lo es («Quedo a la espera de sus comentarios. Un
  cordial saludo.» al final de una entrada de blog).
- **Por qué es un rasgo:** Son marcadores del género epistolar; usados
  fuera de ese género, delatan que el texto se generó como un "mensaje"
  genérico en vez de adaptarse al formato real.
- **Cuándo no tocarlo:** Son plenamente legítimos en una carta o un correo
  real: los saludos y despedidas propios de ese género nunca se tocan.
- **Qué hacer:** Cortar la fórmula epistolar cuando el género del texto no
  sea correspondencia; dejarla si lo es.
- **Ejemplo:** al final de una entrada de blog sobre Panadería Olmo:
  «Panadería Olmo abre de martes a domingo. Quedo a la espera de sus
  comentarios. Un cordial saludo.» → «Panadería Olmo abre de martes a
  domingo.»
- **Escáner:** `vocabulario.hallazgos` cubre la entrada "espero que te sea
  útil" (familia "Restos de chatbot", fuerte, compartida con P22) de
  [`vocabulario-es.md`](vocabulario-es.md); el resto de despedidas
  epistolares no está en la lista y no las detecta — juicio del modelo.

## Patrones descartados

Estos 19 patrones se estudiaron y se descartaron en `docs/auditoria.md`,
§2: no tienen entrada en este archivo y no deben reintroducirse sin una
decisión nueva que revise el motivo del descarte.

| Id | Motivo del descarte |
|---|---|
| P10 | Guion en compuestos: es norma inglesa; en español rompería el INCI y los códigos. |
| P21 | Comillas curvas: no son error en español; lo sustituye P55. |
| P67 | Hilo único: arreglarlo exige añadir una trama que el original no da (cero invención). |
| P68 | Resolución fabricada: el arreglo reescribiría lo que el autor afirma (cero invención). |
| P69 | Señales humanas a restaurar: restaurarlas sería añadir contenido (cero invención). |
| P70 | Huella por modelo: sirve para atribuir autoría, no para mejorar el texto, y caduca con cada modelo nuevo. |
| P71 | Variación elegante: evitar la repetición es norma escolar española; blader v3 la retiró de su propio catálogo. |
| P72 | Falsos rangos: retirado por blader v3 y por Wikipedia. |
| P73 | Longitud de frase uniforme: es la métrica de *burstiness* que la regla dura 4 prohíbe. |
| P74 | Prosa densa: la prosa formal española usa periodos largos con normalidad. |
| P75 | Emoción declarada: StoryScope muestra que los humanos etiquetan la emoción más, no menos, que los textos de IA. |
| P76 | Vocabulario inglés por eras: no se traduce a un vocabulario equivalente en español. |
| P77 | Prohibiciones generales (adverbios, pasiva, arranques con "Wh-", palabras extremas): sin matiz, y los extremos pueden ser un claim. |
| P78 | Alternancia de perfección y errores: no es un rasgo de estilo; la regla de cero invención ya cubre lo relevante. |
| P79 | Etiquetas compuestas inventadas: rechazado en su propia fuente, y raro en español. |
| P80 | Locuciones prepositivas de relleno ("a la hora de"): muy frecuentes en la prosa humana peninsular. |
| P81 | Nominalización pesada: es un consejo de estilo general, con riesgo alto de falso positivo en registro técnico o jurídico. |
| P82 | Puntos suspensivos de un carácter: sin base normativa. |
| P83 | *Sino* / *si no* y la coma ante *sino*: es una corrección ortográfica general, no un rasgo de texto generado. |
