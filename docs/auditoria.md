# Auditoría de patrones (Fase 1)

Decisiones sobre cada patrón del catálogo de [estudio.md](estudio.md) §3, con motivo, destino en la skill y fuerza. Resultado: 83 patrones, de los que 27 se mantienen, 37 se adaptan y 19 se descartan. De los 25 de blader/humanizer v3.0.0 se mantienen 11, se adaptan 12 y se descartan 2. Las siete propuestas de §7 quedaron resueltas por delegación expresa del usuario el 2026-09-23; son decisiones documentales para el trabajo futuro y no implementan la Fase 2.

## 1. Criterios de decisión

- Mantener: el mecanismo y su salvaguarda valen igual en español; solo cambian los ejemplos, que serán propios.
- Adaptar: en español cambian la forma, el alcance o la fuerza, o hace falta una salvaguarda nueva (claims, intocables, norma).
- Descartar: no existe en español, contradice la norma, choca con las reglas duras de [SKILL.md][skill] o su riesgo de falso positivo supera su valor.
- Prioridad ante un conflicto: reglas duras de [SKILL.md][skill] > norma lingüística vigente (DPD 2.ª ed., con fecha) > evidencia empírica > convergencia de fuentes > criterio propio.
- Fuerza: "fuerte" justifica editar con una sola aparición; "débil" solo cuenta en acumulación, como los rasgos *weak alone* de blader ([SKILL.md:362][bl]). Ante la duda, débil.
- Ningún patrón de reescritura se aplica a una frase con claim: se deja literal y se señala (regla dura 2).
- Un patrón nuevo solo entra si ningún otro lo implica ya, criterio que blader aplica a su propio catálogo ([AGENTS.md:24][bl-agents]).

## 2. Tabla principal

