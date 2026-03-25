"""
Typography verifier for the first executable subset of the typography spec.

WHY: TYPOGRAPHY_SYSTEM.md defines strong legibility invariants, but the runtime
previously had no executable typography checks at all. This module starts with
the smallest honest subset: font-contract data integrity plus body-text rules
on repo-owned example surfaces.
"""
# ruff: noqa: I001
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from base import (
        CheckResult,
        GateResult,
        Severity,
        Status,
        ValidatorGate,
    )
else:
    from .base import (
        CheckResult,
        GateResult,
        Severity,
        Status,
        ValidatorGate,
    )


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FONT_CONTRACT_JSON = (
    REPO_ROOT / "specs" / "tokens" / "typography" / "font-contract.json"
)
DEFAULT_FONT_FAMILIES_JSON = (
    REPO_ROOT / "specs" / "tokens" / "typography" / "font-families.json"
)
DEFAULT_HTML_PATHS = (
    REPO_ROOT / "examples" / "ui" / "variant-toggle.html",
    REPO_ROOT / "examples" / "ui" / "palette-compare.html",
)
DEFAULT_CSS_PATHS = (
    REPO_ROOT / "tokens" / "color-tokens.css",
)
REQUIRED_FONT_CATEGORIES = ("ui_sans", "reading_sans", "reading_serif", "mono")
DISAMBIGUATION_ORDER = {"good": 1, "excellent": 2, "exceptional": 3}

STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(?P<body>.*?)</style>", re.I | re.S)
CSS_BLOCK_RE = re.compile(r"(?P<selectors>[^{}]+)\{(?P<body>[^{}]*)\}", re.S)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
CSS_MEDIA_RE = re.compile(r"@media[^{]+\{(?:[^{}]|\{[^{}]*\})*\}", re.S)
CSS_VALUE_RE = re.compile(r"(-?\d+(?:\.\d+)?)(px|em|rem|ch)?")


def _extract_style_text(html_text: str) -> str:
    return "\n".join(match.group("body") for match in STYLE_BLOCK_RE.finditer(html_text))


def _parse_css_blocks(css_text: str) -> dict[str, dict[str, str]]:
    css_text = CSS_COMMENT_RE.sub("", css_text)
    css_text = CSS_MEDIA_RE.sub("", css_text)
    blocks: dict[str, dict[str, str]] = {}
    for match in CSS_BLOCK_RE.finditer(css_text):
        selector_text = match.group("selectors")
        body = match.group("body")
        selectors = [part.strip() for part in selector_text.split(",") if part.strip()]
        declarations: dict[str, str] = {}
        for item in body.split(";"):
            if ":" not in item:
                continue
            prop, value = item.split(":", 1)
            declarations[prop.strip()] = value.strip()
        for selector in selectors:
            blocks[selector] = declarations
    return blocks


def _parse_css_value(value: str | None) -> tuple[float | None, str]:
    if not value:
        return None, ""
    match = CSS_VALUE_RE.search(value)
    if not match:
        return None, ""
    return float(match.group(1)), match.group(2) or ""


def _to_px(value: float | None, unit: str, *, base_px: float = 16.0) -> float | None:
    if value is None:
        return None
    if unit == "px":
        return value
    if unit in {"rem", "em"}:
        return value * base_px
    return None


