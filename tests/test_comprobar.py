"""Tests estrictos (TDD) para evals/comprobar.py.

Todos los textos de prueba son propios, con marcas y nombres ficticios.
Se ejecuta con `python3 -m unittest discover -s tests -v` (stdlib, sin pytest).

Sigue la misma convención de carga por ruta que tests/test_scan_tells.py,
porque ni evals/comprobar.py ni skill/prosa-natural/scripts/scan_tells.py son
paquetes instalables.
"""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPROBAR_PATH = REPO_ROOT / "evals" / "comprobar.py"
SCAN_TELLS_PATH = (
    REPO_ROOT / "skill" / "prosa-natural" / "scripts" / "scan_tells.py"
)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


comprobar = _load(COMPROBAR_PATH, "comprobar")
scan_tells = _load(SCAN_TELLS_PATH, "scan_tells")
VOCAB_ENTRIES = scan_tells.parse_vocabulary(scan_tells.DEFAULT_VOCAB_PATH)


def make_ctx(input_text, final_text=None, respuesta_text="Respuesta de prueba.",
             input_path=None, final_path=None, respuesta_path=None):
    return comprobar.EvalContext(
        input_path=input_path or Path("/no-usado/entrada.md"),
        input_text=input_text,
        final_path=final_path or Path("/no-usado/version_final.md"),
        final_text=final_text,
        respuesta_path=respuesta_path or Path("/no-usado/respuesta.md"),
        respuesta_text=respuesta_text,
        scan_tells=scan_tells,
        scan_tells_path=SCAN_TELLS_PATH,
        vocab_entries=VOCAB_ENTRIES,
    )


def evaluate(check, ctx):
    expectation = {"text": "expectativa de prueba", "check": check}
    return comprobar.evaluate_expectation(expectation, ctx)


class NormalizeTextTests(unittest.TestCase):
    def test_collapses_whitespace_and_applies_nfc(self):
        texto = "Hola\n\n   mundo\tcon   espacios"
        self.assertEqual(comprobar.normalize_text(texto), "Hola mundo con espacios")