| Id | Patrón | Origen | Decisión | Motivo | Destino | Fuerza |
|---|---|---|---|---|---|---|
| P01 | Contraste "no X, sino Y" | blader §1; anti-ai contrastes; HUM P09; P151 B | Mantener | Mismo mecanismo. Se conserva si corrige una creencia real o si las dos mitades informan ([SKILL.md:61][bl]). La construcción es correcta (DPD): se marca el molde | patrones.md; scan_tells.py | Fuerte |
| P02 | Cierre de una línea y fragmentos | blader §2; kjm (kicker) | Mantener | Igual en posts en español; una frase corta vale si aporta un hecho nuevo | patrones.md | Fuerte |
| P03 | Sentencia que suena profunda | blader §3; HUM P28; kjm (mannered prose) | Adaptar | Formas españolas ("en el fondo", "lo que de verdad importa"). El arreglo es cortar o decir lo que el original afirma; el ejemplo de blader reinterpreta y añade contenido | patrones.md; vocabulario-es.md | Fuerte |
| P04 | Preámbulo escenificado | blader §4; Aboudjem P41; ADS | Mantener | Mismo mecanismo y salvaguarda ("mira" dentro de una frase coloquial es normal). Coherente con §4.4: se quitan, nunca se ponen | patrones.md; vocabulario-es.md | Fuerte |
| P05 | Discutir con nadie | blader §5 | Mantener | Igual en español; se conservan las objeciones atribuidas o respondidas | patrones.md | Fuerte |
| P06 | Tríada forzada | blader §6; anti-ai regla de tres; HUM P10; P151 B; NTE | Adaptar | Salvaguarda nueva: listas reales (ingredientes, INCI, pasos, especificaciones). Solo quitar o fusionar; nunca añadir un cuarto elemento | patrones.md; scan_tells.py | Fuerte |
| P07 | Arranques repetidos | blader §7; NTE (pro-drop) | Adaptar | El español omite el sujeto: el rasgo es el pronombre explícito o el mismo arranque repetido; se respeta la anáfora deliberada | patrones.md | Débil |
| P08 | Raya a la inglesa | blader §8; anti-ai; HUM P14; P151 C | Adaptar | Inciso cerrado, diálogo y listas son normativos. Se descarta "cero rayas en la versión final". Manda la muestra de voz | patrones.md; scan_tells.py | Débil; fuerte si va espaciada, sin cierre o en un encabezado |
| P09 | Matices apilados | blader §9; HUM P25; P151 E; NTE | Adaptar | Nunca se quita un matiz dentro de un claim ("ayuda a reducir"): cambiaría su alcance. Se conservan avisos legales y de seguridad | patrones.md | Débil |
| P10 | Pares con guion | blader §10; anti-ai banned-list | Descartar | Norma inglesa; en español el guion sigue la ortografía académica; prohibirlo rompe INCI y códigos | — | — |
| P11 | Pasiva perifrástica e impersonal de relleno | blader §11; HUM P13; P151 B; stop-slop | Adaptar | La pasiva refleja nunca se marca; la perifrástica solo si es innecesaria; excepción en registros jurídico y administrativo | patrones.md | Débil |
| P12 | Vocabulario de registro IA | blader §12; anti-ai banned-list ES; HUM §6.1; P151 A; NTE; ADS; I92; HES | Adaptar | La lista inglesa no sirve. Se sustituye por una lista española por niveles y familias (§3) | vocabulario-es.md; scan_tells.py | Según entrada |
| P13 | Significado inflado | blader §13; HUM P01, P06; P151; Wikipedia | Mantener | Igual; acabar en el último hecho concreto. Puerta de claims en fichas | patrones.md; vocabulario-es.md | Fuerte |
| P14 | Relación vaga | blader §14 | Mantener | La salvaguarda de blader ya impide inventar la relación ([SKILL.md:227][bl]). "Vinculado a" es corriente en español: débil | patrones.md | Débil |
| P15 | Gerundio ilativo o de posterioridad | blader §15; HUM P03, P22; P151 B; DPD | Adaptar | Dos niveles: la posterioridad pura se señala con alternativa, sin tratarla como error (el DPD la admite si se infiere sucesión o relación lógica; §7.5); el de consecuencia solo si cuelga una interpretación sin apoyo | patrones.md; scan_tells.py | Media (posterioridad); débil (consecuencia) |
| P16 | Lenguaje de folleto | blader §16; HUM P04; HES | Adaptar | Frecuente en fichas, donde suele coincidir con claims. "State what the thing is" solo fuera de claims | patrones.md; vocabulario-es.md | Fuerte |
| P17 | Autoridad prestada y atribución vaga | blader §17; anti-ai H6; Wikipedia; HUM P05 | Adaptar | "Clínicamente probado" o "según estudios" son claims: no se cortan ni se reformulan. Fuera de claims, preguntar la fuente o mantener lo vago; no "restaurar" datos (H6) | patrones.md; claims.md | Fuerte |
| P18 | Evitar "ser" y "tener" | blader §18; anti-ai verbos débiles; I92; HUM P08; adewale | Adaptar | "Se erige como" es fuerte; "cuenta con" y "ofrece" son corrientes y solo pesan acumulados. Se descarta "is designed to → will" (§5) | patrones.md; vocabulario-es.md | Débil, salvo "se erige/posiciona como" |
| P19 | Negrita decorativa | blader §19; anti-ai; HUM P15, P16 | Mantener | Igual. El Libro de estilo reserva la negrita para localizar elementos | patrones.md; scan_tells.py | Fuerte |
| P20 | Encabezados decorativos y Title Case | blader §20; HUM P17; P151 C; ADS | Adaptar | La mayúscula inicial única es norma (Libro de estilo). Se excluyen marcas, nombres propios, siglas y títulos extranjeros (§4.3) | patrones.md; scan_tells.py | Fuerte |
| P21 | Comillas curvas | blader §21; HES | Descartar | Las inglesas no son error en español y las angulares son las recomendadas. Lo sustituye P55 | — | — |
| P22 | Restos de chatbot | blader §22; anti-ai aperturas; HUM P20, P23; P151 D; Aboudjem P51; kjm | Mantener | El rasgo más seguro. Saludos y despedidas de carta no cuentan (P63) | patrones.md; vocabulario-es.md; scan_tells.py | Fuerte |
| P23 | Límite de conocimiento y conjeturas | blader §23; HUM P21; P151 D | Mantener | Refuerza §4.1: nunca presentar una conjetura como hecho | patrones.md; vocabulario-es.md | Fuerte |
| P24 | Encabezado repetido en la primera frase | blader §24; Aboudjem P49 | Mantener | Igual en español | patrones.md | Fuerte |
| P25 | Escribir sobre la versión anterior | blader §25; HUM P30 | Mantener | Legítimo en registros de cambios; poco frecuente en fichas y posts | patrones.md | Débil |
| P26 | Frase portátil | kjm | Mantener | Útil en fichas. El arreglo necesita un dato del autor: se pregunta (§4.1) | patrones.md | Débil |
| P27 | Promesa de revelación | kjm | Adaptar | Formas españolas de LinkedIn y marketing ("lo que nadie te cuenta") | patrones.md; vocabulario-es.md | Fuerte |
| P28 | Declarativa vaga | stop-slop | Mantener | Cortar o preguntar; nunca inventar la magnitud | patrones.md | Débil |
| P29 | Agencia falsa | stop-slop; Aboudjem P44; kjm | Adaptar | El español recurre más a la impersonal con "se"; solo en acumulación | patrones.md | Débil |
| P30 | Autoevaluación de calidad | slopornot S7 | Adaptar | Se trata como candidato a claim (criterios 2 y 4 del Reglamento 655/2013): se señala, no se reescribe | claims.md | Fuerte |
| P31 | Fórmula de relevancia vacía | anti-ai; HUM §6.2; P151 E; I92; TPE; NTE; ADS; semilla | Mantener | Converge en siete fuentes españolas y en la familia "destacar, subrayar" de Juzek (2026) | vocabulario-es.md; scan_tells.py | Fuerte |
| P32 | Modificador hueco | adewale PR #17; semilla | Adaptar | Solo cuando contrasta con una alternativa que nadie planteó; su fuente aún no lo ha incorporado | vocabulario-es.md | Débil |
| P33 | Calco censurado | DPD; RAE | Adaptar | Corrección que no cambia el sentido; se hace porque la norma lo censura, no porque delate IA | vocabulario-es.md (calcos) | Fuerte |
| P34 | Calco admitido, menos recomendable | DPD; Fundéu; semilla | Adaptar | No es error: se señala y pesa si se repite | vocabulario-es.md (calcos) | Débil |
| P35 | Anglicismo admitido | DPD; DLE | Adaptar | Registrados sin censura; solo densidad de registro | vocabulario-es.md | Débil |
| P36 | "Tomar lugar" | semilla | Adaptar | Sin pronunciamiento normativo localizado: entrada provisional hasta verificar (§7) | vocabulario-es.md | Débil (provisional) |
| P37 | Conectores apilados | anti-ai; HUM P33; P151 A; NTE; ADS; semilla | Adaptar | Un conector suelto no es rasgo ("un 'sin embargo' no es un tic", [HUM:474][hum]); se marca la cadena | patrones.md; scan_tells.py | Débil |
| P38 | Enumeración mecánica | TPE; HUM §6.2 | Mantener | Legítima en procedimientos y textos jurídicos (puerta de registro) | patrones.md | Débil |
| P39 | Simetría cautelosa | adewale; jalaalrd; kjm | Adaptar | Formas españolas ("tanto si… como si", "ya seas… o"); se conserva si nombra una bifurcación real ([ADW:60][adw]) | patrones.md; scan_tells.py | Débil |
| P40 | Revelación tras dos puntos | kjm | Adaptar | Solo si se repite | patrones.md | Débil |
| P41 | Acumulación de epítetos | NTE; semilla; NGLE | Adaptar | La anteposición es gramatical; se marca la acumulación | patrones.md; scan_tells.py | Débil |
| P42 | Aposición explicativa de manual | HUM P31 | Adaptar | Una sola fuente; solo si explica lo obvio | patrones.md | Débil |
| P43 | Moraleja, resumen o epílogo | anti-ai H1, H8, resumen; HUM P26; P151 E; Aboudjem P39; StoryScope | Adaptar | Solo cortar. Se descarta "break the flatness", que añade datos. Resúmenes legítimos en documentos largos. StoryScope ([arXiv:2604.03136][storyscope]) respalda la moraleja explícita en ficción (el narrador comenta el tema: IA 77 % frente a 52 %; §4.1, tabla 16); el epílogo es solo huella de Claude (tabla 17), no rasgo central. La fuerza se apoya en las fórmulas de cierre de las demás fuentes | discurso.md; vocabulario-es.md | Fuerte |
| P44 | Apertura temporal o panorámica vacía | anti-ai; P151 A; ADS; I92; HUM §6.2 | Mantener | Cortar la frase; "en los últimos años" con un dato no cuenta | vocabulario-es.md; discurso.md | Fuerte |
| P45 | Apertura de ambiente o pregunta retórica | anti-ai H5; P151 D; Russell et al. | Mantener | Abrir con el contenido | discurso.md | Débil |
| P46 | Contexto ya conocido | anti-ai H7 | Mantener | Útil en emails; cortar no inventa | discurso.md | Débil |
| P47 | Párrafos sin relación | adewale; Aboudjem P38 | Adaptar | Solo se nombra la relación si el original la da; si no, se señala (prueba sintaxis-relación, [ADW:68][adw]) | discurso.md | Débil |
| P48 | Plantilla de exposición | NTE | Adaptar | Solo en textos divulgativos largos; se señala, no se reestructura a la fuerza | discurso.md | Débil |
| P49 | Metadiscurso que anuncia | HUM P27; stop-slop; Aboudjem | Mantener | Frecuente en prosa académica humana: débil, salvo las fórmulas de chatbot (P04) | patrones.md; vocabulario-es.md | Débil |
| P50 | Emoción contada en el cuerpo | anti-ai H4; StoryScope | Adaptar | Solo se señala en textos personales; nombrar la emoción sería reinterpretar | discurso.md | Débil |
| P51 | Convergencia de lote | anti-ai | Adaptar | Se señala en Revisión con varios textos; no se fuerza variación | revision.md | Débil |
| P52 | Markdown fuera de contexto | Aboudjem P28; jalaalrd; Wikipedia | Mantener | Decidible por el canal declarado | patrones.md | Fuerte |
| P53 | Estructura donde bastaba prosa | anti-ai; Wikipedia; P151 B | Mantener | "Prose is the default" ([rewrites.md:159][aa-rewrites]) | patrones.md; scan_tells.py | Débil |
| P54 | Encabezado en pregunta | Aboudjem P27 | Mantener | Legítimo en preguntas frecuentes | patrones.md; scan_tells.py | Débil |
| P55 | Comillas incoherentes | semilla; RAE; Wikilengua | Adaptar | Sustituye a P21. Se señala la mezcla; no se convierte sin guía de estilo | patrones.md; scan_tells.py | Débil |
| P56 | Signos de apertura omitidos | DPD; HUM §6.5 | Mantener | Error objetivo y calco | patrones.md; scan_tells.py | Fuerte |
| P57 | Mayúscula tras dos puntos | RAE | Adaptar | Solo señalar, con las excepciones normativas | patrones.md; scan_tells.py | Débil |
| P58 | Exceso de exclamaciones | jalaalrd | Adaptar | Recuento; el umbral de la fuente es arbitrario | scan_tells.py | Débil |
| P59 | Caracteres invisibles y homoglifos | NTE; Aboudjem P52; graef | Mantener | Detectar y avisar, nunca insertar; excluir el espacio de no separación y el espacio fino | scan_tells.py; revision.md | Fuerte |
| P60 | Marcadores de posición | Aboudjem P33; Wikipedia | Mantener | Determinista; no se rellenan: se pregunta | scan_tells.py; patrones.md | Fuerte |
| P61 | Marcado de chatbot filtrado | Aboudjem P34; Wikipedia | Mantener | Determinista | scan_tells.py; patrones.md | Fuerte |
| P62 | UTM de herramientas de IA | Aboudjem P35; Wikipedia | Adaptar | Solo se señala: las URL son intocables (§4.3) | scan_tells.py | Fuerte |
| P63 | Fórmulas epistolares fuera de lugar | slopornot S5; jalaalrd; blader | Adaptar | En cartas y emails son legítimas; blader protege los saludos y despedidas propios del género ([SKILL.md:362][bl]) | patrones.md | Débil |
| P64 | Cambio de registro o de variante | semilla; slopornot S8; Aboudjem P36; ADS | Adaptar | Se señala y no se cambia sin confirmación. "Ustedes" formal es correcto en ES-ES | revision.md; scan_tells.py; vocabulario-es.md | Fuerte (mezcla); débil (léxico) |
| P65 | Transición de relleno | HUM §6.2; ADS; Aboudjem P43 | Adaptar | NTE recomienda "dicho esto": ni se veta ni se inserta; solo cuenta repetida | vocabulario-es.md | Débil |
| P66 | Tics de humanización | P151; TPE; HPA; anti-ai; kjm; graef | Mantener | Autocomprobación de la salida de la propia skill (§4.4) | revision.md | Fuerte |
| P67 | Hilo único | anti-ai H2 | Descartar | Corregirlo exige añadir un elemento que no está en el original. StoryScope confirma la brecha en ficción (sin subtramas: IA 79 % frente a 57 %; §4.1, tabla 16), pero cerrarla exigiría añadir trama (reglas 1 y 4) | — | — |
| P68 | Resolución fabricada | anti-ai H3 | Descartar | Su arreglo reescribe lo que el autor afirma (§5). StoryScope confirma la brecha en ficción (resolución por decisión del protagonista: IA 69 % frente a 46 %; §4.1, tabla 16), pero cerrarla exigiría añadir ambigüedad o causas externas (reglas 1 y 4) | — | — |
| P69 | Señales humanas a restaurar | anti-ai (6 señales) | Descartar | Son adiciones; solo se conservan si ya están en el original. StoryScope confirma las brechas en ficción (referencias con nombre: humanos 47 % frente a 24 %; §4.1, tabla 16), pero restaurarlas exigiría añadir referencias, saltos temporales o ambigüedad (reglas 1 y 4) | — | — |
| P70 | Huella por modelo y primeras palabras | anti-ai; jalaalrd | Descartar | Sirve para atribuir autoría; caduca con cada modelo | — | — |
| P71 | Variación elegante | Aboudjem; kjm; HUM P11; blader v2.5.1 | Descartar | Evitar la repetición es norma escolar en español; blader v3 la retiró y Wikipedia la pasó a histórico | — | — |
| P72 | Falsos rangos | Aboudjem; kjm; HUM P12; blader v2.5.1 | Descartar | Retirado por blader v3 y por Wikipedia | — | — |
| P73 | Longitud de frase uniforme | Aboudjem; stop-slop; jalaalrd; kjm; HUM P32; P151 B | Descartar | Es *burstiness* (§4.4). En Revisión solo se señala una monotonía concreta | — | — |
| P74 | Prosa densa | kjm | Descartar | La prosa formal española usa periodos largos | — | — |
| P75 | Emoción declarada | kjm | Descartar | StoryScope: los humanos etiquetan más la emoción (29 % frente a 8 %; §4.1, tabla 16). Las fórmulas de anuncio van en P12 | — | — |
| P76 | Vocabulario inglés por eras | anti-ai; lista de blader §12 | Descartar | No se traduce (estudio §5) | — | — |
| P77 | Prohibiciones generales | stop-slop (adverbios, pasiva, arranques con Wh-, extremos) | Descartar | Sin matiz; los extremos ("nunca", "siempre") pueden ser claims | — | — |
| P78 | Alternancia de perfección y errores | Aboudjem P25, P26 | Descartar | No es estilo; la cero invención cubre lo relevante | — | — |
| P79 | Etiquetas compuestas inventadas | adewale PR #18 | Descartar | Rechazado en su propia fuente; raro en español | — | — |
| P80 | Locuciones prepositivas de relleno | HUM §6.1; NTE ("a la hora de") | Descartar | Muy frecuentes en prosa humana peninsular | — | — |
| P81 | Nominalización pesada | NTE | Descartar | Consejo de estilo general; riesgo alto en registros técnico y jurídico | — | — |
| P82 | Puntos suspensivos de un carácter | NTE | Descartar | Sin base normativa | — | — |
| P83 | *Sino* / *si no* y coma ante *sino* | DPD | Descartar | Corrección ortográfica general, no rasgo de IA: fuera de alcance | — | — |