class TypographyGate(ValidatorGate):
    """Executable subset of typography contract and example-surface checks."""

    gate_id = "TYPE-001"
    gate_name = "TYPOGRAPHY"
    severity = Severity.WARNING

    def __init__(
        self,
        font_contract_path: Path | None = None,
        font_families_path: Path | None = None,
        html_paths: tuple[Path, ...] | None = None,
        css_paths: tuple[Path, ...] | None = None,
    ):
        self.font_contract_path = font_contract_path or DEFAULT_FONT_CONTRACT_JSON
        self.font_families_path = font_families_path or DEFAULT_FONT_FAMILIES_JSON
        self.html_paths = html_paths or DEFAULT_HTML_PATHS
        self.css_paths = css_paths or DEFAULT_CSS_PATHS

    def _check_font_registry(self, result: GateResult) -> None:
        contract = json.loads(self.font_contract_path.read_text())
        families = json.loads(self.font_families_path.read_text())
        categories = families["categories"]
        min_x_height = contract["contract"]["static_metrics"]["x_height_ratio"]["minimum"]

        missing_categories = [
            category for category in REQUIRED_FONT_CATEGORIES if category not in categories
        ]
        result.checks.append(
            CheckResult(
                name="fonts/required_categories_present",
                status=Status.PASS if not missing_categories else Status.FAIL,
                message=(
                    "All required font categories are present"
                    if not missing_categories
                    else f"Missing categories: {', '.join(missing_categories)}"
                ),
                value=float(len(missing_categories)),
                threshold=0.0,
            )
        )

        for category in REQUIRED_FONT_CATEGORIES:
            if category not in categories:
                continue
            spec = categories[category]
            fallback_stack = spec.get("fallback_stack", "")
            result.checks.append(
                CheckResult(
                    name=f"fonts/{category}_fallback_stack",
                    status=Status.PASS if bool(fallback_stack.strip()) else Status.FAIL,
                    message=(
                        "Fallback stack declared"
                        if fallback_stack.strip()
                        else "Fallback stack missing"
                    ),
                )
            )

            required_weights = spec.get("requirements", {}).get("weights_required", [])
            available_weights = set(spec.get("primary", {}).get("weights", []))
            missing_weights = [
                weight for weight in required_weights if weight not in available_weights
            ]
            result.checks.append(
                CheckResult(
                    name=f"fonts/{category}_required_weights",
                    status=Status.PASS if not missing_weights else Status.FAIL,
                    message=(
                        f"Primary font covers required weights {required_weights}"
                        if not missing_weights
                        else f"Primary font missing weights {missing_weights}"
                    ),
                    value=float(len(available_weights)),
                    threshold=float(len(required_weights)),
                )
            )

            x_height_ratio = spec.get("primary", {}).get("x_height_ratio")
            disambiguation_score = str(
                spec.get("primary", {}).get("disambiguation_score", "")
            ).lower()
            x_height_status = Status.PASS
            x_height_message = (
                "Primary font omits x-height ratio in font-families.json; "
                "add measured metadata for this category"
            )
            if x_height_ratio is None:
                x_height_status = Status.WARN
            else:
                x_height_status = (
                    Status.PASS if x_height_ratio >= min_x_height else Status.FAIL
                )
                x_height_message = (
                    f"x-height ratio {x_height_ratio:.2f} (required >= {min_x_height:.2f})"
                )
            result.checks.append(
                CheckResult(
                    name=f"fonts/{category}_x_height_ratio",
                    status=x_height_status,
                    message=x_height_message,
                    value=x_height_ratio,
                    threshold=float(min_x_height),
                )
            )
            if category == "mono":
                result.checks.append(
                    CheckResult(
                        name="fonts/mono_disambiguation_score",
                        status=(
                            Status.PASS
                            if DISAMBIGUATION_ORDER.get(disambiguation_score, 0) >= 2
                            else Status.WARN
                        ),
                        message=(
                            f"Mono disambiguation score is {disambiguation_score or 'unset'}"
                        ),
                    )
                )

    def _check_example_surface(self, html_path: Path, result: GateResult) -> None:
        blocks = _parse_css_blocks(_extract_style_text(html_path.read_text()))
        body_block = blocks.get("body", {})

        body_font = body_block.get("font-family", "")
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/body_font_family",
                status=Status.PASS if bool(body_font.strip()) else Status.FAIL,
                message=(
                    f"body font-family: {body_font}"
                    if body_font.strip()
                    else "body is missing an explicit font-family"
                ),
            )
        )

        font_size_value, font_size_unit = _parse_css_value(body_block.get("font-size"))
        body_font_px = _to_px(font_size_value, font_size_unit)
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/body_font_size",
                status=(
                    Status.PASS if body_font_px is not None and body_font_px >= 16 else Status.FAIL
                ),
                message=(
                    f"body font-size {body_font_px:g}px"
                    if body_font_px is not None
                    else "body is missing an explicit font-size"
                ),
                value=body_font_px,
                threshold=16.0,
            )
        )

        line_height_value, line_height_unit = _parse_css_value(body_block.get("line-height"))
        if line_height_value is None:
            line_height_status = Status.FAIL
            line_height_message = "body is missing an explicit line-height"
            line_height_ratio = None
        elif line_height_unit == "":
            line_height_ratio = line_height_value
            line_height_status = Status.PASS if line_height_ratio >= 1.5 else Status.FAIL
            line_height_message = f"body line-height {line_height_ratio:g}"
        else:
            line_height_px = _to_px(line_height_value, line_height_unit, base_px=body_font_px or 16.0)
            if line_height_px is None or body_font_px is None:
                line_height_ratio = None
                line_height_status = Status.WARN
                line_height_message = "body line-height could not be normalized"
            else:
                line_height_ratio = line_height_px / body_font_px
                line_height_status = Status.PASS if line_height_ratio >= 1.5 else Status.FAIL
                line_height_message = f"body line-height ratio {line_height_ratio:.2f}"
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/body_line_height",
                status=line_height_status,
                message=line_height_message,
                value=line_height_ratio,
                threshold=1.5,
            )
        )

        long_line_violations = []
        negative_tracking_violations = []
        uppercase_spacing_violations = []
        for selector, declarations in blocks.items():
            max_width_value, max_width_unit = _parse_css_value(declarations.get("max-width"))
            if max_width_value is not None and max_width_unit == "ch" and max_width_value > 80:
                long_line_violations.append(f"{selector}={max_width_value:g}ch")

            letter_spacing_value, letter_spacing_unit = _parse_css_value(
                declarations.get("letter-spacing")
            )
            if letter_spacing_value is not None and letter_spacing_value < 0:
                negative_tracking_violations.append(
                    f"{selector}={letter_spacing_value:g}{letter_spacing_unit}"
                )

            if declarations.get("text-transform") == "uppercase" and (
                letter_spacing_unit != "em"
                or letter_spacing_value is None
                or letter_spacing_value < 0.05
            ):
                uppercase_spacing_violations.append(selector)

        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/max_line_length",
                status=Status.PASS if not long_line_violations else Status.FAIL,
                message=(
                    "No text container exceeds 80ch"
                    if not long_line_violations
                    else f"Over-wide selectors: {', '.join(long_line_violations)}"
                ),
                value=float(len(long_line_violations)),
                threshold=0.0,
            )
        )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/negative_letter_spacing",
                status=Status.PASS if not negative_tracking_violations else Status.FAIL,
                message=(
                    "No negative letter-spacing detected"
                    if not negative_tracking_violations
                    else f"Negative tracking on {', '.join(negative_tracking_violations)}"
                ),
                value=float(len(negative_tracking_violations)),
                threshold=0.0,
            )
        )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/uppercase_spacing",
                status=Status.PASS if not uppercase_spacing_violations else Status.WARN,
                message=(
                    "Uppercase selectors include adequate letter-spacing"
                    if not uppercase_spacing_violations
                    else "Uppercase selectors need >= 0.05em letter-spacing: "
                    + ", ".join(uppercase_spacing_violations)
                ),
                value=float(len(uppercase_spacing_violations)),
                threshold=0.0,
            )
        )

    def _check_link_typography(self, result: GateResult) -> None:
        for css_path in self.css_paths:
            blocks = _parse_css_blocks(css_path.read_text())
            link_block = blocks.get(".link", {})
            text_decoration = link_block.get("text-decoration", "")
            underline_offset_value, underline_offset_unit = _parse_css_value(
                link_block.get("text-underline-offset")
            )
            has_typographic_distinction = "underline" in text_decoration or (
                underline_offset_value is not None and underline_offset_unit == "px"
            )
            result.checks.append(
                CheckResult(
                    name=f"{css_path.name}/link_typographic_distinction",
                    status=Status.PASS if has_typographic_distinction else Status.FAIL,
                    message=(
                        f".link keeps non-color distinction via text-decoration '{text_decoration}'"
                        if has_typographic_distinction
                        else ".link lacks typographic distinction from body text"
                    ),
                )
            )

    def validate(self, **kwargs) -> GateResult:
        result = self._make_result()
        self._check_font_registry(result)
        for html_path in self.html_paths:
            self._check_example_surface(html_path, result)
        self._check_link_typography(result)
        return result


if __name__ == "__main__":
    gate = TypographyGate()
    gate_result = gate.validate()
    print(gate_result)
    raise SystemExit(0 if gate_result.status != Status.FAIL else 1)
