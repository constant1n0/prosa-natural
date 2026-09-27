"""Tests estrictos (TDD) para skill/prosa-natural/scripts/scan_tells.py.

Todos los textos de prueba son propios, con marcas y nombres ficticios.
Se ejecuta con `python3 -m unittest discover -s tests -v` (stdlib, sin pytest).
"""

import ast
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "skill" / "prosa-natural" / "scripts" / "scan_tells.py"
VOCAB_PATH = REPO_ROOT / "skill" / "prosa-natural" / "references" / "vocabulario-es.md"


def load_module():
    spec = importlib.util.spec_from_file_location("scan_tells", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_vocab(tmp_dir, content):
    path = Path(tmp_dir) / "vocabulario-prueba.md"
    path.write_text(content, encoding="utf-8")
    return path


def run_cli(args, input_text=None):
    cmd = [sys.executable, str(SCRIPT_PATH)] + args
    return subprocess.run(
        cmd,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


MINIMAL_VOCAB = """\
## Fuerte

### Restos de ejemplo

¡claro que si! | 2026-09-27 | PXX · prueba

## Débil

### Familia de prueba

optimiz* | 2026-09-27 | PXX · prueba
clave | 2026-09-27 | PXX · prueba
en resumen, | 2026-09-27 | PXX · prueba
a nivel de | 2026-09-27 | PXX · prueba | pendiente
"""


class TestVocabularyParser(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_parses_valid_minimal_file(self):
        path = write_vocab(self.tmp.name, MINIMAL_VOCAB)
        entries = self.module.parse_vocabulary(path)
        self.assertEqual(len(entries), 5)
        fuerte = [e for e in entries if e.nivel == "Fuerte"]
        debil = [e for e in entries if e.nivel == "Débil"]
        self.assertEqual(len(fuerte), 1)
        self.assertEqual(len(debil), 4)
        self.assertEqual(fuerte[0].expresion, "¡claro que si!")
        self.assertEqual(fuerte[0].familia, "Restos de ejemplo")
        self.assertFalse(fuerte[0].pendiente)

    def test_pendiente_flag(self):
        path = write_vocab(self.tmp.name, MINIMAL_VOCAB)
        entries = self.module.parse_vocabulary(path)
        pendientes = [e for e in entries if e.pendiente]
        self.assertEqual(len(pendientes), 1)
        self.assertEqual(pendientes[0].expresion, "a nivel de")
        no_pendientes = [e for e in entries if e.expresion == "clave"]
        self.assertFalse(no_pendientes[0].pendiente)

    def test_wildcard_entry_parses(self):
        path = write_vocab(self.tmp.name, MINIMAL_VOCAB)
        entries = self.module.parse_vocabulary(path)
        wildcard = [e for e in entries if e.expresion == "optimiz*"]
        self.assertEqual(len(wildcard), 1)

    def test_other_heading_ends_parsed_region(self):
        content = MINIMAL_VOCAB + (
            "\n## Excluidas y variantes\n\n"
            "Esto es prosa suelta que no sigue el formato de entrada "
            "y no debe intentarse parsear.\n"
        )
        path = write_vocab(self.tmp.name, content)
        entries = self.module.parse_vocabulary(path)
        self.assertEqual(len(entries), 5)

    def test_malformed_line_raises_with_line_number(self):
        content = (
            "## Fuerte\n\n"
            "### Familia rota\n\n"
            "esto no tiene el formato correcto\n"
        )
        path = write_vocab(self.tmp.name, content)
        with self.assertRaises(self.module.VocabParseError) as ctx:
            self.module.parse_vocabulary(path)
        self.assertEqual(ctx.exception.line, 5)
        self.assertIn(str(path), str(ctx.exception))
        self.assertIn("5", str(ctx.exception))

    def test_malformed_line_via_cli_exits_2(self):
        content = (
            "## Fuerte\n\n"
            "### Familia rota\n\n"
            "esto no tiene el formato correcto\n"
        )
        path = write_vocab(self.tmp.name, content)
        result = run_cli(["--vocabulario", str(path), "-"], input_text="hola\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn(str(path), result.stderr)
        self.assertIn("5", result.stderr)

    def test_real_vocabulario_invariants(self):
        # Sustituye a los recuentos codificados (104/27/77/7): estas
        # invariantes estructurales permiten añadir entradas al vocabulario
        # real sin tener que tocar los tests (hallazgo de revisión R2).
        import datetime

        entries = self.module.parse_vocabulary(VOCAB_PATH)
        fuerte = [e for e in entries if e.nivel == "Fuerte"]
        debil = [e for e in entries if e.nivel == "Débil"]
        self.assertTrue(fuerte, "el vocabulario debe tener al menos una entrada Fuerte")
        self.assertTrue(debil, "el vocabulario debe tener al menos una entrada Débil")
        for entry in entries:
            if entry.pendiente:
                self.assertEqual(entry.nivel, "Débil")
            self.assertTrue(entry.origen)
            datetime.date.fromisoformat(entry.fecha)
        normalizados = [
            self.module._normalize_for_matching(e.expresion) for e in entries
        ]
        self.assertEqual(
            len(normalizados),
            len(set(normalizados)),
            "no debe haber expresiones duplicadas tras normalizar",
        )

    def test_non_utf8_vocabulary_raises_without_misleading_line(self):
        path = Path(self.tmp.name) / "vocab-binario.md"
        path.write_bytes(
            "## Fuerte\n\n### Familia\n\nalgo ".encode("utf-8") + b"\xff\xfe\n"
        )
        with self.assertRaises(self.module.VocabParseError) as ctx:
            self.module.parse_vocabulary(path)
        mensaje = str(ctx.exception)
        self.assertIn(str(path), mensaje)
        self.assertNotIn(":0:", mensaje)
        self.assertIsNone(ctx.exception.line)

    def test_non_utf8_vocabulary_via_cli_exits_2_without_traceback(self):
        path = Path(self.tmp.name) / "vocab-binario.md"
        path.write_bytes(b"## Fuerte\n\n### Familia\n\nalgo \xff\xfe\n")
        result = run_cli(["--vocabulario", str(path), "-"], input_text="hola\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn(str(path), result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_vocab_without_level_headings_is_malformed(self):
        content = "# Título\n\nEsto es solo prosa sin encabezados de nivel.\n"
        path = write_vocab(self.tmp.name, content)
        with self.assertRaises(self.module.VocabParseError):
            self.module.parse_vocabulary(path)

    def test_vocab_with_heading_but_no_entries_is_malformed(self):
        content = "## Fuerte\n\n### Familia sin entradas\n\n## Otra cosa\n\nprosa\n"
        path = write_vocab(self.tmp.name, content)
        with self.assertRaises(self.module.VocabParseError):
            self.module.parse_vocabulary(path)

    def test_empty_vocabulary_via_cli_exits_2(self):
        content = "# Título\n\nprosa suelta.\n"
        path = write_vocab(self.tmp.name, content)
        result = run_cli(["--vocabulario", str(path), "-"], input_text="hola\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn(str(path), result.stderr)

    def test_invalid_calendar_date_raises(self):
        content = "## Fuerte\n\n### Familia\n\nalgo raro | 2026-13-40 | prueba\n"
        path = write_vocab(self.tmp.name, content)
        with self.assertRaises(self.module.VocabParseError) as ctx:
            self.module.parse_vocabulary(path)
        self.assertEqual(ctx.exception.line, 5)


class TestMatching(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vocab_path = write_vocab(self.tmp.name, MINIMAL_VOCAB)
        self.entries = self.module.parse_vocabulary(self.vocab_path)

    def test_case_and_accent_insensitive(self):
        text = "CLAVE y Clave y cláve no son lo mismo que una clave real.\n"
        report = self.module.build_report(text, self.entries)
        hits = [h for h in report["vocabulario"]["hallazgos"] if h["expresion"] == "clave"]
        # "CLAVE", "Clave", "cláve" (voz inventada) y "clave" -> 4 apariciones
        self.assertEqual(len(hits), 4)

    def test_word_boundaries_reject_claves_and_enclave(self):
        text = "Estas son las claves del enclave, pero no la clave sola.\n"
        report = self.module.build_report(text, self.entries)
        hits = [h for h in report["vocabulario"]["hallazgos"] if h["expresion"] == "clave"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["linea"], 1)

    def test_wildcard_matches_inflections(self):
        text = "Vamos a optimizar y luego seguimos con la optimización final.\n"
        report = self.module.build_report(text, self.entries)
        hits = [h for h in report["vocabulario"]["hallazgos"] if h["expresion"] == "optimiz*"]
        self.assertEqual(len(hits), 2)

    def test_multiword_across_line_break_within_paragraph(self):
        text = "Todo salió bien, en\nresumen, un buen día.\n"
        report = self.module.build_report(text, self.entries)
        hits = [h for h in report["vocabulario"]["hallazgos"] if h["expresion"] == "en resumen,"]
        self.assertEqual(len(hits), 1)

    def test_entry_with_spanish_punctuation(self):
        text = "Y entonces alguien dijo: ¡claro que si! y todos se rieron.\n"
        report = self.module.build_report(text, self.entries)
        hits = [
            h for h in report["vocabulario"]["hallazgos"]
            if h["expresion"] == "¡claro que si!"
        ]
        self.assertEqual(len(hits), 1)

    def test_nfd_input_reports_correct_line_and_column(self):
        import unicodedata

        line2 = "Aquí tenemos la clave del asunto.\n"
        nfd_line2 = unicodedata.normalize("NFD", line2)
        text = "Primera línea sin nada relevante.\n" + nfd_line2
        report = self.module.build_report(text, self.entries)
        hits = [h for h in report["vocabulario"]["hallazgos"] if h["expresion"] == "clave"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["linea"], 2)
        # La columna se mide sobre el texto original (ya en NFD): la "í"
        # decompuesta de "Aquí" ocupa 2 posiciones antes de "clave".
        self.assertEqual(hits[0]["columna"], nfd_line2.index("clave") + 1)


class TestMasking(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vocab_path = write_vocab(self.tmp.name, MINIMAL_VOCAB)
        self.entries = self.module.parse_vocabulary(self.vocab_path)

    def _hits_for(self, text):
        report = self.module.build_report(text, self.entries)
        return report["vocabulario"]["hallazgos"], report["enmascarado"]

    def test_hit_inside_fenced_code_block_is_masked(self):
        text = (
            "Texto normal.\n\n"
            "```python\n"
            "clave = 1  # esto es solo código\n"
            "```\n\n"
            "Después del bloque, otra clave real.\n"
        )
        hits, mask_counts = self._hits_for(text)
        matches = [h for h in hits if h["expresion"] == "clave"]
        self.assertEqual(len(matches), 1)
        self.assertGreaterEqual(mask_counts["bloques_codigo"], 1)
        # la línea reportada debe ser la de después del bloque, no la del código
        last_line = text.count("\n", 0, text.index("Después"))
        self.assertEqual(matches[0]["linea"], last_line + 1)

    def test_hit_inside_inline_code_is_masked(self):
        text = "Aquí usamos `clave = 1` como variable, sin relación con el texto.\n"
        hits, mask_counts = self._hits_for(text)
        matches = [h for h in hits if h["expresion"] == "clave"]
        self.assertEqual(len(matches), 0)
        self.assertEqual(mask_counts["codigo_en_linea"], 1)

    def test_hit_inside_url_is_masked(self):
        text = "Visita https://clave-corp.example.com para más información.\n"
        hits, mask_counts = self._hits_for(text)
        matches = [h for h in hits if h["expresion"] == "clave"]
        self.assertEqual(len(matches), 0)
        self.assertEqual(mask_counts["url"], 1)

    def test_hit_inside_frontmatter_is_masked(self):
        text = (
            "---\n"
            "titulo: clave del proyecto\n"
            "---\n"
            "Cuerpo del texto sin ningún dato especial.\n"
        )
        hits, mask_counts = self._hits_for(text)
        matches = [h for h in hits if h["expresion"] == "clave"]
        self.assertEqual(len(matches), 0)
        self.assertEqual(mask_counts["frontmatter"], 1)

    def test_hit_inside_claim_span_is_masked(self):
        text = "El producto [[claim]]tiene una clave secreta probada[[/claim]] siempre.\n"
        hits, mask_counts = self._hits_for(text)
        matches = [h for h in hits if h["expresion"] == "clave"]
        self.assertEqual(len(matches), 0)
        self.assertEqual(mask_counts["claim"], 1)

    def test_hit_inside_quotes_is_masked(self):
        text = "Ella dijo «esto no tiene clave alguna» y se fue tranquila.\n"
        hits, mask_counts = self._hits_for(text)
        matches = [h for h in hits if h["expresion"] == "clave"]
        self.assertEqual(len(matches), 0)
        self.assertEqual(mask_counts["comillas"], 1)

    def test_unpaired_quote_is_left_alone(self):
        text = 'Un símbolo " suelto no debería enmascarar la clave siguiente.\n'
        hits, mask_counts = self._hits_for(text)
        matches = [h for h in hits if h["expresion"] == "clave"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(mask_counts["comillas"], 0)


class TestCRLF(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vocab_path = write_vocab(self.tmp.name, MINIMAL_VOCAB)
        self.entries = self.module.parse_vocabulary(self.vocab_path)

    def test_frontmatter_masked_with_crlf(self):
        text = "---\r\ntitulo: clave del proyecto\r\n---\r\nCuerpo con una clave real.\r\n"
        report = self.module.build_report(text, self.entries)
        hits = [h for h in report["vocabulario"]["hallazgos"] if h["expresion"] == "clave"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(report["enmascarado"]["frontmatter"], 1)
        self.assertEqual(hits[0]["linea"], 4)

    def test_fenced_code_masked_with_crlf(self):
        text = (
            "Texto normal.\r\n\r\n"
            "```python\r\n"
            "clave = 1\r\n"
            "```\r\n\r\n"
            "Después la clave real.\r\n"
        )
        report = self.module.build_report(text, self.entries)
        hits = [h for h in report["vocabulario"]["hallazgos"] if h["expresion"] == "clave"]
        self.assertEqual(len(hits), 1)
        self.assertGreaterEqual(report["enmascarado"]["bloques_codigo"], 1)
        last_line = text.count("\n", 0, text.index("Después"))
        self.assertEqual(hits[0]["linea"], last_line + 1)

    def test_frontmatter_with_lone_trailing_cr(self):
        text = "---\r\ntitulo: clave\r\n---\r"
        report = self.module.build_report(text, self.entries)
        self.assertEqual(report["enmascarado"]["frontmatter"], 1)


class TestOverlappingMatches(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.real_entries = self.module.parse_vocabulary(VOCAB_PATH)

    def test_collocation_counts_once_not_its_inner_word(self):
        text = "Este proyecto es un pilar fundamental para la empresa.\n"
        report = self.module.build_report(text, self.real_entries)
        hallazgos = report["vocabulario"]["hallazgos"]
        colocacion = [h for h in hallazgos if h["expresion"] == "pilar fundamental"]
        suelto = [h for h in hallazgos if h["expresion"] == "fundamental"]
        self.assertEqual(len(colocacion), 1)
        self.assertEqual(len(suelto), 0)
        densidad = report["vocabulario"]["densidad"]["por_nivel"]["Débil"]
        self.assertEqual(densidad["ocurrencias"], 1)

    def test_collocation_jugar_un_papel_clave_counts_once(self):
        text = "Resulta que jugar un papel clave será determinante hoy.\n"
        report = self.module.build_report(text, self.real_entries)
        hallazgos = report["vocabulario"]["hallazgos"]
        colocacion = [h for h in hallazgos if h["expresion"] == "jugar un papel clave"]
        suelto = [h for h in hallazgos if h["expresion"] == "clave"]
        self.assertEqual(len(colocacion), 1)
        self.assertEqual(len(suelto), 0)

    def test_fuerte_wins_over_debil_on_equal_span(self):
        content = (
            "## Fuerte\n\n### Familia fuerte\n\n"
            "clave | 2026-09-27 | PXX · prueba\n\n"
            "## Débil\n\n### Familia débil\n\n"
            "clave | 2026-09-27 | PXX · prueba\n"
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_vocab(tmp_dir, content)
            entries = self.module.parse_vocabulary(path)
        text = "Esto es la clave del proyecto.\n"
        report = self.module.build_report(text, entries)
        hallazgos = report["vocabulario"]["hallazgos"]
        self.assertEqual(len(hallazgos), 1)
        self.assertEqual(hallazgos[0]["nivel"], "Fuerte")
        self.assertEqual(hallazgos[0]["familia"], "Familia fuerte")

    def test_alphabetical_tiebreak_on_equal_span_and_level(self):
        content = (
            "## Débil\n\n### Familia\n\n"
            "Clave | 2026-09-27 | PXX · prueba\n"
            "clave | 2026-09-27 | PXX · prueba\n"
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_vocab(tmp_dir, content)
            entries = self.module.parse_vocabulary(path)
        text = "Esto es la clave del proyecto.\n"
        report = self.module.build_report(text, entries)
        hallazgos = report["vocabulario"]["hallazgos"]
        self.assertEqual(len(hallazgos), 1)
        self.assertEqual(hallazgos[0]["expresion"], "Clave")


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_file_and_stdin_produce_identical_json(self):
        text = "Este es un texto de prueba con una clave dentro.\n"
        file_path = Path(self.tmp.name) / "entrada.txt"
        file_path.write_text(text, encoding="utf-8")
        result_file = run_cli([str(file_path)])
        result_stdin = run_cli(["-"], input_text=text)
        self.assertEqual(result_file.returncode, 0)
        self.assertEqual(result_stdin.returncode, 0)
        self.assertEqual(result_file.stdout, result_stdin.stdout)

    def test_two_runs_are_byte_identical(self):
        text = "Repetimos el mismo análisis dos veces seguidas.\n"
        result_a = run_cli(["-"], input_text=text)
        result_b = run_cli(["-"], input_text=text)
        self.assertEqual(result_a.stdout, result_b.stdout)

    def test_unreadable_file_exits_2(self):
        missing = Path(self.tmp.name) / "no_existe.txt"
        result = run_cli([str(missing)])
        self.assertEqual(result.returncode, 2)
        self.assertIn(str(missing), result.stderr)

    def test_usage_error_exits_2(self):
        result = run_cli(["--flag-que-no-existe"])
        self.assertEqual(result.returncode, 2)

    def test_output_is_valid_json_with_expected_top_level_keys(self):
        result = run_cli(["-"], input_text="Un texto cualquiera sin nada especial.\n")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(
            set(data.keys()),
            {
                "version",
                "entrada",
                "enmascarado",
                "vocabulario",
                "rayas",
                "comillas",
                "encabezados",
                "tipografia",
                "estructuras",
                "deterministas",
                "registro",
                "candidatos_claim",
                "privacidad",
            },
        )
        self.assertEqual(set(data["entrada"].keys()), {"lineas", "palabras", "parrafos"})
        self.assertIn("hallazgos", data["vocabulario"])
        self.assertIn("densidad", data["vocabulario"])

    def test_output_includes_comparacion_key_only_with_original(self):
        result_sin = run_cli(["-"], input_text="Un texto cualquiera sin nada especial.\n")
        data_sin = json.loads(result_sin.stdout)
        self.assertNotIn("comparacion", data_sin)

        with tempfile.TemporaryDirectory() as tmp_dir:
            original_path = Path(tmp_dir) / "original.txt"
            original_path.write_text("Un texto cualquiera sin nada especial.\n", encoding="utf-8")
            result_con = run_cli(
                ["--original", str(original_path), "-"],
                input_text="Un texto cualquiera sin nada especial.\n",
            )
        self.assertEqual(result_con.returncode, 0)
        data_con = json.loads(result_con.stdout)
        self.assertIn("comparacion", data_con)


class TestDensity(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vocab_path = write_vocab(self.tmp.name, MINIMAL_VOCAB)
        self.entries = self.module.parse_vocabulary(self.vocab_path)

    def test_density_counts_on_controlled_text(self):
        # Párrafo 1: 4 palabras, un hallazgo débil ("clave").
        # Párrafo 2: 4 palabras, un hallazgo débil ("clave").
        text = "Aquí va la clave.\n\nOtra vez la clave.\n"
        report = self.module.build_report(text, self.entries)
        entrada = report["entrada"]
        self.assertEqual(entrada["palabras"], 8)
        self.assertEqual(entrada["parrafos"], 2)

        densidad = report["vocabulario"]["densidad"]
        self.assertEqual(densidad["por_nivel"]["Débil"]["ocurrencias"], 2)
        self.assertAlmostEqual(
            densidad["por_nivel"]["Débil"]["por_mil_palabras"], 2 / 8 * 1000
        )
        self.assertEqual(densidad["por_nivel"]["Fuerte"]["ocurrencias"], 0)

        por_parrafo = densidad["por_parrafo"]
        self.assertEqual(len(por_parrafo), 2)
        self.assertEqual(por_parrafo[0]["linea_inicio"], 1)
        self.assertEqual(por_parrafo[0]["palabras"], 4)
        self.assertEqual(por_parrafo[0]["por_nivel"]["Débil"], 1)
        self.assertEqual(por_parrafo[1]["linea_inicio"], 3)
        self.assertEqual(por_parrafo[1]["palabras"], 4)
        self.assertEqual(por_parrafo[1]["por_nivel"]["Débil"], 1)


class TestControlProse(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.entries = self.module.parse_vocabulary(VOCAB_PATH)

    def test_clean_spain_spanish_prose_yields_no_strong_hits(self):
        text = (
            "Marta llegó a la oficina de Ferretería Robledo a las nueve de la "
            "mañana. Revisó el correo, contestó dos llamadas de proveedores y "
            "preparó el pedido para la tienda de Alcalá. Por la tarde salió a "
            "repartir tres cajas con la furgoneta y volvió antes de las seis. "
            "Su jefe le preguntó si el nuevo catálogo había llegado y ella dijo "
            "que sí, que estaba en el almacén desde el martes.\n"
        )
        report = self.module.build_report(text, self.entries)
        fuertes = [
            h for h in report["vocabulario"]["hallazgos"] if h["nivel"] == "Fuerte"
        ]
        self.assertEqual(fuertes, [])


class TestStaticImports(unittest.TestCase):
    FORBIDDEN = {
        "socket",
        "urllib",
        "http",
        "ftplib",
        "smtplib",
        "requests",
        "ssl",
        "asyncio",
        "subprocess",
    }

    def test_no_network_or_subprocess_imports(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(SCRIPT_PATH))
        found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    found.add(node.module.split(".")[0])
        offending = found & self.FORBIDDEN
        self.assertEqual(offending, set())


class TestSourceHygiene(unittest.TestCase):
    """Revisión de la slice 04 (A5): los puntos de código invisibles que el
    script vigila deben escribirse siempre como escapes ``\\uXXXX`` en el
    propio código fuente, nunca como el carácter invisible en crudo (que es
    ilegible en un editor y fácil de borrar por accidente)."""

    INVISIBLES_VIGILADOS = (
        "​",  # ZERO WIDTH SPACE
        "‌",  # ZERO WIDTH NON-JOINER
        "‍",  # ZERO WIDTH JOINER
        "⁠",  # WORD JOINER
        "­",  # SOFT HYPHEN
        "﻿",  # ZERO WIDTH NO-BREAK SPACE / BOM
    )

    def test_source_file_has_no_raw_invisible_characters(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        encontrados = [ch for ch in self.INVISIBLES_VIGILADOS if ch in source]
        self.assertEqual(
            encontrados,
            [],
            "el código fuente debe escribir estos puntos de código como "
            "escapes \\uXXXX, nunca como el carácter en crudo",
        )

    def test_source_file_has_no_raw_nbsp_or_narrow_nbsp(self):
        """Revisión review-4e912a0ac78c9cff (R2-002): el espacio de no
        separación (NBSP, U+00A0) y el espacio fino de no separación
        (U+202F) usados en las clases de caracteres de las expresiones
        regulares de cifras, porcentajes y duraciones/unidades deben
        escribirse siempre como escapes ``\\u00a0``/``\\u202f``, nunca como
        el carácter en crudo: un carácter en crudo es indistinguible de un
        espacio normal en un editor o en un diff, y un editor puede
        normalizarlo sin avisar."""
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertNotIn(chr(0x00A0), source, "NBSP en crudo: debe ser el escape \\u00a0")
        self.assertNotIn(
            chr(0x202F), source, "espacio fino de no separación en crudo: debe ser \\u202f"
        )


# ---------------------------------------------------------------------------
# T3, parte B: detectores de forma (rayas, comillas, encabezados, tipografía)
# ---------------------------------------------------------------------------


class TestRayas(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.entries = []  # estos tests no necesitan vocabulario

    def _rayas(self, text):
        report = self.module.build_report(text, self.entries)
        return report["rayas"]

    def test_dialogue_dash_at_line_start(self):
        text = "—Buenos días, ¿ya llegó el pedido?\n"
        rayas = self._rayas(text)
        tipos = [h["tipo"] for h in rayas["hallazgos"]]
        self.assertEqual(tipos, ["dialogo"])
        self.assertEqual(rayas["conteo"]["dialogo"]["ocurrencias"], 1)

    def test_closed_inciso_pair_within_paragraph(self):
        text = "El pedido —según nos dijo Marta— llegó tarde hoy.\n"
        rayas = self._rayas(text)
        tipos = [h["tipo"] for h in rayas["hallazgos"]]
        self.assertEqual(tipos, ["inciso_cerrado", "inciso_cerrado"])
        self.assertEqual(rayas["conteo"]["raya_inglesa"]["ocurrencias"], 0)

    def test_closed_inciso_followed_by_comma_is_still_valid(self):
        text = "—Sí —contestó Luis—, está en el almacén desde ayer.\n"
        rayas = self._rayas(text)
        tipos = [h["tipo"] for h in rayas["hallazgos"]]
        self.assertEqual(tipos, ["dialogo", "inciso_cerrado", "inciso_cerrado"])

    def test_english_style_glued_dash(self):
        text = "El gato—cansado—corrió por el jardín.\n"
        rayas = self._rayas(text)
        subtipos = [h.get("subtipo") for h in rayas["hallazgos"]]
        self.assertEqual(rayas["conteo"]["raya_inglesa"]["ocurrencias"], 2)
        self.assertTrue(all(s == "pegada" for s in subtipos))

    def test_english_style_spaced_dash_without_closing(self):
        text = "Fue un buen día — al menos eso pensaba Marta.\n"
        rayas = self._rayas(text)
        self.assertEqual(len(rayas["hallazgos"]), 1)
        self.assertEqual(rayas["hallazgos"][0]["tipo"], "raya_inglesa")
        self.assertEqual(rayas["hallazgos"][0]["subtipo"], "sin_cierre")

    def test_dash_in_heading_is_classified_separately(self):
        text = "# Un título — con raya\n\nTexto normal sin rayas.\n"
        rayas = self._rayas(text)
        self.assertEqual(len(rayas["hallazgos"]), 1)
        self.assertEqual(rayas["hallazgos"][0]["tipo"], "en_encabezado")

    def test_numeric_ranges_are_never_reported_as_rayas(self):
        text = "El horario es de 10-20 y también de 10–20 horas.\n"
        rayas = self._rayas(text)
        self.assertEqual(rayas["hallazgos"], [])

    def test_dialogue_closing_dash_omitted_before_narrator_period_is_valid(self):
        # Revisión review-faf981a2b76764c9: "—Ya voy —dijo Marta." es correcto
        # en español (el comentario del narrador cierra la frase, así que la
        # raya de cierre se omite); nunca debe salir como raya_inglesa/sin_cierre.
        text = "—Ya voy —dijo Marta.\n"
        rayas = self._rayas(text)
        tipos = [h["tipo"] for h in rayas["hallazgos"]]
        self.assertEqual(tipos, ["dialogo", "inciso_sin_cierre"])
        self.assertEqual(rayas["conteo"]["raya_inglesa"]["ocurrencias"], 0)

    def test_dialogue_inciso_that_continues_the_speech_pairs_correctly(self):
        text = "—No sé —dijo—. Mañana lo miro.\n"
        rayas = self._rayas(text)
        tipos = [h["tipo"] for h in rayas["hallazgos"]]
        self.assertEqual(tipos, ["dialogo", "inciso_cerrado", "inciso_cerrado"])
        self.assertEqual(rayas["conteo"]["raya_inglesa"]["ocurrencias"], 0)

    def test_unclosed_english_dash_does_not_split_a_correct_inciso_pair(self):
        # La raya espaciada sin cierre no debe "robar" la raya de apertura del
        # inciso correcto que viene después en el mismo párrafo (emparejado
        # voraz de la revisión review-faf981a2b76764c9).
        text = (
            "Fue un buen día — al menos eso pensaba Marta. "
            "El pedido —según nos dijo Marta— llegó tarde hoy.\n"
        )
        rayas = self._rayas(text)
        tipos = [h["tipo"] for h in rayas["hallazgos"]]
        self.assertEqual(tipos, ["raya_inglesa", "inciso_cerrado", "inciso_cerrado"])
        self.assertEqual(rayas["hallazgos"][0]["subtipo"], "sin_cierre")
        self.assertEqual(rayas["conteo"]["raya_inglesa"]["ocurrencias"], 1)
        self.assertEqual(rayas["conteo"]["inciso_cerrado"]["ocurrencias"], 2)


class TestComillas(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.entries = []

    def _comillas(self, text):
        report = self.module.build_report(text, self.entries)
        return report["comillas"]

    def test_mixing_of_types_at_level_one(self):
        text = 'Ella dijo «hola» y luego dijo "adiós" al salir.\n'
        comillas = self._comillas(text)
        self.assertEqual(len(comillas["mezcla_de_tipos"]), 1)
        self.assertEqual(comillas["mezcla_de_tipos"][0]["nivel"], 1)
        self.assertEqual(comillas["anidamiento_invertido"], [])

    def test_inverted_nesting(self):
        text = "Dijo: “Recuerda «esto es importante» siempre.”\n"
        comillas = self._comillas(text)
        self.assertEqual(len(comillas["anidamiento_invertido"]), 1)
        hallazgo = comillas["anidamiento_invertido"][0]
        self.assertEqual(hallazgo["tipo_interior"], "«»")
        self.assertEqual(hallazgo["tipo_exterior"], "“”")

    def test_angular_alone_is_never_a_finding(self):
        text = "Ella dijo «hola» y se fue.\n\nDespués volvió y dijo «adiós».\n"
        comillas = self._comillas(text)
        self.assertEqual(comillas["mezcla_de_tipos"], [])
        self.assertEqual(comillas["anidamiento_invertido"], [])

    def test_straight_quotes_alone_are_never_a_finding(self):
        text = 'Ella dijo "hola" y se fue.\n\nDespués volvió y dijo "adiós".\n'
        comillas = self._comillas(text)
        self.assertEqual(comillas["mezcla_de_tipos"], [])
        self.assertEqual(comillas["anidamiento_invertido"], [])

    def test_correct_nesting_of_angular_and_curly_is_not_inverted(self):
        text = "Dijo: «Recuerda “esto es importante” siempre.»\n"
        comillas = self._comillas(text)
        self.assertEqual(comillas["anidamiento_invertido"], [])


class TestEncabezados(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.entries = []

    def _encabezados(self, text):
        report = self.module.build_report(text, self.entries)
        return report["encabezados"]

    def test_title_case_ratio_detects_capitalized_words(self):
        text = "## Un Ejemplo Con Muchas Palabras\n\nTexto normal.\n"
        encabezados = self._encabezados(text)
        title_case = encabezados["hallazgos"][0]["title_case"]
        self.assertGreater(title_case["ratio"], 0.5)

    def test_sentence_case_heading_has_zero_ratio(self):
        text = "## Un ejemplo con muchas palabras\n\nTexto normal.\n"
        encabezados = self._encabezados(text)
        title_case = encabezados["hallazgos"][0]["title_case"]
        self.assertEqual(title_case["ratio"], 0.0)

    def test_heading_phrased_as_question(self):
        text = "## ¿Cómo funciona esto?\n\nTexto normal.\n"
        encabezados = self._encabezados(text)
        self.assertTrue(encabezados["hallazgos"][0]["es_pregunta"])
        self.assertEqual(encabezados["resumen"]["preguntas"], 1)

    def test_level_jump_detected(self):
        text = "# Título\n\n### Subtítulo saltado\n\nTexto.\n"
        encabezados = self._encabezados(text)
        self.assertFalse(encabezados["hallazgos"][0]["salto_de_nivel"])
        self.assertTrue(encabezados["hallazgos"][1]["salto_de_nivel"])
        self.assertEqual(encabezados["resumen"]["saltos_de_nivel"], 1)

    def test_empty_heading_detected(self):
        text = "##\n\nTexto.\n"
        encabezados = self._encabezados(text)
        self.assertTrue(encabezados["hallazgos"][0]["vacio"])
        self.assertEqual(encabezados["resumen"]["vacios"], 1)

    def test_missing_separator_between_sections(self):
        text = "# Primera\n\nTexto de la primera sección.\n\n# Segunda\n\nMás texto.\n"
        encabezados = self._encabezados(text)
        self.assertEqual(encabezados["resumen"]["secciones_sin_separador"], 1)

    def test_separator_present_between_sections(self):
        text = "# Primera\n\nTexto de la primera sección.\n\n---\n\n# Segunda\n\nMás texto.\n"
        encabezados = self._encabezados(text)
        self.assertEqual(encabezados["resumen"]["secciones_sin_separador"], 0)


class TestTipografia(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.entries = []

    def _tipografia(self, text):
        report = self.module.build_report(text, self.entries)
        return report["tipografia"]

    def test_closing_question_mark_without_opening(self):
        text = "No sabemos si vendrá a la fiesta mañana?\n"
        tipografia = self._tipografia(text)
        signos = tipografia["signos_sin_apertura"]
        self.assertEqual(len(signos), 1)
        self.assertEqual(signos[0]["signo"], "?")

    def test_closing_exclamation_without_opening(self):
        text = "Menudo día llevamos hoy!\n"
        tipografia = self._tipografia(text)
        signos = tipografia["signos_sin_apertura"]
        self.assertEqual(len(signos), 1)
        self.assertEqual(signos[0]["signo"], "!")

    def test_capital_after_colon_in_running_text(self):
        text = "El problema era claro: Necesitábamos más tiempo para todo.\n"
        tipografia = self._tipografia(text)
        self.assertEqual(len(tipografia["mayuscula_tras_dos_puntos"]), 1)

    def test_capital_after_colon_introducing_quote_is_safe(self):
        text = "Ella explicó: «Necesitábamos más tiempo».\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["mayuscula_tras_dos_puntos"], [])

    def test_capital_after_colon_introducing_list_is_safe(self):
        text = "Los pasos son los siguientes:\n- Primero\n- Segundo\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["mayuscula_tras_dos_puntos"], [])

    def test_exclamations_per_thousand_words(self):
        text = "Hola. " * 998 + "Qué bien! Qué suerte!\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["exclamaciones"]["ocurrencias"], 2)
        self.assertGreater(tipografia["exclamaciones"]["por_mil_palabras"], 0)

    def test_markdown_image_exclamation_is_not_counted(self):
        text = "![Foto de la tienda](imagenes/tienda.jpg)\n\nTexto normal sin exclamaciones.\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["exclamaciones"]["ocurrencias"], 0)
        self.assertEqual(tipografia["signos_sin_apertura"], [])

    def test_markdown_image_does_not_hide_a_real_exclamation_next_to_it(self):
        text = "![Foto de la tienda](imagenes/tienda.jpg)\n\nMenudo día llevamos hoy!\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["exclamaciones"]["ocurrencias"], 1)
        self.assertEqual(len(tipografia["signos_sin_apertura"]), 1)

    def test_markdown_reference_style_image_exclamation_is_not_counted(self):
        text = "Mira este ![logo][logo-ref] con atención.\n\n[logo-ref]: imagenes/logo.png\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["exclamaciones"]["ocurrencias"], 0)

    def test_bare_bracket_after_exclamation_is_not_masked_as_markdown_image(self):
        # Revisión de la slice 04 (A3): "![alt]" sin destino (ni "(...)" ni
        # "[ref]") no es una imagen Markdown real; un "!" seguido de una
        # nota a pie de página entre corchetes (p. ej. "¡Por fin![1]") debe
        # seguir contando como cierre de exclamación normal.
        text = "¡Por fin![1] llegó el pedido de Ferretería Robledo.\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["exclamaciones"]["ocurrencias"], 1)
        self.assertEqual(tipografia["signos_sin_apertura"], [])

    def test_capital_after_colon_is_skipped_inside_heading(self):
        text = "## El plan: Una Guía Rápida\n\nTexto normal sin dos puntos raros.\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["mayuscula_tras_dos_puntos"], [])

    def test_capital_after_colon_stops_at_masked_region_instead_of_skipping_it(self):
        # El código enmascarado no cuenta como "espacio real": la mayúscula
        # de después de "Necesitamos" no está pegada a los dos puntos, así
        # que no debe reportarse (revisión review-faf981a2b76764c9, R2-002).
        text = "Usa esto: `Config` Necesitamos revisar el resto.\n"
        tipografia = self._tipografia(text)
        self.assertEqual(tipografia["mayuscula_tras_dos_puntos"], [])


CONTROL_PROSA_FORMA = (
    "# Un día cualquiera en la tienda\n"
    "\n"
    "Marta llegó temprano y dijo:\n"
    "\n"
    "—Buenos días, ¿ya llegó el pedido de Ferretería Robledo?\n"
    "\n"
    "—Sí —contestó Luis—, está en el almacén desde ayer.\n"
    "\n"
    "Antes de irse añadió: «Recuerda que el cliente pidió "
    "“el modelo pequeño” para la reforma», y salió con la furgoneta.\n"
    "\n"
    "## Qué se hizo por la tarde\n"
    "\n"
    "Por la tarde repartieron tres cajas y volvieron antes de las seis. "
    "¡Menudo día! Nadie preguntó nada más.\n"
)


class TestFormSafeguards(unittest.TestCase):
    """Prosa de control en español de España, propia y con marcas/nombres
    ficticios: usa raya de diálogo, inciso cerrado con rayas, «» con “”
    anidadas en el orden correcto, encabezados en minúscula sentence-case y
    ¿…?/¡…! bien emparejados. Ninguno de los cuatro detectores de forma debe
    dar un hallazgo bloqueante sobre este texto.
    """

    def setUp(self):
        self.module = load_module()
        self.report = self.module.build_report(CONTROL_PROSA_FORMA, [])

    def test_no_english_style_dash_findings(self):
        rayas = self.report["rayas"]
        self.assertEqual(rayas["conteo"]["raya_inglesa"]["ocurrencias"], 0)

    def test_no_quote_mixing_or_inversion_findings(self):
        comillas = self.report["comillas"]
        self.assertEqual(comillas["mezcla_de_tipos"], [])
        self.assertEqual(comillas["anidamiento_invertido"], [])

    def test_sentence_case_headings_yield_zero_ratio_and_no_jumps(self):
        encabezados = self.report["encabezados"]
        for h in encabezados["hallazgos"]:
            self.assertEqual(h["title_case"]["ratio"], 0.0)
            self.assertFalse(h["salto_de_nivel"])
            self.assertFalse(h["vacio"])

    def test_no_missing_opening_marks(self):
        tipografia = self.report["tipografia"]
        self.assertEqual(tipografia["signos_sin_apertura"], [])


def _entradas_pilar_fundamental(module):
    """Vocabulario mínimo y propio del test, aislado de
    ``references/vocabulario-es.md`` (revisión review-4e912a0ac78c9cff,
    R3-test-rendimiento-acoplado-vocabulario): el test de rendimiento
    necesita EXACTAMENTE dos entradas que se solapen ("pilar fundamental" y
    "fundamental") para predecir un número de comparaciones exacto: si
    dependiera del archivo de vocabulario real, añadir o editar cualquier
    entrada que coincidiese con la frase de la muestra cambiaría ese número
    sin que hubiera ninguna regresión real. Construye los objetos
    ``VocabEntry`` directamente (sin pasar por un archivo), como permite
    ``_build_pattern``.
    """
    return [
        module.VocabEntry(
            expresion="pilar fundamental",
            nivel="Débil",
            familia="Familia de prueba",
            origen="PXX · prueba",
            pendiente=False,
            fecha="2026-09-27",
            line=1,
            pattern=module._build_pattern("pilar fundamental"),
        ),
        module.VocabEntry(
            expresion="fundamental",
            nivel="Débil",
            familia="Familia de prueba",
            origen="PXX · prueba",
            pendiente=False,
            fecha="2026-09-27",
            line=2,
            pattern=module._build_pattern("fundamental"),
        ),
    ]


class TestPerformance(unittest.TestCase):
    """Revisión review-faf981a2b76764c9 (R4-001, R4-002): el anidamiento de
    comillas y la resolución de solapamientos deben comparar solo dentro de
    un mismo párrafo, no todo contra todo.

    Revisión de la slice 04 (A1): el test anterior medía un límite de
    tiempo de reloj sobre todo ``build_report``, lo que es un test no
    determinista (depende de la máquina y de la carga del sistema). Se
    sustituye por una comprobación determinista de la propia corrección
    algorítmica: se cuenta, con un contador inyectado sobre las funciones
    de comparación de tramos (``_span_strictly_contains`` y
    ``_ranges_overlap``), cuántas comparaciones se ejecutan realmente, y
    se compara con el número exacto que predice una resolución acotada
    por párrafo. Si la resolución comparase párrafos entre sí (el defecto
    original), el número de comparaciones crecería de forma cuadrática en
    vez de ser exactamente proporcional al número de párrafos.
    """

    def setUp(self):
        self.module = load_module()

    def test_quote_nesting_and_overlap_resolution_scale_per_paragraph_not_globally(self):
        entries = _entradas_pilar_fundamental(self.module)
        n_parrafos = 300
        parrafos = [
            "Marta dijo «uno» y «dos» sobre un pilar fundamental hoy."
            for _ in range(n_parrafos)
        ]
        text = "\n\n".join(parrafos) + "\n"

        contains_calls = []
        overlap_calls = []
        original_contains = self.module._span_strictly_contains
        original_overlap = self.module._ranges_overlap

        def contando_contains(*args):
            contains_calls.append(args)
            return original_contains(*args)

        def contando_overlap(*args):
            overlap_calls.append(args)
            return original_overlap(*args)

        with mock.patch.object(
            self.module, "_span_strictly_contains", side_effect=contando_contains
        ), mock.patch.object(
            self.module, "_ranges_overlap", side_effect=contando_overlap
        ):
            report = self.module.build_report(text, entries)

        # Dos comillas por párrafo (no anidadas entre sí) -> exactamente
        # 2 comparaciones por párrafo (cada tramo se compara con el otro,
        # k*(k-1) con k=2). Un anidamiento que comparase párrafos entre sí
        # daría un total muy superior y creciente en O(n²).
        self.assertEqual(len(contains_calls), 2 * n_parrafos)
        # Dos hallazgos de vocabulario solapados por párrafo ("pilar
        # fundamental" y "fundamental"): el primero (más largo) no compara
        # contra nada; el segundo compara una vez contra el primero y se
        # descarta. Exactamente 1 comparación por párrafo.
        self.assertEqual(len(overlap_calls), n_parrafos)

        self.assertEqual(report["comillas"]["mezcla_de_tipos"], [])
        self.assertEqual(report["comillas"]["anidamiento_invertido"], [])
        self.assertEqual(
            report["vocabulario"]["densidad"]["por_nivel"]["Débil"]["ocurrencias"],
            n_parrafos,
        )

    def test_overlap_resolution_unchanged_on_known_fixture(self):
        entries = _entradas_pilar_fundamental(self.module)
        text = "Este proyecto es un pilar fundamental para la empresa.\n"
        report = self.module.build_report(text, entries)
        hallazgos = report["vocabulario"]["hallazgos"]
        colocacion = [h for h in hallazgos if h["expresion"] == "pilar fundamental"]
        suelto = [h for h in hallazgos if h["expresion"] == "fundamental"]
        self.assertEqual(len(colocacion), 1)
        self.assertEqual(len(suelto), 0)

    def test_original_comparison_overlap_check_is_linear_not_quadratic(self):
        """Revisión review-4e912a0ac78c9cff (R4-001): las categorías de
        hechos de ``--original`` (fechas, porcentajes, precios, duraciones,
        códigos, cifras) comparten un único ``consumidos`` para todo el
        documento. Comprobar el solapamiento de cada coincidencia contra
        TODOS los tramos ya consumidos (en vez de solo contra el más
        cercano) haría que el número de comparaciones creciera de forma
        cuadrática con el número de cifras del documento.

        Con ``n`` cifras sueltas, sin ninguna otra categoría que las
        preceda: la primera consulta encuentra la lista de tramos
        consumidos vacía (0 comparaciones); cada una de las siguientes
        compara exactamente una vez, contra su predecesora inmediata
        (nunca contra las demás, porque los tramos consumidos están
        ordenados y no se solapan entre sí). Total exacto: n - 1. Una
        resolución que comparase contra todos los tramos anteriores daría
        n * (n - 1) / 2 (cuadrático): con n=400 eso son 79 800
        comparaciones frente a las 399 que predice la resolución acotada.
        """
        n = 400
        parrafos = [
            "Este texto de prueba contiene el número {} en la frase.".format(1000 + i)
            for i in range(n)
        ]
        text = "\n\n".join(parrafos) + "\n"
        line_starts = self.module._build_line_index(text)

        overlap_calls = []
        original_overlap = self.module._ranges_overlap

        def contando(*args):
            overlap_calls.append(args)
            return original_overlap(*args)

        with mock.patch.object(self.module, "_ranges_overlap", side_effect=contando):
            hechos = self.module._extract_all_facts(text, line_starts)

        self.assertEqual(len(hechos["cifras"]), n)
        self.assertEqual(len(overlap_calls), n - 1)


class TestEstructuras(unittest.TestCase):
    """T4 parte B: regex de estructura sobre ``masked_text``. Solo datos: sin
    umbral, sin veredicto, sin reescritura."""

    def setUp(self):
        self.module = load_module()
        self.entries = []

    def _estructuras(self, text):
        report = self.module.build_report(text, self.entries)
        return report["estructuras"]

    def test_no_solo_sino_is_reported_as_data(self):
        text = "El proyecto no solo cumplió el plazo, sino que además redujo costes.\n"
        estructuras = self._estructuras(text)
        self.assertEqual(len(estructuras["no_solo_sino"]), 1)

    def test_no_solo_sino_inside_code_block_is_masked(self):
        text = "```python\n# no solo esto, sino aquello también\n```\n\nTexto normal.\n"
        estructuras = self._estructuras(text)
        self.assertEqual(estructuras["no_solo_sino"], [])

    def test_no_se_trata_de_sino(self):
        text = "No se trata de vender más, sino de fidelizar a quien ya compra.\n"
        estructuras = self._estructuras(text)
        self.assertEqual(len(estructuras["no_se_trata_de"]), 1)

    def test_no_es_es_contrast(self):
        text = "Esto no es un lujo, es una necesidad para cualquier taller.\n"
        estructuras = self._estructuras(text)
        self.assertEqual(len(estructuras["no_es_es"]), 1)

    def test_tanto_si_como_si(self):
        text = "Tanto si llueve como si hace sol, la furgoneta sale a repartir.\n"
        estructuras = self._estructuras(text)
        self.assertEqual(len(estructuras["tanto_si_como_si"]), 1)

    def test_ya_seas_o(self):
        text = "Ya seas cliente nuevo o de toda la vida, el precio es el mismo.\n"
        estructuras = self._estructuras(text)
        self.assertEqual(len(estructuras["ya_seas_o"]), 1)

    def test_enumeracion_mecanica_en_secuencia(self):
        text = (
            "En primer lugar, revisamos el pedido.\n\n"
            "En segundo lugar, lo empaquetamos.\n\n"
            "Por último, lo enviamos a Ferretería Robledo.\n"
        )
        estructuras = self._estructuras(text)
        self.assertEqual(len(estructuras["enumeracion_mecanica"]), 1)
        marcadores = [m.lower() for m in estructuras["enumeracion_mecanica"][0]["marcadores"]]
        self.assertEqual(
            marcadores, ["en primer lugar", "en segundo lugar", "por último"]
        )

    def test_enumeracion_sin_secuencia_completa_no_se_reporta(self):
        text = "En primer lugar, revisamos el pedido y lo enviamos hoy mismo.\n"
        estructuras = self._estructuras(text)
        self.assertEqual(estructuras["enumeracion_mecanica"], [])

    def test_conectores_al_inicio_de_parrafo_se_cuentan_por_conector(self):
        text = (
            "Además, el pedido llegó a tiempo.\n\n"
            "Además, nadie se quejó del retraso anterior.\n\n"
            "Asimismo, el cliente renovó el contrato.\n"
        )
        estructuras = self._estructuras(text)
        conectores = estructuras["conectores_parrafo"]
        self.assertEqual(conectores["además"]["ocurrencias"], 2)
        self.assertEqual(conectores["asimismo"]["ocurrencias"], 1)
        self.assertEqual(conectores["por otro lado"]["ocurrencias"], 0)

    def test_triada_de_ingredientes_reales_se_reporta_como_probable(self):
        # Salvaguarda (auditoria.md P06): una lista real de tres elementos
        # (aquí, ingredientes) no puede distinguirse por regex de una tríada
        # de adjetivos forzada; se reporta igual, siempre como "probable",
        # sin ninguna etiqueta más fuerte.
        text = "La fórmula lleva agua, glicerina y aloe en su composición habitual.\n"
        estructuras = self._estructuras(text)
        triadas = estructuras["triadas_adjetivos"]
        self.assertEqual(len(triadas), 1)
        self.assertEqual(triadas[0]["certeza"], "probable")

    def test_triada_con_epiteto_antepuesto(self):
        text = "Ofrecemos una increíble experiencia única, natural y eficaz.\n"
        estructuras = self._estructuras(text)
        triadas = estructuras["triadas_adjetivos"]
        self.assertEqual(len(triadas), 1)
        self.assertEqual(triadas[0]["certeza"], "probable")

    def test_no_estructuras_findings_have_a_verdict_field(self):
        text = (
            "El proyecto no solo cumplió el plazo, sino que además redujo costes. "
            "La fórmula lleva agua, glicerina y aloe.\n"
        )
        estructuras = self._estructuras(text)
        for lista in (
            estructuras["no_solo_sino"],
            estructuras["triadas_adjetivos"],
        ):
            for hallazgo in lista:
                self.assertNotIn("veredicto", hallazgo)
                self.assertNotIn("probabilidad_ia", hallazgo)


class TestDeterministas(unittest.TestCase):
    """T4 parte B: marcas deterministas fuera de bloques de código y
    frontmatter."""

    def setUp(self):
        self.module = load_module()
        self.entries = []

    def _deterministas(self, text):
        report = self.module.build_report(text, self.entries)
        return report["deterministas"]

    def test_clean_spain_spanish_prose_yields_no_findings(self):
        text = (
            "Marta llegó a la oficina de Ferretería Robledo a las nueve. "
            "Revisó el correo y contestó dos llamadas de proveedores.\n"
        )
        deterministas = self._deterministas(text)
        self.assertEqual(deterministas["marcado_filtrado"], [])
        self.assertEqual(deterministas["utm_ia"], [])
        self.assertEqual(deterministas["marcadores_de_posicion"], [])
        self.assertEqual(deterministas["invisibles"], [])
        self.assertEqual(deterministas["homoglifos"], [])

    def test_oaicite_marker_is_detected(self):
        text = "Esto es un dato citado :contentReference[oaicite:0]{index=0} en el texto.\n"
        deterministas = self._deterministas(text)
        tipos = [h["tipo"] for h in deterministas["marcado_filtrado"]]
        self.assertIn("oaicite", tipos)
        self.assertIn("content_reference", tipos)

    def test_turn_search_token_is_detected(self):
        text = "Un dato de referencia turn0search3 apareció en el texto pegado.\n"
        deterministas = self._deterministas(text)
        tipos = [h["tipo"] for h in deterministas["marcado_filtrado"]]
        self.assertIn("turn_search_token", tipos)

    def test_bracket_dagger_citation_is_detected(self):
        text = "Un dato con cita filtrada 【3†fuente】 en medio de la frase.\n"
        deterministas = self._deterministas(text)
        tipos = [h["tipo"] for h in deterministas["marcado_filtrado"]]
        self.assertIn("cita_corchete_angular", tipos)

    def test_marcado_filtrado_inside_code_block_is_masked(self):
        text = "```text\noaicite turn0search1 【3†fuente】 contentReference\n```\n\nTexto normal.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(deterministas["marcado_filtrado"], [])

    def test_ai_utm_source_is_flagged_as_notice(self):
        text = "Visita https://ejemplo-tienda.example.com/oferta?utm_source=chatgpt.com para más.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(len(deterministas["utm_ia"]), 1)
        self.assertEqual(deterministas["utm_ia"][0]["utm_source"], "chatgpt.com")

    def test_ordinary_utm_source_is_not_flagged(self):
        text = "Visita https://ejemplo-tienda.example.com/oferta?utm_source=newsletter para más.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(deterministas["utm_ia"], [])

    def test_placeholder_bracket_is_detected(self):
        text = "Estimado [Nombre], le escribimos desde Ferretería Robledo.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(len(deterministas["marcadores_de_posicion"]), 1)

    def test_double_brace_placeholder_is_detected(self):
        text = "Hola {{nombre_cliente}}, aquí tienes tu pedido.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(len(deterministas["marcadores_de_posicion"]), 1)

    def test_lorem_ipsum_placeholder_is_detected(self):
        text = "Lorem ipsum dolor sit amet, texto de relleno sin terminar.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(len(deterministas["marcadores_de_posicion"]), 1)

    def test_invisible_character_is_reported_by_codepoint_name(self):
        text = "Esto tiene un​espacio invisible en medio de la frase.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(len(deterministas["invisibles"]), 1)
        self.assertEqual(deterministas["invisibles"][0]["codepoint"], "U+200B")
        self.assertNotIn("​", json.dumps(deterministas["invisibles"]))

    def test_bom_at_very_start_of_text_is_not_flagged(self):
        text = "﻿Texto normal que empieza con marca de orden de bytes.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(deterministas["invisibles"], [])

    def test_nbsp_and_narrow_nbsp_are_never_flagged(self):
        text = "Son las 9 h en punto y cuestan 10 € el kilo.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(deterministas["invisibles"], [])

    def test_homoglyph_cyrillic_letter_in_latin_word_is_detected(self):
        # La "а" de "аpple" es cirílica (U+0430), no latina.
        text = "Escribió аpple en vez de apple por error de teclado.\n"
        deterministas = self._deterministas(text)
        self.assertEqual(len(deterministas["homoglifos"]), 1)
        self.assertIn("latin", deterministas["homoglifos"][0]["escrituras"])
        self.assertIn("cirilico", deterministas["homoglifos"][0]["escrituras"])


class TestRegistro(unittest.TestCase):
    """T4 parte B: recuento de tú/usted, vosotros/ustedes y léxico
    americano. Solo aviso, nunca corrección."""

    def setUp(self):
        self.module = load_module()
        self.entries = []

    def _registro(self, text):
        report = self.module.build_report(text, self.entries)
        return report["registro"]

    def test_tuteo_is_counted(self):
        text = "Tú ya sabes que tu pedido llegará mañana, te lo confirmo hoy.\n"
        registro = self._registro(text)
        self.assertGreater(registro["tuteo"]["ocurrencias"], 0)
        self.assertEqual(registro["usted"]["ocurrencias"], 0)

    def test_usted_alone_in_spain_text_is_not_labelled_as_error(self):
        text = "Usted puede recoger su pedido cuando quiera, ustedes ya lo saben.\n"
        registro = self._registro(text)
        self.assertGreater(registro["usted"]["ocurrencias"], 0)
        self.assertGreater(registro["ustedes"]["ocurrencias"], 0)
        self.assertFalse(registro["mezcla_vosotros_ustedes"])
        for h in [registro["usted"], registro["ustedes"]]:
            self.assertNotIn("error", h)
            self.assertNotIn("veredicto", h)

    def test_vosotros_and_ustedes_coexisting_is_flagged_as_mezcla_data(self):
        text = "Vosotros ya lo sabéis, y ustedes también lo saben desde ayer.\n"
        registro = self._registro(text)
        self.assertTrue(registro["mezcla_vosotros_ustedes"])

    def test_lexico_americano_computadora_is_reported(self):
        text = "Guardó el archivo en la computadora de la oficina.\n"
        registro = self._registro(text)
        expresiones = [h["expresion"] for h in registro["lexico_americano"]]
        self.assertIn("computadora", expresiones)

    def test_clean_spain_spanish_prose_has_no_lexico_americano(self):
        text = "Guardó el archivo en el ordenador de la oficina.\n"
        registro = self._registro(text)
        self.assertEqual(registro["lexico_americano"], [])

    def test_te_infusion_with_accent_is_not_counted_as_tuteo(self):
        # Revisión de la slice 04 (A2): antes de esta revisión la
        # comparación plegaba tildes, así que "té" (la infusión) contaba
        # como el pronombre "te".
        text = "Tomamos un té mientras hablábamos del pedido de hoy.\n"
        registro = self._registro(text)
        self.assertEqual(registro["tuteo"]["ocurrencias"], 0)

    def test_te_pronoun_is_counted_even_next_to_te_with_accent(self):
        text = "¿Te apetece un té después del reparto de hoy?\n"
        registro = self._registro(text)
        self.assertEqual(registro["tuteo"]["ocurrencias"], 1)


# ---------------------------------------------------------------------------
# T5, parte B: comparación con el original (--original), candidatos a claim
# y detección de datos personales. Todos los textos son propios, con marcas
# y personas ficticias; ningún dato personal es real (fase2-mapa.md §4.1).
# ---------------------------------------------------------------------------


def _con_original(module, nuevo_texto, original_texto, entries=None):
    entries = entries if entries is not None else []
    return module.build_report(nuevo_texto, entries, original_text=original_texto)


class TestComparacionCifras(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_missing_and_new_bare_figure(self):
        original = "El almacén tiene 1000 cajas guardadas hoy.\n"
        nuevo = "El almacén tiene 800 cajas guardadas hoy.\n"
        report = _con_original(self.module, nuevo, original)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual([h["texto"] for h in cifras["faltantes"]], ["1000"])
        self.assertEqual([h["texto"] for h in cifras["nuevas"]], ["800"])

    def test_thousand_separator_space_and_plain_digits_are_equal(self):
        original = "El pedido incluye 1 000 unidades en total.\n"
        nuevo = "El pedido incluye 1000 unidades en total.\n"
        report = _con_original(self.module, nuevo, original)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual(cifras["faltantes"], [])
        self.assertEqual(cifras["nuevas"], [])

    def test_narrow_nbsp_thousand_separator_and_plain_digits_are_equal(self):
        original = "El pedido incluye 1 000 unidades en total.\n"
        nuevo = "El pedido incluye 1000 unidades en total.\n"
        report = _con_original(self.module, nuevo, original)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual(cifras["faltantes"], [])
        self.assertEqual(cifras["nuevas"], [])

    def test_ambiguous_dot_thousand_reading_matches_thousands_form(self):
        original = "El pedido tiene un valor de 1.500 en el sistema.\n"
        nuevo = "El pedido tiene un valor de 1500 en el sistema.\n"
        report = _con_original(self.module, nuevo, original)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual(cifras["faltantes"], [])
        self.assertEqual(cifras["nuevas"], [])

    def test_ambiguous_dot_thousand_reading_matches_decimal_form(self):
        original = "El pedido tiene un valor de 1.500 en el sistema.\n"
        nuevo = "El pedido tiene un valor de 1.5 en el sistema.\n"
        report = _con_original(self.module, nuevo, original)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual(cifras["faltantes"], [])
        self.assertEqual(cifras["nuevas"], [])

    def test_comma_decimal_missing_and_new(self):
        original = "La densidad es de 3,5 en la prueba de hoy.\n"
        nuevo = "La densidad es de 3,8 en la prueba de hoy.\n"
        report = _con_original(self.module, nuevo, original)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual([h["lecturas"] for h in cifras["faltantes"]], [["3.5"]])
        self.assertEqual([h["lecturas"] for h in cifras["nuevas"]], [["3.8"]])

    def test_identical_dot_decimal_yields_no_difference(self):
        original = "La densidad es de 3.5 en la prueba de hoy.\n"
        nuevo = "La densidad es de 3.5 en la prueba de hoy.\n"
        report = _con_original(self.module, nuevo, original)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual(cifras["faltantes"], [])
        self.assertEqual(cifras["nuevas"], [])


class TestComparacionPorcentajes(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_missing_and_new_percentage(self):
        original = "El descuento es del 20 % esta semana.\n"
        nuevo = "El descuento es del 15 % esta semana.\n"
        report = _con_original(self.module, nuevo, original)
        porcentajes = report["comparacion"]["porcentajes"]
        self.assertEqual([h["lecturas"] for h in porcentajes["faltantes"]], [["20"]])
        self.assertEqual([h["lecturas"] for h in porcentajes["nuevas"]], [["15"]])

    def test_percent_sign_and_por_ciento_are_equal(self):
        original = "El producto elimina el 99 % de las bacterias.\n"
        nuevo = "El producto elimina el 99 por ciento de las bacterias.\n"
        report = _con_original(self.module, nuevo, original)
        porcentajes = report["comparacion"]["porcentajes"]
        self.assertEqual(porcentajes["faltantes"], [])
        self.assertEqual(porcentajes["nuevas"], [])


class TestComparacionFechas(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_textual_and_numeric_forms_of_same_date_are_equal(self):
        original = "La entrega es el 3 de marzo de 2026.\n"
        nuevo = "La entrega es el 03/03/2026.\n"
        report = _con_original(self.module, nuevo, original)
        fechas = report["comparacion"]["fechas"]
        self.assertEqual(fechas["faltantes"], [])
        self.assertEqual(fechas["nuevas"], [])

    def test_different_date_is_missing_and_new(self):
        original = "La entrega es el 3 de marzo de 2026.\n"
        nuevo = "La entrega es el 10 de marzo de 2026.\n"
        report = _con_original(self.module, nuevo, original)
        fechas = report["comparacion"]["fechas"]
        self.assertEqual(fechas["faltantes"][0]["lecturas"], ["2026-03-03"])
        self.assertEqual(fechas["nuevas"][0]["lecturas"], ["2026-03-10"])


class TestComparacionPrecios(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_missing_and_new_price(self):
        original = "El producto cuesta 10 € en la tienda.\n"
        nuevo = "El producto cuesta 12 € en la tienda.\n"
        report = _con_original(self.module, nuevo, original)
        precios = report["comparacion"]["precios"]
        self.assertEqual([h["lecturas"] for h in precios["faltantes"]], [["10"]])
        self.assertEqual([h["lecturas"] for h in precios["nuevas"]], [["12"]])

    def test_euro_sign_eur_and_euros_word_are_equal(self):
        original = "El producto cuesta 10 € en la tienda.\n"
        nuevo = "El producto cuesta 10 euros en la tienda.\n"
        report = _con_original(self.module, nuevo, original)
        precios = report["comparacion"]["precios"]
        self.assertEqual(precios["faltantes"], [])
        self.assertEqual(precios["nuevas"], [])

    def test_amount_without_thousands_separator_is_read_whole(self):
        # «1500 €» no puede leerse como «500 €»: si no, un cambio de
        # 1500 a 2500 pasaría sin aviso.
        for moneda in ("€", "euros", "EUR"):
            with self.subTest(moneda=moneda):
                original = f"El sofá Arcilla cuesta 1500 {moneda} en la tienda.\n"
                nuevo = f"El sofá Arcilla cuesta 2500 {moneda} en la tienda.\n"
                report = _con_original(self.module, nuevo, original)
                precios = report["comparacion"]["precios"]
                self.assertEqual(
                    [h["lecturas"] for h in precios["faltantes"]], [["1500"]]
                )
                self.assertEqual([h["lecturas"] for h in precios["nuevas"]], [["2500"]])

    def test_prefixed_euro_sign_reads_whole_amount(self):
        original = "Precio de lanzamiento: €1500 en la tienda.\n"
        nuevo = "Precio de lanzamiento: €2500 en la tienda.\n"
        report = _con_original(self.module, nuevo, original)
        precios = report["comparacion"]["precios"]
        self.assertEqual([h["lecturas"] for h in precios["faltantes"]], [["1500"]])
        self.assertEqual([h["lecturas"] for h in precios["nuevas"]], [["2500"]])


class TestComparacionDuracionesUnidades(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_missing_and_new_duration(self):
        original = "Hidrata la piel durante 48 h de forma continua.\n"
        nuevo = "Hidrata la piel durante 24 h de forma continua.\n"
        report = _con_original(self.module, nuevo, original)
        duraciones = report["comparacion"]["duraciones_unidades"]
        self.assertEqual(len(duraciones["faltantes"]), 1)
        self.assertEqual(len(duraciones["nuevas"]), 1)
        self.assertNotEqual(
            duraciones["faltantes"][0]["lecturas"], duraciones["nuevas"][0]["lecturas"]
        )

    def test_missing_and_new_weight_unit(self):
        original = "El envase contiene 200 g de producto.\n"
        nuevo = "El envase contiene 50 g de producto.\n"
        report = _con_original(self.module, nuevo, original)
        duraciones = report["comparacion"]["duraciones_unidades"]
        self.assertEqual(len(duraciones["faltantes"]), 1)
        self.assertEqual(len(duraciones["nuevas"]), 1)


class TestComparacionCodigos(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_missing_and_new_lot_code(self):
        original = "El lote es AB-1234 según el albarán.\n"
        nuevo = "El lote es AB-5678 según el albarán.\n"
        report = _con_original(self.module, nuevo, original)
        codigos = report["comparacion"]["codigos"]
        self.assertEqual([h["texto"] for h in codigos["faltantes"]], ["AB-1234"])
        self.assertEqual([h["texto"] for h in codigos["nuevas"]], ["AB-5678"])

    def test_case_difference_alone_is_not_flagged(self):
        original = "El lote es AB-1234 según el albarán.\n"
        nuevo = "El lote es ab-1234 según el albarán.\n"
        report = _con_original(self.module, nuevo, original)
        codigos = report["comparacion"]["codigos"]
        self.assertEqual(codigos["faltantes"], [])
        self.assertEqual(codigos["nuevas"], [])


class TestComparacionNombresPropios(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_missing_and_new_proper_noun_mid_sentence(self):
        original = "El pedido lo confirmó Marta ayer por la tarde.\n"
        nuevo = "El pedido lo confirmó Laura ayer por la tarde.\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertIn("Marta", [h["texto"] for h in nombres["faltantes"]])
        self.assertIn("Laura", [h["texto"] for h in nombres["nuevas"]])

    def test_sentence_initial_capital_is_never_flagged(self):
        original = "Marta llegó temprano a la oficina.\n"
        nuevo = "Laura llegó temprano a la oficina.\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_capital_after_inverted_question_mark_is_not_a_proper_noun(self):
        """Revisión review-4e912a0ac78c9cff (R3-nombres-propios-falsos-
        bloqueantes): una mayúscula justo tras "¿" es principio de
        pregunta, no un nombre propio."""
        original = "¿Te apetece un descuento esta semana, Marta?\n"
        nuevo = "¿Quieres un descuento esta semana, Marta?\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_capital_after_inverted_exclamation_mark_is_not_a_proper_noun(self):
        original = "¡Enhorabuena por tu compra, Marta!\n"
        nuevo = "¡Felicidades por tu compra, Marta!\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_capital_after_bullet_list_marker_is_not_a_proper_noun(self):
        original = "Ventajas:\n\n- Envío gratuito en 48 h.\n- Devolución sencilla.\n"
        nuevo = "Ventajas:\n\n- Entrega gratuita en 48 h.\n- Devolución sencilla.\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_capital_after_heading_hashes_is_not_a_proper_noun(self):
        original = "## Cuidados básicos\n\nSigue estos pasos cada día.\n"
        nuevo = "## Consejos básicos\n\nSigue estos pasos cada día.\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_capital_after_colon_starting_a_new_sentence_is_not_a_proper_noun(self):
        original = "Aviso: Este producto no sustituye un tratamiento médico.\n"
        nuevo = "Aviso: Ese producto no sustituye un tratamiento médico.\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_capital_after_dialogue_dash_at_sentence_start_is_not_a_proper_noun(self):
        original = "Marta llegó pronto. —Buenos días —dijo con una sonrisa.\n"
        nuevo = "Marta llegó pronto. —Hola de nuevo —dijo con una sonrisa.\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_capital_after_opening_quote_at_sentence_start_is_not_a_proper_noun(self):
        original = 'Marta explicó lo siguiente. "Aplica el producto cada noche."\n'
        nuevo = 'Marta explicó lo siguiente. "Usa el producto cada noche."\n'
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(nombres["faltantes"], [])
        self.assertEqual(nombres["nuevas"], [])

    def test_real_proper_noun_in_a_list_item_is_still_detected(self):
        """El aval a los marcadores de lista no debe tapar un nombre propio
        real que cambia a mitad de la línea, dentro del mismo elemento."""
        original = "- Contacta con Marta en atención al cliente.\n"
        nuevo = "- Contacta con Laura en atención al cliente.\n"
        report = _con_original(self.module, nuevo, original)
        nombres = report["comparacion"]["nombres_propios"]
        self.assertIn("Marta", [h["texto"] for h in nombres["faltantes"]])
        self.assertIn("Laura", [h["texto"] for h in nombres["nuevas"]])


class TestComparacionUrl(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_identical_url_yields_no_difference(self):
        texto = "Más información en https://tienda-robledo.example.com/ofertas.\n"
        report = _con_original(self.module, texto, texto)
        url = report["comparacion"]["url"]
        self.assertEqual(url["faltantes"], [])
        self.assertEqual(url["nuevas"], [])

    def test_different_url_is_missing_and_new(self):
        original = "Más información en https://tienda-robledo.example.com/ofertas.\n"
        nuevo = "Más información en https://tienda-robledo.example.com/catalogo.\n"
        report = _con_original(self.module, nuevo, original)
        url = report["comparacion"]["url"]
        self.assertEqual(len(url["faltantes"]), 1)
        self.assertEqual(len(url["nuevas"]), 1)


class TestComparacionClaims(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_identical_claim_yields_no_difference(self):
        texto = "[[claim]]Reduce las arrugas visibles en 30 días[[/claim]] siempre.\n"
        report = _con_original(self.module, texto, texto)
        claims = report["comparacion"]["claims_marcados"]
        self.assertEqual(claims["faltantes"], [])
        self.assertEqual(claims["nuevas"], [])

    def test_claim_changed_by_one_word_is_missing_and_new(self):
        original = "[[claim]]Reduce las arrugas visibles en 30 días[[/claim]] siempre.\n"
        nuevo = "[[claim]]Reduce las arrugas visibles en 60 días[[/claim]] siempre.\n"
        report = _con_original(self.module, nuevo, original)
        claims = report["comparacion"]["claims_marcados"]
        self.assertEqual(len(claims["faltantes"]), 1)
        self.assertEqual(len(claims["nuevas"]), 1)

    def test_claim_that_disappears_is_reported_as_missing(self):
        original = "[[claim]]Reduce las arrugas visibles en 30 días[[/claim]] siempre.\n"
        nuevo = "El producto es muy agradable de usar siempre.\n"
        report = _con_original(self.module, nuevo, original)
        claims = report["comparacion"]["claims_marcados"]
        self.assertEqual(len(claims["faltantes"]), 1)
        self.assertEqual(claims["nuevas"], [])


class TestComparacionCitas(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_identical_quote_yields_no_difference(self):
        texto = "Ella dijo «el envío es gratuito siempre» y se despidió.\n"
        report = _con_original(self.module, texto, texto)
        citas = report["comparacion"]["citas"]
        self.assertEqual(citas["faltantes"], [])
        self.assertEqual(citas["nuevas"], [])

    def test_changed_quote_is_missing_and_new(self):
        original = "Ella dijo «el envío es gratuito siempre» y se despidió.\n"
        nuevo = "Ella dijo «el envío tarda una semana» y se despidió.\n"
        report = _con_original(self.module, nuevo, original)
        citas = report["comparacion"]["citas"]
        self.assertEqual(len(citas["faltantes"]), 1)
        self.assertEqual(len(citas["nuevas"]), 1)


class TestComparacionPrivacidad(unittest.TestCase):
    """Revisión review-4e912a0ac78c9cff (R1-001): 'comparacion' no debe
    repetir nunca un valor que coincida con un patrón de datos personales,
    ni siquiera cuando ese valor cambia y por tanto cuenta como hecho
    faltante o nuevo (un teléfono cambiado SÍ es un hecho cambiado: debe
    seguir contando para el código de salida, solo el valor se oculta).
    Identificadores sintéticos y evidentemente ficticios, igual que en
    TestPrivacidad."""

    DNI_ORIGINAL = "11223344B"
    DNI_NUEVO = "99887766P"
    TELEFONO_ORIGINAL = "611223344"
    TELEFONO_NUEVO = "622334455"
    EMAIL_LOCAL_ORIGINAL = "Contacto"
    EMAIL_LOCAL_NUEVO = "Soporte"
    EMAIL_DOMINIO = "tienda-robledo.example"

    def setUp(self):
        self.module = load_module()

    def test_changed_email_inside_url_never_appears_raw_in_url(self):
        plantilla = "Reserva en https://reservas.example/alta?correo={}@{} hoy.\n"
        original = plantilla.format(self.EMAIL_LOCAL_ORIGINAL, self.EMAIL_DOMINIO)
        nuevo = plantilla.format(self.EMAIL_LOCAL_NUEVO, self.EMAIL_DOMINIO)
        report = _con_original(self.module, nuevo, original)
        volcado = json.dumps(report, ensure_ascii=False)
        for local in (self.EMAIL_LOCAL_ORIGINAL, self.EMAIL_LOCAL_NUEVO):
            self.assertNotIn("{}@{}".format(local, self.EMAIL_DOMINIO), volcado)
        url = report["comparacion"]["url"]
        self.assertEqual(len(url["faltantes"]), 1)
        self.assertEqual(len(url["nuevas"]), 1)
        self.assertEqual(url["faltantes"][0]["texto"], "[dato personal: email]")
        self.assertEqual(url["nuevas"][0]["lecturas"], [])
        self.assertTrue(
            self.module._comparacion_tiene_diferencias_bloqueantes(report["comparacion"])
        )

    def test_changed_phone_number_never_appears_raw_in_cifras(self):
        original = "Puedes llamarnos al {} en horario de oficina.\n".format(
            self.TELEFONO_ORIGINAL
        )
        nuevo = "Puedes llamarnos al {} en horario de oficina.\n".format(
            self.TELEFONO_NUEVO
        )
        report = _con_original(self.module, nuevo, original)
        volcado = json.dumps(report, ensure_ascii=False)
        self.assertNotIn(self.TELEFONO_ORIGINAL, volcado)
        self.assertNotIn(self.TELEFONO_NUEVO, volcado)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual(len(cifras["faltantes"]), 1)
        self.assertEqual(len(cifras["nuevas"]), 1)
        self.assertEqual(cifras["faltantes"][0]["texto"], "[dato personal: telefono]")
        self.assertEqual(cifras["faltantes"][0]["lecturas"], [])
        self.assertEqual(cifras["nuevas"][0]["texto"], "[dato personal: telefono]")
        self.assertEqual(cifras["nuevas"][0]["lecturas"], [])
        self.assertTrue(
            self.module._comparacion_tiene_diferencias_bloqueantes(report["comparacion"])
        )

    def test_unchanged_phone_number_yields_no_difference(self):
        texto = "Puedes llamarnos al {} en horario de oficina.\n".format(
            self.TELEFONO_ORIGINAL
        )
        report = _con_original(self.module, texto, texto)
        cifras = report["comparacion"]["cifras"]
        self.assertEqual(cifras["faltantes"], [])
        self.assertEqual(cifras["nuevas"], [])

    def test_changed_dni_never_appears_raw_in_codigos(self):
        original = "Datos del cliente: DNI {}.\n".format(self.DNI_ORIGINAL)
        nuevo = "Datos del cliente: DNI {}.\n".format(self.DNI_NUEVO)
        report = _con_original(self.module, nuevo, original)
        volcado = json.dumps(report, ensure_ascii=False)
        self.assertNotIn(self.DNI_ORIGINAL, volcado)
        self.assertNotIn(self.DNI_NUEVO, volcado)
        codigos = report["comparacion"]["codigos"]
        self.assertEqual(len(codigos["faltantes"]), 1)
        self.assertEqual(len(codigos["nuevas"]), 1)
        self.assertEqual(codigos["faltantes"][0]["texto"], "[dato personal: dni_nie]")
        self.assertEqual(codigos["nuevas"][0]["texto"], "[dato personal: dni_nie]")

    def test_phone_inside_quote_never_appears_raw_in_citas(self):
        original = "Ella dijo «Llámanos al {} por la mañana».\n".format(
            self.TELEFONO_ORIGINAL
        )
        nuevo = "Ella dijo «Llámanos al {} por la mañana».\n".format(self.TELEFONO_NUEVO)
        report = _con_original(self.module, nuevo, original)
        volcado = json.dumps(report, ensure_ascii=False)
        self.assertNotIn(self.TELEFONO_ORIGINAL, volcado)
        self.assertNotIn(self.TELEFONO_NUEVO, volcado)
        citas = report["comparacion"]["citas"]
        self.assertEqual(len(citas["faltantes"]), 1)
        self.assertEqual(len(citas["nuevas"]), 1)
        self.assertEqual(citas["faltantes"][0]["texto"], "[dato personal: telefono]")
        self.assertEqual(citas["faltantes"][0]["lecturas"], [])

    def test_email_local_part_never_appears_raw_in_nombres_propios(self):
        original = "Escríbenos a {}@{} si tienes dudas.\n".format(
            self.EMAIL_LOCAL_ORIGINAL, self.EMAIL_DOMINIO
        )
        nuevo = "Escríbenos a {}@{} si tienes dudas.\n".format(
            self.EMAIL_LOCAL_NUEVO, self.EMAIL_DOMINIO
        )
        report = _con_original(self.module, nuevo, original)
        volcado = json.dumps(report, ensure_ascii=False)
        self.assertNotIn(
            "{}@{}".format(self.EMAIL_LOCAL_ORIGINAL, self.EMAIL_DOMINIO), volcado
        )
        self.assertNotIn(
            "{}@{}".format(self.EMAIL_LOCAL_NUEVO, self.EMAIL_DOMINIO), volcado
        )
        nombres = report["comparacion"]["nombres_propios"]
        self.assertEqual(len(nombres["faltantes"]), 1)
        self.assertEqual(len(nombres["nuevas"]), 1)
        self.assertEqual(nombres["faltantes"][0]["texto"], "[dato personal: email]")
        self.assertEqual(nombres["nuevas"][0]["texto"], "[dato personal: email]")


class TestComparacionRegistro(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_tu_to_usted_switch_is_reported_as_data_not_error(self):
        original = "Tú puedes recoger tu pedido cuando quieras.\n"
        nuevo = "Usted puede recoger su pedido cuando quiera.\n"
        report = _con_original(self.module, nuevo, original)
        registro = report["comparacion"]["registro"]
        self.assertGreater(registro["tuteo"]["original"], 0)
        self.assertEqual(registro["tuteo"]["nuevo"], 0)
        self.assertEqual(registro["usted"]["original"], 0)
        self.assertGreater(registro["usted"]["nuevo"], 0)
        for clave in ("tuteo", "usted", "vosotros", "ustedes"):
            self.assertNotIn("error", registro[clave])


class TestComparacionExitCodes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def _run(self, nuevo_texto, original_texto):
        original_path = Path(self.tmp.name) / "original.txt"
        original_path.write_text(original_texto, encoding="utf-8")
        return run_cli(["--original", str(original_path), "-"], input_text=nuevo_texto)

    def test_identical_texts_exit_0_with_empty_differences(self):
        texto = (
            "El pedido llega el 3 de marzo de 2026 y cuesta 10 €. "
            "Marta lo confirmó por la tarde de ayer mismo.\n"
        )
        result = self._run(texto, texto)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        comparacion = data["comparacion"]
        for clave in (
            "cifras", "porcentajes", "fechas", "precios", "duraciones_unidades",
            "codigos", "nombres_propios", "url", "claims_marcados", "citas",
        ):
            self.assertEqual(comparacion[clave]["faltantes"], [], clave)
            self.assertEqual(comparacion[clave]["nuevas"], [], clave)

    def test_changed_four_digit_price_exits_1(self):
        original = "El sofá Arcilla cuesta 1500 € en la tienda.\n"
        nuevo = "El sofá Arcilla cuesta 2500 € en la tienda.\n"
        result = self._run(nuevo, original)
        self.assertEqual(result.returncode, 1)

    def test_claim_changed_by_one_word_exits_1(self):
        original = "[[claim]]Reduce las arrugas visibles en 30 días[[/claim]] siempre.\n"
        nuevo = "[[claim]]Reduce las arrugas visibles en 60 días[[/claim]] siempre.\n"
        result = self._run(nuevo, original)
        self.assertEqual(result.returncode, 1)

    def test_rewrite_removing_only_filler_vocabulary_exits_0(self):
        original = (
            "Cabe destacar que el pedido llega el 3 de marzo de 2026 y cuesta 10 €, "
            "según nos confirmó Marta ayer por la tarde.\n"
        )
        nuevo = (
            "El pedido llega el 3 de marzo de 2026 y cuesta 10 €, "
            "según nos confirmó Marta ayer por la tarde.\n"
        )
        result = self._run(nuevo, original)
        self.assertEqual(result.returncode, 0)

    def test_missing_figure_exits_1(self):
        original = "El almacén tiene 1000 cajas guardadas hoy.\n"
        nuevo = "El almacén tiene algunas cajas guardadas hoy.\n"
        result = self._run(nuevo, original)
        self.assertEqual(result.returncode, 1)


class TestCandidatosClaim(unittest.TestCase):
    """Ficha de producto cosmético propia y ficticia (marca "CremaViva",
    inventada para estas pruebas): percentages, duraciones, "sin parabenos"
    y "dermatológicamente testado" deben marcarse como candidatos, nunca
    como claims ya decididos; un descuento porcentual también se marca,
    por diseño (auditoria.md §7.4, resuelto: no se restringe el porcentaje a
    contextos de eficacia)."""

    def setUp(self):
        self.module = load_module()

    def _candidatos(self, text):
        report = self.module.build_report(text, [])
        return report["candidatos_claim"]

    def test_percentage_duration_sin_x_and_dermatologically_tested_are_candidates(self):
        text = (
            "CremaViva hidrata la piel durante 24 horas seguidas. "
            "Es sin parabenos y sin sulfatos. "
            "Está dermatológicamente testado en un laboratorio independiente. "
            "Aprovecha el 20 % de descuento esta semana.\n"
        )
        candidatos = self._candidatos(text)["candidatos"]
        reglas_encontradas = set()
        for c in candidatos:
            reglas_encontradas.update(c["reglas"])
        self.assertIn("duracion_unidad", reglas_encontradas)
        self.assertIn("sin_x", reglas_encontradas)
        self.assertIn("dermatologicamente", reglas_encontradas)
        self.assertIn("porcentaje", reglas_encontradas)

    def test_discount_percentage_alone_is_flagged_by_design(self):
        text = "Llévate un 20 % de descuento en tu próxima compra.\n"
        candidatos = self._candidatos(text)["candidatos"]
        self.assertEqual(len(candidatos), 1)
        self.assertIn("porcentaje", candidatos[0]["reglas"])

    def test_hipoalergenico_and_no_testado_en_animales_are_candidates(self):
        text = "CremaViva es hipoalergénico y no testado en animales.\n"
        candidatos = self._candidatos(text)["candidatos"]
        reglas = {r for c in candidatos for r in c["reglas"]}
        self.assertIn("hipoalergenico", reglas)
        self.assertIn("no_testado_en_animales", reglas)

    def test_natural_plus_effect_is_a_candidate(self):
        text = "CremaViva, con ingredientes naturales, reduce las rojeces visibles.\n"
        candidatos = self._candidatos(text)["candidatos"]
        reglas = {r for c in candidatos for r in c["reglas"]}
        self.assertIn("natural_mas_efecto", reglas)

    def test_marked_claim_is_not_reported_as_candidate(self):
        text = (
            "[[claim]]Reduce las arrugas visibles en un 30 % en cuatro semanas[[/claim]] "
            "Nadie más lo dice.\n"
        )
        resultado = self._candidatos(text)
        self.assertEqual(resultado["candidatos"], [])
        self.assertEqual(resultado["marcados"], 1)

    def test_clean_spain_spanish_prose_yields_no_candidates(self):
        text = (
            "Marta llegó a la oficina de Ferretería Robledo a las nueve. "
            "Revisó el correo y contestó dos llamadas de proveedores.\n"
        )
        candidatos = self._candidatos(text)["candidatos"]
        self.assertEqual(candidatos, [])


class TestPrivacidad(unittest.TestCase):
    """Identificadores sintéticos y evidentemente ficticios que cumplen el
    formato (DNI/IBAN calculados, no reales) para comprobar categoría y
    línea sin que el valor aparezca nunca en la salida."""

    DNI_FICTICIO = "11223344B"
    IBAN_FICTICIO = "ES25 0111 1022 2200 0333 4444"
    TELEFONO_FICTICIO = "611223344"
    EMAIL_FICTICIO = "contacto@tienda-robledo.example"

    def setUp(self):
        self.module = load_module()

    def _privacidad(self, text):
        report = self.module.build_report(text, [])
        return report, report["privacidad"]

    def test_dni_is_detected_by_category_and_line_only(self):
        text = "Datos del cliente:\nDNI {}\n".format(self.DNI_FICTICIO)
        report, privacidad = self._privacidad(text)
        categorias = [h["categoria"] for h in privacidad["hallazgos"]]
        self.assertIn("dni_nie", categorias)
        hallazgo = [h for h in privacidad["hallazgos"] if h["categoria"] == "dni_nie"][0]
        self.assertEqual(set(hallazgo.keys()), {"categoria", "linea"})
        self.assertEqual(hallazgo["linea"], 2)
        self.assertNotIn(self.DNI_FICTICIO, json.dumps(report, ensure_ascii=False))

    def test_iban_is_detected_by_category_and_line_only(self):
        text = "Cuenta para el reembolso:\nIBAN {}\n".format(self.IBAN_FICTICIO)
        report, privacidad = self._privacidad(text)
        categorias = [h["categoria"] for h in privacidad["hallazgos"]]
        self.assertIn("iban", categorias)
        self.assertNotIn(
            self.IBAN_FICTICIO.replace(" ", ""), json.dumps(report, ensure_ascii=False)
        )

    def test_phone_is_detected_by_category_and_line_only(self):
        text = "Puedes llamarnos al {} en horario de oficina.\n".format(self.TELEFONO_FICTICIO)
        report, privacidad = self._privacidad(text)
        categorias = [h["categoria"] for h in privacidad["hallazgos"]]
        self.assertIn("telefono", categorias)
        self.assertNotIn(self.TELEFONO_FICTICIO, json.dumps(report, ensure_ascii=False))

    def test_email_is_detected_by_category_and_line_only(self):
        text = "Escríbenos a {} si tienes dudas.\n".format(self.EMAIL_FICTICIO)
        report, privacidad = self._privacidad(text)
        categorias = [h["categoria"] for h in privacidad["hallazgos"]]
        self.assertIn("email", categorias)
        self.assertNotIn(self.EMAIL_FICTICIO, json.dumps(report, ensure_ascii=False))

    def test_notice_field_is_always_present(self):
        _, privacidad = self._privacidad("Un texto cualquiera sin datos personales.\n")
        self.assertIn("aviso", privacidad)
        self.assertTrue(privacidad["aviso"])

    def test_clean_spain_spanish_prose_yields_no_privacy_findings(self):
        text = (
            "Marta llegó a la oficina de Ferretería Robledo a las nueve. "
            "Revisó el correo y contestó dos llamadas de proveedores.\n"
        )
        _, privacidad = self._privacidad(text)
        self.assertEqual(privacidad["hallazgos"], [])

    def test_random_alphanumeric_code_is_not_a_false_positive_dni(self):
        # Un código de lote de 8 dígitos y una letra que NO cumple el
        # control del DNI no debe contarse como DNI/NIE.
        text = "El lote de fabricación es 12345678A.\n"
        _, privacidad = self._privacidad(text)
        self.assertEqual(
            [h for h in privacidad["hallazgos"] if h["categoria"] == "dni_nie"], []
        )


class TestControlProseOriginalComparison(unittest.TestCase):
    """Prosa de control en español de España comparada contra sí misma: no
    debe producir ninguna diferencia en 'comparacion' ni hallazgos de
    privacidad."""

    def setUp(self):
        self.module = load_module()

    def test_control_prose_against_itself_has_no_differences(self):
        text = (
            "Marta llegó a la oficina de Ferretería Robledo a las nueve de la "
            "mañana el 3 de marzo de 2026. Revisó el correo, contestó dos "
            "llamadas de proveedores y preparó un pedido de 200 g de tornillos "
            "que cuesta 10 € y tarda 48 h en llegar. El código del lote es "
            "AB-1234, según confirmó Luis por la tarde.\n"
        )
        report = self.module.build_report(text, [], original_text=text)
        comparacion = report["comparacion"]
        for clave in (
            "cifras", "porcentajes", "fechas", "precios", "duraciones_unidades",
            "codigos", "nombres_propios", "url", "claims_marcados", "citas",
        ):
            self.assertEqual(comparacion[clave]["faltantes"], [], clave)
            self.assertEqual(comparacion[clave]["nuevas"], [], clave)
        self.assertEqual(report["privacidad"]["hallazgos"], [])


if __name__ == "__main__":
    unittest.main()
