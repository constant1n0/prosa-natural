# Ejemplos

Pares de "antes" y "después" propios, con marcas y personas ficticias
(Ferretería Robledo, Panadería Olmo, Botánica Iris, Hostal Lumbre,
Academia Arcilla, Marta…), pensados para ilustrar un patrón concreto de un
vistazo. No son el corpus de evaluación de la Fase 3 (mucho más grande y
con casos de ajuste y de control separados): son solo el punto de apoyo
cuando hace falta ver un patrón aplicado a un texto completo, no solo a su
definición. El modelo lee este archivo bajo demanda, cuando dude de cómo
se aplica un patrón concreto a un caso real; no hace falta cargarlo para
juzgar un texto de rutina.

Cada par preserva los mismos hechos que el original: ninguna cifra,
nombre, fecha, precio o cita se añade ni se quita entre el "antes" y el
"después". Varios pares terminan siendo iguales o casi iguales al
original: eso es una salvaguarda, no un fallo del ejemplo — un patrón que
no se aplica en ese caso concreto no fuerza un cambio (`patrones.md`,
"Esto no es un tribunal").

## Contenido — P13 · Significado inflado

- **Antes:** «Ferretería Robledo repara herramientas desde 1990, lo que la
  convierte en un símbolo del compromiso con el oficio de todo el barrio.»