class DebeContenerTests(unittest.TestCase):
    def test_pasa_con_texto_reformateado_en_varias_lineas(self):
        final = "El precio\nes   24,90 €\ny el código es REF-2201."
        ctx = make_ctx(input_text="original", final_text=final)
        passed, evidencia = evaluate(
            {"type": "debe_contener", "values": ["24,90 €", "REF-2201"], "en": "final"},
            ctx,
        )
        self.assertTrue(passed, evidencia)

    def test_falla_si_falta_un_valor(self):
        ctx = make_ctx(input_text="original", final_text="Solo el precio: 24,90 €.")
        passed, evidencia = evaluate(
            {"type": "debe_contener", "values": ["24,90 €", "REF-2201"], "en": "final"},
            ctx,
        )
        self.assertFalse(passed)
        self.assertIn("REF-2201", evidencia)

    def test_en_respuesta_usa_respuesta_md(self):
        ctx = make_ctx(
            input_text="original",
            final_text=None,
            respuesta_text="He revisado la ficha y conservo el código REF-9000.",
        )
        passed, _ = evaluate(
            {"type": "debe_contener", "values": ["REF-9000"], "en": "respuesta"}, ctx
        )
        self.assertTrue(passed)

    def test_falla_sin_version_final_con_evidencia_generica(self):
        ctx = make_ctx(input_text="original", final_text=None)
        passed, evidencia = evaluate(
            {"type": "debe_contener", "values": ["REF-2201"], "en": "final"}, ctx
        )
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class NoAumentaTests(unittest.TestCase):
    def test_pasa_si_no_aumenta_el_recuento(self):
        ctx = make_ctx(
            input_text="Envío gratis para el primer pedido.",
            final_text="Envío incluido para el primer pedido.",
        )
        passed, _ = evaluate(
            {"type": "no_aumenta", "pattern": r"(?i)env[ií]o\s+gratis", "en": "final"}, ctx
        )
        self.assertTrue(passed)

    def test_falla_si_aumenta_el_recuento(self):
        ctx = make_ctx(
            input_text="Sin menciones de envío.",
            final_text="Envío gratis, envío gratis, envío gratis para todos.",
        )
        passed, evidencia = evaluate(
            {"type": "no_aumenta", "pattern": r"(?i)env[ií]o\s+gratis", "en": "final"}, ctx
        )
        self.assertFalse(passed)
        self.assertIn("0", evidencia)
        self.assertIn("3", evidencia)

    def test_falla_sin_version_final(self):
        ctx = make_ctx(input_text="texto", final_text=None)
        passed, evidencia = evaluate(
            {"type": "no_aumenta", "pattern": "x", "en": "final"}, ctx
        )
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class SinFuertesTests(unittest.TestCase):
    def test_pasa_sin_vocablos_fuertes(self):
        ctx = make_ctx(
            input_text="original",
            final_text="Gracias por escribirnos, resolvemos tu duda enseguida.",
        )
        passed, _ = evaluate({"type": "sin_fuertes"}, ctx)
        self.assertTrue(passed)

    def test_falla_con_un_vocablo_fuerte(self):
        ctx = make_ctx(
            input_text="original",
            final_text="Aquí tienes la respuesta. Espero que te sea útil.",
        )
        passed, evidencia = evaluate({"type": "sin_fuertes"}, ctx)
        self.assertFalse(passed)
        self.assertIn("espero que te sea útil", evidencia)

    def test_falla_sin_version_final(self):
        ctx = make_ctx(input_text="original", final_text=None)
        passed, evidencia = evaluate({"type": "sin_fuertes"}, ctx)
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class DensidadDebilTests(unittest.TestCase):
    def test_pasa_si_no_aumenta_la_densidad(self):
        ctx = make_ctx(
            input_text="En la actualidad, en la actualidad usamos esta fórmula.",
            final_text="En la actualidad usamos esta fórmula desde hace tiempo.",
        )
        passed, _ = evaluate({"type": "densidad_debil_no_aumenta"}, ctx)
        self.assertTrue(passed)

    def test_falla_si_aumenta_la_densidad(self):
        ctx = make_ctx(
            input_text="Usamos esta fórmula desde hace tiempo.",
            final_text="En la actualidad usamos esta fórmula.",
        )
        passed, _ = evaluate({"type": "densidad_debil_no_aumenta"}, ctx)
        self.assertFalse(passed)

    def test_falla_sin_version_final(self):
        ctx = make_ctx(input_text="original", final_text=None)
        passed, evidencia = evaluate({"type": "densidad_debil_no_aumenta"}, ctx)
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class IntocablesTests(unittest.TestCase):
    def test_pasa_si_se_conservan_url_y_codigo(self):
        input_text = (
            "Más información en https://tienda-ficticia.test/promo y el "
            "código es `REF-1000`."
        )
        final_text = (
            "Puedes ampliar la información en\nhttps://tienda-ficticia.test/promo, "
            "con el código `REF-1000` de siempre."
        )
        ctx = make_ctx(input_text=input_text, final_text=final_text)
        passed, evidencia = evaluate({"type": "intocables"}, ctx)
        self.assertTrue(passed, evidencia)

    def test_falla_si_falta_la_url(self):
        input_text = "Visítanos en https://tienda-ficticia.test/promo hoy mismo."
        final_text = "Visítanos hoy mismo, tenemos novedades."
        ctx = make_ctx(input_text=input_text, final_text=final_text)
        passed, evidencia = evaluate({"type": "intocables"}, ctx)
        self.assertFalse(passed)
        self.assertIn("tienda-ficticia.test", evidencia)

    def test_falla_sin_version_final(self):
        ctx = make_ctx(input_text="https://x.test/y", final_text=None)
        passed, evidencia = evaluate({"type": "intocables"}, ctx)
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class RegistroIgualTests(unittest.TestCase):
    def test_pasa_si_se_mantiene_el_tuteo(self):
        ctx = make_ctx(
            input_text="Tú puedes escribirnos cuando quieras. Te avisaremos.",
            final_text="Puedes escribirnos cuando quieras. Te avisaremos pronto.",
        )
        passed, _ = evaluate({"type": "registro_igual"}, ctx)
        self.assertTrue(passed)

    def test_falla_si_cambia_a_usted(self):
        ctx = make_ctx(
            input_text="Tú puedes escribirnos cuando quieras. Te avisaremos.",
            final_text="Usted puede escribirnos cuando quiera. Le avisaremos.",
        )
        passed, evidencia = evaluate({"type": "registro_igual"}, ctx)
        self.assertFalse(passed, evidencia)

    def test_falla_sin_version_final(self):
        ctx = make_ctx(input_text="Tú puedes.", final_text=None)
        passed, evidencia = evaluate({"type": "registro_igual"}, ctx)
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class SimilitudMinimaTests(unittest.TestCase):
    ORIGINAL = (
        "La ferretería Casa Benítez lleva treinta años en el barrio. "
        "Vendemos tornillería, pintura y herramienta de mano a buen precio."
    )

    def test_pasa_con_texto_casi_identico(self):
        final = self.ORIGINAL.replace("treinta años", "más de treinta años")
        ctx = make_ctx(input_text=self.ORIGINAL, final_text=final)
        passed, evidencia = evaluate(
            {"type": "similitud_minima", "min": 0.9, "sin_final_valido_si": "(?i)sin cambios"},
            ctx,
        )
        self.assertTrue(passed, evidencia)

    def test_falla_con_texto_muy_distinto(self):
        final = "Hoy hace sol y mañana lloverá en la costa, según el parte."
        ctx = make_ctx(input_text=self.ORIGINAL, final_text=final)
        passed, evidencia = evaluate(
            {"type": "similitud_minima", "min": 0.9, "sin_final_valido_si": "(?i)sin cambios"},
            ctx,
        )
        self.assertFalse(passed, evidencia)

    def test_sin_final_pasa_si_la_respuesta_dice_sin_cambios(self):
        ctx = make_ctx(
            input_text=self.ORIGINAL,
            final_text=None,
            respuesta_text="El texto ya está bien escrito, sale SIN CAMBIOS.",
        )
        passed, evidencia = evaluate(
            {"type": "similitud_minima", "min": 0.9, "sin_final_valido_si": "(?i)sin cambios"},
            ctx,
        )
        self.assertTrue(passed, evidencia)

    def test_sin_final_falla_si_la_respuesta_no_lo_dice(self):
        ctx = make_ctx(
            input_text=self.ORIGINAL,
            final_text=None,
            respuesta_text="No he podido revisar el texto todavía.",
        )
        passed, evidencia = evaluate(
            {"type": "similitud_minima", "min": 0.9, "sin_final_valido_si": "(?i)sin cambios"},
            ctx,
        )
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class SinVersionFinalTests(unittest.TestCase):
    def test_pasa_si_no_hay_final(self):
        ctx = make_ctx(input_text="original", final_text=None)
        passed, evidencia = evaluate({"type": "sin_version_final"}, ctx)
        self.assertTrue(passed)
        self.assertEqual(evidencia, "no hay versión final")

    def test_falla_si_hay_final(self):
        ctx = make_ctx(input_text="original", final_text="Versión reescrita.")
        passed, evidencia = evaluate({"type": "sin_version_final"}, ctx)
        self.assertFalse(passed)
        self.assertEqual(evidencia, "se entregó una versión final")


