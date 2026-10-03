#!/usr/bin/env python3
"""Escáner determinista de rasgos de texto generado, para la skill
``prosa-natural``.

Qué hace y qué no hace
-----------------------
Este script es una pasada previa barata y determinista. Solo informa: nunca
reescribe el texto de entrada, nunca decide por sí solo qué hacer con un
hallazgo, y nunca calcula una puntuación de "probabilidad de IA" ni ninguna
métrica de ritmo o "burstiness". Es opcional para el flujo de la skill: si el
entorno no puede ejecutar código, la skill sigue funcionando solo con el
criterio del modelo. Todo lo que reporta son datos (línea, columna, nivel,
familia, densidad); la decisión de cortar, reformular o dejar el texto como
está es siempre de quien revisa.

Restricciones duras
--------------------
Solo biblioteca estándar de Python, sin red y sin paquetes de terceros. El
código es compatible con la sintaxis de Python 3.9+ (nada de ``match`` ni de
uniones de tipos ``X | Y`` evaluadas en tiempo de ejecución).

Contrato de formato de ``references/vocabulario-es.md``
---------------------------------------------------------
Este script parsea ese archivo con la biblioteca estándar (sin YAML ni CSV de
terceros), así que el formato es estricto y se repite aquí porque el
docstring debe seguir exactamente las mismas reglas que documenta el propio
archivo (ver su sección "Formato"):

- Solo existen dos encabezados de nivel, escritos tal cual: ``## Fuerte`` y
  ``## Débil``. El parseo no empieza hasta encontrar el primero de los dos.
  Una vez dentro, cualquier otro encabezado ``##`` (que no sea exactamente
  uno de esos dos) cierra la región que se parsea: todo lo que venga después
  se ignora, sin error, aunque no tenga formato de entrada.
- Dentro de un nivel, cada familia es un encabezado ``### <nombre>``. Puede
  ir seguida de una o dos líneas de motivo que empiezan por ``> ``; esas
  líneas se saltan, no son entradas.
- Cada línea de contenido no vacía que no empiece por ``#`` ni por ``> `` es
  una entrada: ``expresión | AAAA-MM-DD | origen``, con un cuarto campo
  opcional ``pendiente``. Los campos van separados exactamente por
  ``" | "`` (espacio, barra vertical, espacio). La fecha se valida como
  fecha de calendario real (no solo por forma). Una línea que no cumpla
  este formato, con fecha inválida, con un cuarto campo distinto de
  ``pendiente``, o con una entrada fuera de toda familia activa, es
  malformada: el script aborta con código de salida 2 y un mensaje en
  stderr con el archivo y el número de línea exactos.
- El asterisco ``*`` solo se admite una vez y al final de una palabra, como
  comodín de letras (por ejemplo, ``optimiz*``).
- Se permiten líneas en blanco entre entradas y entre bloques.
- La comparación con el texto de entrada es insensible a mayúsculas y a
  tildes: se normaliza con Unicode NFD y se eliminan las marcas de
  combinación, y solo se buscan coincidencias en límites de palabra
  (``\\w`` con soporte Unicode). Esto afecta a cómo busca el script, nunca a
  cómo se escribe la entrada en el archivo de vocabulario.
- Un archivo que no se puede leer, que no es UTF-8 válido, o que no
  contiene ninguna entrada válida (por no tener las regiones ``## Fuerte``
  / ``## Débil``, o por tenerlas vacías) también aborta con código de
  salida 2; en estos casos el error es del archivo completo, no de una
  línea concreta, así que el mensaje no incluye ningún número de línea.

El campo ``pendiente`` marca que la base normativa de esa entrada está sin
verificar en fuente primaria; mientras lo esté, el script se limita a
reportarla igual que cualquier otra entrada débil, nunca la trata como una
regla ya establecida ni la usa para corregir nada automáticamente.

Hallazgos que se solapan en el mismo tramo de texto (por ejemplo, la
colocación "pilar fundamental" y la palabra suelta "fundamental" dentro de
ella) se reducen a uno solo: gana el tramo más largo: empate por nivel
(Fuerte sobre Débil); empate por orden alfabético de la expresión. La
densidad de vocabulario solo cuenta los hallazgos que sobreviven a esta
resolución.

Claves del informe JSON y qué vista del texto usa cada una
------------------------------------------------------------
``entrada`` y ``enmascarado`` describen el texto de entrada y el
enmascarado aplicado. ``vocabulario`` y ``registro`` buscan sobre el texto
con el frontmatter, el código, las URL, los ``[[claim]]…[[/claim]]`` Y las
citas entre comillas enmascarados (para no marcar como propia una palabra
que en realidad está dentro de una cita textual). ``rayas``, ``comillas``,
``encabezados`` y ``tipografia`` son los detectores de forma: buscan sobre
una vista distinta, con el frontmatter, el código, las URL y los
``[[claim]]…[[/claim]]`` enmascarados pero las comillas SIN enmascarar,
porque necesitan ver los propios caracteres de puntuación (comillas,
rayas, mayúsculas) para poder analizarlos; ``tipografia`` además enmascara
aparte la sintaxis de imagen Markdown antes de contar exclamaciones.
Ninguno de estos aplica un umbral ni emite un veredicto: solo reportan
hechos (tipo, ubicación y, donde corresponde, densidad por mil palabras).

``estructuras`` busca regex de contraste, simetría, enumeración mecánica,
conectores al inicio de párrafo y tríadas probables de adjetivos sobre la
misma vista que ``vocabulario`` (frontmatter, código, URL, claims y citas
enmascarados); toda tríada se etiqueta siempre como "probable" porque un
escáner determinista no puede confirmar la categoría gramatical.
``deterministas`` busca marcado de chatbot filtrado, parámetros UTM de IA,
marcadores de posición, caracteres invisibles y homoglifos sobre una vista
propia que enmascara frontmatter y código pero deja las URL visibles (para
poder leer sus parámetros); nunca corre dentro de un bloque de código ni
del frontmatter. ``registro`` cuenta formas de tú/usted, de vosotros/ustedes
y un léxico americano corto: es solo aviso, nunca corrige ni reformula
nada, y "ustedes" en solitario no se trata como error.

``candidatos_claim`` (siempre presente) señala frases con marcadores de
eficacia, salud o seguridad (verbos de eficacia, duraciones, "clínicamente
probado", "dermatológicamente probado/testado", "hipoalergénico", "sin X",
"no testado en animales", "natural" + efecto, referencias a estudios,
autoevaluaciones de calidad y CUALQUIER porcentaje, sin restringirlo a
contextos de eficacia): solo marca candidatos, nunca decide si son un
claim ni los reformula; esa decisión es de quien revisa o del modelo. El
texto ya protegido con ``[[claim]]…[[/claim]]`` no se cuenta aquí (queda en
blanco en ``masked_text``); su recuento aparte está en la clave
``marcados``.

``privacidad`` (siempre presente) detecta DNI/NIE (con la letra de control
cuando es barato comprobarla), IBAN español (con el dígito de control
ISO 7064), teléfonos españoles y correos electrónicos, sobre una vista que
enmascara frontmatter y código pero deja visibles las URL y las comillas.
Es local y efímero: informa solo la categoría y la línea, JAMÁS el valor
encontrado, y no lo guarda ni lo registra en ningún sitio; la ausencia de
hallazgos no certifica que el texto esté libre de datos personales.

``comparacion`` (solo presente cuando se pasa ``--original RUTA``) compara
el texto fuente con el texto ya analizado, categoría por categoría: cifras,
porcentajes, fechas, precios, duraciones/unidades, códigos, siglas, nombres
propios, URL, claims marcados y citas literales, señalando en ambas
direcciones lo que falta en el nuevo texto (``faltantes``) y lo que aparece
de nuevo (``nuevas``); también compara los recuentos de tú/usted y
vosotros/ustedes bajo la subclave ``registro``, solo como dato. La
comparación es por presencia de una lectura normalizada, no por
multiconjunto (ver el docstring de ``_diff_by_any_reading``); una cifra
ambigua como "1.500" guarda dos lecturas ("1500" y "1.5") y basta
coincidir con cualquiera de las dos.

Ningún elemento de ``comparacion`` repite jamás un valor que coincida con
un patrón de datos personales (los mismos de ``privacidad``): si el tramo
de un hecho —cifra, código, nombre propio, cita o claim marcado— solapa un
DNI/NIE, un IBAN, un teléfono o un correo, sus campos ``texto`` y
``lecturas`` se sustituyen por un marcador (``"[dato personal:
<categoría>]"`` y ``[]``), conservando categoría, línea y columna; el
elemento se sigue contando igual, así que un dato personal que cambia
entre los dos textos sigue produciendo código de salida 1, solo se oculta
el valor.

Códigos de salida: 2 en errores de uso, de lectura de archivo o de
vocabulario (antes de imprimir cualquier JSON); 1 cuando se pasa
``--original`` y falta o aparece nuevo algún dato de las categorías
bloqueantes (cifras, porcentajes, fechas, precios, duraciones/unidades,
códigos, nombres propios, URL, claims marcados o citas) — las siglas y el
aviso de registro tú/usted son solo informativos y nunca cambian el código
de salida; 0 en cualquier otro caso, incluida la ejecución sin
``--original``.
"""

import argparse
import bisect
import datetime
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

VERSION = 1

DEFAULT_VOCAB_PATH = (
    Path(__file__).resolve().parent.parent / "references" / "vocabulario-es.md"
)

NIVELES_VALIDOS = ("Fuerte", "Débil")


# ---------------------------------------------------------------------------
# Vocabulario: modelo de datos y parser
# ---------------------------------------------------------------------------


class VocabParseError(Exception):
    """Error de formato al parsear ``vocabulario-es.md`` (o equivalente).

    Se informa con archivo y número de línea siempre que el error señale una
    línea concreta, para que el mensaje en stderr permita localizar y
    corregir la entrada sin ambigüedad. Cuando el fallo es del archivo
    completo (no se pudo leer, o no es UTF-8 válido) ``line`` es ``None`` y
    el mensaje no menciona ningún número de línea, para no sugerir de forma
    engañosa que el problema está en una línea concreta (por ejemplo, no se
    informa como "línea 0").
    """

    def __init__(self, path, line, message):
        self.path = path
        self.line = line
        self.message = message
        if line is None:
            text = "{}: {}".format(path, message)
        else:
            text = "{}:{}: {}".format(path, line, message)
        super().__init__(text)


@dataclass
class VocabEntry:
    """Una entrada del vocabulario, ya lista para buscarse en un texto."""

    expresion: str
    nivel: str
    familia: str
    origen: str
    pendiente: bool
    fecha: str
    line: int
    pattern: "re.Pattern" = field(repr=False, compare=False)


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_word_char(ch):
    return re.match(r"\w", ch, re.UNICODE) is not None


def _normalize_for_matching(text):
    """NFD + minúsculas + eliminación de marcas de combinación.

    Usada tanto para normalizar expresiones del vocabulario como para
    normalizar el texto analizado, así que el resultado es comparable.
    """
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def _build_pattern(expresion):
    """Construye el patrón compilado para una expresión del vocabulario.

    Recibe la expresión tal como está escrita en el archivo de vocabulario
    (sin normalizar) y la normaliza aquí mismo con
    ``_normalize_for_matching`` antes de construir el patrón, para que
    coincida con el texto ya normalizado sobre el que se busca (el
    llamador no la normaliza). Además de esa normalización, esta función se
    ocupa de los límites de palabra, del comodín final y de permitir que
    las palabras de una expresión multipalabra se separen por cualquier
    tanda de espacio en blanco (incluido un salto de línea dentro de un
    mismo párrafo).
    """
    normalized = _normalize_for_matching(expresion)
    tokens = re.split(r"\s+", normalized.strip())
    token_patterns = []
    for token in tokens:
        if token.endswith("*") and token.count("*") == 1:
            base = token[:-1]
            token_patterns.append(re.escape(base) + r"\w*")
        else:
            token_patterns.append(re.escape(token))
    body = r"\s+".join(token_patterns)

    first_token = tokens[0]
    last_token = tokens[-1]
    left_boundary = r"\b" if first_token and _is_word_char(first_token[0]) else ""
    if last_token.endswith("*"):
        right_boundary = r"\b"
    else:
        right_boundary = r"\b" if last_token and _is_word_char(last_token[-1]) else ""

    pattern_text = left_boundary + body + right_boundary
    return re.compile(pattern_text, re.UNICODE)


def _validate_expresion_wildcard(expresion, path, line):
    count = expresion.count("*")
    if count == 0:
        return
    if count > 1 or not expresion.endswith("*"):
        raise VocabParseError(
            path, line, "el comodín '*' solo se admite una vez y al final de una palabra"
        )


def parse_vocabulary(path):
    """Parsea un archivo de vocabulario con el contrato descrito arriba.

    Devuelve una lista de :class:`VocabEntry`. Lanza :class:`VocabParseError`
    ante cualquier línea malformada, con el número de línea exacto.
    """
    path = Path(path)
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise VocabParseError(
            path, None, "no se pudo leer el archivo de vocabulario ({})".format(exc)
        )
    except UnicodeDecodeError as exc:
        raise VocabParseError(
            path, None, "el archivo de vocabulario no es UTF-8 válido ({})".format(exc)
        )

    entries = []
    nivel_actual = None
    familia_actual = None
    parsing_active = False

    for lineno, line in enumerate(raw_text.splitlines(), start=1):
        stripped = line.strip()

        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            if heading in NIVELES_VALIDOS:
                nivel_actual = heading
                familia_actual = None
                parsing_active = True
                continue
            if parsing_active:
                # Cualquier otro encabezado de nivel dos cierra la región.
                break
            # Todavía no hemos entrado en una región de nivel: preámbulo.
            continue

        if not parsing_active:
            # Antes del primer "## Fuerte"/"## Débil" todo es preámbulo.
            continue

        if stripped.startswith("### "):
            familia_actual = stripped[4:].strip()
            continue

        if stripped.startswith("> "):
            continue

        if stripped == "":
            continue

        if stripped.startswith("#"):
            # Encabezado de otro nivel (p. ej. "#### algo"); no es una
            # entrada válida dentro de esta región.
            raise VocabParseError(path, lineno, "encabezado inesperado dentro de un nivel")

        # A partir de aquí, la línea debe ser una entrada.
        if familia_actual is None:
            raise VocabParseError(
                path, lineno, "entrada sin una familia '### ...' activa"
            )

        fields = stripped.split(" | ")
        if len(fields) not in (3, 4):
            raise VocabParseError(
                path,
                lineno,
                "formato de entrada inválido (se esperaba "
                "'expresión | AAAA-MM-DD | origen' con un cuarto campo "
                "opcional 'pendiente', separados por ' | ')",
            )

        expresion, fecha, origen = fields[0], fields[1], fields[2]
        pendiente = False
        if len(fields) == 4:
            if fields[3] != "pendiente":
                raise VocabParseError(
                    path, lineno, "el cuarto campo solo puede ser 'pendiente'"
                )
            pendiente = True

        if not expresion:
            raise VocabParseError(path, lineno, "la expresión no puede estar vacía")
        if not _DATE_RE.match(fecha):
            raise VocabParseError(
                path, lineno, "fecha inválida, se esperaba el formato AAAA-MM-DD"
            )
        try:
            datetime.date.fromisoformat(fecha)
        except ValueError:
            raise VocabParseError(
                path, lineno, "fecha inválida, se esperaba el formato AAAA-MM-DD"
            )
        if not origen:
            raise VocabParseError(path, lineno, "el origen no puede estar vacío")

        _validate_expresion_wildcard(expresion, path, lineno)

        entries.append(
            VocabEntry(
                expresion=expresion,
                nivel=nivel_actual,
                familia=familia_actual,
                origen=origen,
                pendiente=pendiente,
                fecha=fecha,
                line=lineno,
                pattern=_build_pattern(expresion),
            )
        )

    if not entries:
        raise VocabParseError(
            path,
            None,
            "el vocabulario está vacío: no contiene los encabezados "
            "'## Fuerte' / '## Débil' con al menos una entrada válida",
        )

    return entries