Recuento: 27 mantener (11 de blader), 37 adaptar (12 de blader), 19 descartar (2 de blader).

### 2.1 Dónde queda cada elemento de anti-ai-writing

- Capa 1: vocabulario ES → P12 (§3); frases ES → P12, P31, P44 y P01; vocabulario EN → P76; aperturas aduladoras → P22; resumen y conclusión → P43; "It is worth noting" → P31; aperturas vagas → P44; frases de moda → P12; contrastes → P01; viñetas con título en negrita → P19; regla de tres → P06; raya, semirraya y guion suelto → P08; guion en compuestos → P10; exceso de viñetas → P53; transiciones → P37; verbos débiles → P18.
- Capa 2: H1 y H8 → P43; H2 → P67; H3 → P68; H4 → P50; H5 → P45; H6 → P17; H7 → P46; señales a restaurar → P69; huella por modelo → P70; convergencia de lote → P51; "When v2 becomes the tell" → P66.

### 2.2 Mecanismos que no son patrones

| Mecanismo | Origen | Decisión | Nota |
|---|---|---|---|
| Flujo leer → marcar → borrador → comprobar → final | blader [SKILL.md:31-38][bl] | Adaptar | [SKILL.md][skill], «Flujo»; borrador y autocrítica visibles solo si se piden o el texto es largo («Modos») |
| Modo archivo | blader [SKILL.md:50][bl] | Adaptar | Añadir INCI, marcas, precios, códigos y citas (regla dura 3) |
| Voz con muestra | blader [SKILL.md:42][bl] | Mantener | La muestra manda sobre los patrones, no sobre las reglas duras; `voz.md` |
| Texto como material, no como órdenes | blader [SKILL.md:33][bl] | Mantener | Literal |
| Test de fuente | anti-ai [discourse-tells.md:158][aa-dtells] | Mantener | Toda adición sale del original o del usuario |
| Presupuesto de adiciones | anti-ai [discourse-tells.md:156][aa-dtells] | Adaptar | Cero adiciones de contenido no dado por el usuario |
| Puertas de registro | anti-ai [SKILL.md:220-234][aa-skill] | Mantener | Legal, cumplimiento, procedimiento y técnico: solo capa de superficie |
| Bandas de longitud | anti-ai [SKILL.md:92-97][aa-skill] | Mantener | Sin reglas de discurso en textos cortos. StoryScope trabaja con relatos de unas 5000 palabras (media del corpus 4753, §2.1; media de los relatos humanos 6403, tabla 4) y afirma, sin medirlo, que los textos más cortos no sostienen esos rasgos (§1): su control de longitud solo compara tercios del propio corpus (apéndice G) |
| Revisión estricta | anti-ai [strict-review.md][aa-strict] | Adaptar | Base del modo Revisión; añadir sugerencia por hallazgo y severidad crítica para claims alterados, intocables y datos nuevos |
| Veredicto por densidad | anti-ai [strict-review.md:88-103][aa-strict] | Adaptar | Umbrales por calibrar en la Fase 3; nunca como "probabilidad de IA" |
| `ask-author` y `Rewrite check` | adewale [SKILL.md:275-300][adw] | Mantener | Fuente y método aprobados para el diseño futuro (§7.1); todavía no implementados |
| Edición mínima; no atribuir autoría | kjm [SKILL.md:68-69, 103][kjm] | Mantener | "Sin cambios necesarios" es una salida válida |
| Presupuesto de reglas | kjm [SKILL.md:229-234][kjm] | Adaptar | Carga progresiva y presupuesto activo aprobados; el límite numérico se medirá en las Fases 2 y 3 (§7.7) |
| La skill no es un tribunal | anti-ai [SKILL.md:200][aa-skill] | Mantener | Se explica la regla y se acepta la decisión del usuario |