class RespuestaCoincideTests(unittest.TestCase):
    def test_pasa_si_coinciden_todos_los_patrones(self):
        ctx = make_ctx(
            input_text="original",
            final_text=None,
            respuesta_text=(
                "Veredicto global: requiere decisión del autor.\n"
                "Hay un candidato a claim sin marcar: preguntar al autor."
            ),
        )
        passed, evidencia = evaluate(
            {
                "type": "respuesta_coincide",
                "patterns": [
                    "(?i)veredicto global.*requiere decisi[oó]n del autor",
                    "(?i)candidato[s]? a claim",
                ],
            },
            ctx,
        )
        self.assertTrue(passed, evidencia)

    def test_falla_si_falta_un_patron(self):
        ctx = make_ctx(
            input_text="original",
            final_text=None,
            respuesta_text="No hay ningún candidato a claim en este texto.",
        )
        passed, evidencia = evaluate(
            {
                "type": "respuesta_coincide",
                "patterns": ["(?i)veredicto global.*requiere decisi[oó]n del autor"],
            },
            ctx,
        )
        self.assertFalse(passed)
        self.assertIn("veredicto global", evidencia)


class SinInvencionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)

    def _write(self, nombre, contenido):
        ruta = self.tmp_path / nombre
        ruta.write_text(contenido, encoding="utf-8")
        return ruta

    def test_pasa_sin_diferencias_bloqueantes(self):
        input_path = self._write(
            "entrada.md", "La crema reduce arrugas en un 30 % en 4 semanas. Precio: 24,90 €."
        )
        final_path = self._write(
            "final.md",
            "La crema reduce visiblemente las arrugas en un 30 % en 4 semanas, "
            "según nuestros datos. Precio: 24,90 €.",
        )
        ctx = make_ctx(
            input_text=input_path.read_text(encoding="utf-8"),
            final_text=final_path.read_text(encoding="utf-8"),
            input_path=input_path,
            final_path=final_path,
        )
        passed, evidencia = evaluate({"type": "sin_invencion"}, ctx)
        self.assertTrue(passed, evidencia)

    def test_falla_con_diferencias_bloqueantes(self):
        input_path = self._write(
            "entrada.md", "La crema reduce arrugas en un 30 % en 4 semanas. Precio: 24,90 €."
        )
        final_path = self._write(
            "final.md",
            "La crema reduce arrugas de forma notable en pocas semanas. Precio: 24,90 €.",
        )
        ctx = make_ctx(
            input_text=input_path.read_text(encoding="utf-8"),
            final_text=final_path.read_text(encoding="utf-8"),
            input_path=input_path,
            final_path=final_path,
        )
        passed, evidencia = evaluate({"type": "sin_invencion"}, ctx)
        self.assertFalse(passed)
        self.assertIn("porcentajes", evidencia)

    def test_omitir_si_sin_final_pasa_sin_version_final(self):
        ctx = make_ctx(input_text="original", final_text=None)
        passed, evidencia = evaluate(
            {"type": "sin_invencion", "omitir_si_sin_final": True}, ctx
        )
        self.assertTrue(passed)
        self.assertEqual(evidencia, "sin versión final: no aplica")

    def test_sin_version_final_falla_sin_la_opcion(self):
        ctx = make_ctx(input_text="original", final_text=None)
        passed, evidencia = evaluate({"type": "sin_invencion"}, ctx)
        self.assertFalse(passed)
        self.assertEqual(evidencia, "no hay versión final")