- **Después:** «Ferretería Robledo repara herramientas desde 1990.»
- **Por qué:** El hecho concreto (repara herramientas desde 1990) ya está
  completo; la cláusula de significado ("símbolo del compromiso… de todo
  el barrio") no añade ningún dato nuevo, solo infla el hecho con una
  interpretación que el original no sustenta. Ver P13 en
  [`patrones.md`](patrones.md).

## Sintaxis y construcción — P37 · Conectores apilados

- **Antes:** «Ferretería Robledo repara electrodomésticos pequeños.
  Asimismo, presta herramientas a sus clientes habituales. Por otro lado,
  abre también los domingos de mercado.»
- **Después:** «Ferretería Robledo repara electrodomésticos pequeños,
  presta herramientas a sus clientes habituales y abre también los
  domingos de mercado.»
- **Por qué:** Los tres son párrafos seguidos que abren con un conector
  distinto sin que ninguno aporte una relación real entre las frases; se
  fusionan en uno solo sin perder ningún hecho (los tres servicios y el
  horario de domingo). Ver P37 en [`patrones.md`](patrones.md).

## Formato y tipografía — P56 · Signos de apertura omitidos

- **Antes:** «Sabías que el Hostal Lumbre abre todo el año? Nunca cierra ni
  en invierno!»
- **Después:** «¿Sabías que el Hostal Lumbre abre todo el año? ¡Nunca
  cierra ni en invierno!»
- **Por qué:** Falta el signo de apertura de la interrogación y de la
  exclamación; se añaden sin cambiar ninguna otra palabra ni ningún hecho
  ("abre todo el año", "nunca cierra ni en invierno" quedan igual). Ver
  P56 en [`patrones.md`](patrones.md).

## Comunicación con el lector — P22 · Restos de chatbot

- **Antes:** «¡Claro! Aquí tienes la información que pediste: en
  Panadería Olmo elaboran pan de trigo y de centeno.»
- **Después:** «En Panadería Olmo elaboran pan de trigo y de centeno.»
- **Por qué:** La apertura de asistente conversacional no aporta ningún
  dato sobre Panadería Olmo; se corta entera y se deja el hecho que ya
  daba la segunda parte de la frase, sin tocarlo. Ver P22 en
  [`patrones.md`](patrones.md).

## Discurso — P44 · Apertura temporal o panorámica vacía

Este par es un fragmento recortado de un texto más largo (igual que los
ejemplos de [`discurso.md`](discurso.md)): la banda de longitud de ese
archivo se mide sobre el texto completo, no sobre este fragmento de una
frase.

- **Antes:** «En el panorama actual del comercio de cercanía, Botánica
  Iris vende plantas y macetas de barro en la misma calle desde hace
  quince años.»
- **Después:** «Desde hace quince años, Botánica Iris vende plantas y
  macetas de barro en la misma calle.»
- **Por qué:** La apertura panorámica no da ningún dato del comercio real
  de Botánica Iris; cualquier tema admitiría la misma frase de apertura.
  Se corta y se empieza directamente por el hecho concreto ("quince
  años", "la misma calle"), que no cambia de sitio en el texto ni de
  valor. Ver P44 en [`discurso.md`](discurso.md).

## Vocabulario — P31 · Fórmula de relevancia vacía

- **Antes:** «Cabe destacar que el Hostal Lumbre está a cinco minutos a
  pie de la playa.»
- **Después:** «El Hostal Lumbre está a cinco minutos a pie de la playa.»
- **Por qué:** "Cabe destacar que" anuncia relevancia sin añadir ningún
  hecho por sí solo; el dato real ("a cinco minutos a pie de la playa")
  queda igual con la fórmula cortada. Familia "Metadiscurso vacío" (P31)
  de [`vocabulario-es.md`](vocabulario-es.md).

## Claim marcado que se mantiene literal

- **Antes:** «Botánica Iris presenta su nuevo aceite corporal. Además, es
  importante mencionar que la fórmula incluye aceite de argán.
  [[claim]]Reduce visiblemente las líneas de expresión en 4
  semanas.[[/claim]] El aceite viene en un frasco de vidrio reciclado.»
- **Después:** «Botánica Iris presenta su nuevo aceite corporal. La
  fórmula incluye aceite de argán. [[claim]]Reduce visiblemente las líneas
  de expresión en 4 semanas.[[/claim]] El aceite viene en un frasco de
  vidrio reciclado.»
- **Por qué:** Solo se corta el relleno ("Además, es importante mencionar
  que", familia "Metadiscurso vacío", P31); el claim marcado no se toca ni
  una coma, porque es una alegación de eficacia protegida por una regla
  dura del proyecto, no un candidato a mejora de estilo. La versión final
  conserva las marcas `[[claim]]`/`[[/claim]]`; junto a ella, la respuesta
  también ofrecería una copia sin marcas, lista para publicar. Ver
  [`claims.md`](claims.md).

## Salvaguarda — texto ya bueno

- **Antes:** «Panadería Olmo hornea el pan de centeno los martes y los
  viernes. La masa fermenta doce horas antes de entrar al horno de leña.
  Los clientes habituales reservan barra por encargo.»
- **Después:** idéntico al original.
- **Por qué:** No hay ningún rasgo del catálogo: cada frase da un hecho
  concreto y ninguna sobra. "Sin cambios necesarios" es una salida tan
  válida como cualquier edición; sobrecorregir un texto ya bueno es el
  mismo fallo que dejar pasar un texto generado, solo que al revés
  (`docs/estudio.md` §6, fila "Texto ya bueno").

## Salvaguarda — lista real de tres ingredientes

- **Antes:** «El pan de Panadería Olmo lleva tres ingredientes: harina de
  trigo, agua y sal.»
- **Después:** idéntico al original.
- **Por qué:** P06 (tríada forzada) se aplica a una tríada retórica
  fabricada para sonar completa, no a una lista real de ingredientes; aquí
  los tres elementos son el hecho, no un adorno, así que no se toca ni se
  fusiona con un cuarto elemento inventado. Ver P06 en
  [`patrones.md`](patrones.md).

## Salvaguarda — "robusto" en sentido técnico legítimo

- **Antes:** «La balda de Ferretería Robledo lleva un anclaje robusto que
  aguanta 40 kg sin combarse.»
- **Después:** idéntico al original.
- **Por qué:** "Robusto" es una entrada débil de
  [`vocabulario-es.md`](vocabulario-es.md) (familia "Vocabulario de
  registro IA") y el escáner puede seguir marcándola por densidad: una
  aparición sola no significa nada, y aquí describe un mecanismo real con
  una cifra que lo justifica (40 kg), no una cualidad vacía de marketing
  (`docs/estudio.md` §5.3, "el uso técnico legítimo no cuenta").
- **Aviso:** `scan_tells.py` puede reportar aquí un hallazgo de
  `vocabulario` para "robusto" (nivel Débil): es esperable y no es un
  hallazgo que pese solo, por diseño (D5, un hallazgo débil aislado nunca
  justifica una edición).

## Salvaguarda — raya de diálogo normativa

- **Antes:** «—Ya está el pan —dijo Marta.»
- **Después:** idéntico al original.
- **Por qué:** Es una raya de diálogo cerrada, normativa en español; no es
  la raya a la inglesa de P08 (espaciada, sin cierre o pegada a las dos
  palabras). Ver P08 en [`patrones.md`](patrones.md).

## Salvaguarda — carta que abre legítimamente con saludo

- **Antes:**

  > Querida Marta:
  >
  > Te escribo para confirmar que el pedido de harina llega el jueves.
  > Gracias por avisarme con tiempo.
  >
  > Un abrazo,
  > Pablo

- **Después:** idéntico al original.
- **Por qué:** Es una carta real dirigida a una persona real: el saludo
  epistolar (P63) y la mayúscula tras los dos puntos del saludo (P57) son
  ambos excepciones normativas explícitas, no rasgos. Ver P57 y P63 en
  [`patrones.md`](patrones.md).

## Ejemplo completo de salida en modo Revisión

Texto de entrada, con varios rasgos y un claim marcado, entregado a la
skill con "revisa esta ficha, por favor":

> ¡Claro! Aquí tienes la ficha de la Academia Arcilla. Cabe destacar que
> los cursos de la Academia Arcilla están pensados para cualquier nivel.
> Los cursos [[claim]]garantizan resultados profesionales en 3
> meses[[/claim]]. Para reservar plaza, llama al 912345678.

Salida en modo Revisión, con el formato y el vocabulario de veredicto de
[`revision.md`](revision.md):

```markdown
## Veredicto global: requiere decisión del autor

### Hallazgo 1
- **Ubicación:** «¡Claro! Aquí tienes la ficha de la Academia Arcilla.»
- **Patrón:** P22 (restos de chatbot)
- **Por qué:** Apertura de asistente conversacional que no aporta ningún
  dato sobre la Academia Arcilla.
- **Sugerencia:** Cortar la frase entera; empezar directamente por el
  contenido.
- **Veredicto:** revisar

### Hallazgo 2
- **Ubicación:** «Cabe destacar que»
- **Patrón:** P31 (metadiscurso vacío)
- **Por qué:** Anuncia relevancia sin añadir ningún hecho nuevo sobre los
  cursos.
- **Sugerencia:** Cortar la fórmula y dejar la frase como afirmación
  directa: «Los cursos de la Academia Arcilla están pensados para
  cualquier nivel.»
- **Veredicto:** revisar

### Hallazgo 3
- **Ubicación:** «[[claim]]garantizan resultados profesionales en 3
  meses[[/claim]]»
- **Patrón:** claim marcado (`claims.md`)
- **Por qué:** Es una alegación de eficacia ya marcada de forma explícita;
  está correctamente protegida, no reformulada.
- **Sugerencia:** Ninguna: se deja literal, como ya está.
- **Veredicto:** mantener

### Hallazgo 4
- **Ubicación:** «llama al 912345678»
- **Patrón:** aviso de privacidad (`privacidad.telefono`)
- **Por qué:** Es un número de teléfono; la skill no sabe si es el
  contacto público de la Academia Arcilla (legítimo en una ficha) o un
  número personal que no debería publicarse.
- **Sugerencia:** Confirmar con quien escribe si este teléfono es el
  contacto público del negocio antes de publicar la ficha tal cual.
- **Veredicto:** preguntar al autor
```

El veredicto global es «requiere decisión del autor» porque hay un
hallazgo con veredicto preguntar al autor y ninguno con veredicto
rechazar, aunque también haya dos hallazgos con veredicto revisar: la
regla de derivación de [`revision.md`](revision.md) va de mayor a menor
severidad, no cuenta cuál hallazgo abunda más.
