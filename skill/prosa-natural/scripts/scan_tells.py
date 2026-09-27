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
enmascarado aplicado. ``vocabulario`` busca sobre el texto con el
frontmatter, el código, las URL, los ``[[claim]]…[[/claim]]`` Y las citas
entre comillas enmascarados (para no marcar como propia una palabra que en
realidad está dentro de una cita textual). ``rayas``, ``comillas``,
``encabezados`` y ``tipografia`` son los detectores de forma: buscan sobre
una vista distinta, con el frontmatter, el código, las URL y los
``[[claim]]…[[/claim]]`` enmascarados pero las comillas SIN enmascarar,
porque necesitan ver los propios caracteres de puntuación (comillas,
rayas, mayúsculas) para poder analizarlos. Ninguno de los cuatro aplica un
umbral ni emite un veredicto: solo reportan hechos (tipo, ubicación y,
donde corresponde, densidad por mil palabras), igual que el resto del
script.
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
    mask_counts: Dict[str, int]
    vocab_entries: List[VocabEntry]
    paragraphs: List[Tuple[int, int]]
    surface_paragraphs: List[Tuple[int, int]]
    line_starts: List[int]
    normalized_text: str
    orig_index_for_normpos: List[int]
    norm_start_for_orig: List[int]
    total_words: int


def _build_context(text, vocab_entries):
    masked_text, surface_text, mask_counts = mask_text(text)
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
    """
    ordered = sorted(
        raw_hits,
        key=lambda h: (
            -(h["_fin"] - h["_inicio"]),
            NIVELES_VALIDOS.index(h["nivel"]),
            h["expresion"],
        ),
    )
    kept = []
    covered = []
    for h in ordered:
        inicio, fin = h["_inicio"], h["_fin"]
        if any(inicio < c_fin and c_inicio < fin for c_inicio, c_fin in covered):
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
                    }
                )

    hits = _resolve_overlapping_hits(raw_hits)
    for h in hits:
        del h["_inicio"]
        del h["_fin"]
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


def _raya_inglesa_subtipo(d):
    if not d["sin_palabra_antes"] and not d["sin_palabra_despues"]:
        return "pegada"
    if d["sin_palabra_antes"] and d["sin_palabra_despues"]:
        return "espaciada"
    return "conector_universal"


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
        i = 0
        while i < len(pendientes):
            if i + 1 < len(pendientes):
                d1, d2 = pendientes[i], pendientes[i + 1]
                apertura_ok = d1["sin_palabra_antes"] and not d1["sin_palabra_despues"]
                cierre_ok = not d2["sin_palabra_antes"] and d2["sin_palabra_despues"]
                if apertura_ok and cierre_ok:
                    hallazgos.append({"tipo": "inciso_cerrado", "linea": d1["linea"], "columna": d1["columna"]})
                    hallazgos.append({"tipo": "inciso_cerrado", "linea": d2["linea"], "columna": d2["columna"]})
                else:
                    for d in (d1, d2):
                        hallazgos.append(
                            {
                                "tipo": "raya_inglesa",
                                "subtipo": _raya_inglesa_subtipo(d),
                                "linea": d["linea"],
                                "columna": d["columna"],
                            }
                        )
                i += 2
            else:
                d = pendientes[i]
                hallazgos.append(
                    {
                        "tipo": "raya_inglesa",
                        "subtipo": "sin_cierre",
                        "linea": d["linea"],
                        "columna": d["columna"],
                    }
                )
                i += 1

    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    conteo = {}
    for tipo in ("dialogo", "inciso_cerrado", "raya_inglesa", "en_encabezado"):
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


def _find_quote_spans(ctx):
    spans = []
    for p_start, p_end in ctx.surface_paragraphs:
        sub = ctx.surface_text[p_start:p_end]
        for tipo, pattern in _QUOTE_TYPES:
            for m in pattern.finditer(sub):
                spans.append({"tipo": tipo, "inicio": p_start + m.start(), "fin": p_start + m.end()})

    for span in spans:
        nivel = 1
        padre = None
        for otro in spans:
            if otro is span:
                continue
            contiene = otro["inicio"] <= span["inicio"] and span["fin"] <= otro["fin"]
            si_estricto = otro["inicio"] < span["inicio"] or span["fin"] < otro["fin"]
            if contiene and si_estricto:
                nivel += 1
                if padre is None or (otro["fin"] - otro["inicio"]) < (padre["fin"] - padre["inicio"]):
                    padre = otro
        span["nivel"] = nivel
        span["padre"] = padre
    return spans


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
# prosa corrida y exclamaciones por mil palabras. Usa ``surface_text``.
# ---------------------------------------------------------------------------


def _tipografia_signos(ctx):
    hallazgos = []
    for p_start, p_end in ctx.surface_paragraphs:
        sub = ctx.surface_text[p_start:p_end]
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

    Salvaguardas (auditoria.md, P57): no se informa si los dos puntos
    introducen una cita textual (les sigue directamente una comilla de
    apertura) ni si introducen un elemento de lista o un bloque en la línea
    siguiente (hay un salto de línea entre los dos puntos y el siguiente
    carácter no en blanco).
    """
    text = ctx.surface_text
    hallazgos = []
    for m in re.finditer(":", text):
        idx = m.start()
        j = idx + 1
        while j < len(text) and text[j] in (" ", "\t"):
            j += 1
        if j >= len(text):
            continue
        siguiente = text[j]
        if siguiente in "«\"“'":
            continue
        if "\n" in text[idx + 1 : j]:
            continue
        if siguiente.isalpha() and siguiente.isupper():
            line_no, col = _line_col(ctx.line_starts, j)
            hallazgos.append({"linea": line_no, "columna": col})
    hallazgos.sort(key=lambda h: (h["linea"], h["columna"]))
    return hallazgos


def analyze_tipografia(ctx):
    total_excl = ctx.surface_text.count("!")
    por_mil = round(total_excl / ctx.total_words * 1000, 3) if ctx.total_words else 0.0
    return {
        "signos_sin_apertura": _tipografia_signos(ctx),
        "mayuscula_tras_dos_puntos": _tipografia_mayuscula_tras_dos_puntos(ctx),
        "exclamaciones": {"ocurrencias": total_excl, "por_mil_palabras": por_mil},
    }


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
)


def build_report(text, vocab_entries):
    """Punto de entrada de análisis, independiente de la CLI. Construye el
    contexto una vez y ejecuta cada analizador registrado en ``ANALYZERS``.
    """
    ctx = _build_context(text, vocab_entries)
    report = {"version": VERSION}
    for name, analyzer in ANALYZERS:
        report[name] = analyzer(ctx)
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
    report = build_report(text, vocab_entries)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