class TipoDesconocidoTests(unittest.TestCase):
    def test_lanza_comprobar_error(self):
        ctx = make_ctx(input_text="original", final_text="final")
        with self.assertRaises(comprobar.ComprobarError):
            evaluate({"type": "tipo_que_no_existe"}, ctx)


class GradeRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo_root = Path(self.tmp.name)
        (self.repo_root / "evals" / "casos").mkdir(parents=True)
        self.input_path = self.repo_root / "evals" / "casos" / "01-texto.md"
        self.input_path.write_text(
            "Nuestra academia Aurora lleva cinco años enseñando costura.",
            encoding="utf-8",
        )
        self.run_dir = self.repo_root / "run-1"
        (self.run_dir / "outputs").mkdir(parents=True)
        (self.run_dir / "outputs" / "respuesta.md").write_text(
            "Aquí tienes la versión pulida.", encoding="utf-8"
        )
        (self.run_dir / "outputs" / "version_final.md").write_text(
            "Nuestra academia Aurora lleva cinco años enseñando costura en el barrio.",
            encoding="utf-8",
        )
        self.eval_obj = {
            "id": 1,
            "name": "01-texto",
            "files": ["evals/casos/01-texto.md"],
            "expectations": [
                {
                    "text": "El nombre de la academia se conserva.",
                    "check": {"type": "debe_contener", "values": ["Aurora"], "en": "final"},
                },
                {
                    "text": "Esta expectativa está diseñada para fallar.",
                    "check": {"type": "debe_contener", "values": ["No existe"], "en": "final"},
                },
            ],
        }

    def test_estructura_y_campos_exactos_del_grading(self):
        grading = comprobar.grade_run(
            self.eval_obj,
            self.run_dir,
            repo_root=self.repo_root,
            scan_tells_module=scan_tells,
            scan_tells_path=SCAN_TELLS_PATH,
            vocab_entries=VOCAB_ENTRIES,
        )
        self.assertEqual(set(grading.keys()), {"expectations", "summary"})
        for expectativa in grading["expectations"]:
            self.assertEqual(set(expectativa.keys()), {"text", "passed", "evidence"})
        self.assertEqual(
            grading["summary"],
            {"passed": 1, "failed": 1, "total": 2, "pass_rate": 0.5},
        )

        grading_path = self.run_dir / "grading.json"
        self.assertTrue(grading_path.exists())
        contenido = grading_path.read_text(encoding="utf-8")
        self.assertIn("á", contenido)  # ensure_ascii=False
        self.assertIn("\n  \"", contenido)  # indent=2
        datos = json.loads(contenido)
        self.assertEqual(datos, grading)


