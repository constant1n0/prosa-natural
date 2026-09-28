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
3. Formato y tipografía (parte 2, `patrones.md` §3)
4. Comunicación con el lector (parte 2, `patrones.md` §4)

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
- **Ejemplo:** «En el fondo, atender la panadería cada mañana es escuchar
  al barrio.» → «Atender la panadería cada mañana es escuchar al barrio.»
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
- **Escáner:** [`vocabulario-es.md`](vocabulario-es.md) todavía no tiene una
  familia con formas concretas para este patrón; no lo detecta por ahora —
  juicio del modelo.

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
  la valida con coma delante de "sino" (verificación pendiente en fuente
  primaria, `docs/auditoria.md` §7.5)— pero se repite como molde retórico
  automático incluso cuando la mitad negativa no corrige ninguna creencia
  real; se marca el molde, nunca la construcción en sí.
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
- **Por qué es un rasgo:** En el español actual la pasiva refleja sería más
  frecuente que la perifrástica según la NGLE (verificación pendiente en
  fuente primaria, `docs/auditoria.md` §7.5); el tic real en castellano no
  es tanto la pasiva inglesa como el impersonal de relleno.
- **Cuándo no tocarlo:** La pasiva refleja ("se lanzó la campaña en
  marzo") nunca se marca. Se exceptúa además el registro jurídico y
  administrativo, donde la perifrástica es propia del género.
- **Qué hacer:** Sustituir la perifrástica innecesaria por activa y cortar
  el impersonal de relleno, sin cambiar quién hace qué.
- **Ejemplo:** «La campaña fue lanzada por el equipo de Arcilla en marzo.»
  → «El equipo de Arcilla lanzó la campaña en marzo.»
- **Escáner:** no lo detecta: juicio del modelo.

### P15 · Gerundio ilativo o de posterioridad

- **Fuerza:** Fuerte (posterioridad pura); Débil (consecuencia sin apoyo)
- **Qué es:** Un gerundio que cuelga un hecho posterior o una
  interpretación sin apoyo en el original.
- **Por qué es un rasgo:** El gerundio de pura posterioridad se da por
  incorrecto según el DPD (verificación pendiente en fuente primaria,
  `docs/auditoria.md` §7.5); el de consecuencia es gramatical, y se
  convierte en rasgo solo cuando cuelga una interpretación que el original
  no respalda.
- **Cuándo no tocarlo:** El gerundio de consecuencia inmediata o casi
  simultánea es correcto y no se toca; solo se corrige la pura
  posterioridad temporal o la interpretación sin apoyo.
- **Qué hacer:** Si es posterioridad pura, separar en dos frases sin
  inventar la relación entre ellas; si es una interpretación sin apoyo,
  cortarla y dejar el hecho tal cual.
- **Ejemplo:** «La tienda abrió en 2019, convirtiéndose en un referente
  del barrio.» → «La tienda abrió en 2019.»
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
- **Por qué es un rasgo:** La anteposición de un epíteto sería un rasgo
  gramatical normal de la lengua literaria según la NGLE (verificación
  pendiente en fuente primaria, `docs/auditoria.md` §7.5); el rasgo no es
  anteponer un adjetivo, sino acumular varios hasta saturar el sustantivo.
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
