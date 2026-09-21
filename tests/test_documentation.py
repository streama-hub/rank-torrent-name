import inspect
from pathlib import Path
import re
import textwrap
import tomllib

import pytest

from RTN import RTN


@pytest.mark.parametrize("target", [RTN, RTN.__init__, RTN.rank])
def test_parser_docstring_examples(target):
    examples = re.findall(r"```python[ \t]*\n(.*?)```", inspect.getdoc(target), re.S)
    assert examples
    for example in examples:
        namespace = {}
        exec(textwrap.dedent(example), namespace)
        if target is RTN.__init__:
            assert namespace["rtn"].lev_threshold == 0.94


def test_custom_ranking_documentation():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs/devs/introduction.md").read_text(encoding="utf-8")
    example = next(code for code in re.findall(r"```python\s*(.*?)```", text, re.S) if "class MyRankingModel" in code)
    namespace = {}
    exec(example, namespace)
    model = namespace["MyRankingModel"]()
    assert model.uhd == 200
    assert model.hdr == 100


def test_ranking_documentation_example():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs/devs/ranking.md").read_text(encoding="utf-8")
    example = text.split("**Example**", 1)[1].split("```python", 1)[1].split("```", 1)[0]
    namespace = {}
    exec(example, namespace)
    assert namespace["torrent"].lev_ratio == 1.0


@pytest.mark.parametrize("document", ["settings.md", "models.md"])
def test_model_configuration_examples(document):
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs/devs" / document).read_text(encoding="utf-8")
    examples = [code for code in re.findall(r"```python[^\n]*\n(.*?)```", text, re.S) if "from RTN.models import" in code]
    assert examples
    for example in examples:
        namespace = {}
        exec(example, namespace)
        assert isinstance(namespace["settings"], namespace["SettingsModel"])


def test_documentation_source_links_target_current_repository():
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    repository = project["tool"]["poetry"]["urls"]["Repository"]
    links = []
    for path in (root / "docs").rglob("*.md"):
        links.extend(re.findall(r"\[source\]\(([^)]+)\)", path.read_text(encoding="utf-8")))
    assert links
    for link in links:
        prefix = repository + "/blob/main/"
        assert link.startswith(prefix)
        assert (root / link.removeprefix(prefix)).is_file()


def test_documentation_local_links_exist():
    root = Path(__file__).resolve().parents[1]
    for path in [root / "README.md", root / "CONTRIBUTING.md", *(root / "docs").rglob("*.md")]:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            assert (path.parent / target.split("#", 1)[0]).exists(), (path, target)
