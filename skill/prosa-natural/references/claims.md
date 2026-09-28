# Claims protegidos

Una alegación (*claim*) de eficacia, salud o seguridad es una regla dura
del proyecto: se deja literal en cualquier reescritura y se señala; ningún
patrón de [`patrones.md`](patrones.md) ni de [`discurso.md`](discurso.md)
se aplica dentro de una frase con un claim. Este archivo explica por qué,
cómo se detecta un claim y qué hace la skill con él.

## Por qué se protegen los claims

En la Unión Europea, las alegaciones sobre productos cosméticos, de salud
y otros productos regulados tienen requisitos legales sobre su propia
redacción, no solo sobre el hecho que afirman. El Reglamento (UE)
655/2013 fija los criterios comunes para las alegaciones cosméticas y se
aplica a lo que un texto transmite "explícita o implícitamente", no solo
de forma literal; exige que la redacción concreta de la alegación sea
coherente con la documentación que la sustenta y que no vaya más allá de
esa documentación (docs/estudio.md §10.1;
<https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32013R0655>).
El Reglamento (CE) 1223/2009, en su artículo 20, prohíbe atribuir a un
cosmético características o funciones de las que carece y limita en
particular el uso de "no probado en animales" (docs/estudio.md §10.2;
<https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32009R1223>).
El Reglamento (CE) 1924/2006 trata como "declaración" cualquier mensaje
que afirme, sugiera o dé a entender una propiedad saludable, exige que se
apoye en datos científicos generalmente aceptados y admite también
cualquier formulación que tenga "el mismo significado para el consumidor"
que una declaración ya autorizada (docs/estudio.md §10.3;
<https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32006R1924>).
El documento técnico de la AEMPS sobre reivindicaciones cosméticas (2017,
traducción no vinculante de un documento de la Comisión) recuerda que
estos criterios no fijan una redacción concreta, pero exige que la
redacción real cumpla igualmente esos criterios (docs/estudio.md §10.4;
<https://www.aemps.gob.es/cosmeticos-cuidado-personal/docs/doc-tec-reivindicaciones-cosmeticos.pdf>).

La consecuencia práctica es que una reescritura "más natural" puede
ampliar sin querer el alcance de lo que se afirma. Son ejemplos propios,
no del texto legal: "hasta 24 h" convertido en "todo el día"; "ayuda a
reducir" convertido en "reduce"; "fórmula con ácido hialurónico"
convertido en "hidratación con ácido hialurónico"; "rico en fibra"
convertido en "cuida tu digestión" (docs/estudio.md §10.5). En ninguno de
los cuatro casos cambia un hecho a ojos de quien no conoce la norma, pero
cambia el alcance de lo que la frase afirma o insinúa. La skill no tiene
acceso a la documentación que sustenta cada alegación y no puede decidir
que dos redacciones son equivalentes: esa equivalencia la juzga la
autoridad competente, no un modelo de lenguaje (docs/estudio.md §10.5).

## Cómo se detecta un claim

La detección sigue este orden:

1. **Marcado explícito.** Un fragmento envuelto en `[[claim]] … [[/claim]]`
   es un claim sin más comprobación, igual que una lista de claims ya
   aprobados que el propio usuario entregue en la conversación.
2. **Lista aprobada del proyecto.** Si existe un archivo
   `claims-aprobados.md` en la raíz del proyecto del usuario, sus entradas
   se tratan también como claims.
3. **Heurística.** A falta de marcado explícito o de lista aprobada, se
   trata como candidato a claim cualquier frase con: un verbo o fórmula de
   eficacia ("reduce", "elimina", "combate", "previene", "repara",
   "regenera", "calma", "alivia"); "hidrata durante X horas" o fórmulas de
   duración equivalentes; "clínicamente probado"; "dermatológicamente
   probado/testado"; "elimina el 99 %" o cualquier otro porcentaje;
   cualquier duración con unidad ("24 h", "48 horas"); "hipoalergénico";
   "sin X" (sin parabenos, sin sulfatos, sin siliconas…); "no testado en
   animales"; "natural" asociado a un efecto concreto; referencias a
   estudios ("según estudios", "los estudios demuestran"); y
   autoevaluaciones de calidad o cumplimiento sin dato que las sustente
   ("el mejor", "el número uno", "líder del sector") — ver P30 más abajo
   (docs/estudio.md §10.5; docs/auditoria.md §7.4).

Ante la duda, la frase se trata como un claim. Esta regla de duda ya
estaba resuelta al conservar la detección conservadora de porcentajes: la
skill prefiere marcar de más a dejar sin proteger una alegación real
(docs/auditoria.md §4.1, fila sobre porcentajes como claim; §7.4).

## Qué hace la skill con un claim

- En modo Reescritura, la frase con el claim se mantiene literal y se
  señala; nunca se reformula, aunque suene a folleto o repita una fórmula
  que en cualquier otra frase se cortaría.
- El relleno alrededor del claim sí puede editarse con los patrones de
  `patrones.md` y `discurso.md`; ningún patrón se aplica dentro del propio
  claim.
- Si se detectan claims (marcados o candidatos) y el usuario no ha elegido
  un modo, la skill pasa a modo Revisión y lo explica en una sola frase,
  antes de tocar nada del texto.
- Nunca se añade ni se quita nada de un claim: ni un dato que lo refuerce,
  ni una cautela que lo suavice.
- Si una frase mejoraría con un dato concreto que el original no da (por
  ejemplo, qué estudio respalda "según estudios"), se pregunta al autor;
  nunca se inventa el dato ni se "restaura" una fuente supuesta.

## Porcentajes

La detección de porcentajes es deliberadamente amplia: cualquier
porcentaje en el texto es candidato a claim, incluidos los que no hablan
de eficacia ("20 % de descuento"). Esta amplitud es una decisión ya
resuelta en la auditoría, no un descuido: se estudió restringirla a los
porcentajes acompañados de un verbo o sustantivo de eficacia y se
rechazó, precisamente para no dejar sin marcar un porcentaje de eficacia
con una redacción distinta a la prevista (docs/auditoria.md §7.4). La
consecuencia reconocida es que, con esta regla, casi cualquier ficha con
un descuento acaba en modo Revisión; calibrar ese volumen corresponde a
la Fase 3, no a esta versión (docs/auditoria.md §4.1, fila sobre
porcentajes como claim). No se suaviza esta regla por su cuenta.

## Qué hace el escáner

`candidatos_claim` (siempre presente en la salida de `scan_tells.py`)
marca frases candidatas con estas reglas exactas: `verbo_eficacia`,
`hidrata_durante_horas`, `clinicamente_probado`, `dermatologicamente`,
`hipoalergenico`, `sin_x`, `no_testado_en_animales`,
`referencia_estudio`, `autoevaluacion`, `porcentaje`, `duracion_unidad` y
`natural_mas_efecto`. El texto ya protegido con
`[[claim]] … [[/claim]]` no se cuenta como candidato: se informa aparte,
en la clave `marcados`, y nunca vuelve a marcarse como candidato. En
ambos casos, decidir si de verdad es un claim y qué hacer con él es
responsabilidad de quien revisa o del modelo; el escáner solo señala.

Con `--original`, `comparacion.claims_marcados` compara los claims
marcados del texto original y del nuevo de forma literal, con los
espacios en blanco normalizados (varios espacios o saltos de línea
cuentan como uno solo, para no marcar una diferencia por un simple
reformateo). Cualquier claim que falte, que cambie o que aparezca nuevo
da código de salida 1, igual que el resto de categorías bloqueantes. Un
dato personal (DNI/NIE, IBAN, teléfono, correo) dentro de un claim nunca
se muestra en la salida: se sustituye por un marcador de categoría y el
claim se sigue comparando igual, así que un cambio en ese dato sigue
dando código de salida 1 sin revelar el valor.

Dos límites del escáner, ya documentados en el propio script, afectan a
los claims:

- La comparación es por presencia de una lectura, no por multiconjunto:
  si un mismo dato aparece dos veces en un texto y una sola en el otro, no
  se marca como ausente. Esto también aplica a `claims_marcados`.
- Las duraciones no se convierten entre unidades: "48 h" no se reconoce
  como igual a "2 días". Un cambio de unidad dentro de un claim con
  duración se marca siempre como diferencia, aunque el valor real no
  cambie; el escáner no decide si son equivalentes, solo señala el cambio
  para que lo haga quien revisa.

### P17 · Autoridad prestada y atribución vaga (dentro de un claim)

- **Fuerza:** Fuerte
- **Qué es:** Dentro de una alegación de eficacia, salud o seguridad,
  invocar una autoridad sin nombrar la fuente ("clínicamente probado",
  "según estudios") como parte de la propia redacción del claim.
- **Por qué es un rasgo:** Esa fórmula es la propia alegación, no un
  adorno retórico: forma parte de lo que el Reglamento 655/2013 exige
  sustentar con datos y no ampliar más allá de las pruebas disponibles
  (docs/estudio.md §10.1). Cortarla o reformularla cambiaría lo que se
  afirma que hay detrás del producto.
- **Cuándo no tocarlo:** Dentro de un claim, nunca se corta ni se
  reformula, sea cual sea su registro. Fuera de un claim, esta misma
  fórmula es el patrón P17 general de `patrones.md`, con su propio
  tratamiento.
- **Qué hacer:** Dentro de un claim, dejar la frase literal y señalarla.
  Fuera de un claim, preguntar al autor cuál era la fuente real, o
  mantener lo vago si el original no la da; nunca inventar ni "restaurar"
  una fuente.
- **Ejemplo:** «[[claim]]Clínicamente probado: hidrata la piel durante 24
  horas.[[/claim]]» se deja literal y se señala. Fuera de un claim: «Los
  expertos coinciden en que este aceite es mejor que otros.» → se pregunta
  al autor qué fuente da el original para "los expertos"; sin ella, la
  frase se deja como está.
- **Escáner:** `candidatos_claim` marca la frase con la regla
  `clinicamente_probado` o `referencia_estudio` solo cuando el marcador
  aparece fuera de `[[claim]] … [[/claim]]`; dentro del marcado, el
  fragmento queda en blanco para `candidatos_claim` y se cuenta aparte en
  `marcados`.

### P30 · Autoevaluación de calidad

- **Fuerza:** Fuerte
- **Qué es:** Declarar la calidad o el cumplimiento de un producto o
  servicio sin ningún dato que lo sustente ("el mejor del mercado", "la
  más alta calidad", "número uno", "líder del sector").
- **Por qué es un rasgo:** En una ficha de producto, es candidata a claim
  bajo los criterios del Reglamento 655/2013 que cita la auditoría: la
  veracidad de la afirmación y la honradez, que exige no ir más allá de
  las pruebas disponibles (docs/auditoria.md §2, patrón P30).
- **Cuándo no tocarlo:** No se rechaza por su cuenta ni se suaviza a una
  versión "más segura": cambiar "el mejor del mercado" por "una buena
  crema" seguiría siendo una autoevaluación sin dato, solo que más
  discreta. Si ya está dentro de un claim marcado, se trata como
  cualquier otro claim: literal y señalado.
- **Qué hacer:** Señalar la autoevaluación como candidata a claim; nunca
  reescribirla ni suavizarla por iniciativa propia.
- **Ejemplo:** «Nuestra crema es la mejor del mercado.» → se señala como
  candidata a claim; no se reescribe como «una buena crema», que seguiría
  siendo una autoevaluación sin ningún dato que la sustente.
- **Escáner:** `candidatos_claim` marca la frase con la regla
  `autoevaluacion` ("el/la mejor", "el más…", "número uno", "líder").

## Ejemplo propio: ficha de un cosmético ficticio

Texto de entrada, con un claim marcado, un claim heurístico (un
porcentaje) y relleno sin ningún claim:

> Botánica Iris presenta su nueva crema de manos. [[claim]]Clínicamente
> probado: hidrata durante 24 horas.[[/claim]] Elimina el 99 % de la
> sequedad de la piel. Además, cabe destacar que esta joya para tus manos
> es un auténtico placer para los sentidos.

Como el texto tiene un claim marcado y un candidato heurístico (la frase
del 99 % dispara a la vez las reglas `verbo_eficacia` y `porcentaje`), y
no se ha elegido un modo, la skill pasa a Revisión con una frase como:

> Este texto tiene alegaciones de eficacia (un claim marcado y un
> candidato con un porcentaje), así que se revisa sin tocar su redacción
> en vez de reescribirlo directamente.

La edición se limita al relleno (P31, metadiscurso vacío; P16, lenguaje
de folleto), sin tocar ninguno de los dos claims y sin añadir ningún dato
nuevo:

> Botánica Iris presenta su nueva crema de manos. [[claim]]Clínicamente
> probado: hidrata durante 24 horas.[[/claim]] Elimina el 99 % de la
> sequedad de la piel.