## 3. Vocabulario

Criterio: niveles de [estudio.md](estudio.md) §5.3. Cada entrada de `vocabulario-es.md` lleva familia, nivel, fecha de alta y origen. Una palabra débil solo cuenta en acumulación; una excluida no se lista.

### 3.1 anti-ai-writing, palabras en español ([banned-list.md:152-154][aa-banned])

| Decisión | Entradas (40) | Motivo |
|---|---|---|
| Débil, por familia (21) | crucial, fundamental, esencial, imprescindible; potenciar, fomentar, optimizar, maximizar; holístico, multifacético, paradigma, sinergia, robusto, innovador, revolucionario; empoderar; brindar; subrayar; panorama (figurado); navegar (figurado); adentrarse en | Uso humano corriente: solo pesan acumuladas. "Subrayar" e "innovador" tienen apoyo en Juzek (2026). "Adentrarse en" es fuerte como metadiscurso ("adentrémonos en", P04) |
| Solo en colocación (2) | aprovechar ("aprovechar al máximo", "aprovechar el poder de"); potencial ("liberar/desbloquear el potencial") | La palabra suelta es corriente |
| Excluida (17) | desarrollar, diversa, diversos, dinámico, enriquecer, estimular, excepcional, explorar, fortalecer, integrar, interactuar, notable, permitirá, relevante, sólido, transformar, aprovechemos | Falso positivo alto. "Excepcional" en fichas lo cubre P16; "diversos estudios", P17; "exploraremos", P49 |

### 3.2 anti-ai-writing, frases en español ([banned-list.md:156-169][aa-banned])

| Decisión | Entradas (12) |
|---|---|
| Fuerte | "En el mundo actual", "En el competitivo mundo de", "Hoy en día más que nunca" (P44); "Cabe destacar que", "Vale la pena mencionar que" (P31); "Llevar al siguiente nivel", "Liberar el potencial de" (colocaciones calcadas) |
| Débil | "En la actualidad" (solo como apertura del primer párrafo); "Marcar la diferencia", "Aprovechar al máximo", "Potenciar al máximo" (frases hechas corrientes) |
| Pasa a patrón | "No solo X, sino también Y" (P01) |

Las estructuras de [banned-list.md:171-172][aa-banned] van a P08 (adaptada), P06, P19, P37 y P31.

### 3.3 Otras listas en español

| Fuente | Pasan | Se descartan |
|---|---|---|
| humanamente §6.1-6.3 ([HUM:416-441][hum]) | "sumergirse en" (fuerte en metadiscurso); "recalcar", "poner de relieve" (débil); "el ámbito", "el universo de", "el reino de" (débil); "un sinfín de", "una miríada de", "un abanico de" (débil; "una amplia gama" puede ser exacta, [HUM:173][hum]); "clave", "vital", "primordial" (familia importancia); "integral", "sinérgico", "disruptivo", "vanguardista" (débil); "sin lugar a dudas", "indudablemente" (débil); "en conclusión", "en síntesis", "en última instancia", "como hemos visto" (P43); "¿a qué esperas para…?" (P43, débil) | "en aras de", "de la mano de", "a la hora de", "en pos de" (P80); §6.6 entero (P73, P66) |
| PR #151 ([P151:15-33][p151]) | "se erige como" (P18); "constituye un testimonio de" (fuerte); "marca un hito", "pilar fundamental", "piedra angular", "rico tapiz de", "de vital importancia" (débil, P13); "desbloquear el potencial", "navegar por los retos" (fuerte); "Por último, pero no menos importante" (fuerte, calco de *last but not least*) | "No obstante", "garantizar", "abordar" (corrientes); el límite de una raya cada 500 palabras como norma |
| naturalizacion-texto-es ([NTE:40-60][nte]) | "Es evidente que", "Como se puede ver" (débil, P31); adverbios en *-mente* en cadena (P06) | "Sin embargo", "Por lo tanto", "En consecuencia", "También" al inicio (corrientes); "invaluable" (el DLE lo registra); "requerimiento" (sin verificar); "implementación", "metodología", "utilización" (P81) |
| adelaidasofia e issue #92 ([ADS:95-112][ads]; [I92][i92]) | "es importante mencionar" (fuerte, P31); "en la era de" (fuerte, P44); "se posiciona como", "se presenta como", "se consolida como" (P18); "Profundicemos en", "Descubramos juntos" (fuerte, P04); "en este sentido", "Es menester", "Resulta imperativo", "Cobra especial relevancia" (débil) | — |
| Humanizer-es ([HES:171][hes]) | "enclavado en", "en el corazón de", "visita obligada" (P16, débil) | Traducción literal del resto de la lista inglesa |
| anti-ai, ejemplos ([examples.md:274][aa-examples]) | "me complace compartir" (débil) | — |

### 3.4 Semilla del proyecto

Lista de expresiones de partida del diseño. Hoy está repartida entre `vocabulario-es.md` (entradas con origen «semilla») y, para las construcciones, `patrones.md`.

| Entrada | Nivel y patrón | Matiz |
|---|---|---|
| "¡Claro!", "¡Por supuesto!" | Fuerte al inicio de una respuesta (P22) | En diálogo o réplica real, nada |
| "En resumen,", "En definitiva," | Débil; fuerte si abre el último párrafo de un texto breve para recapitular (P43) | NTE recomienda "en definitiva" (§4) |
| "Espero que te sea útil" | Fuerte fuera de cartas y emails (P22, P63) | En un email es una despedida normal |
| "Es importante destacar que", "Cabe destacar/mencionar que", "Vale la pena señalar" | Fuerte (P31) | Familia "destacar, subrayar" de Juzek (2026) |
| "En este sentido" | Débil | Sin pronunciamiento normativo: criterio propio |
| "Asimismo", "Además" en cadena | Patrón P37 | La coma tras el conector sí es norma |
| "en el panorama actual", "en un mundo cada vez más" | Fuerte (P44) | — |
| "un antes y un después", "marca un hito", "sin lugar a dudas" | Débil (P13, P12) | Frases hechas corrientes en prensa |
| "un verdadero referente" | Débil (P32) | — |
| "revolucionario" | Débil (P12) | En fichas puede ser claim o hipérbole; la hipérbole no tomada literalmente no necesita justificación (655/2013, anexo I, criterio 3) |
| "potenciar", "fomentar", "impulsar", "optimizar" | Débil, familia verbos comodín (P12) | — |
| "sumergirse en" | Fuerte en metadiscurso (P04); débil en otros usos | — |
| "desbloquear" | Fuerte solo en "desbloquear el potencial" | En sentido literal o técnico, nada |
| "aprovechar al máximo" | Débil | Frase hecha corriente |
| "jugar un rol/papel clave" | Débil (P34) | "Jugar un papel" no es incorrecto (DPD); "rol" está admitido; "clave" cuenta en la familia importancia |
| "a nivel de" | Fuerte si no hay idea de jerarquía (P33) | Censurado en ese sentido (DPD) |
| "en base a" | Débil (P34) | Admisible, menos recomendable (DPD 2.ª ed.): no se trata como error |
| "de cara a" en exceso | Débil (P34) | Desaconsejado solo como 'en relación con' |
| "tomar lugar" | Débil provisional (P36) | Sin pronunciamiento localizado |
| "hacer sentido" | Fuerte (P33) | Lo recomendado es "tener sentido" |
| Gerundio de posterioridad | Media (P15) | NGLE: incorrecto si es mera sucesión temporal; el DPD lo admite si se infiere sucesión o relación lógica. Se señala con alternativa |
| Adjetivos antepuestos y en tríada | Débil (P41, P06) | La anteposición es gramatical |
| "No solo… sino también…", "no se trata de X, se trata de Y" | Fuerte (P01), con salvaguarda | Construcción correcta |

