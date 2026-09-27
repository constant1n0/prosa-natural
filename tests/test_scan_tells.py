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
            },
        )
        self.assertEqual(set(data["entrada"].keys()), {"lineas", "palabras", "parrafos"})
        self.assertIn("hallazgos", data["vocabulario"])
        self.assertIn("densidad", data["vocabulario"])


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


class TestPerformance(unittest.TestCase):
    """Revisión review-faf981a2b76764c9 (R4-001, R4-002): el anidamiento de
    comillas y la resolución de solapamientos deben comparar solo dentro de
    un mismo párrafo (o con un barrido ordenado), no todo contra todo."""

    def setUp(self):
        self.module = load_module()

    def test_many_quotes_and_vocabulary_hits_complete_quickly_and_correctly(self):
        import time

        vocab_content = (
            "## Débil\n\n### Familia de prueba\n\n"
            "clave | 2026-09-27 | PXX · prueba\n"
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            vocab_path = write_vocab(tmp_dir, vocab_content)
            entries = self.module.parse_vocabulary(vocab_path)

        parrafos = [
            "Marta dijo «una frase de prueba número {}» y anotó la clave del caso.".format(i)
            for i in range(10000)
        ]
        text = "\n\n".join(parrafos) + "\n"

        inicio = time.perf_counter()
        report = self.module.build_report(text, entries)
        duracion = time.perf_counter() - inicio

        # Con la comparación global O(N²) previa a la revisión
        # review-faf981a2b76764c9 (R4-001/R4-002), 10 000 párrafos tardaban
        # cerca de 19 s; acotado a un tramo por párrafo, debe bajar de 8 s.
        self.assertLess(duracion, 8.0)
        self.assertEqual(report["comillas"]["mezcla_de_tipos"], [])
        self.assertEqual(report["comillas"]["anidamiento_invertido"], [])
        self.assertEqual(
            report["vocabulario"]["densidad"]["por_nivel"]["Débil"]["ocurrencias"], 10000
        )

    def test_overlap_resolution_unchanged_on_known_fixture(self):
        entries = self.module.parse_vocabulary(VOCAB_PATH)
        text = "Este proyecto es un pilar fundamental para la empresa.\n"
        report = self.module.build_report(text, entries)
        hallazgos = report["vocabulario"]["hallazgos"]
        colocacion = [h for h in hallazgos if h["expresion"] == "pilar fundamental"]
        suelto = [h for h in hallazgos if h["expresion"] == "fundamental"]
        self.assertEqual(len(colocacion), 1)
        self.assertEqual(len(suelto), 0)


if __name__ == "__main__":
    unittest.main()