class DiscoverRunDirsTests(unittest.TestCase):
    def test_orden_numerico_natural_de_las_ejecuciones(self):
        with tempfile.TemporaryDirectory() as tmp:
            iter_dir = Path(tmp)
            eval_dir = iter_dir / "eval-01-texto"
            (eval_dir).mkdir(parents=True)
            (eval_dir / "eval_metadata.json").write_text(
                json.dumps({"eval_id": 1, "eval_name": "01-texto"}), encoding="utf-8"
            )
            for configuracion in ("without_skill", "with_skill"):
                for numero in (2, 10, 1):
                    run_dir = eval_dir / configuracion / "run-{}".format(numero)
                    (run_dir / "outputs").mkdir(parents=True)
            encontrados = comprobar.discover_run_dirs(iter_dir)
            nombres = [run_dir.name for (_e, _id, _c, run_dir) in encontrados]
            self.assertEqual(
                nombres,
                ["run-1", "run-2", "run-10", "run-1", "run-2", "run-10"],
            )
            configuraciones = [c for (_e, _id, c, _r) in encontrados]
            self.assertEqual(configuraciones[:3], ["with_skill"] * 3)
            self.assertEqual(configuraciones[3:], ["without_skill"] * 3)


class FindEvalTests(unittest.TestCase):
    def test_lanza_error_si_no_existe_el_id(self):
        with self.assertRaises(comprobar.ComprobarError):
            comprobar.find_eval({"evals": [{"id": 1}]}, 99)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo_root = Path(self.tmp.name)
        (self.repo_root / "evals" / "casos").mkdir(parents=True)

    def _escribir_entrada(self, nombre, texto):
        ruta = self.repo_root / "evals" / "casos" / nombre
        ruta.write_text(texto, encoding="utf-8")
        return "evals/casos/{}".format(nombre)

    def test_tipo_de_chequeo_desconocido_devuelve_codigo_2(self):
        ruta_relativa = self._escribir_entrada("caso.md", "Texto de entrada.")
        evals_data = {
            "evals": [
                {
                    "id": 1,
                    "name": "01-caso",
                    "files": [ruta_relativa],
                    "expectations": [
                        {"text": "chequeo inventado", "check": {"type": "no_existe"}}
                    ],
                }
            ]
        }
        evals_path = self.repo_root / "evals" / "evals.json"
        evals_path.write_text(json.dumps(evals_data), encoding="utf-8")

        iter_dir = self.repo_root / "evals" / "resultados" / "iter-1"
        eval_dir = iter_dir / "eval-01-caso"
        run_dir = eval_dir / "with_skill" / "run-1"
        (run_dir / "outputs").mkdir(parents=True)
        (run_dir / "outputs" / "respuesta.md").write_text("Respuesta.", encoding="utf-8")
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps({"eval_id": 1, "eval_name": "01-caso"}), encoding="utf-8"
        )

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            codigo = comprobar.main(
                ["--evals", str(evals_path), "--iteracion", str(iter_dir)]
            )
        self.assertEqual(codigo, 2)
        self.assertIn("no_existe", stderr.getvalue())

    def test_iteracion_completa_dos_evals_dos_configuraciones(self):
        ruta_1 = self._escribir_entrada("01-caso.md", "Texto de entrada uno.")
        ruta_2 = self._escribir_entrada("02-caso.md", "Texto de entrada dos.")
        evals_data = {
            "evals": [
                {
                    "id": 1,
                    "name": "01-caso",
                    "files": [ruta_1],
                    "expectations": [
                        {
                            "text": "La respuesta menciona 'confirmado'.",
                            "check": {
                                "type": "respuesta_coincide",
                                "patterns": ["(?i)confirmado"],
                            },
                        }
                    ],
                },
                {
                    "id": 2,
                    "name": "02-caso",
                    "files": [ruta_2],
                    "expectations": [
                        {
                            "text": "No se entrega versión final.",
                            "check": {"type": "sin_version_final"},
                        }
                    ],
                },
            ]
        }
        evals_path = self.repo_root / "evals" / "evals.json"
        evals_path.write_text(json.dumps(evals_data), encoding="utf-8")

        iter_dir = self.repo_root / "evals" / "resultados" / "iter-1"
        for eval_id, nombre_eval in ((1, "01-caso"), (2, "02-caso")):
            eval_dir = iter_dir / "eval-{}".format(nombre_eval)
            eval_dir.mkdir(parents=True)
            (eval_dir / "eval_metadata.json").write_text(
                json.dumps({"eval_id": eval_id, "eval_name": nombre_eval}),
                encoding="utf-8",
            )
            for configuracion in ("with_skill", "without_skill"):
                run_dir = eval_dir / configuracion / "run-1"
                (run_dir / "outputs").mkdir(parents=True)
                (run_dir / "outputs" / "respuesta.md").write_text(
                    "Queda confirmado.", encoding="utf-8"
                )

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            codigo = comprobar.main(
                ["--evals", str(evals_path), "--iteracion", str(iter_dir)]
            )
        self.assertEqual(codigo, 0)
        salida = stdout.getvalue()
        self.assertIn("01-caso", salida)
        self.assertIn("02-caso", salida)
        self.assertIn("with_skill", salida)
        self.assertIn("without_skill", salida)

        for eval_id, nombre_eval in ((1, "01-caso"), (2, "02-caso")):
            for configuracion in ("with_skill", "without_skill"):
                grading_path = (
                    iter_dir
                    / "eval-{}".format(nombre_eval)
                    / configuracion
                    / "run-1"
                    / "grading.json"
                )
                self.assertTrue(grading_path.exists())
                datos = json.loads(grading_path.read_text(encoding="utf-8"))
                self.assertEqual(datos["summary"]["total"], 1)
                if eval_id == 1:
                    self.assertEqual(datos["summary"]["passed"], 1)
                else:
                    self.assertEqual(datos["summary"]["passed"], 1)


if __name__ == "__main__":
    unittest.main()