La resolución de estas entradas está en §7.3: las expresiones corrientes se mantienen como señales débiles y dependientes del contexto, no como errores universales.

## 4. Conflictos entre fuentes y cómo se resuelven

| Tema | Posturas | Resolución |
|---|---|---|
| Raya | blader: cero rayas en la versión final salvo muestra ([SKILL.md:161][bl]) y a la vez *weak alone* ([:162][bl]). anti-ai: "No exceptions" ([banned-list.md:109][aa-banned]). NTE: eliminar siempre. Aboudjem: tolerancia cero. adewale: "do not ban em-dashes" ([ADW:61][adw]). Humanamente: raya legítima en incisos y diálogo. RAE y Wikilengua: usos normativos | Norma española: inciso cerrado, diálogo y listas son legítimos; se marca la raya a la inglesa. Manda la muestra de voz |
| Arreglo de "no es X, es Y" | anti-ai propone dos frases, "It is Y." y luego la explicación ([rewrites.md:82][aa-rewrites]), lo que produce el contraste partido que blader marca ([SKILL.md:60][bl]). La salida de ejemplo de NTE comete el rasgo | Seguir a blader: decir Y directamente, sin la mitad negativa |
| Lista negra frente a niveles | anti-ai: "If a word appears below, do not use it" ([banned-list.md:180][aa-banned]). blader: lista corta y "A formal word outside it is not a tell by itself" ([SKILL.md:201][bl]). Aboudjem y kjm: niveles. Wikipedia: los sinónimos no heredan el rasgo | Niveles fuerte, débil y excluida (§3) |
| "Dicho esto", "en el fondo", "en definitiva" | Tics para humanamente, PR #151 y adelaidasofia; NTE los recomienda como marcadores naturales ([NTE:129-134][nte]) | Débiles. prosa-natural nunca los inserta como "marcador humano" (regla dura 4) ni los veta sueltos |
| Comillas | blader y Humanizer-es: curvas → rectas. NTE: → «» o rectas. El README de humanamente convierte a «» ([README:65][hum-readme]). RAE: angulares recomendadas en impresos. Wikilengua: las inglesas no son error | No se convierten por sistema; se señala la incoherencia (P55); cambio solo con confirmación o guía de estilo |
| Voz frente a reglas | blader: la muestra manda sobre los patrones ([SKILL.md:42][bl]). anti-ai: voz "within the rules" ([SKILL.md:135][aa-skill]) | La muestra manda ([SKILL.md][skill], «Voz»), salvo las reglas duras |
| Autoridad sin fuente | blader: "A missing citation alone is not a tell" ([SKILL.md:254][bl]). anti-ai H6: cada párrafo con una afirmación debe nombrar algo real ([discourse-tells.md:130][aa-dtells]) | Seguir a blader; como mucho, preguntar |
| Matices | blader conserva los matices con apoyo ([SKILL.md:171][bl]). anti-ai: "AI hedges. Humans take a stance." ([anti-ai-writing.md:250][aa-personal]). PR #151: "Moja: postura clara" | Se conservan los matices con apoyo y todos los de un claim |
| Objeciones | blader §5 quita las que nadie planteó; la señal 5 de anti-ai añade "the case against" ([discourse-tells.md:188-200][aa-dtells]) | No se añaden; se conservan si están en el original |
| Emoción | kjm marca la emoción declarada; StoryScope halla más etiquetas emocionales explícitas en humanos (29 % frente a 8 %; §4.1, tabla 16); anti-ai H4 propone nombrar la emoción | Ni se añade ni se convierte: P75 descartado, P50 solo se señala |
| Tríadas | blader: "Keep three real items when the meaning needs three" ([SKILL.md:141][bl]). anti-ai, Fix B: añadir un cuarto elemento ([rewrites.md:128][aa-rewrites]) | Solo quitar o fusionar |
| Estructura del original | Humanamente: "Si el original tiene cinco párrafos, la reescritura tiene cinco párrafos" ([HUM:32][hum]). blader permite cambiar la estructura ([SKILL.md:36][bl]) | Gana [SKILL.md][skill], «Flujo» (paso 3): el borrador no trata la estructura como fija; la información se conserva |
| "Sin embargo" al abrir párrafo | NTE lo marca siempre (Tier 1); humanamente: "Un 'sin embargo' no es un tic" | Solo cuenta en cadena (P37) |
| Chat coloquial | anti-ai: "Cut the greeting, cut the sign-off" y un ejemplo en minúsculas ([discourse-rewrites.md:245-251][aa-drew]) | No se imita el descuido; se conserva el registro del original |

### 4.1 Choques del estudio con `SKILL.md` (gana `SKILL.md`)

| Punto | `SKILL.md` | Estudio | Tratamiento |
|---|---|---|---|
| «Español frente a inglés», "en base a" entre los calcos | Lo lista como calco | La DPD 2.ª ed. lo admite como menos recomendable | Se mantiene en la lista como débil, no como error (§7.3) |
| «Claims», porcentajes como claim | Ante la duda, claim | La regulación se refiere a eficacia, salud y seguridad; "20 % de descuento" no es claim | Se conserva la detección conservadora de porcentajes y la regla de duda; no se aprueba una restricción general por verbo o sustantivo (§7.4) |
| «Modos», claims → modo Revisión | Revisión por defecto si hay claims | Con la heurística amplia, casi cualquier ficha con descuento irá a Revisión | Se aplica; medir en la Fase 3 |
| «Español frente a inglés», "ustedes por vosotros" se señala | Rasgo americano | "Ustedes" es el plural formal en España | Se señala solo si convive con tuteo o trato de confianza |
| «Español frente a inglés», "¡Por supuesto!", "Espero que te sea útil" | Semilla | Legítimos en diálogo y en cartas | Se mantienen con la salvaguarda de contexto |
| «Escáner (opcional)», "recuento de rayas" | Recuento | Un recuento sin clasificar no separa la raya normativa | Recuento por tipo (§8), compatible con «Escáner (opcional)» |

## 5. Instrucciones de upstream que chocan con las reglas duras

