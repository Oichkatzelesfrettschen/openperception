"""
SPATIAL gate (GATE-004) - static spatial accessibility checks.

WHY: The validator framework declares broad spatial and reflow validation, but
the runtime had no executable spatial gate. This module implements a first,
static subset over token definitions, CSS utilities, and example HTML.
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
DEFAULT_SPACING_JSON = REPO_ROOT / "specs" / "tokens" / "layout" / "spacing.json"
DEFAULT_CSS = REPO_ROOT / "tokens" / "color-tokens.css"
DEFAULT_HTML_PATHS = (
    REPO_ROOT / "examples" / "ui" / "variant-toggle.html",
    REPO_ROOT / "examples" / "ui" / "palette-compare.html",
)


CSS_BLOCK_RE = re.compile(r"(?P<selectors>[^{}]+)\{(?P<body>[^{}]*)\}", re.S)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
CLASS_DUP_RE = re.compile(
    r"<[^>]*\bclass\s*=\s*\"[^\"]*\"[^>]*\bclass\s*=\s*\"[^\"]*\"[^>]*>"
)
TABINDEX_RE = re.compile(
    r"<(?P<tag>[a-zA-Z0-9-]+)(?P<attrs>[^>]*)\btabindex\s*=\s*\"0\"(?P<rest>[^>]*)>"
)
CLASS_ATTR_RE = re.compile(r"\bclass\s*=\s*\"([^\"]*)\"")
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(?P<body>.*?)</style>", re.I | re.S)
VIEWPORT_RE = re.compile(r"<meta[^>]+name\s*=\s*[\"']viewport[\"'][^>]*>", re.I)
PX_RE = re.compile(r"(-?\d+(?:\.\d+)?)px")
GRID_MINMAX_PX_RE = re.compile(r"minmax\((?P<value>[^,]+),", re.I)
REPEAT_COUNT_RE = re.compile(r"repeat\((?P<count>\d+),", re.I)
SWATCH_MEDIA_RE = re.compile(r"@media[\s\S]*?\.swatch-grid\s*\{", re.I)
BUTTON_SELECTORS = (".btn-primary", ".btn-secondary")
WRAP_SELECTORS = (".page-nav", ".toolbar", ".controls", ".pill-row", ".demo-actions")
NARROW_VIEWPORT_WIDTH = 320.0


def _parse_css_blocks(css_text: str) -> dict[str, dict[str, str]]:
    css_text = CSS_COMMENT_RE.sub("", css_text)
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
            existing = dict(blocks.get(selector, {}))
            existing.update(declarations)
            blocks[selector] = existing
    return blocks


def _extract_px(value: str | None) -> float | None:
    if not value:
        return None
    match = PX_RE.search(value)
    if not match:
        return None
    return float(match.group(1))


def _extract_style_text(html_text: str) -> str:
    return "\n".join(
        match.group("body") for match in STYLE_BLOCK_RE.finditer(html_text)
    )


def _horizontal_padding(value: str | None) -> float:
    if not value:
        return 0.0
    numbers = [float(match) for match in PX_RE.findall(value)]
    if not numbers:
        return 0.0
    if len(numbers) == 1:
        return numbers[0] * 2
    if len(numbers) == 2:
        return numbers[1] * 2
    if len(numbers) == 3:
        return numbers[1] * 2
    return numbers[1] + numbers[3]


def _grid_min_width(grid_template: str) -> float | None:
    match = GRID_MINMAX_PX_RE.search(grid_template)
    if not match:
        return None
    if "100%" in match.group("value"):
        return 0.0
    px_match = PX_RE.search(match.group("value"))
    if not px_match:
        return None
    return float(px_match.group(1))


class SpatialGate(ValidatorGate):
    """GATE-004: SPATIAL - static token/CSS/example validation."""

    gate_id = "GATE-004"
    gate_name = "SPATIAL"
    severity = Severity.WARNING

    def __init__(
        self,
        spacing_json_path: Path | None = None,
        css_path: Path | None = None,
        html_paths: tuple[Path, ...] | None = None,
    ):
        self.spacing_json_path = spacing_json_path or DEFAULT_SPACING_JSON
        self.css_path = css_path or DEFAULT_CSS
        self.html_paths = html_paths or DEFAULT_HTML_PATHS

    def _check_spacing_tokens(self, result: GateResult) -> None:
        data = json.loads(self.spacing_json_path.read_text())
        min_target = data["interactive"]["touch"]["minTarget"]["value"]
        min_spacing = data["interactive"]["touch"]["minSpacing"]["value"]
        outline_width = data["interactive"]["focus"]["outlineWidth"]["value"]

        result.checks.append(
            CheckResult(
                name="spacing/touch_target_size",
                status=Status.PASS if min_target >= 44 else Status.FAIL,
                message=f"{min_target}px (required >= 44px)",
                value=float(min_target),
                threshold=44.0,
            )
        )
        result.checks.append(
            CheckResult(
                name="spacing/touch_target_spacing",
                status=Status.PASS if min_spacing >= 8 else Status.FAIL,
                message=f"{min_spacing}px (required >= 8px)",
                value=float(min_spacing),
                threshold=8.0,
            )
        )
        result.checks.append(
            CheckResult(
                name="spacing/focus_outline_width",
                status=Status.PASS if outline_width >= 2 else Status.FAIL,
                message=f"{outline_width}px (required >= 2px)",
                value=float(outline_width),
                threshold=2.0,
            )
        )

    def _check_css_utilities(self, result: GateResult) -> None:
        blocks = _parse_css_blocks(self.css_path.read_text())

        focus_block = blocks.get(".focus-ring:focus", {})
        outline_px = _extract_px(focus_block.get("outline"))
        outline_offset_px = _extract_px(focus_block.get("outline-offset"))
        link_block = blocks.get(".link", {})
        text_decoration = link_block.get("text-decoration", "")

        result.checks.append(
            CheckResult(
                name="css/focus_ring_rule",
                status=Status.PASS
                if outline_px is not None and outline_px >= 2
                else Status.FAIL,
                message=(
                    f"outline {outline_px:g}px in .focus-ring:focus"
                    if outline_px is not None
                    else "Missing usable outline in .focus-ring:focus"
                ),
                value=outline_px,
                threshold=2.0,
            )
        )
        result.checks.append(
            CheckResult(
                name="css/focus_ring_offset",
                status=Status.PASS
                if outline_offset_px is not None and outline_offset_px >= 2
                else Status.WARN,
                message=(
                    f"outline-offset {outline_offset_px:g}px"
                    if outline_offset_px is not None
                    else "Missing outline-offset in .focus-ring:focus"
                ),
                value=outline_offset_px,
                threshold=2.0,
            )
        )
        result.checks.append(
            CheckResult(
                name="css/link_not_color_only",
                status=Status.PASS if "underline" in text_decoration else Status.FAIL,
                message=(
                    f"text-decoration: {text_decoration}"
                    if text_decoration
                    else "Links are missing explicit underline styling"
                ),
            )
        )

        for selector in BUTTON_SELECTORS:
            block = blocks.get(selector, {})
            min_height_px = _extract_px(block.get("min-height"))
            min_width_px = _extract_px(block.get("min-width"))
            result.checks.append(
                CheckResult(
                    name=f"css/{selector[1:]}_target_height",
                    status=(
                        Status.PASS
                        if min_height_px is not None and min_height_px >= 44
                        else Status.FAIL
                    ),
                    message=(
                        f"min-height {min_height_px:g}px"
                        if min_height_px is not None
                        else f"Missing min-height on {selector}"
                    ),
                    value=min_height_px,
                    threshold=44.0,
                )
            )
            result.checks.append(
                CheckResult(
                    name=f"css/{selector[1:]}_target_width",
                    status=(
                        Status.PASS
                        if min_width_px is not None and min_width_px >= 44
                        else Status.FAIL
                    ),
                    message=(
                        f"min-width {min_width_px:g}px"
                        if min_width_px is not None
                        else f"Missing min-width on {selector}"
                    ),
                    value=min_width_px,
                    threshold=44.0,
                )
            )

    def _check_html_examples(self, result: GateResult) -> None:
        for html_path in self.html_paths:
            text = html_path.read_text()
            inline_css = _extract_style_text(text)
            html_blocks = _parse_css_blocks(inline_css)
            duplicate_class_count = len(CLASS_DUP_RE.findall(text))
            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/duplicate_class_attributes",
                    status=Status.PASS if duplicate_class_count == 0 else Status.FAIL,
                    message=(
                        "No duplicate class attributes found"
                        if duplicate_class_count == 0
                        else f"Found {duplicate_class_count} tag(s) with duplicate class attributes"
                    ),
                    value=float(duplicate_class_count),
                    threshold=0.0,
                )
            )

            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/viewport_meta",
                    status=Status.PASS if VIEWPORT_RE.search(text) else Status.FAIL,
                    message=(
                        "Viewport meta tag declared"
                        if VIEWPORT_RE.search(text)
                        else "Missing viewport meta tag"
                    ),
                )
            )

            focusable_violations = 0
            for match in TABINDEX_RE.finditer(text):
                attrs = match.group("attrs") + match.group("rest")
                class_match = CLASS_ATTR_RE.search(attrs)
                class_value = class_match.group(1) if class_match else ""
                classes = set(class_value.split())
                if "focus-ring" not in classes:
                    focusable_violations += 1

            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/focusable_custom_elements",
                    status=Status.PASS if focusable_violations == 0 else Status.FAIL,
                    message=(
                        'All tabindex="0" elements expose focus-ring class'
                        if focusable_violations == 0
                        else f"{focusable_violations} focusable custom element(s) missing focus-ring class"
                    ),
                    value=float(focusable_violations),
                    threshold=0.0,
                )
            )

            has_media_query = "@media" in inline_css
            has_adaptive_grid = (
                "repeat(auto-fit" in inline_css or "repeat(auto-fill" in inline_css
            )
            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/responsive_layout_markers",
                    status=(
                        Status.PASS
                        if has_media_query or has_adaptive_grid
                        else Status.WARN
                    ),
                    message=(
                        "Responsive adaptation markers found"
                        if has_media_query or has_adaptive_grid
                        else "No media-query or adaptive-grid marker found in inline CSS"
                    ),
                )
            )

            main_block = html_blocks.get("main", {})
            if "<main" not in text:
                main_status = Status.PASS
                main_message = "No main layout scope declared on this page"
            else:
                main_display = main_block.get("display", "")
                main_grid = main_block.get("grid-template-columns", "")
                has_main_layout = "grid" in main_display or "flex" in main_display
                has_adaptive_main = (
                    "repeat(auto-fit" in main_grid
                    or "repeat(auto-fill" in main_grid
                    or has_media_query
                )
                if has_main_layout and has_adaptive_main:
                    main_status = Status.PASS
                    main_message = "Main layout declares adaptive grid/flex behavior"
                elif has_main_layout:
                    main_status = Status.WARN
                    main_message = (
                        "Main layout exists but lacks an explicit adaptive marker"
                    )
                else:
                    main_status = Status.FAIL
                    main_message = (
                        "Main element lacks explicit grid/flex layout declarations"
                    )
            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/main_layout_responsiveness",
                    status=main_status,
                    message=main_message,
                )
            )

            if "<main" not in text:
                mobile_fit_status = Status.PASS
                mobile_fit_message = "No main layout scope declared on this page"
                mobile_fit_value = None
                mobile_fit_threshold = None
            else:
                main_padding_x = _horizontal_padding(main_block.get("padding"))
                main_grid_min = _grid_min_width(
                    main_block.get("grid-template-columns", "")
                )
                available_width = NARROW_VIEWPORT_WIDTH - main_padding_x
                if main_grid_min is None:
                    mobile_fit_status = Status.WARN
                    mobile_fit_message = (
                        "Main grid lacks a parseable minimum column width"
                    )
                    mobile_fit_value = None
                    mobile_fit_threshold = available_width
                elif main_grid_min == 0.0:
                    mobile_fit_status = Status.PASS
                    mobile_fit_message = (
                        "Main grid clamps minimum column width to container width"
                    )
                    mobile_fit_value = 0.0
                    mobile_fit_threshold = available_width
                elif main_grid_min <= available_width:
                    mobile_fit_status = Status.PASS
                    mobile_fit_message = (
                        f"Main grid minimum {main_grid_min:g}px fits within a {NARROW_VIEWPORT_WIDTH:g}px viewport "
                        f"after {main_padding_x:g}px horizontal padding"
                    )
                    mobile_fit_value = main_grid_min
                    mobile_fit_threshold = available_width
                else:
                    mobile_fit_status = Status.FAIL
                    mobile_fit_message = (
                        f"Main grid minimum {main_grid_min:g}px exceeds the {available_width:g}px content width "
                        f"available inside a {NARROW_VIEWPORT_WIDTH:g}px viewport"
                    )
                    mobile_fit_value = main_grid_min
                    mobile_fit_threshold = available_width
            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/main_mobile_column_fit",
                    status=mobile_fit_status,
                    message=mobile_fit_message,
                    value=mobile_fit_value,
                    threshold=mobile_fit_threshold,
                )
            )

            swatch_block = html_blocks.get(".swatch-grid", {})
            swatch_grid = swatch_block.get("grid-template-columns", "")
            swatch_repeat_match = REPEAT_COUNT_RE.search(swatch_grid)
            swatch_has_media_override = SWATCH_MEDIA_RE.search(inline_css) is not None
            if ".swatch-grid" not in text:
                swatch_status = Status.PASS
                swatch_message = "No swatch-grid surface declared on this page"
            elif "auto-fit" in swatch_grid or "auto-fill" in swatch_grid:
                swatch_status = Status.PASS
                swatch_message = "Swatch grid uses adaptive auto-fit/auto-fill columns"
            elif swatch_has_media_override:
                swatch_status = Status.WARN
                swatch_message = "Swatch grid relies on media-query adaptation rather than adaptive columns"
            elif swatch_repeat_match and int(swatch_repeat_match.group("count")) >= 4:
                swatch_status = Status.FAIL
                swatch_message = "Swatch grid uses four or more fixed columns without adaptive fallback"
            else:
                swatch_status = Status.WARN
                swatch_message = "Swatch grid lacks a clear adaptive column strategy"
            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/swatch_grid_adaptation",
                    status=swatch_status,
                    message=swatch_message,
                )
            )

            wrap_selectors_found = 0
            wrap_selectors_ok = 0
            for selector in WRAP_SELECTORS:
                if selector not in text:
                    continue
                wrap_selectors_found += 1
                block = html_blocks.get(selector, {})
                display_value = block.get("display", "")
                wrap_value = block.get("flex-wrap", "")
                if "flex" in display_value and "wrap" in wrap_value:
                    wrap_selectors_ok += 1
            if wrap_selectors_found == 0:
                wrap_status = Status.WARN
                wrap_message = "No known wrapping control-row selectors found"
            elif wrap_selectors_ok == wrap_selectors_found:
                wrap_status = Status.PASS
                wrap_message = f"All {wrap_selectors_found} detected control row(s) declare flex-wrap"
            else:
                wrap_status = Status.FAIL
                wrap_message = f"{wrap_selectors_ok}/{wrap_selectors_found} detected control row(s) declare flex-wrap"
            result.checks.append(
                CheckResult(
                    name=f"{html_path.name}/wrapping_control_rows",
                    status=wrap_status,
                    message=wrap_message,
                    value=float(wrap_selectors_ok),
                    threshold=float(wrap_selectors_found)
                    if wrap_selectors_found
                    else None,
                )
            )

    def validate(self, **kwargs) -> GateResult:
        result = self._make_result()
        self._check_spacing_tokens(result)
        self._check_css_utilities(result)
        self._check_html_examples(result)
        return result


if __name__ == "__main__":
    gate = SpatialGate()
    gate_result = gate.validate()
    print(gate_result)
    raise SystemExit(0 if gate_result.status != Status.FAIL else 1)
