"""Tests for the first typography verifier."""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators.base import Status
from validators.typography import TypographyGate


def write_font_contract(path: Path) -> None:
    payload = {
        "contract": {
            "static_metrics": {
                "x_height_ratio": {
                    "minimum": 0.50,
                }
            }
        }
    }
    path.write_text(json.dumps(payload))


def write_font_families(path: Path) -> None:
    payload = {
        "categories": {
            "ui_sans": {
                "requirements": {"weights_required": [400, 700]},
                "primary": {"weights": [400, 500, 700], "x_height_ratio": 0.55},
                "fallback_stack": "system-ui, sans-serif",
            },
            "reading_sans": {
                "requirements": {"weights_required": [400, 700]},
                "primary": {"weights": [400, 700], "x_height_ratio": 0.56},
                "fallback_stack": "system-ui, sans-serif",
            },
            "reading_serif": {
                "requirements": {"weights_required": [400, 700]},
                "primary": {"weights": [400, 700], "x_height_ratio": 0.52},
                "fallback_stack": "Georgia, serif",
            },
            "mono": {
                "requirements": {"weights_required": [400, 700]},
                "primary": {"weights": [400, 700], "disambiguation_score": "excellent"},
                "fallback_stack": "ui-monospace, monospace",
            },
        }
    }
    path.write_text(json.dumps(payload))


def write_html(
    path: Path,
    *,
    body_font_size: str = "16px",
    body_line_height: str = "1.5",
    body_font_family: str = "system-ui, sans-serif",
    line_length: str = "72ch",
    letter_spacing: str = "0.08em",
) -> None:
    path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html>",
                "<head>",
                "<style>",
                "body {",
                f"  font-family: {body_font_family};",
                f"  font-size: {body_font_size};",
                f"  line-height: {body_line_height};",
                "}",
                ".copy {",
                f"  max-width: {line_length};",
                "}",
                ".eyebrow {",
                "  text-transform: uppercase;",
                f"  letter-spacing: {letter_spacing};",
                "}",
                "</style>",
                "</head>",
                "<body><p class=\"copy\">Example</p><p class=\"eyebrow\">Status lane</p></body>",
                "</html>",
            ]
        )
    )


def write_css(path: Path, *, underline: bool = True, offset: str = "2px") -> None:
    text_decoration = "underline" if underline else "none"
    path.write_text(
        "\n".join(
            [
                ".link {",
                f"  text-decoration: {text_decoration};",
                f"  text-underline-offset: {offset};",
                "}",
            ]
        )
    )


def test_typography_gate_passes_on_valid_contract_and_examples(tmp_path: Path) -> None:
    contract = tmp_path / "font-contract.json"
    families = tmp_path / "font-families.json"
    html = tmp_path / "example.html"
    css = tmp_path / "tokens.css"
    write_font_contract(contract)
    write_font_families(families)
    write_html(html)
    write_css(css)

    gate = TypographyGate(
        font_contract_path=contract,
        font_families_path=families,
        html_paths=(html,),
        css_paths=(css,),
    )
    result = gate.validate()

    assert result.status == Status.WARN
    assert any(
        check.name == "fonts/mono_x_height_ratio" and check.status == Status.WARN
        for check in result.checks
    )
    assert any(
        check.name == "fonts/mono_disambiguation_score" and check.status == Status.PASS
        for check in result.checks
    )


def test_typography_gate_fails_on_tight_body_copy(tmp_path: Path) -> None:
    contract = tmp_path / "font-contract.json"
    families = tmp_path / "font-families.json"
    html = tmp_path / "example.html"
    css = tmp_path / "tokens.css"
    write_font_contract(contract)
    write_font_families(families)
    write_html(html, body_font_size="14px", body_line_height="1.2", line_length="90ch")
    write_css(css)

    gate = TypographyGate(
        font_contract_path=contract,
        font_families_path=families,
        html_paths=(html,),
        css_paths=(css,),
    )
    result = gate.validate()

    assert result.status == Status.FAIL
    assert any(
        check.name == "example.html/body_font_size" and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/max_line_length" and check.status == Status.FAIL
        for check in result.checks
    )


def test_typography_gate_warns_on_uppercase_without_tracking(tmp_path: Path) -> None:
    contract = tmp_path / "font-contract.json"
    families = tmp_path / "font-families.json"
    html = tmp_path / "example.html"
    css = tmp_path / "tokens.css"
    write_font_contract(contract)
    write_font_families(families)
    write_html(html, letter_spacing="0.01em")
    write_css(css)

    gate = TypographyGate(
        font_contract_path=contract,
        font_families_path=families,
        html_paths=(html,),
        css_paths=(css,),
    )
    result = gate.validate()

    assert any(
        check.name == "example.html/uppercase_spacing" and check.status == Status.WARN
        for check in result.checks
    )


def test_typography_gate_fails_when_links_lack_typographic_distinction(tmp_path: Path) -> None:
    contract = tmp_path / "font-contract.json"
    families = tmp_path / "font-families.json"
    html = tmp_path / "example.html"
    css = tmp_path / "tokens.css"
    write_font_contract(contract)
    write_font_families(families)
    write_html(html)
    write_css(css, underline=False, offset="0")

    gate = TypographyGate(
        font_contract_path=contract,
        font_families_path=families,
        html_paths=(html,),
        css_paths=(css,),
    )
    result = gate.validate()

    assert any(
        check.name == "tokens.css/link_typographic_distinction"
        and check.status == Status.FAIL
        for check in result.checks
    )