| Fuente:línea | Instrucción literal | Regla | Tratamiento en prosa-natural |
|---|---|---|---|
| [blader README.md:131-159][u1] | Ejemplo de Lisboa: el "después" añade "By the second day my calves had opinions" o "for about thirty seconds" y cambia "this city completely stole my heart" por "still have mixed feelings about it" | 1 | No se reutiliza. Ejemplos propios verificados con `scan_tells.py --original` |
| [blader SKILL.md:205][u2], [:289][u3], [:302][u4], [:358][u5] | "which is considered a delicacy"; "speeds up load times through optimized algorithms"; "User research showed a preference for simplicity"; "uses a hash map for O(1) lookups" (ausentes del "antes") | 1 | Ídem; además, material de Wikipedia (CC BY-SA) |
| [anti-ai rewrites.md:220][u7]; [examples.md][u6] | "Our software cuts the average workflow from 47 steps to 12…"; casi todos los "después" | 1 | Casos negativos para los evals |
| [anti-ai rewrites.md:209][u8] | "3. Add back specificity (a number, a name, a concrete detail)." | 1 | Se pregunta al autor o se simplifica la frase |
| [anti-ai rewrites.md:236-243][u9] | "Strategy 2: bring back a small specific image" ("Our coffee was on a tree in Ethiopia three weeks ago.") | 1 | Descartada |
| [anti-ai discourse-rewrites.md:148][u10] | "for each claim, add the specific. If the specific is unavailable, weaken the claim to what you can support, or cut it." | 1, 2 | Ni añadir, ni debilitar, ni cortar un claim: se señala y se pregunta |
| [anti-ai discourse-tells.md:130][u11] | "every paragraph that makes a claim names something real" | 1 | Se señala la vaguedad; no se restaura nada |
| [anti-ai discourse-rewrites.md:195][u12] | "Tracking was broken for nine days." (dato ausente del "antes") | 1 | Descartado |
| [anti-ai SKILL.md:186][u13] | "Replaced "industry benchmarks suggest" with the actual competitor bid range (verify the figures)" | 1 | Solo con cifras que dé el usuario |
| [anti-ai discourse-rewrites.md:84-94][u14] | "Once I understood that the problem was scope, everything else fell into place." → "The scope was part of it. The rest I still can't explain." | 1 | Cambia lo que se afirma: descartado (P68) |
| [anti-ai banned-list.md:143-144][u15]; [rewrites.md:190-191][u16] | "is designed to" → "will" or rewrite as direct claim; "This tool is designed to help you..." → "This tool helps you..." | 2 | Nunca en claims: "formulado para hidratar" → "hidrata" amplía la alegación |
| [anti-ai rewrites.md:42][u17] | "revolutionary → new, first (if true), or cut" (y el resto de la tabla de sustituciones) | 2 | Sustituciones prohibidas dentro de claims |
| [blader SKILL.md:254][u18] | "Otherwise cut the unsupported claim or the list." | 2 | Si la autoridad forma parte de un claim ("clínicamente probado"), se señala; fuera de claims, se pregunta |
| [blader SKILL.md:245][u19], [:210][u20], [:267][u21], [:171][u22] | "State what the thing is."; "Keep the fact and drop the significance."; "Use *is*, *are*, and *has*."; quitar matices apilados | 2 | Solo fuera de frases con claim |
| [anti-ai anti-ai-writing.md:250][u23] | "Have a point of view. AI hedges. Humans take a stance." | 1, 2 | No se añade postura ni se quitan matices con apoyo |
| [anti-ai banned-list.md:109][u24], [:115][u25]; [anti-ai-writing.md:203][u26], [:207][u27] | "All forbidden in copy. No exceptions."; "Hyphens in compound words are also banned. Write around them." | 3; «Español frente a inglés» | Descartado: raya normativa legítima; guion intocable en INCI, códigos y compuestos |
| [blader SKILL.md:161][u28] | "The final rewrite must not contain em dashes (—) or en dashes (–) unless the writer's sample uses them" | «Español frente a inglés» | Se descarta la prohibición; se mantiene la prioridad de la muestra |
| [blader SKILL.md:293][u29] | Encabezados en *sentence case* | 3 | Excluir marcas, productos y nombres propios |
| [blader SKILL.md:50][u30] | "Keep code blocks, inline code, commands, paths, YAML metadata, data, and link targets unchanged." | 3 | Incompleto: añadir INCI, marcas, precios, códigos y citas |
| [blader SKILL.md:38][u31]; [anti-ai rewrites.md:231][u32]; [anti-ai-writing.md:251][u33] | "Vary sentence length; real writing alternates short and long."; "Vary your sentence lengths." | 4 | Criterio de calidad solo ante una monotonía concreta; nunca como objetivo |
| [anti-ai discourse-tells.md:231][u34] | "Let one piece be blunt and one be long." | 4 | Se señala la convergencia de lote; no se fuerza variación |
| [anti-ai discourse-tells.md:174][u35]; [discourse-rewrites.md:208][u36], [:211][u37] | "Anyway. Back in June we tried the opposite..."; "The honest version: I want to run it because I want the case study." | 1, 4 | Prohibido: muletilla insertada y dato inventado |
| [anti-ai discourse-rewrites.md:245-251][u38] | "Cut the greeting, cut the sign-off, cut anything that reads as a paragraph." y el ejemplo "landing page is live" | 4 | No se imita el descuido para parecer humano |
| [blader SKILL.md:36][u39], [:44][u40] | "An opinion or reaction is allowed when the voice calls for one"; "you may add a reaction where the writer would"; "Removing tells is half the job; the result must still sound like a person." | 1, 4 | No se añaden opiniones ni reacciones; la voz sale del original o de la muestra |
| [blader SKILL.md:36][u39] | "Fiction is exempt because invented detail is the task." | 1 | Sin excepción; la ficción queda fuera de alcance en v1 |
| [Aboudjem SKILL.md:419][u41]; [metrics.js][u42] | "0-20 \| Pristine \| … No detector should flag it." | 4 | Sin puntuación de "probabilidad de IA" en la skill ni en el script |
| [Aboudjem SKILL.md:279][u43], [:293][u44], [:296][u45] | "AI detectors measure "burstiness""; "Choosing the second or third word that comes to mind"; "informal transitions ("Anyway,", "So here's the thing:", "Look,", "Thing is,")" | 4 | Descartado |
| [Aboudjem SKILL.md:310][u46] | "Improves performance" becomes "cuts p99 latency from 900ms to 40ms" | 1 | Descartado |
| [Humanizer-es SKILL.md:441-455][u47]; [humanizar-texto-es SKILL.md:118-140][u48] | Rúbrica /50 y "Puntuación de humanidad" de 0 a 100 | 4 | Descartado |
| [anti-ai plugin.json:14][u49] | Palabras clave "ai-detection" y "chatgpt-detector" | 4 | prosa-natural no usará palabras clave de detección |

## 6. Enfoques descartados de raíz

| Enfoque | Qué hace | Motivo |
|---|---|---|
| numen-tech/slopornot | Se anuncia como "Bypass AI Detectors"; itera contra un detector cerrado con `AI_THRESHOLD = 40`; en la iteración 5 pide "introduce one concrete example or anecdote-style sentence per paragraph" | Reglas 1 y 4; binario de pago; su `es.md` inventa cifras |
| TempParaphraser | Elige, frase a frase, la paráfrasis que menos puntúa un detector; baja la precisión de cuatro detectores un 82,5 % de media | Regla 4; sin control de hechos (reglas 1-3); necesita red y modelos (regla 5) |
| POlLLOGAMER/Humanizer-Prompt-Advanced | "avoids ALL AI detectors"; faltas deliberadas y sin tildes; "tell personal experiences even if you don't have them" | Reglas 1 y 4; sin licencia |
| ToniPerea/humanizar-texto-es | "research purposes on AI detection evasion techniques"; muletillas ("la verdad es que", "mira", "vamos"); "errores tipográficos controlados" | Reglas 1 y 4; sin LICENSE |
| Partes de Aboudjem | *Burstiness*, perplejidad, transiciones informales, "Soul Injection", "Concretizer", puntuación 0-100 | Reglas 1 y 4 |
| Partes de naturalizacion-texto-es | Reescribir para destruir "cualquier patrón estadístico" (marcas de agua); marcadores "eso sí", "la verdad es que"; modo *always-on* que actúa "sin dejar rastro del proceso" | Regla 4; falta de transparencia |
| Partes de humanamente | §6.6: *burstiness* de 3-5 frente a 25-35 palabras, marcadores "vamos", "oye"; "Ten opiniones" | Regla 4; ese bloque procede de una fuente sin licencia |
| kjm, "Add disfluency" | Añadir disfluencias si el texto es uniforme ([SKILL.md:156][kjm]) | Regla 4 |
| Método del PR #151 | Listas "Validadas empíricamente contra GPTZero" | Se usan sus observaciones, no el método |

## 7. Propuestas resueltas para el diseño futuro

El estudio formuló estas siete propuestas para confirmación. El usuario delegó expresamente su resolución el 2026-09-23. Se conserva el contexto original y se fija aquí el límite de cada decisión; ninguna constituye implementación de la Fase 2.

