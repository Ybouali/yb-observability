from __future__ import annotations

from pathlib import Path

import pytest

from yb_observability.config import (
    ConfigLoader,
)


def write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "config.yml"
    path.write_text(text, encoding="utf-8")
    return path


class TestConfigLoaderSubstitution:
    # ---- injection safety (the reason we moved post-parse) -----------

    def test_value_with_colon_is_not_reparsed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("NAME", "foo: bar")
        path = write(tmp_path, "name: ${NAME}\n")
        assert ConfigLoader(path).load() == {"name": "foo: bar"}

    def test_value_with_hash_is_not_a_comment(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("NAME", "foo # not a comment")
        path = write(tmp_path, "name: ${NAME}\n")
        assert ConfigLoader(path).load() == {"name": "foo # not a comment"}

    def test_value_with_newline(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("BANNER", "line1\nline2")
        path = write(tmp_path, "banner: ${BANNER}\n")
        assert ConfigLoader(path).load() == {"banner": "line1\nline2"}

    def test_value_with_quotes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("VAL", 'he said "hi"')
        path = write(tmp_path, "val: ${VAL}\n")
        assert ConfigLoader(path).load() == {"val": 'he said "hi"'}

    # ---- defaults -----------------------------------------------------

    def test_default_used_when_unset(self, tmp_path: Path) -> None:
        path = write(tmp_path, "port: ${PORT:-8080}\n")
        assert ConfigLoader(path).load() == {"port": "8080"}

    def test_env_overrides_default(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PORT", "9000")
        path = write(tmp_path, "port: ${PORT:-8080}\n")
        assert ConfigLoader(path).load() == {"port": "9000"}

    def test_empty_default(self, tmp_path: Path) -> None:
        path = write(tmp_path, 'val: "${MISSING:-}"\n')
        assert ConfigLoader(path).load() == {"val": ""}

    # ---- escape -------------------------------------------------------

    def test_escaped_var_is_literal(self, tmp_path: Path) -> None:
        path = write(tmp_path, "template: $${NOT_RESOLVED}\n")
        assert ConfigLoader(path).load() == {"template": "${NOT_RESOLVED}"}

    # ---- type preservation -------------------------------------------

    def test_non_string_leaves_untouched(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PORT", "8080")
        path = write(
            tmp_path,
            "port: 8080\nratio: 1.5\nenabled: true\nempty: null\nas_str: '${PORT}'\n",
        )
        assert ConfigLoader(path).load() == {
            "port": 8080,
            "ratio": 1.5,
            "enabled": True,
            "empty": None,
            "as_str": "8080",
        }

    # ---- keys are never substituted ----------------------------------

    def test_keys_are_not_substituted(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("KEY", "resolved")
        path = write(tmp_path, "${KEY}: value\n")
        assert ConfigLoader(path).load() == {"${KEY}": "value"}
