# Modo Revisión

El modo Revisión audita un texto sin tocar su redacción: señala hallazgos,
explica su motivo y propone qué hacer con cada uno, pero nunca reescribe
nada por su cuenta. El modelo lee este archivo siempre que trabaje en este
modo, para usar el mismo formato de salida y el mismo vocabulario de
veredicto en cualquier texto que audite.

## Cuándo se activa

- El usuario lo pide explícitamente ("revisa este texto", "audita esta
  ficha", "dame tu opinión sin cambiar nada").
- El texto tiene claims marcados o candidatos a claim y el usuario no ha
  elegido un modo (Reescritura, Revisión o Archivo): la skill entra en
  Revisión por su cuenta y lo explica en una sola frase antes de tocar
  nada, porque una alegación de eficacia, salud o seguridad no se debe
  reformular sin que alguien decida primero qué hacer con ella
  ([`claims.md`](claims.md)).

En ambos casos la salida de este modo es siempre la de este archivo: un
veredicto global más una lista de hallazgos. Si después se pide una
reescritura, esa reescritura es un paso aparte, sujeto a la comprobación
de la sección "Comprobación de la reescritura" más abajo.

## Formato de salida

```markdown
## Veredicto global: <sin cambios necesarios | cambios recomendados | requiere decisión del autor | no publicable tal cual>

### Hallazgo 1
- **Ubicación:** línea 4, o el fragmento citado entre comillas
- **Patrón:** P31 (metadiscurso vacío) — o el identificador que corresponda
- **Por qué:** motivo concreto, no una orden genérica
- **Sugerencia:** qué se podría hacer (cortar, fusionar, preguntar al autor…)
- **Veredicto:** mantener | revisar | preguntar al autor | rechazar

### Hallazgo 2
- **Ubicación:** …
- **Patrón:** …
- **Por qué:** …
- **Sugerencia:** …
- **Veredicto:** …
```

Si no hay ningún hallazgo, la lista se omite y el veredicto global es «sin
cambios necesarios», con una frase que lo confirme; no hace falta inventar
un hallazgo para justificar la revisión.

## Veredicto por hallazgo

Cada hallazgo lleva uno de estos cuatro veredictos, tomados del método de
veredicto de adewale/anti-slop-writing y traducidos al español
(`docs/auditoria.md` §2.2, fila "`ask-author` y `Rewrite check`"; §7.1):

- **Mantener.** El rasgo es legítimo en este texto, o el autor ya conoce la
  regla y ha decidido conservar su redacción a propósito. No es una
  ausencia de hallazgo: es un hallazgo que se señala y se cierra sin
  cambio, con su motivo.
- **Revisar.** Se recomienda una edición y el propio texto ya da todo lo
  necesario para hacerla (cortar un cierre vacío, fusionar una tríada
  forzada): no hace falta preguntar nada al autor.
- **Preguntar al autor.** La edición correcta necesita un dato o una
  decisión que solo el autor tiene (qué estudio respalda "según estudios",
  si una relación entre dos párrafos existe de verdad, qué emoción hay
  detrás de una sensación contada en un diario, si un candidato a claim
  sin marcar lo es de verdad). Nunca se inventa ese dato ni se elige por el
  autor.
- **Rechazar.** El texto no se puede publicar tal cual: un claim alterado
  respecto al original, un intocable técnico cambiado (INCI, marca, precio,
  código, URL, cita textual), un dato inventado o perdido, un marcador de
  posición sin rellenar, marcado de chatbot filtrado (tokens como
  `oaicite` o `turn0search0`, P61) o un dato personal que no debería estar
  ahí. Un candidato a claim sin marcar no se rechaza: se señala y su
  veredicto es *preguntar al autor*. Una apertura de chatbot como
  «¡Claro!» es P22 y su veredicto es *revisar*, no *rechazar*.

## Veredicto global del texto

El veredicto global se deriva de los veredictos por hallazgo, nunca al
revés: no se elige antes al ojo y después se ajustan los hallazgos para
que cuadren. La regla es determinista y sigue este orden, de mayor a menor
severidad — el primero que se cumpla decide el veredicto global:

1. **No publicable tal cual.** Hay al menos un hallazgo con veredicto
   rechazar.
2. **Requiere decisión del autor.** No hay ningún rechazar, pero hay al
   menos un preguntar al autor.
3. **Cambios recomendados.** No hay ningún rechazar ni ningún preguntar al
   autor, pero hay al menos un revisar.
4. **Sin cambios necesarios.** No hay hallazgos, o todos los que hay llevan
   veredicto mantener.

## Revisión estricta

Los hallazgos que llevan veredicto rechazar son los que anti-ai-writing
trataba como severidad crítica en su revisión estricta, adaptados al
vocabulario de veredicto de esta skill (`docs/auditoria.md` §2.2, fila
"Revisión estricta"): un claim alterado respecto al original, un intocable
técnico cambiado, un dato nuevo o perdido, un marcador de posición o un dato
personal fuera de lugar. La razón de tratarlos aparte no es que sean más
"IA" que el resto de patrones, sino que revierten una de las reglas duras
del proyecto (cero invención, claims protegidos o intocables técnicos), y
esas reglas no admiten grados.

`scan_tells.py --original ANTES.txt DESPUES.txt` automatiza buena parte de
esta comprobación: compara cifras, porcentajes, fechas, precios,
duraciones y unidades, códigos, nombres propios, URL, claims marcados y
citas literales entre los dos textos, y devuelve el código de salida 1 si
falta o aparece algo nuevo en cualquiera de esas categorías, o si cambia un
claim marcado. Tres límites documentados en el propio script afectan a
esta comprobación, y quien revisa debe conocerlos para no confiar en el
código de salida más de lo que da de sí:

- La comparación es por presencia de una lectura normalizada, no por
  multiconjunto: si un dato aparece dos veces en un texto y una sola en el
  otro, no se marca como perdido.
- No hay conversión de unidades: "48 h" y "2 días" se tratan como datos
  distintos aunque signifiquen lo mismo.
- La heurística de nombres propios se basa en la mayúscula inicial fuera de
  posición de inicio de frase; puede dar alguna falsa alarma en casos poco
  frecuentes, pero el diseño prefiere esa falsa alarma ocasional a dejar
  pasar en silencio un nombre cambiado (regla de cero invención).

Además, las siglas (`comparacion.siglas`) y el aviso de registro
(`comparacion.registro`) son solo informativos: una diferencia ahí nunca
cambia el código de salida, así que revisarlos a mano sigue haciendo
falta. La proporción de mayúsculas de `encabezados` (Title Case) tampoco
excluye nombres propios reales, y las tríadas y estructuras de
`estructuras` se etiquetan siempre como "probable": ninguna de las dos
emite un veredicto por sí sola. La densidad de vocabulario y de patrones
estructurales se informa por mil palabras, sin ningún umbral que dispare
un aviso automático: calibrar ese umbral queda para la Fase 3
(`docs/estudio.md` §7.5-7.6; `docs/auditoria.md` §2.2, fila "Veredicto por
densidad").

Si el entorno no puede ejecutar Python, la misma comprobación se hace a
mano con una lista de control: releer el original y el texto nuevo en
paralelo y confirmar, categoría por categoría, que ninguna cifra, fecha,
precio, duración con unidad, código, nombre propio, URL, claim marcado o
cita textual falta, cambia o aparece de nuevo, y que ningún dato personal
(DNI/NIE, IBAN, teléfono, correo) se ha colado en la salida. El resultado
que importa es el mismo tanto si lo da el script como si lo da esta
lista: cualquier diferencia en esas categorías es un hallazgo con
veredicto rechazar, nunca un "revisar" ni un "preguntar al autor".

## Comprobación de la reescritura (Rewrite check)

Después de cualquier reescritura —tanto si viene de modo Revisión seguido
de un paso de edición, como si viene directamente de modo Reescritura— se
compara el resultado con el original, adaptando el `Rewrite check` de
adewale/anti-slop-writing (`docs/auditoria.md` §2.2, fila "`ask-author` y
`Rewrite check`"; §7.1): cifras, nombres, fechas, precios, URL, citas,
claims y registro (tú/usted, vosotros/ustedes) deben coincidir entre las
dos versiones salvo que el propio original ya diera el cambio. Cuando hay
script disponible, `scan_tells.py --original` hace esta comprobación de
forma determinista, con los mismos límites de la sección anterior; cuando
no lo hay, se hace con la misma lista de control a mano. Esta comprobación
no sustituye al juicio del modelo sobre si el significado se conserva
(negaciones, alcance, causalidad): confirma solo que no falta ni sobra
ningún dato, no que el sentido de la frase sea idéntico
(`docs/estudio.md` §7.3).

## Patrones de revisión

Estos cuatro patrones son mecanismos del propio modo Revisión, no rasgos
que aparezcan sueltos en un párrafo: por eso viven aquí y no en
[`patrones.md`](patrones.md). Las reglas duras del proyecto (cero
invención, claims protegidos, intocables técnicos) tienen prioridad sobre
cualquiera de ellos, igual que en el resto de referencias.

### P51 · Convergencia de lote

- **Fuerza:** Débil
- **Qué es:** Varios textos revisados en la misma sesión que comparten
  exactamente la misma apertura, el mismo cierre o la misma estructura,
  sin que el género lo exija.
- **Por qué es un rasgo:** Un lote de textos generados de una sola vez
  tiende a repetir el mismo molde en todos; un lote escrito por una
  persona varía de una pieza a otra sin que nadie se lo proponga.
- **Cuándo no tocarlo:** Si solo hay un texto (no un lote), este patrón no
  aplica: hace falta comparar varias piezas para que exista convergencia.
  Tampoco aplica si el género exige de verdad la misma plantilla en todas
  las piezas (por ejemplo, fichas de un catálogo que deben seguir un
  formato fijo por consistencia de la tienda): ahí la uniformidad es una
  decisión de producto, no un rasgo.
- **Qué hacer:** Señalar la convergencia en modo Revisión, con qué piezas
  la comparten y en qué (apertura, cierre, estructura). Nunca se reescribe
  para forzar variación entre los textos: variar por variar introduciría
  un tic nuevo (regla dura 4) en vez de corregir el rasgo real.
- **Ejemplo:** tres fichas de producto de Ferretería Robledo, Panadería
  Olmo y Botánica Iris que abren, las tres, con "¿Buscas la mejor opción
  para tu hogar?" antes de decir de qué trata cada una. En Revisión se
  señala que las tres comparten la misma apertura vacía (también P44); no
  se reescribe una sí y otra no para que "no se note" la coincidencia.
- **Escáner:** no lo detecta: `scan_tells.py` analiza un texto cada vez y
  no compara varios textos entre sí. Solo aplica cuando quien revisa tiene
  a la vista más de un texto de la misma sesión: juicio del modelo.

### P59 · Caracteres invisibles y homoglifos

- **Fuerza:** Fuerte
- **Qué es:** Caracteres Unicode invisibles en mitad del texto (espacio de
  ancho cero, guion blando, marcas de formato) o caracteres de otro
  alfabeto que se parecen visualmente a una letra latina (una "а" cirílica
  en vez de una "a" latina).
- **Por qué es un rasgo:** Ninguno de los dos tiene un uso legítimo dentro
  de una frase de prosa: son restos de copiar y pegar de otra herramienta,
  de marcado de seguimiento, o un intento de burlar un filtro de texto.
  Ninguna persona los escribe a propósito al redactar.
- **Cuándo no tocarlo:** El espacio de no separación (U+00A0) y el espacio
  fino de no separación (U+202F) quedan fuera de este patrón: son
  legítimos en español (por ejemplo, entre una cifra y su unidad, o antes
  de ciertos signos de puntuación) y no se avisan como invisibles.
- **Qué hacer:** Detectar y avisar de su presencia y su posición; nunca se
  insertan caracteres invisibles ni homoglifos en una reescritura, ni
  siquiera como supuesto "toque humano" para variar el texto (regla dura
  4: la skill no es un evasor de detectores).
- **Ejemplo:** un texto pegado de otra fuente que contiene un espacio de
  ancho cero (U+200B) entre dos palabras, invisible al leerlo pero
  presente en el archivo. Se avisa de su posición; se quita solo si el
  usuario pide limpiar el archivo, nunca se sustituye por otro carácter
  "parecido".
- **Escáner:** `deterministas` busca marcado de chatbot filtrado,
  parámetros UTM de IA, marcadores de posición, caracteres invisibles (por
  su nombre Unicode) y homoglifos, excluyendo explícitamente U+00A0 y
  U+202F. Nunca corre dentro de un bloque de código ni del frontmatter.

### P64 · Cambio de registro o variante

- **Fuerza:** Fuerte cuando hay mezcla en el mismo texto; el léxico
  individual (por ejemplo, "computadora" sola) es débil y vive en
  [`vocabulario-es.md`](vocabulario-es.md) como nota, no como entrada
  activa.
- **Qué es:** Un mismo texto que mezcla tuteo y "usted", o "vosotros" y
  "ustedes", sin que el cambio de interlocutor lo justifique; o que usa de
  forma puntual una palabra propia de otra variante del español
  ("computadora" en un texto que en todo lo demás usa "ordenador").
- **Por qué es un rasgo:** La mezcla sin motivo lee como un texto cosido de
  fragmentos de distinto origen, o traducido automáticamente desde otra
  variante, más que como la voz de una sola persona.
- **Cuándo no tocarlo:** "Ustedes" como plural formal, solo, en un texto de
  España es correcto y no es este patrón: solo cuenta cuando convive en el
  mismo texto con "vosotros" o con un tuteo de confianza. Un cambio de
  trato deliberado (de "usted" a "tú" cuando la relación con el lector
  cambia dentro del propio texto) tampoco es este patrón.
- **Qué hacer:** Solo se avisa; nunca se cambia una forma por otra sin que
  el autor lo confirme, porque decidir cuál de las dos variantes es la
  correcta para ese texto es una decisión del autor, no de la skill.
- **Ejemplo:** una newsletter de Botánica Iris que trata de "tú" al lector
  en la mayor parte del texto pero cambia a "vosotros" en un único párrafo
  final. Se avisa de la mezcla y se pregunta al autor qué trato quiere
  mantener; no se corrige por su cuenta a uno de los dos.
- **Escáner:** `registro` cuenta formas de tú/usted, de vosotros/ustedes y
  un léxico americano corto sobre el texto analizado; con `--original`,
  `comparacion.registro` compara también esos recuentos entre las dos
  versiones. En ambos casos es solo aviso: nunca cambia el código de
  salida ni decide por sí solo si hay mezcla real.

### P66 · Tics de humanización

- **Fuerza:** Fuerte
- **Qué es:** Una autocomprobación de la propia salida de la skill, no un
  rasgo del texto del usuario: confirmar que, al corregir los rasgos de
  este catálogo, la propia skill no ha introducido un tic nuevo (una
  muletilla, una duda fingida, un error deliberado, un mismo recurso de
  variación repetido siempre igual) para que el texto "suene más humano".
- **Por qué es un rasgo:** Es precisamente lo que prohíbe la regla dura 4:
  esta skill no es un evasor de detectores, y sustituir un patrón por otro
  igual de artificial no mejora el texto, solo cambia qué rasgo delata la
  edición.
- **Cuándo no tocarlo:** No aplica al texto del usuario, solo a lo que la
  skill produce; si el usuario ya usa una muletilla como voz propia
  deliberada, esa muletilla es asunto de `patrones.md`/`vocabulario-es.md`
  sobre el texto original, no de esta autocomprobación.
- **Qué hacer:** Antes de entregar cualquier reescritura, revisar que no se
  ha insertado ninguna muletilla, ninguna vacilación fingida, ningún error
  deliberado ni ningún "toque humano" que el original no tenía; y que no
  se ha creado un nuevo patrón uniforme por aplicar siempre el mismo
  arreglo mecánico a un rasgo repetido (por ejemplo, cortar "cabe destacar
  que" con la misma fórmula de sustitución en cada aparición del
  documento, en vez de fusionar cada frase con su contexto concreto).
- **Ejemplo:** al corregir tres apariciones de "cabe destacar que" en el
  mismo texto, no se sustituyen las tres por la misma coletilla nueva
  ("la verdad es que"); cada una se corta o se fusiona con su frase según
  lo que esa frase concreta necesite.
- **Escáner:** no lo detecta de forma directa: `scan_tells.py --original`
  ayuda de forma indirecta, porque un dato inventado para simular un
  "toque humano" (una cifra o un nombre que el original no daba) sí
  dispararía el código de salida 1 en la categoría correspondiente. Pero
  una muletilla o una duda fingida sin ningún dato nuevo no es una cifra
  ni un nombre: esa autocomprobación es siempre del modelo.

## Esto no es un tribunal

Cada hallazgo explica su motivo, no una sentencia. Si el autor conoce el
patrón y decide mantener su redacción a propósito, esa decisión se acepta
tal cual: mantener es un veredicto tan válido como cualquiera de los otros
tres, no una casilla de "sin problemas que reportar" (`docs/auditoria.md`
§2.2, fila "La skill no es un tribunal"; `docs/estudio.md` §6, fila "La
skill no es un tribunal"). El modo Revisión existe para que esa decisión
la tome el autor con toda la información delante, no para imponerla.