# ---------------------------------------------------------------------------
# Enmascarado con posiciones preservadas
# ---------------------------------------------------------------------------

# Los ``\r?`` antes de un ``\n`` (o de un ``$`` de fin de línea) hacen que
# estos dos patrones funcionen igual con saltos de línea CRLF que con LF, sin
# tener que normalizar el texto antes (lo que cambiaría longitudes y
# posiciones). También toleran un ``\r`` suelto al final del archivo, sin
# ``\n`` detrás (revisión R3-001).
_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n.*?\n---[ \t]*\r?\n?", re.DOTALL)
_CODE_FENCE_RE = re.compile(
    r"^([`~]{3,})[^\n]*\n.*?^\1[ \t]*\r?$", re.DOTALL | re.MULTILINE
)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_URL_RE = re.compile(r"(?:https?://|www\.)\S+")
_CLAIM_RE = re.compile(r"\[\[claim\]\].*?\[\[/claim\]\]", re.DOTALL)

_QUOTE_PATTERNS = (
    re.compile(r"«[^»]*»"),
    re.compile(r"“[^”]*”"),
    re.compile(r'"[^"]*"'),
    re.compile(r"‘[^’]*’"),
)


def _blank_span(text):
    return "".join(ch if ch == "\n" else " " for ch in text)


def _mask_pattern(text, pattern):
    return pattern.subn(lambda m: _blank_span(m.group(0)), text)


def find_paragraphs(text):
    """Devuelve los tramos (inicio, fin) de cada párrafo, en offsets de
    carácter del propio ``text``. Un párrafo es una tanda de líneas no
    vacías; una línea en blanco (solo espacio) separa párrafos. El tramo
    incluye los saltos de línea internos entre las líneas del párrafo, para
    que las expresiones multipalabra puedan cruzar un salto de línea dentro
    del mismo párrafo, pero nunca una línea en blanco.
    """
    paragraphs = []
    idx = 0
    para_start = None
    para_end = None
    for raw_line in text.split("\n"):
        line_len = len(raw_line)
        if raw_line.strip() != "":
            if para_start is None:
                para_start = idx
            para_end = idx + line_len
        else:
            if para_start is not None:
                paragraphs.append((para_start, para_end))
                para_start = None
                para_end = None
        idx += line_len + 1
    if para_start is not None:
        paragraphs.append((para_start, para_end))
    return paragraphs


def _mask_quotes(text):
    paragraphs = find_paragraphs(text)
    spans = []
    for p_start, p_end in paragraphs:
        sub = text[p_start:p_end]
        for pattern in _QUOTE_PATTERNS:
            for m in pattern.finditer(sub):
                spans.append((p_start + m.start(), p_start + m.end()))
    if not spans:
        return text, 0
    chars = list(text)
    for start, end in spans:
        for i in range(start, end):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars), len(spans)


def mask_text(text):
    """Enmascara frontmatter, bloques de código, código en línea, URL,
    spans ``[[claim]]…[[/claim]]`` y comillas emparejadas dentro de un
    párrafo, sustituyendo cada carácter (salvo saltos de línea) por un
    espacio para conservar línea y columna exactas.

    Devuelve tres valores: ``masked_text`` (con las comillas también
    enmascaradas; es el texto sobre el que busca el analizador de
    vocabulario, para no marcar una cita textual como si fuera prosa
    propia), ``surface_text`` (igual pero SIN enmascarar las comillas, para
    los detectores de forma —rayas, comillas, encabezados, tipografía— que
    necesitan ver los caracteres de puntuación tal cual están escritos) y
    ``counts`` (recuento de regiones enmascaradas por tipo).
    """
    counts = {}
    text, counts["frontmatter"] = _mask_pattern(text, _FRONTMATTER_RE)
    text, counts["bloques_codigo"] = _mask_pattern(text, _CODE_FENCE_RE)
    text, counts["codigo_en_linea"] = _mask_pattern(text, _INLINE_CODE_RE)
    text, counts["url"] = _mask_pattern(text, _URL_RE)
    text, counts["claim"] = _mask_pattern(text, _CLAIM_RE)
    surface_text = text
    text, counts["comillas"] = _mask_quotes(text)
    return text, surface_text, counts


# ---------------------------------------------------------------------------
# Normalización con mapa de posiciones (para línea/columna correctas)
# ---------------------------------------------------------------------------


def _build_normalized_index(text):
    """Normaliza ``text`` (NFD, minúsculas, sin marcas de combinación) y
    construye los mapas de posición necesarios para volver a las
    coordenadas originales.

    Devuelve ``(normalized_text, orig_index_for_normpos, norm_start_for_orig)``:

    - ``orig_index_for_normpos[i]``: índice en ``text`` del carácter
      original que produjo el carácter normalizado en la posición ``i``.
    - ``norm_start_for_orig[i]``: posición en el texto normalizado que
      corresponde al inicio del carácter original ``i`` (longitud
      ``len(text) + 1`` para poder mapear también el final de un tramo).
    """
    normalized_chars = []
    orig_index_for_normpos = []
    norm_start_for_orig = [0] * (len(text) + 1)

    for orig_idx, ch in enumerate(text):
        norm_start_for_orig[orig_idx] = len(normalized_chars)
        decomposed = unicodedata.normalize("NFD", ch.lower())
        for dch in decomposed:
            if unicodedata.combining(dch):
                continue
            normalized_chars.append(dch)
            orig_index_for_normpos.append(orig_idx)
    norm_start_for_orig[len(text)] = len(normalized_chars)

    return "".join(normalized_chars), orig_index_for_normpos, norm_start_for_orig