### 7.1 Fuentes complementarias

**Propuesta original.** Incorporar el método de adewale/anti-slop-writing (`53370ff`), patrones y salvaguardas de humanamente (`1447b61`) e ideas de kjmagnan1s/anti-slop (`a3807e5`).

**Resolución.** Se acepta de adewale el método de evaluación y veredicto (`keep / revise / ask-author / reject`, `Rewrite check`, casos adversariales y oráculo de aserciones). De humanamente se acepta una selección estrecha de patrones del castellano —P08, P11, P15, P20, P37, P42 y P55 de este catálogo— y sus salvaguardas contra falsos positivos. Se excluyen su §6.6, las muletillas artificiales, la variación de ritmo como objetivo, la invención y cualquier material de procedencia incompatible. De kjm se toman solo las ideas de portabilidad, presupuesto de reglas y prosa de control; no se copia texto ni se presume permiso sobre material de terceros.

### 7.2 Licencias y atribución

**Propuesta original.** Ampliar `NOTICE.md`, aclarar el origen de los ejemplos de blader y citar Wikipedia como fuente de ideas.

**Resolución.** Se mantienen los avisos existentes y se añaden los avisos MIT exactos de adewale (© 2026 Ade Oshineye) y humanamente (© 2025 Siqi Chen, obra original; © 2026 Vicente Álvarez Asencio, adaptación al castellano), verificados en los `LICENSE` de los commits fijados. Las licencias de esos proyectos no cubren los ejemplos procedentes de Wikipedia:Signs of AI writing, revisión 1376018375, CC BY-SA 4.0. Wikipedia y kjm se citan como fuentes de ideas; la skill futura no copiará ejemplos de Wikipedia.

### 7.3 Expresiones corrientes de la semilla

**Propuesta original.** Rebajar, en vez de eliminar, expresiones con alto riesgo de falso positivo: "en base a", "jugar un papel/rol", "un antes y un después", "marca un hito", "sin lugar a dudas", "aprovechar al máximo", "En este sentido", "En definitiva", "¡Por supuesto!", "Espero que te sea útil" y "tomar lugar".

**Resolución.** Se aceptan como señales débiles y dependientes del contexto, con las salvaguardas ya detalladas en §3.4. No son errores universales. Se conservan como fuertes los restos de chatbot inequívocos cuando aparecen fuera de su género. Claims, citas y contenido técnico protegido tienen prioridad sobre cualquier clasificación estilística. Las afirmaciones normativas pendientes, incluida "tomar lugar", siguen pendientes: rebajar la fuerza estilística no demuestra su corrección normativa.

### 7.4 Heurística de claims

**Propuesta original.** Añadir los marcadores de `estudio.md` §10.5 y restringir los porcentajes a los acompañados por un verbo o sustantivo de eficacia.

**Resolución.** Se añaden al diseño futuro "dermatológicamente probado/testado", duraciones, "hipoalergénico", "sin X", "no testado en animales" y otras alegaciones sobre experimentación animal, "natural" asociado a un efecto y autoevaluaciones de calidad o cumplimiento (P30). Se rechaza la restricción general de porcentajes: se conserva la detección conservadora de porcentajes, la regla "ante la duda, claim" y la cobertura de todas las alegaciones de eficacia, salud o seguridad. No se aprueban excepciones ni listas blancas monetarias en esta fase.

### 7.5 Verificación normativa

**Propuesta original.** Completar en fuente primaria las comprobaciones que la descarga automática no permitió.

**Resolución.** Se difirió a verificación manual, sin sortear bloqueos. Resuelta el 2026-09-27: el usuario guardó desde el navegador las 32 páginas de rae.es citadas en `estudio.md` §4 y dos copias en prensa de notas de Fundéu BBVA, y cada afirmación se cotejó literalmente con el texto de esas páginas.

De las 27 afirmaciones marcadas, 13 coinciden (en dos de ellas, solo la parte de la RAE), 12 coinciden con matices y 2 no coinciden. Las 14 últimas se han corregido en `estudio.md` para ajustarlas a la fuente, con citas literales. Ninguna corrección cambia una decisión de §2. La única fuerza que cambia es la de P15, por decisión del usuario (véase abajo). Las de más peso:

- NGLE, pasiva refleja: no dice que en lo jurídico se prefiera la activa o la perifrástica; dice que los complementos agentes de la refleja "se aceptan a menudo en el código restrictivo del lenguaje jurídico". La excepción de registro de P11 se mantiene.
- DPD *computador*: la 2.ª edición no contiene "igualmente normativas"; describe la distribución geográfica sin censurar ninguna forma.
- DPD *gerundio*: matiza la censura del gerundio de posterioridad y lo considera "admisible cuando puede inferirse una sucesión o una relación lógicas"; la NGLE lo da por incorrecto cuando introduce "una mera sucesión temporal". **Decisión del usuario (P15, 2026-09-27):** la fuerza baja de "Fuerte (posterioridad)" a "Media (posterioridad)". La skill señala el gerundio de posterioridad pura y propone una alternativa, pero no lo trata como error ni lo corrige sola. El ejemplo ilustrativo de `estudio.md` ya no lleva "después".
- DPD *dos puntos*: no formula la regla general de minúscula ni la excepción de las citas y remite a *mayúsculas*, no guardada. P57 ya solo señala.
- DPD *porcentajes*: exige el espacio, pero no menciona la Ortografía de 2010; se ha retirado esa fecha.

Siguen pendientes y no autorizan correcciones automáticas como reglas establecidas:

- Publicaciones en X, que exigen iniciar sesión: FundéuRAE sobre "en base a" y @RAEinforma sobre "enfocarse". Conservan la marca en `estudio.md` §4.5.
- Páginas de la RAE no guardadas: DPD *mayúsculas*, DPD *usted*, Libro de estilo, "clase de letra", duda lingüística sobre los emojis y DLE *invaluable*.
- Fundéu en fundeu.es: "poner en valor" y "escalar" solo se han cotejado en copias de prensa; "de cara a" y "severo" (Vademécum), "tomar lugar", las muletillas "cabe destacar" y "en este sentido" y el abuso de la pasiva no se han cotejado.

### 7.6 Aviso de privacidad

**Propuesta original.** Ampliar en la Fase 2 `scan_tells.py` para detectar patrones de DNI/NIE, IBAN, teléfono y correo con el único fin de activar el aviso de privacidad.

**Resolución.** Se acepta como requisito futuro, no como implementación actual. El análisis será local, efímero y con biblioteca estándar; no almacenará, registrará ni repetirá en diagnósticos los valores personales encontrados. La salida incluirá solo la categoría y la ubicación mínima necesaria para localizar el aviso. La ausencia de hallazgos heurísticos no garantiza que el texto carezca de datos personales o sensibles. Se mantienen la confirmación del usuario y el aviso de valorar un modelo local; la skill no recogerá datos personales nuevos.

### 7.7 Carga progresiva y presupuesto de reglas

**Propuesta original.** Fijar un tope de patrones activos en `patrones.md`, siguiendo el presupuesto de reglas de kjm.

**Resolución.** Se aceptan la carga progresiva y un mecanismo de presupuesto de reglas activas. El límite numérico se difiere hasta medir el contexto y los resultados reales en las Fases 2 y 3: no hay evidencia para fijar ahora un tope. Las reglas duras conservan siempre la prioridad y no se descartan patrones del catálogo ni salvaguardas para encajar en el presupuesto.

## 8. Implicaciones para `scan_tells.py`

