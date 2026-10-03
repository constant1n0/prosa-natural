#!/usr/bin/env python3
"""Corrector automático de las aserciones de los evals de ``prosa-natural``.

Qué hace y qué no hace
-----------------------
Este script gradúa, de forma programática, las ejecuciones registradas en
``evals/resultados/iter-N/`` contra las aserciones con chequeo máquina de
``evals/evals.json``. Es herramienta de repositorio para la Fase 3 de evals,
no forma parte de la skill distribuida (regla dura 5 de ``CLAUDE.md``: la
skill solo es Markdown). Usa exclusivamente la biblioteca estándar de Python
y, cuando lo necesita, importa o invoca como subproceso
``skill/prosa-natural/scripts/scan_tells.py`` (ese script sí es de solo
lectura: nunca se reescribe nada desde aquí).

Disposición de carpetas que gradúa
-------------------------------------
``evals/resultados/iter-N/eval-NN-<slug>/`` contiene ``eval_metadata.json``
(con la clave ``eval_id``, que enlaza con el id del eval en ``evals.json``) y,
por cada configuración ``with_skill``/``without_skill``, carpetas
``run-K/outputs/`` con ``respuesta.md`` (siempre) y, solo cuando se entregó
una reescritura, ``version_final.md``. El texto de entrada de un eval es su
primera ruta en ``files`` (relativa a la raíz del repositorio, entendida como
la carpeta que contiene ``evals/evals.json``).

Contrato de los tipos de chequeo
-----------------------------------
Antes de cualquier comparación de subcadena o de expresión regular, ambos
textos se normalizan con Unicode NFC y colapsando cualquier tanda de espacio
en blanco a un único espacio (``normalize_text``), porque el modelo evaluado
puede reformatear los párrafos sin cambiar el contenido. Los chequeos que
delegan en ``scan_tells.py`` (``sin_invencion``, ``sin_fuertes``,
``densidad_debil_no_aumenta``, ``registro_igual``) pasan el texto tal cual,
sin esa normalización, porque el propio escáner ya tolera reformateos dentro
de un párrafo y necesita los saltos de línea para separar párrafos.

Cada chequeo que necesita una versión final y no la encuentra falla con la
evidencia literal ``"no hay versión final"``, salvo que su propia opción
diga lo contrario (``sin_invencion`` con ``omitir_si_sin_final``, y
``similitud_minima`` con ``sin_final_valido_si``). Un tipo de chequeo
desconocido es un error de uso: aborta con :class:`ComprobarError` (código de
salida 2 en la CLI), nunca se informa como aserción fallida.

Formato de ``grading.json``: ``{"expectations": [{"text", "passed",
"evidence"}], "summary": {"passed", "failed", "total", "pass_rate"}}``, con
los mismos nombres de clave exactos que usan el agregador y el visor de la
Fase 3. Se escribe con ``ensure_ascii=False``, ``indent=2`` y
``sort_keys=True``; ``pass_rate`` se redondea a 4 decimales.

Códigos de salida de la CLI: 0 cuando la graduación se completa (aunque
alguna aserción falle); 2 en errores de uso o de entrada (archivo o carpeta
inexistente, JSON inválido, id de eval inexistente, tipo de chequeo
desconocido), siempre con un mensaje en español en stderr.
"""

import argparse
import difflib
import functools
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SCRIPT_ROOT = Path(__file__).resolve().parent.parent
SCAN_TELLS_RELATIVE_PATH = Path("skill") / "prosa-natural" / "scripts" / "scan_tells.py"

_NO_HAY_VERSION_FINAL = "no hay versión final"


class ComprobarError(Exception):
    """Error de uso o de entrada: la CLI lo traduce al código de salida 2."""


# ---------------------------------------------------------------------------
# Normalización de texto (NFC + colapso de espacios en blanco)
# ---------------------------------------------------------------------------


def normalize_text(text):
    """Unicode NFC y colapso de cualquier tanda de espacio en blanco a uno
    solo, para que un simple reformateo de párrafos del modelo evaluado no
    rompa una comparación de subcadena o de expresión regular."""
    texto = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", texto).strip()