def _build_line_index(text):
    """Offsets (0-based) de inicio de cada línea, para bisect."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def _line_col(line_starts, orig_idx):
    line_no = bisect.bisect_right(line_starts, orig_idx)
    column = orig_idx - line_starts[line_no - 1] + 1
    return line_no, column


# ---------------------------------------------------------------------------
# Conteo de palabras y párrafos
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"\w+", re.UNICODE)


def _count_words(text):
    return len(_WORD_RE.findall(text))


# ---------------------------------------------------------------------------
# Contexto de análisis compartido entre analizadores
# ---------------------------------------------------------------------------


@dataclass
class AnalysisContext:
    original_text: str
    masked_text: str
    surface_text: str
    deterministas_text: str
    mask_counts: Dict[str, int]
    vocab_entries: List[VocabEntry]
    paragraphs: List[Tuple[int, int]]
    surface_paragraphs: List[Tuple[int, int]]
    line_starts: List[int]
    normalized_text: str
    orig_index_for_normpos: List[int]
    norm_start_for_orig: List[int]
    total_words: int


def _mask_for_deterministas(text):
    """Vista para el analizador ``deterministas``: enmascara frontmatter y
    código (bloques e inline), pero deja las URL visibles, porque ese
    analizador necesita leer sus parámetros ``utm_*`` (P62). No enmascara
    comillas ni ``[[claim]]…[[/claim]]``: las marcas de chatbot filtradas,
    los marcadores de posición, los caracteres invisibles y los homoglifos
    pueden aparecer dentro de una cita o de un claim y siguen siendo el
    mismo dato técnico a reportar.
    """
    text, _ = _mask_pattern(text, _FRONTMATTER_RE)
    text, _ = _mask_pattern(text, _CODE_FENCE_RE)
    text, _ = _mask_pattern(text, _INLINE_CODE_RE)
    return text


def _build_context(text, vocab_entries):
    masked_text, surface_text, mask_counts = mask_text(text)
    deterministas_text = _mask_for_deterministas(text)
    paragraphs = find_paragraphs(masked_text)
    surface_paragraphs = find_paragraphs(surface_text)
    line_starts = _build_line_index(text)
    normalized_text, orig_index_for_normpos, norm_start_for_orig = _build_normalized_index(
        masked_text
    )
    total_words = _count_words(masked_text)
    return AnalysisContext(
        original_text=text,
        masked_text=masked_text,
        surface_text=surface_text,
        deterministas_text=deterministas_text,
        mask_counts=mask_counts,
        vocab_entries=vocab_entries,
        paragraphs=paragraphs,
        surface_paragraphs=surface_paragraphs,
        line_starts=line_starts,
        normalized_text=normalized_text,
        orig_index_for_normpos=orig_index_for_normpos,
        norm_start_for_orig=norm_start_for_orig,
        total_words=total_words,
    )


# ---------------------------------------------------------------------------
# Analizador: entrada
# ---------------------------------------------------------------------------


def analyze_entrada(ctx):
    lineas = ctx.original_text.count("\n")
    if ctx.original_text and not ctx.original_text.endswith("\n"):
        lineas += 1
    return {
        "lineas": lineas,
        "palabras": ctx.total_words,
        "parrafos": len(ctx.paragraphs),
    }


# ---------------------------------------------------------------------------
# Analizador: enmascarado
# ---------------------------------------------------------------------------


def analyze_enmascarado(ctx):
    return dict(ctx.mask_counts)


# ---------------------------------------------------------------------------
# Analizador: vocabulario (hallazgos + densidad)
# ---------------------------------------------------------------------------


def _ranges_overlap(a_inicio, a_fin, b_inicio, b_fin):
    """True si los tramos ``[a_inicio, a_fin)`` y ``[b_inicio, b_fin)``
    comparten al menos una posición.

    Aislada como función propia (revisión de la slice 04, A1) para que un
    test determinista pueda contar cuántas veces se invoca esta
    comparación, en vez de medir un límite de tiempo de reloj: si la
    resolución de solapamientos comparase párrafos entre sí en lugar de
    acotarse a cada párrafo, el número de llamadas crecería de forma
    cuadrática y el test lo detectaría sin depender del reloj.
    """
    return a_inicio < b_fin and b_inicio < a_fin


def _resolve_overlapping_hits(raw_hits):
    """Descarta hallazgos solapados, quedándose con uno solo por tramo.

    Dos hallazgos "solapan" cuando sus tramos de carácter en el texto
    original comparten al menos una posición (por ejemplo, la colocación
    "pilar fundamental" y la palabra suelta "fundamental" que cae dentro de
    ella). Ante un solapamiento se aplica, en este orden: el tramo más
    largo; si empatan en longitud, el nivel más alto (Fuerte antes que
    Débil); si también empatan, la expresión por orden alfabético (revisión
    R3-005). La densidad se calcula después, solo sobre los hallazgos que
    sobreviven a esta resolución.

    Revisión review-faf981a2b76764c9 (R4-002): dos hallazgos solo pueden
    solapar si están en el mismo párrafo (cada uno se busca ya acotado a su
    propio párrafo en ``_find_vocabulary_hits``), así que la resolución se
    hace párrafo a párrafo en vez de comparar cada hallazgo contra todos los
    ya aceptados en el documento entero; el resultado no cambia, solo el
    coste.
    """
    hits_by_parrafo = {}
    for h in raw_hits:
        hits_by_parrafo.setdefault(h["_parrafo"], []).append(h)

    kept = []
    for grupo in hits_by_parrafo.values():
        ordered = sorted(
            grupo,
            key=lambda h: (
                -(h["_fin"] - h["_inicio"]),
                NIVELES_VALIDOS.index(h["nivel"]),
                h["expresion"],
            ),
        )
        covered = []
        for h in ordered:
            inicio, fin = h["_inicio"], h["_fin"]
            if any(_ranges_overlap(inicio, fin, c_inicio, c_fin) for c_inicio, c_fin in covered):
                continue
            covered.append((inicio, fin))
            kept.append(h)
    return kept


def _find_vocabulary_hits(ctx):
    raw_hits = []
    for entry in ctx.vocab_entries:
        for p_start, p_end in ctx.paragraphs:
            n_start = ctx.norm_start_for_orig[p_start]
            n_end = ctx.norm_start_for_orig[p_end]
            if n_start >= n_end:
                continue
            for m in entry.pattern.finditer(ctx.normalized_text, n_start, n_end):
                orig_inicio = ctx.orig_index_for_normpos[m.start()]
                orig_fin = ctx.orig_index_for_normpos[m.end() - 1] + 1
                line_no, column = _line_col(ctx.line_starts, orig_inicio)
                raw_hits.append(
                    {
                        "expresion": entry.expresion,
                        "nivel": entry.nivel,
                        "familia": entry.familia,
                        "origen": entry.origen,
                        "pendiente": entry.pendiente,
                        "linea": line_no,
                        "columna": column,
                        "_inicio": orig_inicio,
                        "_fin": orig_fin,
                        "_parrafo": p_start,
                    }
                )

    hits = _resolve_overlapping_hits(raw_hits)
    for h in hits:
        del h["_inicio"]
        del h["_fin"]
        del h["_parrafo"]
    hits.sort(key=lambda h: (h["linea"], h["columna"], h["expresion"]))
    return hits


def _paragraph_word_counts(ctx):
    return [_count_words(ctx.masked_text[start:end]) for start, end in ctx.paragraphs]


def analyze_vocabulario(ctx):
    hits = _find_vocabulary_hits(ctx)
    densidad = _compute_density(ctx, hits)
    return {"hallazgos": hits, "densidad": densidad}


def _compute_density(ctx, hits):
    """Densidad por nivel, por familia y por párrafo.

    Cada hallazgo se asigna a su párrafo por offset real de carácter (no
    por una heurística de número de línea), reconstruyendo ese offset a
    partir de la línea/columna ya calculada para el hallazgo. Línea y
    columna identifican un único carácter, así que la reconstrucción es
    exacta.
    """
    total_words = ctx.total_words

    por_nivel = {}
    for nivel in NIVELES_VALIDOS:
        ocurrencias = sum(1 for h in hits if h["nivel"] == nivel)
        por_mil = round(ocurrencias / total_words * 1000, 3) if total_words else 0.0
        por_nivel[nivel] = {"ocurrencias": ocurrencias, "por_mil_palabras": por_mil}

    por_familia = {}
    for h in hits:
        familia = h["familia"]
        datos = por_familia.setdefault(
            familia, {"nivel": h["nivel"], "ocurrencias": 0, "por_mil_palabras": 0.0}
        )
        datos["ocurrencias"] += 1
    for datos in por_familia.values():
        datos["por_mil_palabras"] = (
            round(datos["ocurrencias"] / total_words * 1000, 3) if total_words else 0.0
        )

    paragraph_word_counts = _paragraph_word_counts(ctx)

    # Asignar cada hallazgo a un párrafo por offset real: reconstruimos el
    # offset original de cada hallazgo buscando su línea/columna contra
    # line_starts (inverso de _line_col), que es exacto porque línea y
    # columna identifican un único carácter.
    def _offset_for(line_no, column):
        return ctx.line_starts[line_no - 1] + column - 1

    hit_offsets = [_offset_for(h["linea"], h["columna"]) for h in hits]

    por_parrafo = []
    for idx, (p_start, p_end) in enumerate(ctx.paragraphs):
        line_no, _col = _line_col(ctx.line_starts, p_start)
        conteo_por_nivel = {nivel: 0 for nivel in NIVELES_VALIDOS}
        for h, offset in zip(hits, hit_offsets):
            if p_start <= offset < p_end:
                conteo_por_nivel[h["nivel"]] += 1
        por_parrafo.append(
            {
                "linea_inicio": line_no,
                "palabras": paragraph_word_counts[idx],
                "por_nivel": conteo_por_nivel,
            }
        )

    return {
        "por_nivel": por_nivel,
        "por_familia": por_familia,
        "por_parrafo": por_parrafo,
    }


# ---------------------------------------------------------------------------
# Analizador: encabezados Markdown (usado también por el de rayas, para
# saber qué líneas son encabezados y tratar sus rayas aparte)
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
_HR_RE = re.compile(r"^-{3,}[ \t]*\r?$", re.MULTILINE)

_PALABRAS_FUNCIONALES = {
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante",
    "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según",
    "sin", "so", "sobre", "tras", "el", "la", "los", "las", "un", "una",
    "unos", "unas", "y", "e", "o", "u", "que", "pero", "sino", "aunque",
    "si", "del", "al", "ni",
}

_PALABRA_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)


def _iter_headings(ctx):
    """Encabezados ATX (``#`` a ``######``) de ``surface_text``, ignorando
    el frontmatter y los bloques de código (ya enmascarados a espacios, así
    que un ``#`` de un comentario de código ya no puede coincidir).
    Devuelve cada encabezado con su nivel, su texto y el offset de carácter
    de inicio de línea, tolerando un ``\\r`` final de línea (CRLF).
    """
    headings = []
    offset = 0
    for raw_line in ctx.surface_text.split("\n"):
        line = raw_line[:-1] if raw_line.endswith("\r") else raw_line
        m = _HEADING_RE.match(line)
        if m:
            headings.append(
                {
                    "nivel": len(m.group(1)),
                    "texto": (m.group(2) or "").strip(),
                    "offset": offset,
                }
            )
        offset += len(raw_line) + 1
    return headings


def _is_eligible_word(word):
    if word.isupper() and len(word) > 1:
        return False  # sigla o acrónimo: nunca cuenta como Title Case
    return word.lower() not in _PALABRAS_FUNCIONALES


def _title_case_ratio(heading_text):
    """Proporción de palabras con mayúscula no inicial sobre las palabras
    elegibles (se excluyen la primera palabra del encabezado, las palabras
    funcionales y las siglas/acrónimos en mayúsculas). Es solo un dato
    (razón entre 0 y 1); este script no aplica ningún corte.

    Limitación conocida: no se excluyen nombres propios ni marcas
    (detectarlos exigiría un diccionario o NER, fuera del alcance de un
    escáner determinista basado en expresiones regulares); el propio
    modelo debe descartarlos al revisar cada hallazgo.
    """
    palabras = _PALABRA_RE.findall(heading_text)
    if len(palabras) <= 1:
        return {"elegibles": 0, "con_mayuscula_no_inicial": 0, "ratio": 0.0}
    resto = palabras[1:]
    elegibles = [w for w in resto if _is_eligible_word(w)]
    con_mayuscula = [w for w in elegibles if w[:1].isupper()]
    ratio = round(len(con_mayuscula) / len(elegibles), 3) if elegibles else 0.0
    return {
        "elegibles": len(elegibles),
        "con_mayuscula_no_inicial": len(con_mayuscula),
        "ratio": ratio,
    }


def analyze_encabezados(ctx):
    headings = _iter_headings(ctx)
    hallazgos = []
    resumen = {
        "total": len(headings),
        "vacios": 0,
        "preguntas": 0,
        "saltos_de_nivel": 0,
        "secciones_sin_separador": 0,
    }
    anterior = None
    for h in headings:
        line_no, column = _line_col(ctx.line_starts, h["offset"])
        vacio = h["texto"] == ""
        es_pregunta = h["texto"].endswith("?")
        salto = anterior is not None and h["nivel"] > anterior["nivel"] + 1
        entrada = {
            "nivel": h["nivel"],
            "texto": h["texto"],
            "linea": line_no,
            "columna": column,
            "vacio": vacio,
            "es_pregunta": es_pregunta,
            "title_case": _title_case_ratio(h["texto"]),
            "salto_de_nivel": salto,
        }
        hallazgos.append(entrada)
        if vacio:
            resumen["vacios"] += 1
        if es_pregunta:
            resumen["preguntas"] += 1
        if salto:
            resumen["saltos_de_nivel"] += 1
        if anterior is not None:
            entre = ctx.surface_text[anterior["offset"]:h["offset"]]
            if not _HR_RE.search(entre):
                resumen["secciones_sin_separador"] += 1
        anterior = h
    return {"hallazgos": hallazgos, "resumen": resumen}


# ---------------------------------------------------------------------------
# Analizador: rayas (—). Clasifica diálogo, inciso cerrado, raya a la
# inglesa y raya en encabezado; ignora guion y semirraya en intervalos
# numéricos porque solo busca el carácter — (U+2014), nunca "-" ni "–".
# ---------------------------------------------------------------------------

_EM_DASH = "—"


def _dash_word_adjacency(linea, idx):
    """Si la raya está pegada (sin separación) a una palabra antes/después.

    Se usa "es carácter de palabra", no "es un espacio", porque una raya de
    cierre española correcta puede ir seguida de una coma o un punto sin
    espacio (``—dijo—, entonces…``) y eso es normativo, no un calco inglés.
    """
    antes = linea[idx - 1] if idx > 0 else None
    despues = linea[idx + 1] if idx + 1 < len(linea) else None
    sin_palabra_antes = antes is None or not _is_word_char(antes)
    sin_palabra_despues = despues is None or not _is_word_char(despues)
    return sin_palabra_antes, sin_palabra_despues


def _raya_estructura(d):
    """Clasifica una raya suelta por su estructura (revisión
    review-faf981a2b76764c9): "apertura" abre un inciso (separada de lo
    anterior por espacio o inicio de línea, pegada a la palabra siguiente);
    "cierre" lo cierra (pegada a la palabra anterior, separada de lo
    siguiente por espacio, puntuación o fin de línea); "pegada" y
    "espaciada" no encajan en ninguna de las dos.
    """
    if d["sin_palabra_antes"] and not d["sin_palabra_despues"]:
        return "apertura"
    if not d["sin_palabra_antes"] and d["sin_palabra_despues"]:
        return "cierre"
    if not d["sin_palabra_antes"] and not d["sin_palabra_despues"]:
        return "pegada"
    return "espaciada"


def _pair_rayas_pendientes(pendientes):
    """Empareja las rayas de un párrafo (que no están al inicio de línea)
    por estructura, no por posición secuencial (revisión
    review-faf981a2b76764c9: el emparejado por índice era voraz y una raya
    espaciada sin cierre podía "robarse" la apertura del inciso correcto
    que venía después en el mismo párrafo).

    Se mantiene como mucho una apertura pendiente: al llegar una raya de
    cierre, se empareja con ella como ``inciso_cerrado``; al llegar
    cualquier otra raya (o al acabar el párrafo) sin haber encontrado
    cierre, la apertura pendiente se reclasifica como ``inciso_sin_cierre``,
    porque en español la raya de cierre se omite cuando el comentario del
    narrador termina la frase o el párrafo (p. ej. "—Ya voy —dijo Marta.");
    esto nunca es una raya a la inglesa. Las rayas "pegada" y "espaciada" se
    reportan siempre sueltas, con su propio subtipo.
    """
    hallazgos = []
    abierta = None
    for d in pendientes:
        estructura = _raya_estructura(d)
        if estructura == "cierre" and abierta is not None:
            hallazgos.append(
                {"tipo": "inciso_cerrado", "linea": abierta["linea"], "columna": abierta["columna"]}
            )
            hallazgos.append(
                {"tipo": "inciso_cerrado", "linea": d["linea"], "columna": d["columna"]}
            )
            abierta = None
            continue
        if abierta is not None:
            hallazgos.append(
                {"tipo": "inciso_sin_cierre", "linea": abierta["linea"], "columna": abierta["columna"]}
            )
            abierta = None
        if estructura == "apertura":
            abierta = d
        elif estructura == "espaciada":
            hallazgos.append(
                {"tipo": "raya_inglesa", "subtipo": "sin_cierre", "linea": d["linea"], "columna": d["columna"]}
            )
        elif estructura == "pegada":
            hallazgos.append(
                {"tipo": "raya_inglesa", "subtipo": "pegada", "linea": d["linea"], "columna": d["columna"]}
            )
        else:  # "cierre" sin ninguna apertura pendiente antes
            hallazgos.append(
                {
                    "tipo": "raya_inglesa",
                    "subtipo": "conector_universal",
                    "linea": d["linea"],
                    "columna": d["columna"],
                }
            )
    if abierta is not None:
        hallazgos.append(
            {"tipo": "inciso_sin_cierre", "linea": abierta["linea"], "columna": abierta["columna"]}
        )
    return hallazgos


def analyze_rayas(ctx):
    heading_lines = {
        _line_col(ctx.line_starts, h["offset"])[0] for h in _iter_headings(ctx)
    }
    text = ctx.surface_text
    hallazgos = []
    for p_start, p_end in ctx.surface_paragraphs:
        pendientes = []
        line_no_inicio, _col = _line_col(ctx.line_starts, p_start)
        for offset_en_parrafo, linea in enumerate(text[p_start:p_end].split("\n")):
            line_no = line_no_inicio + offset_en_parrafo
            if line_no in heading_lines:
                for idx, ch in enumerate(linea):
                    if ch == _EM_DASH:
                        hallazgos.append(
                            {"tipo": "en_encabezado", "linea": line_no, "columna": idx + 1}
                        )
                continue
            for idx, ch in enumerate(linea):
                if ch != _EM_DASH:
                    continue
                columna = idx + 1
                if linea[:idx].strip() == "":
                    hallazgos.append({"tipo": "dialogo", "linea": line_no, "columna": columna})
                    continue
                sin_antes, sin_despues = _dash_word_adjacency(linea, idx)
                pendientes.append(
                    {
                        "linea": line_no,
                        "columna": columna,
                        "sin_palabra_antes": sin_antes,
                        "sin_palabra_despues": sin_despues,
                    }
                )
        hallazgos.extend(_pair_rayas_pendientes(pendientes))

    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    conteo = {}
    for tipo in ("dialogo", "inciso_cerrado", "inciso_sin_cierre", "raya_inglesa", "en_encabezado"):
        n = sum(1 for h in hallazgos if h["tipo"] == tipo)
        conteo[tipo] = {
            "ocurrencias": n,
            "por_mil_palabras": round(n / ctx.total_words * 1000, 3) if ctx.total_words else 0.0,
        }
    return {"hallazgos": hallazgos, "conteo": conteo}


# ---------------------------------------------------------------------------
# Analizador: comillas. Mezcla de tipos en el mismo nivel de anidamiento y
# anidamiento invertido (el orden español es « " ' ' " »). Usa
# ``surface_text`` (comillas sin enmascarar), no ``masked_text``.
# ---------------------------------------------------------------------------

_QUOTE_TYPES = (
    ("angular", re.compile(r"«[^»]*»")),
    ("curly_doble", re.compile(r"“[^”]*”")),
    ("recta_doble", re.compile(r'"[^"]*"')),
    ("curly_simple", re.compile(r"‘[^’]*’")),
)
_QUOTE_RANK = {"angular": 1, "curly_doble": 2, "recta_doble": 2, "curly_simple": 3}
_QUOTE_LABEL = {"angular": "«»", "curly_doble": "“”", "recta_doble": '""', "curly_simple": "‘’"}


def _span_strictly_contains(outer_inicio, outer_fin, inner_inicio, inner_fin):
    """True si el tramo exterior cubre por completo al interior y, además,
    es estrictamente más grande en al menos un extremo (para no tratar dos
    tramos idénticos como si uno anidara al otro).

    Aislada como función propia (revisión de la slice 04, A1) por el mismo
    motivo que ``_ranges_overlap``: permite un test determinista que cuenta
    invocaciones en vez de medir tiempo de reloj.
    """
    contiene = outer_inicio <= inner_inicio and inner_fin <= outer_fin
    contencion_estricta = outer_inicio < inner_inicio or inner_fin < outer_fin
    return contiene and contencion_estricta


def _find_quote_spans(ctx):
    """Encuentra los tramos de comillas y calcula su anidamiento.

    Revisión review-faf981a2b76764c9 (R4-001): dos comillas solo pueden
    anidarse si están en el mismo párrafo (cada tramo se busca ya acotado a
    ``sub = texto[p_start:p_end]``), así que el anidamiento se calcula
    párrafo a párrafo en vez de comparar cada tramo contra todos los del
    documento; el resultado no cambia, solo el coste.
    """
    all_spans = []
    for p_start, p_end in ctx.surface_paragraphs:
        sub = ctx.surface_text[p_start:p_end]
        spans = []
        for tipo, pattern in _QUOTE_TYPES:
            for m in pattern.finditer(sub):
                spans.append({"tipo": tipo, "inicio": p_start + m.start(), "fin": p_start + m.end()})

        for span in spans:
            nivel = 1
            padre = None
            for otro in spans:
                if otro is span:
                    continue
                if _span_strictly_contains(otro["inicio"], otro["fin"], span["inicio"], span["fin"]):
                    nivel += 1
                    if padre is None or (otro["fin"] - otro["inicio"]) < (padre["fin"] - padre["inicio"]):
                        padre = otro
            span["nivel"] = nivel
            span["padre"] = padre
        all_spans.extend(spans)
    return all_spans


def _quotes_mixing(ctx, spans):
    por_nivel = {}
    for s in spans:
        por_nivel.setdefault(s["nivel"], {}).setdefault(s["tipo"], []).append(s)
    hallazgos = []
    for nivel in sorted(por_nivel):
        tipos_presentes = por_nivel[nivel]
        if len(tipos_presentes) <= 1:
            continue
        ubicaciones = []
        for tipo, items in tipos_presentes.items():
            for it in items:
                line_no, col = _line_col(ctx.line_starts, it["inicio"])
                ubicaciones.append({"tipo": _QUOTE_LABEL[tipo], "linea": line_no, "columna": col})
        ubicaciones.sort(key=lambda u: (u["linea"], u["columna"]))
        hallazgos.append(
            {
                "nivel": nivel,
                "tipos": sorted(_QUOTE_LABEL[t] for t in tipos_presentes),
                "ubicaciones": ubicaciones,
            }
        )
    return hallazgos


def _quotes_inverted(ctx, spans):
    hallazgos = []
    for s in spans:
        padre = s["padre"]
        if padre is None:
            continue
        if _QUOTE_RANK[s["tipo"]] < _QUOTE_RANK[padre["tipo"]]:
            line_no, col = _line_col(ctx.line_starts, s["inicio"])
            p_line, p_col = _line_col(ctx.line_starts, padre["inicio"])
            hallazgos.append(
                {
                    "tipo_interior": _QUOTE_LABEL[s["tipo"]],
                    "tipo_exterior": _QUOTE_LABEL[padre["tipo"]],
                    "linea": line_no,
                    "columna": col,
                    "linea_exterior": p_line,
                    "columna_exterior": p_col,
                }
            )
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def analyze_comillas(ctx):
    spans = _find_quote_spans(ctx)
    return {
        "mezcla_de_tipos": _quotes_mixing(ctx, spans),
        "anidamiento_invertido": _quotes_inverted(ctx, spans),
    }


# ---------------------------------------------------------------------------
# Analizador: tipografía. ¿/¡ sin su apertura, mayúscula tras dos puntos en
# prosa corrida y exclamaciones por mil palabras. Usa ``surface_text``, pero
# con la sintaxis de imagen Markdown (``![alt](ruta)``, incluida la forma de
# referencia ``![alt][ref]``) enmascarada aparte: su "!" no es una
# exclamación y no debe contar como "!" sin "¡" (revisión
# review-faf981a2b76764c9).
# ---------------------------------------------------------------------------

# El destino ("(ruta)" o "[ref]") es obligatorio: "![alt]" sin destino no es
# una imagen Markdown real, así que ese destino nunca es opcional (revisión
# de la slice 04, A3). Con el destino opcional, un "!" real seguido de una
# nota a pie de página entre corchetes (p. ej. "¡Por fin![1]") se enmascaraba
# como si fuera una imagen y su "!" de cierre dejaba de contarse.
_MD_IMAGE_RE = re.compile(r"!\[[^\]\n]*\](?:\([^)\n]*\)|\[[^\]\n]*\])")


def _mask_markdown_images(text):
    return _mask_pattern(text, _MD_IMAGE_RE)[0]


def _tipografia_signos(ctx, text):
    hallazgos = []
    for p_start, p_end in ctx.surface_paragraphs:
        sub = text[p_start:p_end]
        abre_interrogacion = False
        abre_exclamacion = False
        for i, ch in enumerate(sub):
            if ch == "¿":
                abre_interrogacion = True
            elif ch == "¡":
                abre_exclamacion = True
            elif ch == "?":
                if abre_interrogacion:
                    abre_interrogacion = False
                else:
                    line_no, col = _line_col(ctx.line_starts, p_start + i)
                    hallazgos.append({"signo": "?", "linea": line_no, "columna": col})
            elif ch == "!":
                if abre_exclamacion:
                    abre_exclamacion = False
                else:
                    line_no, col = _line_col(ctx.line_starts, p_start + i)
                    hallazgos.append({"signo": "!", "linea": line_no, "columna": col})
            elif ch == ".":
                abre_interrogacion = False
                abre_exclamacion = False
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _tipografia_mayuscula_tras_dos_puntos(ctx):
    """Mayúscula tras dos puntos en prosa corrida.

    Salvaguardas (auditoria.md, P57; revisión review-faf981a2b76764c9,
    R2-001): no se informa si los dos puntos introducen una cita textual
    (les sigue directamente una comilla de apertura); no se informa si los
    dos puntos introducen un elemento de lista o un bloque en la línea
    siguiente, de forma explícita: si tras saltarse solo espacios y
    tabulaciones (nunca un salto de línea) no queda ningún carácter en esa
    misma línea, los dos puntos cierran la línea y no hay nada que
    comprobar. La mayúscula debe ser el carácter que sigue a los dos puntos
    y a sus espacios reales; si en ese tramo aparece una región ya
    enmascarada (código, URL, frontmatter, claim), la comprobación se
    detiene ahí en vez de saltársela como si fuera un espacio normal, para
    no comparar contra un carácter que en realidad no está pegado a los dos
    puntos. Tampoco se informa dentro de un encabezado.
    """
    heading_lines = {
        _line_col(ctx.line_starts, h["offset"])[0] for h in _iter_headings(ctx)
    }
    text = ctx.surface_text
    original = ctx.original_text
    hallazgos = []
    for m in re.finditer(":", text):
        idx = m.start()
        line_no_dos_puntos, _col = _line_col(ctx.line_starts, idx)
        if line_no_dos_puntos in heading_lines:
            continue
        j = idx + 1
        region_enmascarada = False
        while j < len(text) and text[j] in (" ", "\t"):
            if original[j] not in (" ", "\t"):
                region_enmascarada = True
                break
            j += 1
        if region_enmascarada:
            continue
        if j >= len(text) or text[j] == "\n":
            continue
        siguiente = text[j]
        if siguiente in "«\"“'":
            continue
        if siguiente.isalpha() and siguiente.isupper():
            line_no, col = _line_col(ctx.line_starts, j)
            hallazgos.append({"linea": line_no, "columna": col})
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def analyze_tipografia(ctx):
    sin_imagenes = _mask_markdown_images(ctx.surface_text)
    total_excl = sin_imagenes.count("!")
    por_mil = round(total_excl / ctx.total_words * 1000, 3) if ctx.total_words else 0.0
    return {
        "signos_sin_apertura": _tipografia_signos(ctx, sin_imagenes),
        "mayuscula_tras_dos_puntos": _tipografia_mayuscula_tras_dos_puntos(ctx),
        "exclamaciones": {"ocurrencias": total_excl, "por_mil_palabras": por_mil},
    }


# ---------------------------------------------------------------------------
# Analizador: estructuras. Regex de contraste y simetría (P01, P39), tríadas
# probables de adjetivos (P06, P41), enumeración mecánica (P38) y
# conectores al inicio de párrafo (P37), sobre ``masked_text`` (frontmatter,
# código, URL, claims y citas textuales ya enmascarados). Solo reporta
# hechos: ubicación y texto encontrado, nunca un umbral ni un veredicto. Una
# construcción correcta en español (p. ej. "no solo… sino también") se
# reporta igual que cualquier otra: el script no decide si es un rasgo de
# IA, eso es criterio del modelo o de quien revisa (auditoria.md P01, P39).
# ---------------------------------------------------------------------------

_NO_SOLO_SINO_RE = re.compile(
    r"\bno\s+solo\b.{0,150}?\bsino\b(?:\s+tambi[ée]n\b)?", re.IGNORECASE | re.DOTALL
)
_NO_SE_TRATA_DE_RE = re.compile(
    r"\bno\s+se\s+trata\s+de\b.{0,150}?\b(?:sino|se\s+trata\s+de)\b",
    re.IGNORECASE | re.DOTALL,
)
_NO_ES_ES_RE = re.compile(
    r"\bno\s+es\s+[^,.\n]{1,80},\s*es\s+[^,.\n]{1,80}", re.IGNORECASE
)
_TANTO_SI_RE = re.compile(
    r"\btanto\s+si\b.{0,80}?\bcomo\s+si\b", re.IGNORECASE | re.DOTALL
)
_YA_SEAS_RE = re.compile(r"\bya\s+se(?:a|as)\b.{0,80}?\bo\b", re.IGNORECASE | re.DOTALL)

_ENUM_INICIO_RE = re.compile(
    r"\ben\s+primer\s+lugar\b|\bprimeramente\b|(?<=[.\n])\s*primero,",
    re.IGNORECASE,
)
_ENUM_MEDIO_RE = re.compile(
    r"\ben\s+segundo\s+lugar\b|\ben\s+tercer\s+lugar\b"
    r"|(?<=[.\n])\s*segundo,|(?<=[.\n])\s*tercero,",
    re.IGNORECASE,
)
_ENUM_FINAL_RE = re.compile(
    r"\bpor\s+último\b|\ben\s+último\s+lugar\b|\bfinalmente\b", re.IGNORECASE
)

# Conectores al inicio de párrafo (P37, "conectores apilados"): un conector
# suelto no es un rasgo (auditoria.md, tabla principal, P37: "un 'sin
# embargo' no es un tic"), así que aquí solo se cuenta, nunca se juzga la
# cadena. Lista derivada de auditoria.md (tabla principal P37/P43, §3 y §4)
# y de los ejemplos del encargo de esta tarea.
_CONECTORES_PARRAFO = (
    "además",
    "asimismo",
    "por otro lado",
    "en conclusión",
    "sin embargo",
    "no obstante",
    "por último",
    "en definitiva",
    "dicho esto",
)

# Adjetivos antepuestos corrientes en el ejemplo de referencia de P06
# («una increíble experiencia única, natural y eficaz», fase2-mapa.md §2.7).
_EPITETOS_ANTEPUESTOS = (
    "increíble",
    "increíbles",
    "extraordinario",
    "extraordinaria",
    "magnífico",
    "magnífica",
    "maravilloso",
    "maravillosa",
    "asombroso",
    "asombrosa",
    "impresionante",
    "excepcional",
)

_TRIADA_RE = re.compile(r"\b(\w+),\s*(\w+)\s+(?:y|e)\s+(\w+)\b", re.IGNORECASE | re.UNICODE)
_TRIADA_EPITETO_RE = re.compile(
    r"\b(?:{})\s+\w+\s+(\w+),\s*(\w+)\s+(?:y|e)\s+(\w+)\b".format(
        "|".join(_EPITETOS_ANTEPUESTOS)
    ),
    re.IGNORECASE | re.UNICODE,
)


def _clip_texto(texto):
    """Recorta un fragmento encontrado a una sola línea legible para el
    JSON: colapsa saltos de línea y espacios repetidos, y acorta si es muy
    largo. Es solo para identificar el hallazgo, nunca material reescrito.
    """
    colapsado = re.sub(r"\s+", " ", texto).strip()
    if len(colapsado) > 120:
        colapsado = colapsado[:117] + "..."
    return colapsado


def _find_regex_hits(text, pattern, line_starts):
    hallazgos = []
    for m in pattern.finditer(text):
        line_no, col = _line_col(line_starts, m.start())
        hallazgos.append({"linea": line_no, "columna": col, "texto": _clip_texto(m.group(0))})
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_enumeracion_mecanica(text, line_starts):
    """Secuencia "en primer lugar… en segundo lugar… por último" (P38).

    Es una construcción legítima en procedimientos y textos jurídicos
    (auditoria.md P38, "puerta de registro"): se reporta como dato, nunca
    como error. Solo se informa si aparecen, en ese orden, un marcador de
    inicio, uno intermedio y uno final.
    """
    inicios = list(_ENUM_INICIO_RE.finditer(text))
    medios = list(_ENUM_MEDIO_RE.finditer(text))
    finales = list(_ENUM_FINAL_RE.finditer(text))
    hallazgos = []
    usados_medio = set()
    usados_final = set()
    for mi in inicios:
        medio = next(
            (mm for mm in medios if mm.start() > mi.start() and id(mm) not in usados_medio),
            None,
        )
        if medio is None:
            continue
        final = next(
            (mf for mf in finales if mf.start() > medio.start() and id(mf) not in usados_final),
            None,
        )
        if final is None:
            continue
        usados_medio.add(id(medio))
        usados_final.add(id(final))
        line_no, col = _line_col(line_starts, mi.start())
        hallazgos.append(
            {
                "linea": line_no,
                "columna": col,
                "marcadores": [
                    _clip_texto(mi.group(0)),
                    _clip_texto(medio.group(0)),
                    _clip_texto(final.group(0)),
                ],
            }
        )
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_conectores_parrafo(ctx):
    """Cuenta, por conector, cuántos párrafos empiezan con él (P37). Solo
    dato: ni un conector suelto ni varios repartidos por el texto son un
    veredicto, es la acumulación lo que el modelo debe valorar.
    """
    conteo = {c: 0 for c in _CONECTORES_PARRAFO}
    ubicaciones = {c: [] for c in _CONECTORES_PARRAFO}
    for p_start, p_end in ctx.paragraphs:
        parrafo = ctx.masked_text[p_start:p_end]
        sin_espacio_inicial = parrafo.lstrip()
        offset_inicial = p_start + (len(parrafo) - len(sin_espacio_inicial))
        normalizado = _normalize_for_matching(sin_espacio_inicial)
        for conector in _CONECTORES_PARRAFO:
            conector_norm = _normalize_for_matching(conector)
            if normalizado.startswith(conector_norm + ","):
                conteo[conector] += 1
                line_no, col = _line_col(ctx.line_starts, offset_inicial)
                ubicaciones[conector].append({"linea": line_no, "columna": col})
                break
    total_words = ctx.total_words
    resultado = {}
    for conector in _CONECTORES_PARRAFO:
        n = conteo[conector]
        resultado[conector] = {
            "ocurrencias": n,
            "por_mil_palabras": round(n / total_words * 1000, 3) if total_words else 0.0,
            "ubicaciones": ubicaciones[conector],
        }
    return resultado


def _find_triadas_probables(text, line_starts):
    """Tríadas de adjetivos probables: "X, Y y Z" tras un sustantivo, o un
    epíteto antepuesto seguido de tríada (P06, P41).

    Un escáner determinista basado en expresiones regulares no puede
    confirmar la categoría gramatical de "X", "Y" ni "Z" (no distingue un
    adjetivo de un sustantivo): por eso toda coincidencia se etiqueta
    siempre como "probable", nunca como un hallazgo confirmado. Una lista
    real de tres sustantivos (por ejemplo, tres ingredientes) coincide con
    el mismo patrón y se reporta igual, como dato; es el modelo o quien
    revisa quien debe descartarla (auditoria.md P06, salvaguarda de listas
    reales).
    """
    hallazgos = []
    ocupados = []  # tramos ya reportados como epíteto antepuesto
    for m in _TRIADA_EPITETO_RE.finditer(text):
        ocupados.append((m.start(), m.end()))
        line_no, col = _line_col(line_starts, m.start())
        hallazgos.append(
            {
                "linea": line_no,
                "columna": col,
                "texto": _clip_texto(m.group(0)),
                "variante": "epiteto_antepuesto",
                "certeza": "probable",
            }
        )
    for m in _TRIADA_RE.finditer(text):
        inicio, fin = m.start(), m.end()
        # La tríada final del epíteto antepuesto ("única, natural y eficaz")
        # también encaja en el patrón genérico "X, Y y Z"; si su tramo ya
        # quedó cubierto por un hallazgo de epíteto, no se duplica.
        if any(inicio < o_fin and o_inicio < fin for o_inicio, o_fin in ocupados):
            continue
        line_no, col = _line_col(line_starts, inicio)
        hallazgos.append(
            {
                "linea": line_no,
                "columna": col,
                "texto": _clip_texto(m.group(0)),
                "variante": "enumeracion",
                "certeza": "probable",
            }
        )
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def analyze_estructuras(ctx):
    text = ctx.masked_text
    return {
        "no_solo_sino": _find_regex_hits(text, _NO_SOLO_SINO_RE, ctx.line_starts),
        "no_se_trata_de": _find_regex_hits(text, _NO_SE_TRATA_DE_RE, ctx.line_starts),
        "no_es_es": _find_regex_hits(text, _NO_ES_ES_RE, ctx.line_starts),
        "tanto_si_como_si": _find_regex_hits(text, _TANTO_SI_RE, ctx.line_starts),
        "ya_seas_o": _find_regex_hits(text, _YA_SEAS_RE, ctx.line_starts),
        "enumeracion_mecanica": _find_enumeracion_mecanica(text, ctx.line_starts),
        "conectores_parrafo": _find_conectores_parrafo(ctx),
        "triadas_adjetivos": _find_triadas_probables(text, ctx.line_starts),
    }


# ---------------------------------------------------------------------------
# Analizador: deterministas. Marcado de chatbot filtrado (P61), UTM de IA
# (P62, solo aviso), marcadores de posición (P60), caracteres invisibles y
# homoglifos (P59), sobre ``deterministas_text`` (frontmatter y código
# enmascarados, pero con las URL visibles para poder leer sus parámetros).
# ---------------------------------------------------------------------------

_MARCADO_FILTRADO = (
    ("oaicite", re.compile(r"oaicite")),
    ("turn_search_token", re.compile(r"\bturn\d+[a-z]+\d+\b")),
    ("cita_corchete_angular", re.compile(r"【[^】\n]*†[^】\n]*】")),
    ("content_reference", re.compile(r"contentReference")),
)

_UTM_IA_TOKENS = (
    "chatgpt",
    "openai",
    "gpt",
    "perplexity",
    "copilot",
    "gemini",
    "claude",
    "anthropic",
)
_UTM_SOURCE_RE = re.compile(r"utm_source=([^&\s]+)", re.IGNORECASE)

_PLACEHOLDER_PATTERNS = (
    ("corchete_marcador", re.compile(
        r"\[(?:nombre|apellido|ciudad|empresa|fecha|insertar[^\]\n]*|placeholder|TODO|pendiente)\]",
        re.IGNORECASE,
    )),
    ("doble_llave", re.compile(r"\{\{[^}\n]*\}\}")),
    ("xxx", re.compile(r"\bXXX\b")),
    ("lorem_ipsum", re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE)),
)

# U+00A0 (espacio de no separación) y U+202F (espacio fino de no
# separación) son legítimos en la tipografía española (p. ej. antes de "%",
# "€" o una unidad) y nunca se incluyen aquí (auditoria.md P59).
#
# Cada punto de código se escribe como escape "\uXXXX", nunca como el
# carácter invisible en crudo (revisión de la slice 04, A5): un carácter
# invisible pegado en el código fuente es ilegible en un editor normal y muy
# fácil de borrar o corromper por accidente sin que se note en un diff.
_INVISIBLES_A_VIGILAR = (
    "\u200B",  # ZERO WIDTH SPACE
    "\u200C",  # ZERO WIDTH NON-JOINER
    "\u200D",  # ZERO WIDTH JOINER
    "\u2060",  # WORD JOINER
    "\u00AD",  # SOFT HYPHEN
    "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE (también usado como BOM)
)


def _find_marcado_filtrado(ctx):
    hallazgos = []
    for tipo, pattern in _MARCADO_FILTRADO:
        for m in pattern.finditer(ctx.deterministas_text):
            line_no, col = _line_col(ctx.line_starts, m.start())
            hallazgos.append(
                {"tipo": tipo, "linea": line_no, "columna": col, "texto": _clip_texto(m.group(0))}
            )
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_utm_ia(ctx):
    """UTM de herramientas de IA en una URL (P62): solo aviso, nunca
    bloquea; la URL en sí es intocable y nunca se modifica aquí.
    """
    hallazgos = []
    for m in _URL_RE.finditer(ctx.deterministas_text):
        url = m.group(0)
        for um in _UTM_SOURCE_RE.finditer(url):
            valor = um.group(1)
            if any(tok in valor.lower() for tok in _UTM_IA_TOKENS):
                line_no, col = _line_col(ctx.line_starts, m.start())
                hallazgos.append(
                    {"linea": line_no, "columna": col, "url": url, "utm_source": valor}
                )
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_placeholders(ctx):
    hallazgos = []
    for tipo, pattern in _PLACEHOLDER_PATTERNS:
        for m in pattern.finditer(ctx.deterministas_text):
            line_no, col = _line_col(ctx.line_starts, m.start())
            hallazgos.append(
                {"tipo": tipo, "linea": line_no, "columna": col, "texto": _clip_texto(m.group(0))}
            )
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_invisibles(ctx):
    """Caracteres invisibles sospechosos (P59). Se informa del nombre
    Unicode del carácter (p. ej. "ZERO WIDTH SPACE"), nunca del carácter en
    sí, para que el JSON no repita un carácter pensado para no verse.
    U+FEFF (u otro de esta lista) al principio mismo del texto no se
    reporta: ahí es una marca de orden de bytes legítima, no una inserción
    en mitad del texto.
    """
    hallazgos = []
    text = ctx.deterministas_text
    for idx, ch in enumerate(text):
        if ch in _INVISIBLES_A_VIGILAR and idx != 0:
            line_no, col = _line_col(ctx.line_starts, idx)
            nombre = unicodedata.name(ch, "DESCONOCIDO")
            hallazgos.append(
                {
                    "caracter": nombre,
                    "codepoint": "U+{:04X}".format(ord(ch)),
                    "linea": line_no,
                    "columna": col,
                }
            )
    return hallazgos


def _script_de(ch):
    if not ch.isalpha():
        return None
    try:
        nombre = unicodedata.name(ch)
    except ValueError:
        return None
    if nombre.startswith("LATIN"):
        return "latin"
    if nombre.startswith("CYRILLIC"):
        return "cirilico"
    if nombre.startswith("GREEK"):
        return "griego"
    return None


def _find_homoglifos(ctx):
    """Letras cirílicas o griegas mezcladas dentro de una palabra latina
    (P59). Compara los alfabetos (script Unicode) de cada letra de la
    palabra; si conviven letras latinas con cirílicas o griegas, se reporta
    la palabra completa.
    """
    hallazgos = []
    for m in _WORD_RE.finditer(ctx.deterministas_text):
        palabra = m.group(0)
        escrituras = {s for s in (_script_de(ch) for ch in palabra) if s}
        if "latin" in escrituras and ("cirilico" in escrituras or "griego" in escrituras):
            line_no, col = _line_col(ctx.line_starts, m.start())
            hallazgos.append(
                {
                    "palabra": palabra,
                    "escrituras": sorted(escrituras),
                    "linea": line_no,
                    "columna": col,
                }
            )
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def analyze_deterministas(ctx):
    return {
        "marcado_filtrado": _find_marcado_filtrado(ctx),
        "utm_ia": _find_utm_ia(ctx),
        "marcadores_de_posicion": _find_placeholders(ctx),
        "invisibles": _find_invisibles(ctx),
        "homoglifos": _find_homoglifos(ctx),
    }


# ---------------------------------------------------------------------------
# Analizador: registro. Recuento tú/usted y vosotros/ustedes, y léxico
# americano corto (P64), sobre ``masked_text``. Solo aviso: nunca cambia
# nada ni etiqueta una forma como error (auditoria.md, P64: "ustedes"
# formal es correcto en ES-ES). Lista conservadora y documentada
# de pronombres y formas inequívocas; ante la duda, se prefiere no contar
# antes que arriesgar un falso positivo (p. ej. no se cuentan "su"/"le", que
# son iguales para "usted" y para "él/ella").
# ---------------------------------------------------------------------------

# "tú" (pronombre sujeto), "tu"/"tus" (posesivo), "te" (pronombre objeto),
# "ti" (término de preposición) y "contigo" son marcadores inequívocos de
# tuteo. Revisión de la slice 04 (A2): antes de esta revisión la
# comparación plegaba tildes (vía ``_normalize_for_matching``), así que
# "té" (la infusión) contaba como el pronombre "te", y "tú" y "tu"
# resultaban indistinguibles entre sí (ambos se normalizaban a "tu"). La
# comparación ahora es sensible a tildes (solo se pliegan mayúsculas y
# minúsculas, nunca los diacríticos), así que cada forma cuenta solo la
# suya: "tú" ya no coincide con "tu", y "té" ya no coincide con "te".
# Al ser sensible a tildes, cada marcador cuenta solo su propia forma:
# "tu"/"tus" (posesivo) nunca se confunden con "tú" (pronombre sujeto) ni
# con ninguna forma de "usted", así que no queda ninguna colisión abierta
# para este conjunto de marcadores (revisión review-4e912a0ac78c9cff,
# R2-001: este párrafo sustituye a uno anterior que se contradecía a sí
# mismo).
_TU_MARCADORES = ("tú", "tu", "tus", "te", "ti", "contigo")
_USTED_MARCADORES = ("usted",)
_VOSOTROS_MARCADORES = ("vosotros", "vosotras", "vuestro", "vuestra", "vuestros", "vuestras", "os")
_USTEDES_MARCADORES = ("ustedes",)

# Léxico americano corto y explícitamente citado (fase2-mapa.md §3.2,
# auditoria.md, P64 y §8): solo se lista lo que las fuentes leídas nombran,
# nunca se amplía por criterio propio.
_LEXICO_AMERICANO = (("computadora", "ordenador"),)


def _count_marcadores(ctx, marcadores):
    """Cuenta ocurrencias de ``marcadores`` en ``ctx.masked_text``.

    A diferencia de la búsqueda de vocabulario, esta comparación pliega
    mayúsculas y minúsculas (``re.IGNORECASE``) pero NUNCA tildes: dos
    formas que solo se distinguen por un diacrítico (p. ej. "tú"/"tu" o
    "te"/"té") son palabras distintas en español, y plegar tildes las
    confundiría (revisión de la slice 04, A2).
    """
    pattern = re.compile(
        r"\b(?:{})\b".format("|".join(re.escape(m) for m in marcadores)),
        re.UNICODE | re.IGNORECASE,
    )
    ocurrencias = len(pattern.findall(ctx.masked_text))
    por_mil = round(ocurrencias / ctx.total_words * 1000, 3) if ctx.total_words else 0.0
    return {"ocurrencias": ocurrencias, "por_mil_palabras": por_mil}


def _find_lexico_americano(ctx):
    hallazgos = []
    for expresion, _equivalente_es in _LEXICO_AMERICANO:
        pattern = re.compile(r"\b" + re.escape(_normalize_for_matching(expresion)) + r"\b")
        for m in pattern.finditer(ctx.normalized_text):
            orig_inicio = ctx.orig_index_for_normpos[m.start()]
            line_no, col = _line_col(ctx.line_starts, orig_inicio)
            hallazgos.append({"expresion": expresion, "linea": line_no, "columna": col})
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def analyze_registro(ctx):
    tuteo = _count_marcadores(ctx, _TU_MARCADORES)
    usted = _count_marcadores(ctx, _USTED_MARCADORES)
    vosotros = _count_marcadores(ctx, _VOSOTROS_MARCADORES)
    ustedes = _count_marcadores(ctx, _USTEDES_MARCADORES)
    return {
        "tuteo": tuteo,
        "usted": usted,
        "vosotros": vosotros,
        "ustedes": ustedes,
        "mezcla_tu_usted": tuteo["ocurrencias"] > 0 and usted["ocurrencias"] > 0,
        "mezcla_vosotros_ustedes": vosotros["ocurrencias"] > 0 and ustedes["ocurrencias"] > 0,
        "lexico_americano": _find_lexico_americano(ctx),
    }


# ---------------------------------------------------------------------------
# Comparación con el original (--original). Extrae hechos (cifras,
# porcentajes, fechas, precios, duraciones/unidades, códigos, siglas,
# nombres propios y URL) de dos textos y señala, por categoría, lo que falta
# en el nuevo texto y lo que aparece de nuevo, en ambas direcciones
# (auditoria.md §8; a diferencia de Aboudjem, que solo informa de lo
# perdido, aquí se informa también de lo añadido). Los claims marcados
# ``[[claim]]…[[/claim]]`` y las citas literales se comparan aparte, de
# forma literal y con los espacios normalizados. También se comparan los
# recuentos de tú/usted y vosotros/ustedes entre los dos textos, solo como
# dato informativo (nunca hace que el código de salida sea 1).
# ---------------------------------------------------------------------------


def _mask_for_comparacion(text):
    """Vista para la comparación con el original: enmascara frontmatter y
    código (igual que ``_mask_for_deterministas``), pero dejando visibles
    las URL, las comillas y los claims marcados, porque cada uno de ellos
    es su propia categoría de comparación y necesita verse tal cual.
    """
    text, _ = _mask_pattern(text, _FRONTMATTER_RE)
    text, _ = _mask_pattern(text, _CODE_FENCE_RE)
    text, _ = _mask_pattern(text, _INLINE_CODE_RE)
    return text


def _ranges_overlap_span(start, end, spans):
    """True si ``[start, end)`` solapa con algún tramo de ``spans``.

    ``spans`` (la lista compartida ``consumidos`` de ``_extract_all_facts``)
    se mantiene siempre ordenada por inicio y con sus tramos disjuntos entre
    sí: cada nuevo tramo solo se añade (con ``bisect.insort``, en el
    llamador) después de comprobar aquí que no solapa con ninguno de los ya
    presentes. Con esa invariante, dos tramos disjuntos y ordenados por
    inicio quedan también ordenados por fin, así que basta comparar
    ``[start, end)`` contra su predecesor inmediato (el último tramo cuyo
    inicio es menor que ``end``): si ese no solapa, ninguno de los
    anteriores puede hacerlo tampoco, porque todos terminan antes o en el
    mismo punto que él. Antes (revisión review-4e912a0ac78c9cff, R4-001)
    esta función comparaba contra TODOS los tramos ya consumidos en el
    documento entero, con coste O(n) por consulta y O(n²) en total; con
    ``bisect`` el coste por consulta es O(log n) y como mucho una sola
    llamada a ``_ranges_overlap``.
    """
    idx = bisect.bisect_left(spans, (end,))
    if idx == 0:
        return False
    s_ini, s_fin = spans[idx - 1]
    return _ranges_overlap(start, end, s_ini, s_fin)


# --- Cifras: enteros, separador de miles (punto, espacio, NBSP o espacio
# fino de no separación U+202F) y decimales (coma o punto). Un token de un
# único grupo "N.NNN" es ambiguo entre lectura de miles y lectura decimal
# (p. ej. "1.500"): se devuelven ambas lecturas, y basta una coincidencia
# con cualquiera de ellas para considerarlo el mismo dato (fase2-mapa.md
# §4.1, fila "--original").
_CIFRA_TOKEN_RE = re.compile(
    r"(?<![\w.,])(?:"
    r"\d{1,3}(?:\.\d{3})+,\d+"
    r"|\d{1,3}(?:[\u0020\u00a0\u202f]\d{3})+(?:,\d+)?"
    r"|\d{1,3}(?:\.\d{3})+"
    r"|\d+,\d+"
    r"|\d+\.\d+"
    r"|\d+"
    r")(?!\w)"
)


def _parse_cifra(token):
    """Normaliza un token numérico español a una o más lecturas canónicas
    comparables. Ver la cabecera de esta sección para el caso ambiguo."""
    m = re.fullmatch(r"(\d{1,3}(?:\.\d{3})+),(\d+)", token)
    if m:
        return [m.group(1).replace(".", "") + "." + m.group(2)]

    m = re.fullmatch(r"(\d{1,3}(?:[\u0020\u00a0\u202f]\d{3})+)(?:,(\d+))?", token)
    if m:
        entero = re.sub(r"[\u0020\u00a0\u202f]", "", m.group(1))
        return [entero + "." + m.group(2)] if m.group(2) else [entero]

    if re.fullmatch(r"\d{1,3}\.\d{3}", token):
        miles = token.replace(".", "")
        decimal = str(float(token))
        return sorted({miles, decimal})

    if re.fullmatch(r"\d{1,3}(?:\.\d{3}){2,}", token):
        return [token.replace(".", "")]

    m = re.fullmatch(r"(\d+),(\d+)", token)
    if m:
        return [m.group(1) + "." + m.group(2)]

    return [token]


def _find_cifras(text, line_starts, consumidos, privacy_spans):
    hallazgos = []
    for m in _CIFRA_TOKEN_RE.finditer(text):
        if _ranges_overlap_span(m.start(), m.end(), consumidos):
            continue
        lecturas = _parse_cifra(m.group(0))
        bisect.insort(consumidos, (m.start(), m.end()))
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {"texto": m.group(0), "linea": line_no, "columna": col, "lecturas": lecturas}
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


# --- Porcentajes: "50 %", "50%" y "50 por ciento" son la misma lectura.
_PORCENTAJE_RE = re.compile(
    r"\b(\d+(?:[.,]\d+)?)[\u0020\u00a0\u202f]?%"
    r"|\b(\d+(?:[.,]\d+)?)\s+por\s+ciento\b",
    re.IGNORECASE,
)


def _find_porcentajes(text, line_starts, consumidos, privacy_spans):
    hallazgos = []
    for m in _PORCENTAJE_RE.finditer(text):
        if _ranges_overlap_span(m.start(), m.end(), consumidos):
            continue
        numero = m.group(1) or m.group(2)
        bisect.insort(consumidos, (m.start(), m.end()))
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {
            "texto": _clip_texto(m.group(0)),
            "linea": line_no,
            "columna": col,
            "lecturas": [numero.replace(",", ".")],
        }
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


# --- Fechas españolas: "3 de marzo de 2026" y "03/03/2026". Se normalizan
# a ISO AAAA-MM-DD para comparar ambas formas por igual.
_MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}
_FECHA_TEXTUAL_RE = re.compile(
    r"\b(\d{1,2})\s+de\s+(" + "|".join(_MESES) + r")\s+de[l]?\s+(\d{4})\b",
    re.IGNORECASE,
)
_FECHA_NUMERICA_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")


def _normalizar_fecha_textual(m):
    mes = _MESES.get(m.group(2).lower())
    if mes is None:
        return None
    try:
        return datetime.date(int(m.group(3)), mes, int(m.group(1))).isoformat()
    except ValueError:
        return None


def _normalizar_fecha_numerica(m):
    try:
        return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))).isoformat()
    except ValueError:
        return None


def _find_fechas(text, line_starts, consumidos, privacy_spans):
    hallazgos = []
    for pattern, normalizar in (
        (_FECHA_TEXTUAL_RE, _normalizar_fecha_textual),
        (_FECHA_NUMERICA_RE, _normalizar_fecha_numerica),
    ):
        for m in pattern.finditer(text):
            if _ranges_overlap_span(m.start(), m.end(), consumidos):
                continue
            valor = normalizar(m)
            if valor is None:
                continue
            bisect.insort(consumidos, (m.start(), m.end()))
            line_no, col = _line_col(line_starts, m.start())
            hallazgo = {
                "texto": _clip_texto(m.group(0)),
                "linea": line_no,
                "columna": col,
                "lecturas": [valor],
            }
            _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
            hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


# --- Precios: "10 €", "€10", "10 EUR", "10 euros". Se compara solo el
# importe (misma lógica de lectura que las cifras), no la forma de
# escribir la moneda.
_PRECIO_RE = re.compile(
    # Límite inicial y final: «1500 €» se lee entero, nunca como «500 €»,
    # y «€1500» tampoco se corta en «€150».
    r"(?<![\w.,])(\d{1,3}(?:[.\u0020\u00a0\u202f]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"
    r"[\u0020\u00a0\u202f]?(?:€|EUR\b|euros?\b)"
    r"|€[\u0020\u00a0\u202f]?(\d{1,3}(?:[.\u0020\u00a0\u202f]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?)(?!\d)",
    re.IGNORECASE,
)


def _find_precios(text, line_starts, consumidos, privacy_spans):
    hallazgos = []
    for m in _PRECIO_RE.finditer(text):
        if _ranges_overlap_span(m.start(), m.end(), consumidos):
            continue
        numero = m.group(1) or m.group(2)
        bisect.insort(consumidos, (m.start(), m.end()))
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {
            "texto": _clip_texto(m.group(0)),
            "linea": line_no,
            "columna": col,
            "lecturas": _parse_cifra(numero),
        }
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


# --- Duraciones y unidades: "48 h", "24 horas", "50 ml", "200 g". La
# lectura combina número y unidad tal cual se escribieron; no se convierte
# entre unidades distintas ("horas" no se compara con "h"), limitación que
# se documenta aquí porque exigiría una tabla de conversión fuera de
# alcance de un escáner determinista.
_UNIDADES = (
    "h", "hora", "horas", "min", "minuto", "minutos", "s", "segundo", "segundos",
    "dia", "dias", "día", "días", "semana", "semanas", "mes", "meses",
    "ano", "anos", "año", "años", "ml", "l", "litro", "litros",
    "g", "gr", "gramo", "gramos", "kg", "mg", "cm", "mm",
)
_DURACION_UNIDAD_RE = re.compile(
    r"\b(\d+(?:[.,]\d+)?)[\u0020\u00a0\u202f](?:"
    + "|".join(sorted(_UNIDADES, key=len, reverse=True))
    + r")\b",
    re.IGNORECASE,
)


def _find_duraciones_unidades(text, line_starts, consumidos, privacy_spans):
    hallazgos = []
    for m in _DURACION_UNIDAD_RE.finditer(text):
        if _ranges_overlap_span(m.start(), m.end(), consumidos):
            continue
        numero = m.group(1).replace(",", ".")
        unidad = _normalize_for_matching(m.group(0)[len(m.group(1)):].strip())
        bisect.insort(consumidos, (m.start(), m.end()))
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {
            "texto": _clip_texto(m.group(0)),
            "linea": line_no,
            "columna": col,
            "lecturas": ["{}|{}".format(numero, unidad)],
        }
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


# --- Códigos y referencias: tokens alfanuméricos con al menos una letra y
# un dígito (p. ej. lotes o referencias de producto). La comparación pliega
# mayúsculas: una diferencia de caja sola no se marca.
_CODIGO_RE = re.compile(r"\b(?=[A-Za-z0-9-]*\d)(?=[A-Za-z0-9-]*[A-Za-z])[A-Za-z0-9][A-Za-z0-9-]{3,}\b")


def _find_codigos(text, line_starts, consumidos, privacy_spans):
    hallazgos = []
    for m in _CODIGO_RE.finditer(text):
        if _ranges_overlap_span(m.start(), m.end(), consumidos):
            continue
        bisect.insort(consumidos, (m.start(), m.end()))
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {
            "texto": m.group(0),
            "linea": line_no,
            "columna": col,
            "lecturas": [m.group(0).upper()],
        }
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


# --- Siglas: tokens en mayúsculas de dos o más letras (P59/INCI). Solo
# informativo: nunca hace que el código de salida sea 1 (el riesgo de falso
# positivo es mayor que en el resto de categorías).
_SIGLA_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{2,}\b")


def _find_siglas(text, line_starts, privacy_spans):
    hallazgos = []
    for m in _SIGLA_RE.finditer(text):
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {"texto": m.group(0), "linea": line_no, "columna": col, "lecturas": [m.group(0)]}
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


# --- Nombres propios: palabras con mayúscula inicial que NO están al
# principio de una oración ni de un párrafo. Heurística basada en
# puntuación de cierre de frase (".", "!", "?"), en los signos de apertura
# "¿"/"¡", en saltos de párrafo (dos o más saltos de línea seguidos), en
# marcadores de lista Markdown y encabezados, y en una comilla de apertura
# o una raya que a su vez sean principio de oración (revisión
# review-4e912a0ac78c9cff, R3-nombres-propios-falsos-bloqueantes). Tras
# dos puntos no se asume principio de oración, para no ocultar un nombre
# cambiado («Contacto: Marta»); se acepta alguna falsa alarma a cambio.
# No distingue un nombre propio
# real de cualquier otra palabra capitalizada a mitad de frase (p. ej. una
# sigla de una sola letra en mayúscula no cuenta, ya la excluye la clase de
# caracteres). Limitación documentada, igual que la de "title_case" en el
# analizador de encabezados.
_PALABRA_CAPITALIZADA_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b")

# Comilla de apertura o raya que, si a su vez es principio de oración,
# arrastra ese principio de oración a la palabra que la sigue pegada (sin
# espacio, como en la raya de diálogo, o con espacio, como tras dos
# puntos). "«" y "“" y "‘" son siempre de apertura; la comilla recta '"'
# es ambigua entre apertura y cierre, pero tratarla aquí como posible
# apertura solo amplía qué se EXCLUYE de nombres propios, nunca al revés,
# así que no crea un falso negativo de privacidad ni de cifras.
_APERTURA_ORACION_CHARS = "«“‘\"" + _EM_DASH
# La marca de apertura de un claim no cambia si lo que sigue abre frase.
_CLAIM_APERTURA = "[[claim]]"
_ENCABEZADO_PREFIJO_RE = re.compile(r"^#{1,6}[ \t]+$")
_LISTA_PREFIJO_RE = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]+$")


# Longitud máxima del prefijo de línea que puede ser solo un marcador de
# lista o de encabezado (con su sangría). Más allá, no hace falta mirar:
# acota el coste por palabra en líneas muy largas.
_PREFIJO_LINEA_MAX = 40


def _prefijo_de_linea_es_marcador(text, pos):
    """True si lo que hay entre el principio de la línea y ``pos`` es solo
    un marcador de lista Markdown o las almohadillas de un encabezado."""
    inicio_busqueda = max(0, pos - _PREFIJO_LINEA_MAX - 1)
    line_start = text.rfind("\n", inicio_busqueda, pos) + 1
    if line_start == 0 and inicio_busqueda > 0:
        return False
    prefijo_linea = text[line_start:pos]
    return bool(
        _ENCABEZADO_PREFIJO_RE.match(prefijo_linea) or _LISTA_PREFIJO_RE.match(prefijo_linea)
    )


def _es_adorno(ch):
    """True para un emoji o símbolo decorativo (y sus selectores de
    variación o uniones), que se salta al buscar el signo que cierra la
    frase anterior: «¿Ya lo probaste? 🌿✨ En el mundo…» abre frase en «En»."""
    return ch in "\ufe0f\u200d" or unicodedata.category(ch) in ("So", "Sk")


def _es_inicio_de_oracion(text, inicio):
    """True si la posición ``inicio`` empieza una oración (o un párrafo, o
    el texto), y por tanto una mayúscula ahí nunca debe tratarse como
    nombre propio.

    Además del final de frase (".", "!", "?") y del salto de párrafo (dos
    o más saltos de línea seguidos), se consideran principio de oración:
    justo tras un signo de apertura español ("¿" o "¡"); al principio de
    la línea, tras un marcador de lista Markdown ("-", "*", "+" o "1.") o
    tras las almohadillas de un encabezado ("#" a "######"); tras un
    final de frase seguido de emojis o símbolos decorativos; y tras una
    comilla de apertura, una marca «[[claim]]» o una raya que a su vez
    sean principio de oración (la raya de diálogo, o una cita que
    reproduce una frase completa). Las
    cadenas de comillas y rayas se recorren con un bucle, sin recursión,
    para que una racha muy larga no agote la pila.

    Tras dos puntos NO se asume principio de oración: «Contacto: Marta»
    lleva un nombre propio, y esta comprobación de cero invención prefiere
    una falsa alarma («Aviso: Este» → «Aviso: Ese») a dejar pasar un
    nombre cambiado.
    """
    pos = inicio
    while True:
        j = pos
        saltos_seguidos = 0
        while j > 0 and (text[j - 1] in " \t\n" or _es_adorno(text[j - 1])):
            if text[j - 1] == "\n":
                saltos_seguidos += 1
            j -= 1
        if j == 0 or saltos_seguidos >= 2:
            return True
        anterior = text[j - 1]
        if anterior in ".!?¿¡":
            return True
        if _prefijo_de_linea_es_marcador(text, pos):
            return True
        if anterior in _APERTURA_ORACION_CHARS:
            pos = j - 1
            continue
        if text.endswith(_CLAIM_APERTURA, 0, j):
            pos = j - len(_CLAIM_APERTURA)
            continue
        return False


def _find_nombres_propios(text, line_starts, privacy_spans):
    hallazgos = []
    for m in _PALABRA_CAPITALIZADA_RE.finditer(text):
        if _es_inicio_de_oracion(text, m.start()):
            continue
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {"texto": m.group(0), "linea": line_no, "columna": col, "lecturas": [m.group(0)]}
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_urls_comparacion(text, line_starts, privacy_spans):
    hallazgos = []
    for m in _URL_RE.finditer(text):
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {
            "texto": m.group(0), "linea": line_no, "columna": col, "lecturas": [m.group(0)],
        }
        # Una URL puede llevar un correo o un teléfono en la consulta
        # (p. ej. «?correo=…»): se oculta igual que en el resto de categorías.
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_claims_marcados(text, privacy_spans):
    line_starts = _build_line_index(text)
    hallazgos = []
    for m in _CLAIM_RE.finditer(text):
        interior = m.group(0)[len("[[claim]]"):-len("[[/claim]]")]
        valor = re.sub(r"\s+", " ", interior).strip()
        line_no, col = _line_col(line_starts, m.start())
        hallazgo = {
            "texto": _clip_texto(interior),
            "linea": line_no,
            "columna": col,
            "lecturas": [valor],
        }
        _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
        hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _find_citas_literales(text, line_starts, privacy_spans):
    hallazgos = []
    for _tipo, pattern in _QUOTE_TYPES:
        for m in pattern.finditer(text):
            interior = m.group(0)[1:-1]
            valor = re.sub(r"\s+", " ", interior).strip()
            if not valor:
                continue
            line_no, col = _line_col(line_starts, m.start())
            hallazgo = {
                "texto": _clip_texto(m.group(0)),
                "linea": line_no,
                "columna": col,
                "lecturas": [valor],
            }
            _marcar_si_privado(hallazgo, m.start(), m.end(), privacy_spans)
            hallazgos.append(hallazgo)
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def _diff_by_any_reading(originales, nuevas, sigue_en_nuevo=None, estaba_en_original=None):
    """Compara dos listas de ocurrencias por presencia de lectura, no por
    multiconjunto: si un dato aparece dos veces en un texto y una sola en
    el otro, no se marca como falta. Lo relevante para "cero invención" es
    si el dato en sí sigue presente, no cuántas veces se repite; esta
    simplificación se documenta como límite conocido del diseño. Una
    ocurrencia con varias lecturas (cifras ambiguas) cuenta como
    encontrada si CUALQUIERA de sus lecturas aparece en el otro lado.

    ``sigue_en_nuevo`` y ``estaba_en_original`` son comprobaciones
    opcionales sobre el texto completo del otro lado: si devuelven True
    para una ocurrencia, esta no se informa aunque su lectura no esté
    entre los hechos extraídos del otro texto (lo usan los nombres
    propios, cuya extracción ignora las mayúsculas de inicio de frase).
    """
    lecturas_nuevas = set()
    for it in nuevas:
        lecturas_nuevas.update(it["lecturas"])
    lecturas_originales = set()
    for it in originales:
        lecturas_originales.update(it["lecturas"])

    # La comparación de lecturas usa siempre el valor real, ANTES de
    # redactar: dos apariciones idénticas de un mismo dato personal no
    # deben marcarse como diferencia solo porque su valor se oculte al
    # mostrarlo (revisión review-4e912a0ac78c9cff, R1-001). La redacción
    # ocurre después, solo sobre los elementos que de verdad van a
    # aparecer en el informe.
    faltantes = [
        it for it in originales
        if not (set(it["lecturas"]) & lecturas_nuevas)
        and not (sigue_en_nuevo is not None and sigue_en_nuevo(it))
    ]
    agregadas = [
        it for it in nuevas
        if not (set(it["lecturas"]) & lecturas_originales)
        and not (estaba_en_original is not None and estaba_en_original(it))
    ]
    faltantes = [_redactar_si_privado(it) for it in faltantes]
    agregadas = [_redactar_si_privado(it) for it in agregadas]
    faltantes.sort(key=lambda h: (h["linea"], h["columna"]))
    agregadas.sort(key=lambda h: (h["linea"], h["columna"]))
    return faltantes, agregadas


_ENCABEZADO_LINEA_RE = re.compile(r"^[ \t]*#{1,6}[ \t]+")

# Una palabra vecina solo sirve de prueba si es lo bastante larga para no
# ser un artículo o una preposición («de», «la», «que»).
_VECINA_MIN_LETRAS = 4
_VECINA_SIGUIENTE_RE = re.compile(r"[ \t,;:]+(\w+)")
_VECINA_ANTERIOR_RE = re.compile(r"(\w+)[ \t,;:]+$")


def _lineas_de_encabezado(text):
    """Números de línea (desde 1) que son encabezados Markdown."""
    return {
        n for n, linea in enumerate(text.split("\n"), start=1)
        if _ENCABEZADO_LINEA_RE.match(linea)
    }


def _palabras_vecinas(text, inicio, fin, abre_oracion):
    """Palabras (minúsculas, de al menos ``_VECINA_MIN_LETRAS`` letras) que
    rodean a la palabra en [``inicio``, ``fin``): la siguiente y, salvo que
    la palabra abra frase (la anterior sería de otra frase), la anterior.
    Se busca dentro de la misma frase: un punto corta la vecindad."""
    vecinas = []
    m = _VECINA_SIGUIENTE_RE.match(text, fin)
    if m:
        vecinas.append(m.group(1))
    if not abre_oracion:
        m = _VECINA_ANTERIOR_RE.search(text[max(0, inicio - 60):inicio])
        if m:
            vecinas.append(m.group(1))
    return {v.lower() for v in vecinas if len(v) >= _VECINA_MIN_LETRAS}


def _nombre_aparece_en(it, propio, propio_line_starts, propio_encabezados, otro):
    """True si el nombre propio ``it`` (extraído de ``propio``) aparece en
    ``otro`` como palabra completa. Es lo que evita dar por perdido (o por
    nuevo) un nombre que la extracción no ve en el otro texto.

    - Un nombre de un encabezado se busca sin distinguir mayúsculas: pasar
      «Guía Clave De Cuidado» a «Guía clave de cuidado» (P20) no pierde
      nada. Un nombre que desaparece por completo sí se informa.
    - Cualquier otro nombre se busca con su misma mayúscula (una marca
      «Olmo» no es el árbol «olmo»). Una aparición a mitad de frase vale.
      Una que abre frase solo vale si comparte una palabra vecina con la
      aparición original: así «Panadería Olmo abre…» no se da por perdida
      al perder su apertura, pero una palabra común que abre frase
      («Rosa huele bien») no oculta que el nombre «Rosa» ha desaparecido.
      Punto ciego conocido: si cambian todas las palabras vecinas, un
      nombre que solo cambia de sitio se informa (falsa alarma).
    """
    palabra = it["texto"]
    patron = r"(?<!\w)" + re.escape(palabra) + r"(?!\w)"
    if it["linea"] in propio_encabezados:
        return re.search(patron, otro, re.IGNORECASE) is not None
    vecinas_propias = None
    for m in re.finditer(patron, otro):
        if not _es_inicio_de_oracion(otro, m.start()):
            return True
        if vecinas_propias is None:
            inicio = propio_line_starts[it["linea"] - 1] + it["columna"] - 1
            vecinas_propias = _palabras_vecinas(propio, inicio, inicio + len(palabra), False)
        if vecinas_propias & _palabras_vecinas(otro, m.start(), m.end(), True):
            return True
    return False


def _extract_all_facts(text, line_starts):
    """Extrae todas las categorías de hechos de un texto para la
    comparación con el original. El orden importa: cada categoría más
    específica consume su propio tramo de texto (``consumidos``) antes de
    que la categoría más genérica de cifras sueltas la vuelva a encontrar
    (p. ej. el "20" de "20 %" no debe contarse también como cifra suelta).

    Todas las categorías reciben además ``privacy_spans`` (los mismos
    patrones que ``analyze_privacidad``, calculados una sola vez sobre
    ``base``) para poder marcar como dato personal cualquier hecho cuyo
    tramo los solape (revisión review-4e912a0ac78c9cff, R1-001): un
    teléfono, un DNI/NIE o un correo puede coincidir con una cifra, un
    código o un nombre propio, y esta comparación nunca debe repetir su
    valor en el informe.
    """
    base = _mask_for_comparacion(text)
    privacy_spans = _find_privacy_spans(base)
    urls = _find_urls_comparacion(base, line_starts, privacy_spans)
    sin_urls, _ = _mask_pattern(base, _URL_RE)

    consumidos = []
    fechas = _find_fechas(sin_urls, line_starts, consumidos, privacy_spans)
    porcentajes = _find_porcentajes(sin_urls, line_starts, consumidos, privacy_spans)
    precios = _find_precios(sin_urls, line_starts, consumidos, privacy_spans)
    duraciones = _find_duraciones_unidades(sin_urls, line_starts, consumidos, privacy_spans)
    codigos = _find_codigos(sin_urls, line_starts, consumidos, privacy_spans)
    cifras = _find_cifras(sin_urls, line_starts, consumidos, privacy_spans)
    return {
        "cifras": cifras,
        "porcentajes": porcentajes,
        "fechas": fechas,
        "precios": precios,
        "duraciones_unidades": duraciones,
        "codigos": codigos,
        "siglas": _find_siglas(sin_urls, line_starts, privacy_spans),
        "nombres_propios": _find_nombres_propios(sin_urls, line_starts, privacy_spans),
        "url": urls,
    }


def _contar_registro_en_texto(text):
    masked, _, _ = mask_text(text)

    def contar(marcadores):
        pattern = re.compile(
            r"\b(?:{})\b".format("|".join(re.escape(m) for m in marcadores)),
            re.UNICODE | re.IGNORECASE,
        )
        return len(pattern.findall(masked))

    return {
        "tuteo": contar(_TU_MARCADORES),
        "usted": contar(_USTED_MARCADORES),
        "vosotros": contar(_VOSOTROS_MARCADORES),
        "ustedes": contar(_USTEDES_MARCADORES),
    }


def _comparar_registro(registro_nuevo, original_text):
    original_conteo = _contar_registro_en_texto(original_text)
    resultado = {}
    for clave in ("tuteo", "usted", "vosotros", "ustedes"):
        n_original = original_conteo[clave]
        n_nuevo = registro_nuevo[clave]["ocurrencias"]
        resultado[clave] = {
            "original": n_original,
            "nuevo": n_nuevo,
            "diferencia": n_nuevo - n_original,
        }
    return resultado


def _build_comparacion(ctx, original_text, registro_nuevo):
    original_line_starts = _build_line_index(original_text)
    hechos_originales = _extract_all_facts(original_text, original_line_starts)
    hechos_nuevos = _extract_all_facts(ctx.original_text, ctx.line_starts)

    base_original = _mask_for_comparacion(original_text)
    base_nuevo = _mask_for_comparacion(ctx.original_text)

    # Un nombre propio solo falta (o es nuevo) si no aparece en el otro
    # texto según ``_nombre_aparece_en``. La extracción ignora las
    # mayúsculas de inicio de frase, así que un arreglo que deja «Panadería
    # Olmo» al principio de la frase no debe darla por perdida; un nombre
    # cambiado de verdad («Marta» → «Laura») sigue informándose.
    sin_urls_original, _ = _mask_pattern(base_original, _URL_RE)
    sin_urls_nuevo, _ = _mask_pattern(base_nuevo, _URL_RE)
    encabezados_original = _lineas_de_encabezado(original_text)
    encabezados_nuevo = _lineas_de_encabezado(ctx.original_text)
    comprobaciones = {
        "nombres_propios": (
            lambda it: _nombre_aparece_en(
                it, sin_urls_original, original_line_starts, encabezados_original, sin_urls_nuevo
            ),
            lambda it: _nombre_aparece_en(
                it, sin_urls_nuevo, ctx.line_starts, encabezados_nuevo, sin_urls_original
            ),
        ),
    }

    resultado = {}
    for clave in hechos_originales:
        sigue_en_nuevo, estaba_en_original = comprobaciones.get(clave, (None, None))
        faltantes, nuevas = _diff_by_any_reading(
            hechos_originales[clave], hechos_nuevos[clave], sigue_en_nuevo, estaba_en_original
        )
        resultado[clave] = {"faltantes": faltantes, "nuevas": nuevas}

    privacy_original = _find_privacy_spans(base_original)
    privacy_nuevo = _find_privacy_spans(base_nuevo)

    claims_originales = _find_claims_marcados(original_text, privacy_original)
    claims_nuevos = _find_claims_marcados(ctx.original_text, privacy_nuevo)
    faltantes, nuevas = _diff_by_any_reading(claims_originales, claims_nuevos)
    resultado["claims_marcados"] = {"faltantes": faltantes, "nuevas": nuevas}

    citas_originales = _find_citas_literales(base_original, original_line_starts, privacy_original)
    citas_nuevas = _find_citas_literales(base_nuevo, ctx.line_starts, privacy_nuevo)
    faltantes, nuevas = _diff_by_any_reading(citas_originales, citas_nuevas)
    resultado["citas"] = {"faltantes": faltantes, "nuevas": nuevas}

    resultado["registro"] = _comparar_registro(registro_nuevo, original_text)
    return resultado


_CATEGORIAS_BLOQUEANTES = (
    "cifras", "porcentajes", "fechas", "precios", "duraciones_unidades",
    "codigos", "nombres_propios", "url", "claims_marcados", "citas",
)


def _comparacion_tiene_diferencias_bloqueantes(comparacion):
    """Siglas y el aviso de registro tú/usted son solo informativos y
    nunca hacen que el código de salida sea 1 (encargo de esta tarea)."""
    return any(
        comparacion[clave]["faltantes"] or comparacion[clave]["nuevas"]
        for clave in _CATEGORIAS_BLOQUEANTES
    )


# ---------------------------------------------------------------------------
# Analizador: candidatos_claim. Señala frases con marcadores de eficacia,
# salud o seguridad para que el modelo o quien revisa decida si son un
# claim; el script nunca decide por su cuenta (estudio.md §10.5;
# auditoria.md §7.4). El texto ya marcado con
# ``[[claim]]…[[/claim]]`` queda en blanco en ``masked_text``, así que
# nunca se cuenta aquí como candidato: se informa aparte, en ``marcados``.
# ---------------------------------------------------------------------------

_ORACION_RE = re.compile(r"[^.!?]*[.!?]+|[^.!?]+$")


def _iter_oraciones(ctx):
    text = ctx.masked_text
    for p_start, p_end in ctx.paragraphs:
        parrafo = text[p_start:p_end]
        for m in _ORACION_RE.finditer(parrafo):
            if m.group(0).strip():
                yield p_start + m.start(), p_start + m.end(), m.group(0)


_CLAIM_VERBOS_EFICACIA_RE = re.compile(
    r"\b(reduce|elimina|combate|previene|repara|regenera|calma|alivia)\b", re.IGNORECASE
)
_CLAIM_NATURAL_RE = re.compile(r"\bnatural(?:es)?\b", re.IGNORECASE)

_CLAIM_MARKER_RULES = (
    (
        "verbo_eficacia",
        _CLAIM_VERBOS_EFICACIA_RE,
        "verbo de eficacia (reduce, elimina, combate, previene, repara, regenera, calma, alivia)",
    ),
    (
        "hidrata_durante_horas",
        re.compile(
            r"\bhidrata(?:ci[oó]n)?\b.{0,40}\bdurante\b.{0,20}\bhoras?\b",
            re.IGNORECASE | re.DOTALL,
        ),
        "fórmula \"hidrata durante X horas\"",
    ),
    (
        "clinicamente_probado",
        re.compile(r"\bcl[ií]nicamente\s+prob(?:ado|ada)\b", re.IGNORECASE),
        "\"clínicamente probado\"",
    ),
    (
        "dermatologicamente",
        re.compile(r"\bdermatol[oó]gicamente\s+(?:prob|test)ad[oa]\b", re.IGNORECASE),
        "\"dermatológicamente probado/testado\"",
    ),
    (
        "hipoalergenico",
        re.compile(r"\bhipoalerg[eé]nic[oa]\b", re.IGNORECASE),
        "\"hipoalergénico\"",
    ),
    (
        "sin_x",
        re.compile(
            r"\bsin\s+(parabenos|sulfatos|siliconas|alcohol|perfume|conservantes|t[oó]xicos|crueldad)\b",
            re.IGNORECASE,
        ),
        "\"sin X\" (p. ej. \"sin parabenos\")",
    ),
    (
        "no_testado_en_animales",
        re.compile(r"\bno\s+testado\s+en\s+animales\b", re.IGNORECASE),
        "\"no testado en animales\"",
    ),
    (
        "referencia_estudio",
        re.compile(
            r"\bseg[uú]n\s+(?:un\s+)?estudios?\b"
            r"|\bestudios?\s+(?:demuestran?|confirman?|revelan?)\b",
            re.IGNORECASE,
        ),
        "referencia a estudios",
    ),
    (
        "autoevaluacion",
        re.compile(
            r"\b(?:el|la)\s+(?:mejor|m[aá]s\s+\w+|n[uú]mero\s+uno|l[ií]der)\b", re.IGNORECASE
        ),
        "autoevaluación de calidad (P30)",
    ),
)


def analyze_candidatos_claim(ctx):
    candidatos = []
    for start, _end, frag in _iter_oraciones(ctx):
        reglas = []
        marcadores = []
        for id_regla, pattern, _descripcion in _CLAIM_MARKER_RULES:
            m = pattern.search(frag)
            if m:
                reglas.append(id_regla)
                marcadores.append(_clip_texto(m.group(0)))
        m = _PORCENTAJE_RE.search(frag)
        if m:
            reglas.append("porcentaje")
            marcadores.append(_clip_texto(m.group(0)))
        m = _DURACION_UNIDAD_RE.search(frag)
        if m:
            reglas.append("duracion_unidad")
            marcadores.append(_clip_texto(m.group(0)))
        if _CLAIM_NATURAL_RE.search(frag) and _CLAIM_VERBOS_EFICACIA_RE.search(frag):
            reglas.append("natural_mas_efecto")
            marcadores.append("natural + verbo de eficacia")
        if reglas:
            line_no, col = _line_col(ctx.line_starts, start)
            candidatos.append(
                {
                    "linea": line_no,
                    "columna": col,
                    "texto": _clip_texto(frag),
                    "reglas": sorted(set(reglas)),
                    "marcadores": marcadores,
                }
            )
    candidatos.sort(key=lambda h: (h["linea"], h["columna"]))
    return {
        "candidatos": candidatos,
        "marcados": ctx.mask_counts.get("claim", 0),
        "nota": (
            "El script solo señala candidatos a claim: decidir si lo son y "
            "cómo tratarlos es responsabilidad de quien revisa o del "
            "modelo, nunca de este escáner."
        ),
    }


# ---------------------------------------------------------------------------
# Analizador: privacidad. Detecta DNI/NIE, IBAN, teléfono y correo, local y
# efímero: informa solo la categoría y la línea, nunca el valor, y nunca lo
# guarda ni lo registra (auditoria.md §7.6). La ausencia de hallazgos
# no certifica que el texto esté libre de datos personales.
# ---------------------------------------------------------------------------

_DNI_LETRAS = "TRWAGMYFPDXBNJZSQVHLCKE"
_DNI_RE = re.compile(r"\b(\d{8})([A-Za-z])\b")
_NIE_RE = re.compile(r"\b([XYZxyz])(\d{7})([A-Za-z])\b")
_IBAN_RE = re.compile(r"\bES\d{2}(?:[ ]?\d{4}){5}\b")
_TELEFONO_RE = re.compile(r"\b(?:\+34[ .-]?)?[6789]\d{2}(?:[ .-]?\d{3}){2}\b")
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


def _dni_valido(numero_str, letra):
    return _DNI_LETRAS[int(numero_str) % 23] == letra.upper()


def _nie_valido(m):
    mapa = {"X": "0", "Y": "1", "Z": "2"}
    numero_completo = mapa[m.group(1).upper()] + m.group(2)
    return _dni_valido(numero_completo, m.group(3))


def _iban_valido(iban):
    compacto = re.sub(r"\s", "", iban).upper()
    reordenado = compacto[4:] + compacto[:4]
    try:
        numerico = "".join(str(int(ch, 36)) for ch in reordenado)
    except ValueError:
        return False
    return int(numerico) % 97 == 1


_PRIVACY_RULES = (
    ("dni_nie", _NIE_RE, _nie_valido),
    ("dni_nie", _DNI_RE, lambda m: _dni_valido(m.group(1), m.group(2))),
    ("iban", _IBAN_RE, lambda m: _iban_valido(m.group(0))),
    ("telefono", _TELEFONO_RE, None),
    ("email", _EMAIL_RE, None),
)


# ---------------------------------------------------------------------------
# Redacción de datos personales dentro de ``comparacion`` (revisión
# review-4e912a0ac78c9cff, R1-001). ``analyze_privacidad`` nunca repite el
# valor que encuentra, pero antes de esta revisión ``comparacion`` sí lo
# hacía: un teléfono, un DNI/NIE, un IBAN o un correo que cambiaba entre el
# original y el nuevo texto se copiaba tal cual en ``cifras``, ``codigos``,
# ``citas`` o ``nombres_propios`` porque esas categorías no reutilizaban
# los mismos patrones. Estas funciones reutilizan exactamente
# ``_PRIVACY_RULES`` para que ninguna categoría de ``comparacion`` pueda
# volver a filtrar un dato personal, cambie o no entre los dos textos.
# ---------------------------------------------------------------------------


def _find_privacy_spans(text):
    """Tramos ``(inicio, fin, categoria)`` de datos personales detectados
    en ``text`` con los mismos patrones y validadores que
    ``analyze_privacidad``, ordenados por inicio. Se calculan una sola vez
    por texto y se reutilizan para marcar como privado cualquier hecho de
    ``comparacion`` cuyo tramo los solape.
    """
    spans = []
    for categoria, pattern, validador in _PRIVACY_RULES:
        for m in pattern.finditer(text):
            if validador is not None and not validador(m):
                continue
            spans.append((m.start(), m.end(), categoria))
    spans.sort(key=lambda s: s[0])
    return spans


def _categoria_privada_solapada(inicio, fin, privacy_spans):
    """Categoría del primer tramo de ``privacy_spans`` que solapa
    ``[inicio, fin)``, o ``None`` si ninguno lo hace. ``privacy_spans`` está
    ordenado por inicio, así que basta cortar en cuanto un tramo empieza en
    o después de ``fin``: ninguno de los siguientes puede solapar tampoco.
    """
    for p_inicio, p_fin, categoria in privacy_spans:
        if p_inicio >= fin:
            break
        if _ranges_overlap(inicio, fin, p_inicio, p_fin):
            return categoria
    return None


def _marcar_si_privado(hallazgo, inicio, fin, privacy_spans):
    """Si ``[inicio, fin)`` solapa un dato personal, añade la marca interna
    ``_privado`` al hallazgo (nunca se serializa: ``_diff_by_any_reading``
    la consume y la retira con ``_redactar_si_privado`` antes de devolver
    el resultado). El valor real se conserva hasta ese punto porque la
    comparación de lecturas debe seguir funcionando con normalidad."""
    categoria = _categoria_privada_solapada(inicio, fin, privacy_spans)
    if categoria is not None:
        hallazgo["_privado"] = categoria


def _redactar_si_privado(hallazgo):
    """Sustituye ``texto``/``lecturas`` por un marcador de redacción si el
    hallazgo se marcó como dato personal, conservando categoría, línea y
    columna. El elemento se sigue contando (no se descarta) para que un
    dato personal que cambia siga produciendo código de salida 1: lo único
    que se oculta es el valor, nunca el hecho de que hay una diferencia."""
    categoria = hallazgo.get("_privado")
    if categoria is None:
        return hallazgo
    redactado = dict(hallazgo)
    del redactado["_privado"]
    redactado["texto"] = "[dato personal: {}]".format(categoria)
    redactado["lecturas"] = []
    return redactado


_AVISO_PRIVACIDAD = (
    "La ausencia de hallazgos en esta lista NO certifica que el texto esté "
    "libre de datos personales: son patrones deterministas locales y "
    "efímeros, no sustituyen una revisión humana. Ningún valor detectado "
    "se guarda, se registra ni se repite en ningún sitio; solo se informa "
    "de la categoría y la línea."
)


def analyze_privacidad(ctx):
    text = ctx.deterministas_text
    vistos = set()
    hallazgos = []
    for categoria, pattern, validador in _PRIVACY_RULES:
        for m in pattern.finditer(text):
            if validador is not None and not validador(m):
                continue
            line_no, _col = _line_col(ctx.line_starts, m.start())
            clave = (categoria, line_no)
            if clave in vistos:
                continue
            vistos.add(clave)
            hallazgos.append({"categoria": categoria, "linea": line_no})
    hallazgos.sort(key=lambda h: (h["linea"], h["categoria"]))
    return {"hallazgos": hallazgos, "aviso": _AVISO_PRIVACIDAD}


# ---------------------------------------------------------------------------
# Registro de analizadores (T4-T5 añaden aquí sin tocar lo anterior)
# ---------------------------------------------------------------------------

ANALYZERS = (
    ("entrada", analyze_entrada),
    ("enmascarado", analyze_enmascarado),
    ("vocabulario", analyze_vocabulario),
    ("rayas", analyze_rayas),
    ("comillas", analyze_comillas),
    ("encabezados", analyze_encabezados),
    ("tipografia", analyze_tipografia),
    ("estructuras", analyze_estructuras),
    ("deterministas", analyze_deterministas),
    ("registro", analyze_registro),
    ("candidatos_claim", analyze_candidatos_claim),
    ("privacidad", analyze_privacidad),
)


def build_report(text, vocab_entries, original_text=None):
    """Punto de entrada de análisis, independiente de la CLI. Construye el
    contexto una vez y ejecuta cada analizador registrado en ``ANALYZERS``.
    Si se da ``original_text``, añade además la clave ``comparacion`` con
    la comparación entre ese texto fuente y ``text`` (el ya analizado).
    """
    ctx = _build_context(text, vocab_entries)
    report = {"version": VERSION}
    for name, analyzer in ANALYZERS:
        report[name] = analyzer(ctx)
    if original_text is not None:
        report["comparacion"] = _build_comparacion(ctx, original_text, report["registro"])
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="scan_tells.py",
        description=(
            "Escáner determinista y barato de rasgos de texto generado por "
            "IA, para la skill prosa-natural. Solo informa: nunca reescribe "
            "el texto ni calcula una puntuación de 'probabilidad de IA'."
        ),
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Muestra esta ayuda y termina.",
    )
    parser.add_argument(
        "ruta",
        nargs="?",
        default="-",
        help=(
            "Ruta al archivo de texto a analizar (UTF-8). Si se omite o se "
            "pasa '-', se lee de la entrada estándar."
        ),
    )
    parser.add_argument(
        "--vocabulario",
        metavar="RUTA",
        default=None,
        help=(
            "Ruta al archivo de vocabulario a usar en vez del predeterminado "
            "(references/vocabulario-es.md, relativo a este script)."
        ),
    )
    parser.add_argument(
        "--original",
        metavar="RUTA",
        default=None,
        help=(
            "Ruta al texto fuente para comparar con la entrada analizada "
            "(clave 'comparacion' del JSON): cifras, porcentajes, fechas, "
            "precios, duraciones/unidades, códigos, nombres propios, URL, "
            "claims marcados [[claim]]…[[/claim]] y citas literales que "
            "falten en el nuevo texto o que aparezcan de nuevo, en ambas "
            "direcciones; también compara los recuentos de tú/usted y "
            "vosotros/ustedes, solo como dato. Con esta opción, el código "
            "de salida es 1 si hay alguna diferencia en esas categorías "
            "(las siglas y el recuento de tú/usted son solo informativos y "
            "nunca cambian el código de salida)."
        ),
    )
    # argparse no expone una forma pública de traducir los títulos de
    # sección ("positional arguments"/"options"); se ajustan aquí para que
    # la ayuda quede en español de España, como exige el encargo.
    parser._positionals.title = "argumentos posicionales"
    parser._optionals.title = "opciones"
    return parser


def _read_input(ruta):
    if ruta is None or ruta == "-":
        data = sys.stdin.buffer.read()
        source_name = "<stdin>"
    else:
        path = Path(ruta)
        try:
            data = path.read_bytes()
        except OSError as exc:
            print(
                "scan_tells.py: no se pudo leer '{}': {}".format(ruta, exc),
                file=sys.stderr,
            )
            sys.exit(2)
        source_name = ruta
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(
            "scan_tells.py: '{}' no es UTF-8 válido: {}".format(source_name, exc),
            file=sys.stderr,
        )
        sys.exit(2)


def _read_original(ruta):
    path = Path(ruta)
    try:
        data = path.read_bytes()
    except OSError as exc:
        print(
            "scan_tells.py: no se pudo leer '{}' (--original): {}".format(ruta, exc),
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(
            "scan_tells.py: '{}' no es UTF-8 válido (--original): {}".format(ruta, exc),
            file=sys.stderr,
        )
        sys.exit(2)


def main(argv=None):
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    vocab_path = args.vocabulario if args.vocabulario else DEFAULT_VOCAB_PATH
    try:
        vocab_entries = parse_vocabulary(vocab_path)
    except VocabParseError as exc:
        print("scan_tells.py: {}".format(exc), file=sys.stderr)
        sys.exit(2)

    text = _read_input(args.ruta)
    original_text = _read_original(args.original) if args.original is not None else None

    report = build_report(text, vocab_entries, original_text=original_text)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))

    if original_text is not None and _comparacion_tiene_diferencias_bloqueantes(
        report["comparacion"]
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