| Bloque | Qué hace | Patrones |
|---|---|---|
| Entrada y enmascarado | Archivo o stdin. Enmascara frontmatter, bloques y código en línea, URL, rutas, citas entre comillas («», “”, "") y `[[claim]]…[[/claim]]`, conservando las posiciones para dar número de línea | Regla 3 |
| Vocabulario | Lee `vocabulario-es.md` bajo un encabezado fijo, una expresión por línea, con nivel y familia. Compara sin mayúsculas ni tildes (`unicodedata`, NFD). Informa línea, columna, nivel y familia, y densidad por mil palabras y por párrafo | P12, P31, P33-P36, P44, P65 |
| Rayas | Clasifica: diálogo, inciso cerrado, raya a la inglesa (espaciada, sin cierre o pegada a las dos palabras) y raya en encabezado. Ignora guion y semirraya en intervalos numéricos. Recuento por tipo y por mil palabras | P08 |
| Comillas | Mezcla de tipos en el mismo nivel; anidamiento invertido | P55 |
| Encabezados | Title Case (proporción de palabras con mayúscula no inicial, sin palabras funcionales, siglas ni palabras en mayúsculas), encabezados en pregunta, saltos de nivel, encabezados vacíos, `---` entre todas las secciones | P20, P53, P54 |
| Estructuras | Expresiones regulares para "no solo… sino", "no se trata de… sino/se trata de", "no es X, es Y", "tanto si… como si", "ya seas… o", enumeración mecánica y conectores al inicio de párrafo; tríadas probables de adjetivos, siempre como "probable" | P01, P06, P37-P39, P41 |
| Deterministas | Marcado filtrado (`oaicite`, `turn0search0`…), UTM de IA (solo aviso), marcadores de posición, invisibles (U+200B, U+200C, U+200D, U+2060, U+FEFF en mitad del texto, U+00AD) y homoglifos. Excluye U+00A0 y U+202F, legítimos en español | P59-P62 |
| Tipografía | ? y ! sin ¿ ni ¡; mayúscula tras dos puntos; exclamaciones por mil palabras | P56-P58 |
| Registro y variante | Recuento de formas de tú y usted, de vosotros y ustedes; lista corta de léxico americano. Solo aviso | P64 |
| `--original` | Extrae y normaliza cifras (`1.000`, `1 000`, `1000`; `3,5`, `3.5`; ante la ambigüedad, las dos lecturas), porcentajes (`50 %`, `50%`, "por ciento"), fechas en español ("12 de marzo de 2024", "marzo de 2024", dd/mm/aaaa), precios (€, EUR, euros), duraciones y unidades ("48 h", "50 ml"), códigos y referencias, siglas e INCI en mayúsculas, nombres propios, URL, claims marcados y citas (literales). Informa de lo que falta y de lo nuevo, a diferencia de Aboudjem, que solo informa de lo perdido ([facts.js:178][abj-facts]). Compara también los recuentos de tú/usted | Reglas 1, 2 y 3 |
| Candidatos a claim | Marca frases con los marcadores de la heurística de `claims.md`, que incorpora los de [estudio.md](estudio.md) §10.5; la decisión es del modelo o del usuario | P30; regla 2 |
| Aviso de privacidad (Fase 2) | Detectará patrones de DNI/NIE, IBAN, teléfono y correo de forma local y efímera. Informará solo de categoría y ubicación mínima, sin almacenar, registrar ni repetir el valor. La ausencia de hallazgos no certificará que el texto sea seguro | Regla 6; §7.6 |
| Salida | JSON estable (`sort_keys`, sin marcas de tiempo). Código de salida 1 si falta o aparece un dato o cambia un claim marcado. Sin puntuación de "probabilidad de IA" y sin métricas de ritmo en v1 | Regla 4 |
| Tests | Primero hechos y claims; formatos de cifras españoles; un conjunto de prosa humana española que no debe dar hallazgos bloqueantes | §7.6 del estudio |

La carga progresiva y el presupuesto de reglas activas de §7.7 pertenecen a `SKILL.md` y a la selección contextual de sus referencias. No reducen la cobertura determinista de `scan_tells.py` ni ninguna regla dura o salvaguarda.

[bl]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md
[bl-agents]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/AGENTS.md#L24
[i92]: https://github.com/blader/humanizer/issues/92
[p151]: https://github.com/blader/humanizer/blob/0894b08f5604f2fa2bf7feada21fc6f9d96be9a5/references/patrones-espanol.md
[aa-skill]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/SKILL.md
[aa-banned]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/banned-list.md
[aa-rewrites]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/rewrites.md
[aa-dtells]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-tells.md
[aa-drew]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-rewrites.md
[aa-strict]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/strict-review.md
[aa-examples]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/examples.md
[aa-personal]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/anti-ai-writing.md
[adw]: https://github.com/adewale/anti-slop-writing/blob/53370ff70b6d1da376e053cf144d39dca8d64f9e/skills/anti-slop-writing/SKILL.md
[kjm]: https://github.com/kjmagnan1s/anti-slop/blob/a3807e5d9030738eb66cb61df47844e87963cc43/SKILL.md
[hum]: https://github.com/vicentealvarezasencio/humanamente/blob/1447b618301e4b17dc5f88335128ca2522964ca1/SKILL.md
[hum-readme]: https://github.com/vicentealvarezasencio/humanamente/blob/1447b618301e4b17dc5f88335128ca2522964ca1/README.md
[hes]: https://github.com/mattc95/Humanizer-es/blob/2883d4915df5b51114280d087a4a4195f40caf2a/SKILL.md
[ads]: https://github.com/adelaidasofia/humanizer/blob/9c764db0e7331f27f803522205f01c78a0a67ed1/SKILL.md
[nte]: https://github.com/dorelysm/naturalizacion-texto-es/blob/7eaba75f50678343263a17ace92bf09dff9af876/.claude/skills/naturalizacion-texto-ia/SKILL.md
[abj-facts]: https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/cli/lib/facts.js#L178
[storyscope]: https://arxiv.org/abs/2604.03136v6
[u1]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/README.md#L131-L159
[u2]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L205
[u3]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L289
[u4]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L302
[u5]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L358
[u6]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/examples.md
[u7]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/rewrites.md#L220
[u8]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/rewrites.md#L209
[u9]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/rewrites.md#L236-L243
[u10]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-rewrites.md#L148
[u11]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-tells.md#L130
[u12]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-rewrites.md#L195
[u13]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/SKILL.md#L186
[u14]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-rewrites.md#L84-L94
[u15]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/banned-list.md#L143-L144
[u16]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/rewrites.md#L190-L191
[u17]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/rewrites.md#L42
[u18]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L254
[u19]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L245
[u20]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L210
[u21]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L267
[u22]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L171
[u23]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/anti-ai-writing.md#L250
[u24]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/banned-list.md#L109
[u25]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/banned-list.md#L115
[u26]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/anti-ai-writing.md#L203
[u27]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/anti-ai-writing.md#L207
[u28]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L161
[u29]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L293
[u30]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L50
[u31]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L38
[u32]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/rewrites.md#L231
[u33]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/anti-ai-writing.md#L251
[u34]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-tells.md#L231
[u35]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-tells.md#L174
[u36]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-rewrites.md#L208
[u37]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-rewrites.md#L211
[u38]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/skills/anti-ai-writing/references/discourse-rewrites.md#L245-L251
[u39]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L36
[u40]: https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md#L44
[u41]: https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/SKILL.md#L419
[u42]: https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/cli/lib/metrics.js
[u43]: https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/SKILL.md#L279
[u44]: https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/SKILL.md#L293
[u45]: https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/SKILL.md#L296
[u46]: https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/SKILL.md#L310
[u47]: https://github.com/mattc95/Humanizer-es/blob/2883d4915df5b51114280d087a4a4195f40caf2a/SKILL.md#L441-L455
[u48]: https://github.com/ToniPerea/humanizar-texto-es/blob/da5388524250b72d59c15038813813c7b6adb0e8/SKILL.md#L118-L140
[u49]: https://github.com/avectats7/anti-ai-writing/blob/eeb42e5127d844d06568b15b198b23c4a8339d88/.claude-plugin/plugin.json#L14
[skill]: ../skill/prosa-natural/SKILL.md
