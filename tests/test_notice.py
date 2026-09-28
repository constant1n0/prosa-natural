"""Tests del paquete distribuido: SKILL.md y la copia de NOTICE.md.

Solo se distribuye la carpeta skill/prosa-natural/, así que la atribución MIT
de los proyectos de upstream tiene que viajar dentro de ella y coincidir byte
a byte con la del NOTICE.md de la raíz. SKILL.md tiene que ser válido como
skill (frontmatter con nombre y descripción), caber en el límite de líneas y
no enlazar a archivos que no existan en el paquete.

Se ejecuta con `python3 -m unittest discover -s tests -v` (stdlib, sin pytest).
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skill" / "prosa-natural"
ROOT_NOTICE = REPO_ROOT / "NOTICE.md"
SKILL_NOTICE = SKILL_DIR / "NOTICE.md"
SKILL_MD = SKILL_DIR / "SKILL.md"

MAX_SKILL_LINES = 500
REPO_HEADING = re.compile(r"^## [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
LINK_TARGET = re.compile(r"\]\(([^)\s]+)\)")
PACKAGE_PREFIXES = ("references/", "scripts/", "NOTICE.md")


def read_text(path):
    return path.read_text(encoding="utf-8")


def h2_sections(text):
    """Devuelve [(encabezado, contenido)] de cada sección `## `.

    El contenido va desde la línea del encabezado hasta la línea anterior al
    siguiente `## ` (o el final), sin las líneas en blanco finales, que son
    separador y no parte de la sección. Las líneas dentro de un bloque de
    código cercado nunca abren una sección.
    """
    sections = []
    current = None
    in_fence = False
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        if stripped.startswith("```"):
            in_fence = not in_fence
        if not in_fence and stripped.startswith("## "):
            if current is not None:
                sections.append(current)
            current = [stripped, [line]]
            continue
        if current is not None:
            current[1].append(line)
    if current is not None:
        sections.append(current)

    result = []
    for heading, lines in sections:
        while lines and lines[-1].strip() == "":
            lines.pop()
        result.append((heading, "".join(lines)))
    return result


def frontmatter(text):
    """Devuelve el frontmatter como dict {clave: valor}, o None si no hay.

    Parser mínimo, sin YAML de terceros: pares `clave: valor` de una línea;
    las líneas sangradas continúan el valor de la clave anterior.
    """
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    data = {}
    key = None
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line[0] in " \t" and key is not None:
            data[key] = (data[key] + " " + line.strip()).strip()
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match is None:
            raise AssertionError("línea de frontmatter no válida: %r" % line)
        key = match.group(1)
        data[key] = match.group(2).strip()
    return data


def package_links(text):
    """Enlaces Markdown relativos de SKILL.md a archivos del paquete."""
    in_fence = False
    targets = []
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for target in LINK_TARGET.findall(line):
            if target.startswith(PACKAGE_PREFIXES):
                targets.append(target)
    return targets


class TestNoticeCopy(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SKILL_NOTICE.is_file(), "falta %s" % SKILL_NOTICE)
        self.root_sections = [
            (heading, body)
            for heading, body in h2_sections(read_text(ROOT_NOTICE))
            if REPO_HEADING.match(heading)
        ]
        self.skill_sections = h2_sections(read_text(SKILL_NOTICE))

    def test_root_notice_names_upstream_repositories(self):
        # Salvaguarda contra un test vacío: si el parser no encontrara
        # ninguna sección de repositorio, la comparación pasaría sin probar
        # nada.
        self.assertGreater(len(self.root_sections), 0)

    def test_every_repository_section_is_copied_byte_for_byte(self):
        skill_by_heading = dict(self.skill_sections)
        for heading, body in self.root_sections:
            with self.subTest(section=heading):
                self.assertIn(heading, skill_by_heading)
                self.assertEqual(
                    skill_by_heading[heading].encode("utf-8"),
                    body.encode("utf-8"),
                )

    def test_skill_notice_has_no_other_sections(self):
        root_headings = [heading for heading, _ in self.root_sections]
        skill_headings = [heading for heading, _ in self.skill_sections]
        self.assertEqual(skill_headings, root_headings)

    def test_skill_notice_has_no_clone_instructions(self):
        # Reconstruir los clones de upstream es tarea del repositorio
        # completo, no del paquete distribuido.
        self.assertNotIn("git clone", read_text(SKILL_NOTICE))


class TestSkillMd(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SKILL_MD.is_file(), "falta %s" % SKILL_MD)
        self.text = read_text(SKILL_MD)

    def test_frontmatter_has_name_and_description_only(self):
        data = frontmatter(self.text)
        self.assertIsNotNone(data, "SKILL.md debe empezar con frontmatter")
        self.assertEqual(set(data), {"name", "description"})
        self.assertEqual(data["name"], "prosa-natural")
        self.assertTrue(data["description"])

    def test_is_under_line_limit(self):
        self.assertLess(len(self.text.splitlines()), MAX_SKILL_LINES)

    def test_package_links_point_to_existing_files(self):
        targets = package_links(self.text)
        self.assertGreater(len(targets), 0)
        for target in targets:
            with self.subTest(link=target):
                path = SKILL_DIR / target.split("#", 1)[0]
                self.assertTrue(path.is_file(), "enlace roto: %s" % target)

    def test_every_reference_and_notice_is_linked(self):
        linked = {target.split("#", 1)[0] for target in package_links(self.text)}
        expected = {
            "references/" + path.name
            for path in (SKILL_DIR / "references").glob("*.md")
        }
        expected.add("NOTICE.md")
        self.assertEqual(expected - linked, set())


if __name__ == "__main__":
    unittest.main()