# ---------------------------------------------------------------------------
# Carga perezosa de scan_tells.py (import, no como paquete)
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def load_scan_tells_module():
    """Importa ``scan_tells.py`` por ruta (no es un paquete instalable),
    igual que hace ``tests/test_scan_tells.py``. Se cachea porque parsear el
    vocabulario y compilar los patrones tiene un coste no despreciable y
    este módulo lo necesita para cada chequeo basado en el escáner."""
    ruta = SCRIPT_ROOT / SCAN_TELLS_RELATIVE_PATH
    spec = importlib.util.spec_from_file_location("prosa_natural_scan_tells", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@functools.lru_cache(maxsize=1)
def load_default_vocab_entries():
    modulo = load_scan_tells_module()
    return modulo.parse_vocabulary(modulo.DEFAULT_VOCAB_PATH)


# ---------------------------------------------------------------------------
# Contexto de graduación de una expectativa
# ---------------------------------------------------------------------------


@dataclass
class EvalContext:
    """Todo lo que necesita un chequeo para graduar una expectativa de un
    eval concreto sobre una ejecución concreta."""

    input_path: Path
    input_text: str
    final_path: Path
    final_text: Optional[str]
    respuesta_path: Path
    respuesta_text: Optional[str]
    scan_tells: object
    scan_tells_path: Path
    vocab_entries: list


def read_optional(path):
    """Devuelve el contenido de ``path``, o ``None`` si no existe o queda
    vacío tras quitar espacios en los extremos (así se representan tanto
    "no se entregó ``version_final.md``" como un archivo vacío)."""
    if path is None or not Path(path).exists():
        return None
    texto = Path(path).read_text(encoding="utf-8")
    if texto.strip() == "":
        return None
    return texto


# ---------------------------------------------------------------------------
# Chequeos individuales. Cada uno recibe (check, ctx) y devuelve
# (passed: bool, evidence: str).
# ---------------------------------------------------------------------------


def _resolve_target(check, ctx):
    """Resuelve el texto destino de un chequeo con opción ``en``
    ("final" por defecto, o "respuesta"), junto con la evidencia genérica
    que corresponde si ese texto no está disponible."""
    en = check.get("en", "final")
    if en == "respuesta":
        return ctx.respuesta_text, "no se encontró respuesta.md"
    return ctx.final_text, _NO_HAY_VERSION_FINAL


def _handle_debe_contener(check, ctx):
    destino, evidencia_ausente = _resolve_target(check, ctx)
    if destino is None:
        return False, evidencia_ausente
    destino_normalizado = normalize_text(destino)
    faltan = [
        valor for valor in check["values"]
        if normalize_text(valor) not in destino_normalizado
    ]
    if faltan:
        return False, "faltan: {}".format(faltan)
    return True, "todos los valores están presentes"


def _handle_no_aumenta(check, ctx):
    destino, evidencia_ausente = _resolve_target(check, ctx)
    if destino is None:
        return False, evidencia_ausente
    patron = re.compile(check["pattern"])
    n_original = len(patron.findall(normalize_text(ctx.input_text)))
    n_destino = len(patron.findall(normalize_text(destino)))
    passed = n_destino <= n_original
    return passed, "original={}, final={}".format(n_original, n_destino)


def _handle_sin_fuertes(check, ctx):
    if ctx.final_text is None:
        return False, _NO_HAY_VERSION_FINAL
    informe = ctx.scan_tells.build_report(ctx.final_text, ctx.vocab_entries)
    fuertes = sorted({
        h["expresion"] for h in informe["vocabulario"]["hallazgos"] if h["nivel"] == "Fuerte"
    })
    if fuertes:
        return False, "vocablos de nivel Fuerte encontrados: {}".format(fuertes)
    return True, "no se encontraron vocablos de nivel Fuerte"


def _densidad_debil(ctx, text):
    informe = ctx.scan_tells.build_report(text, ctx.vocab_entries)
    return informe["vocabulario"]["densidad"]["por_nivel"]["Débil"]["por_mil_palabras"]


def _handle_densidad_debil_no_aumenta(check, ctx):
    if ctx.final_text is None:
        return False, _NO_HAY_VERSION_FINAL
    original = _densidad_debil(ctx, ctx.input_text)
    final = _densidad_debil(ctx, ctx.final_text)
    passed = final <= original
    return passed, "original={}, final={} (por mil palabras)".format(original, final)


_URL_RE = re.compile(r"(?:https?://|www\.)\S+")
_FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]+`")


def _extract_untouchables(texto_normalizado):
    """URL, bloques de código y código en línea de un texto ya normalizado
    (NFC + espacios colapsados). El código en línea se busca solo fuera de
    los bloques de código, para no confundir sus delimitadores."""
    bloques = _FENCED_CODE_RE.findall(texto_normalizado)
    resto = _FENCED_CODE_RE.sub(" ", texto_normalizado)
    en_linea = _INLINE_CODE_RE.findall(resto)
    urls = _URL_RE.findall(texto_normalizado)
    return urls + bloques + en_linea


def _handle_intocables(check, ctx):
    if ctx.final_text is None:
        return False, _NO_HAY_VERSION_FINAL
    entrada_normalizada = normalize_text(ctx.input_text)
    final_normalizado = normalize_text(ctx.final_text)
    elementos = _extract_untouchables(entrada_normalizada)
    faltan = [elem for elem in elementos if elem not in final_normalizado]
    if faltan:
        return False, "faltan: {}".format(faltan)
    return True, "todos los elementos intocables se conservan"


_CLAVES_REGISTRO = ("tuteo", "usted", "vosotros", "ustedes")


def _registro_presencia(ctx, text):
    informe = ctx.scan_tells.build_report(text, ctx.vocab_entries)
    registro = informe["registro"]
    return {clave: registro[clave]["ocurrencias"] for clave in _CLAVES_REGISTRO}


def _handle_registro_igual(check, ctx):
    if ctx.final_text is None:
        return False, _NO_HAY_VERSION_FINAL
    original = _registro_presencia(ctx, ctx.input_text)
    final = _registro_presencia(ctx, ctx.final_text)
    passed = all((original[c] > 0) == (final[c] > 0) for c in _CLAVES_REGISTRO)
    return passed, "original={}, final={}".format(original, final)


def _handle_similitud_minima(check, ctx):
    if ctx.final_text is None:
        patron = re.compile(check["sin_final_valido_si"], re.IGNORECASE)
        respuesta_normalizada = normalize_text(ctx.respuesta_text or "")
        if patron.search(respuesta_normalizada):
            return True, (
                "sin versión final; respuesta.md coincide con el patrón de "
                "continuidad, ratio tratado como 1.0"
            )
        return False, _NO_HAY_VERSION_FINAL
    ratio = difflib.SequenceMatcher(
        None, normalize_text(ctx.input_text), normalize_text(ctx.final_text)
    ).ratio()
    passed = ratio >= check["min"]
    return passed, "ratio={:.4f} (mínimo {})".format(ratio, check["min"])


def _handle_sin_version_final(check, ctx):
    if ctx.final_text is None:
        return True, _NO_HAY_VERSION_FINAL
    return False, "se entregó una versión final"


def _handle_respuesta_coincide(check, ctx):
    if ctx.respuesta_text is None:
        return False, "no se encontró respuesta.md"
    respuesta_normalizada = normalize_text(ctx.respuesta_text)
    sin_coincidencia = [
        patron_texto for patron_texto in check["patterns"]
        if not re.search(patron_texto, respuesta_normalizada, re.IGNORECASE)
    ]
    if sin_coincidencia:
        return False, "patrones sin coincidencia: {}".format(sin_coincidencia)
    return True, "todos los patrones coinciden"


def _formatear_categorias_comparacion(comparacion):
    partes = []
    for categoria in sorted(comparacion):
        if categoria == "registro":
            continue
        valores = comparacion[categoria]
        faltantes = [it.get("texto") for it in valores.get("faltantes", [])]
        nuevas = [it.get("texto") for it in valores.get("nuevas", [])]
        if not (faltantes or nuevas):
            continue
        detalle = []
        if faltantes:
            detalle.append("faltantes: {}".format(faltantes))
        if nuevas:
            detalle.append("nuevas: {}".format(nuevas))
        partes.append("{} ({})".format(categoria, "; ".join(detalle)))
    return partes


def _handle_sin_invencion(check, ctx):
    if ctx.final_text is None:
        if check.get("omitir_si_sin_final"):
            return True, "sin versión final: no aplica"
        return False, _NO_HAY_VERSION_FINAL

    resultado = subprocess.run(
        [
            sys.executable,
            str(ctx.scan_tells_path),
            "--original",
            str(ctx.input_path),
            str(ctx.final_path),
        ],
        capture_output=True,
        text=True,
    )
    if resultado.returncode == 0:
        return True, "el escáner no detecta diferencias bloqueantes"
    if resultado.returncode == 1:
        try:
            datos = json.loads(resultado.stdout)
        except json.JSONDecodeError as exc:
            raise ComprobarError(
                "scan_tells.py no devolvió JSON válido al comparar '{}' con "
                "'{}': {}".format(ctx.input_path, ctx.final_path, exc)
            )
        partes = _formatear_categorias_comparacion(datos.get("comparacion", {}))
        if partes:
            return False, "categorías con diferencias: {}".format("; ".join(partes))
        return False, "el escáner detectó diferencias bloqueantes"
    raise ComprobarError(
        "scan_tells.py terminó con código {} al comparar '{}' con '{}': {}".format(
            resultado.returncode, ctx.input_path, ctx.final_path, resultado.stderr.strip()
        )
    )


_CHECK_HANDLERS = {
    "sin_invencion": _handle_sin_invencion,
    "debe_contener": _handle_debe_contener,
    "no_aumenta": _handle_no_aumenta,
    "sin_fuertes": _handle_sin_fuertes,
    "densidad_debil_no_aumenta": _handle_densidad_debil_no_aumenta,
    "intocables": _handle_intocables,
    "registro_igual": _handle_registro_igual,
    "similitud_minima": _handle_similitud_minima,
    "sin_version_final": _handle_sin_version_final,
    "respuesta_coincide": _handle_respuesta_coincide,
}


def evaluate_expectation(expectation, ctx):
    """Gradúa una expectativa de ``evals.json`` (con su clave ``check``)
    contra el contexto ``ctx`` de una ejecución. Devuelve
    ``(passed, evidence)``. Lanza :class:`ComprobarError` ante un tipo de
    chequeo desconocido: eso es un error de uso, no una aserción fallida."""
    check = expectation["check"]
    tipo = check["type"]
    manejador = _CHECK_HANDLERS.get(tipo)
    if manejador is None:
        raise ComprobarError(
            "tipo de chequeo desconocido: '{}' (expectativa: '{}')".format(
                tipo, expectation.get("text")
            )
        )
    return manejador(check, ctx)


# ---------------------------------------------------------------------------
# Carga de evals.json
# ---------------------------------------------------------------------------


def load_evals(path):
    ruta = Path(path)
    try:
        contenido = ruta.read_text(encoding="utf-8")
    except OSError as exc:
        raise ComprobarError("no se pudo leer '{}': {}".format(ruta, exc))
    try:
        datos = json.loads(contenido)
    except json.JSONDecodeError as exc:
        raise ComprobarError("'{}' no es JSON válido: {}".format(ruta, exc))
    if "evals" not in datos:
        raise ComprobarError("'{}' no contiene la clave 'evals'".format(ruta))
    return datos


def find_eval(evals_data, eval_id):
    for eval_obj in evals_data.get("evals", []):
        if eval_obj.get("id") == eval_id:
            return eval_obj
    raise ComprobarError("no existe ningún eval con id {}".format(eval_id))


# ---------------------------------------------------------------------------
# Graduación de una carpeta run-K/
# ---------------------------------------------------------------------------


def grade_run(eval_obj, run_dir, *, repo_root, scan_tells_module, scan_tells_path, vocab_entries):
    """Gradúa todas las expectativas de ``eval_obj`` contra la ejecución de
    ``run_dir`` (que debe contener ``outputs/respuesta.md`` y, si procede,
    ``outputs/version_final.md``), escribe ``run_dir/grading.json`` y
    devuelve el mismo diccionario que se escribió."""
    run_dir = Path(run_dir)
    entrada_relativa = eval_obj["files"][0]
    input_path = (Path(repo_root) / entrada_relativa).resolve()
    if not input_path.exists():
        raise ComprobarError(
            "no se encontró el archivo de entrada '{}' del eval {}".format(
                input_path, eval_obj.get("id")
            )
        )
    input_text = input_path.read_text(encoding="utf-8")

    outputs_dir = run_dir / "outputs"
    respuesta_path = outputs_dir / "respuesta.md"
    final_path = outputs_dir / "version_final.md"

    ctx = EvalContext(
        input_path=input_path,
        input_text=input_text,
        final_path=final_path,
        final_text=read_optional(final_path),
        respuesta_path=respuesta_path,
        respuesta_text=read_optional(respuesta_path),
        scan_tells=scan_tells_module,
        scan_tells_path=scan_tells_path,
        vocab_entries=vocab_entries,
    )

    expectativas = []
    for expectation in eval_obj["expectations"]:
        passed, evidence = evaluate_expectation(expectation, ctx)
        expectativas.append({
            "text": expectation["text"],
            "passed": bool(passed),
            "evidence": evidence,
        })

    total = len(expectativas)
    aprobadas = sum(1 for e in expectativas if e["passed"])
    fallidas = total - aprobadas
    pass_rate = round(aprobadas / total, 4) if total else 0.0

    grading = {
        "expectations": expectativas,
        "summary": {
            "passed": aprobadas,
            "failed": fallidas,
            "total": total,
            "pass_rate": pass_rate,
        },
    }

    (run_dir / "grading.json").write_text(
        json.dumps(grading, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return grading


# ---------------------------------------------------------------------------
# Descubrimiento de carpetas de ejecución en una iteración
# ---------------------------------------------------------------------------

_SUFIJO_NUMERICO_RE = re.compile(r"-(\d+)$")


def _clave_orden_numerico(nombre):
    m = _SUFIJO_NUMERICO_RE.search(nombre)
    return int(m.group(1)) if m else 0


def discover_run_dirs(iteracion_dir):
    """Recorre ``iteracion_dir/eval-*/`` y devuelve una lista de tuplas
    ``(nombre_carpeta_eval, eval_id, configuracion, run_dir)`` en orden:
    evals por nombre de carpeta, configuración ``with_skill`` antes que
    ``without_skill``, y ejecuciones por su sufijo numérico (``run-2`` antes
    que ``run-10``)."""
    resultado = []
    carpetas_eval = sorted(
        (p for p in Path(iteracion_dir).glob("eval-*") if p.is_dir()),
        key=lambda p: p.name,
    )
    for carpeta_eval in carpetas_eval:
        metadata_path = carpeta_eval / "eval_metadata.json"
        if not metadata_path.exists():
            raise ComprobarError("falta '{}'".format(metadata_path))
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ComprobarError("'{}' no es JSON válido: {}".format(metadata_path, exc))
        if "eval_id" not in metadata:
            raise ComprobarError("'{}' no contiene 'eval_id'".format(metadata_path))
        eval_id = metadata["eval_id"]
        for configuracion in ("with_skill", "without_skill"):
            config_dir = carpeta_eval / configuracion
            if not config_dir.is_dir():
                continue
            carpetas_run = sorted(
                (p for p in config_dir.glob("run-*") if p.is_dir()),
                key=lambda p: _clave_orden_numerico(p.name),
            )
            for run_dir in carpetas_run:
                resultado.append((carpeta_eval.name, eval_id, configuracion, run_dir))
    return resultado


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="comprobar.py",
        description=(
            "Gradúa programáticamente las ejecuciones de los evals de "
            "prosa-natural contra las aserciones de evals/evals.json."
        ),
    )
    parser.add_argument("--evals", required=True, metavar="RUTA", help="Ruta a evals.json.")
    parser.add_argument(
        "--iteracion", metavar="RUTA", default=None,
        help="Gradúa todas las ejecuciones encontradas en esta carpeta de iteración.",
    )
    parser.add_argument(
        "--run", metavar="RUTA", default=None,
        help="Gradúa una sola carpeta run-K/ (requiere --eval-id).",
    )
    parser.add_argument(
        "--eval-id", type=int, default=None, metavar="N",
        help="Id del eval al que corresponde --run.",
    )
    return parser


def _imprimir_resumen(filas):
    encabezado = ("eval", "configuración", "ejecución", "aprobadas/total")
    lineas = [encabezado]
    for fila in filas:
        lineas.append((
            str(fila["eval"]),
            str(fila["configuration"]),
            str(fila["run"]),
            "{}/{}".format(fila["passed"], fila["total"]),
        ))
    anchos = [max(len(linea[i]) for linea in lineas) for i in range(len(encabezado))]
    for linea in lineas:
        print("  ".join(valor.ljust(ancho) for valor, ancho in zip(linea, anchos)))


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        evals_path = Path(args.evals)
        if not evals_path.exists():
            raise ComprobarError("no se encontró el archivo de evals '{}'".format(evals_path))
        evals_data = load_evals(evals_path)
        repo_root = evals_path.resolve().parent.parent

        scan_tells_module = load_scan_tells_module()
        scan_tells_path = Path(scan_tells_module.__file__)
        vocab_entries = load_default_vocab_entries()

        filas = []
        if args.run is not None or args.eval_id is not None:
            if args.run is None or args.eval_id is None:
                raise ComprobarError("--run y --eval-id se deben usar juntos")
            if args.iteracion is not None:
                raise ComprobarError("--iteracion no se puede combinar con --run/--eval-id")
            run_dir = Path(args.run)
            if not run_dir.is_dir():
                raise ComprobarError(
                    "no se encontró la carpeta de ejecución '{}'".format(run_dir)
                )
            eval_obj = find_eval(evals_data, args.eval_id)
            grading = grade_run(
                eval_obj, run_dir, repo_root=repo_root,
                scan_tells_module=scan_tells_module, scan_tells_path=scan_tells_path,
                vocab_entries=vocab_entries,
            )
            filas.append({
                "eval": eval_obj["name"],
                "configuration": run_dir.parent.name,
                "run": run_dir.name,
                **grading["summary"],
            })
        elif args.iteracion is not None:
            iteracion_dir = Path(args.iteracion)
            if not iteracion_dir.is_dir():
                raise ComprobarError(
                    "no se encontró la carpeta de iteración '{}'".format(iteracion_dir)
                )
            for nombre_carpeta, eval_id, configuracion, run_dir in discover_run_dirs(iteracion_dir):
                eval_obj = find_eval(evals_data, eval_id)
                grading = grade_run(
                    eval_obj, run_dir, repo_root=repo_root,
                    scan_tells_module=scan_tells_module, scan_tells_path=scan_tells_path,
                    vocab_entries=vocab_entries,
                )
                filas.append({
                    "eval": eval_obj["name"],
                    "configuration": configuracion,
                    "run": run_dir.name,
                    **grading["summary"],
                })
        else:
            raise ComprobarError(
                "se debe indicar --iteracion, o bien --run junto con --eval-id"
            )

        _imprimir_resumen(filas)
        return 0
    except ComprobarError as exc:
        print("comprobar.py: {}".format(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
