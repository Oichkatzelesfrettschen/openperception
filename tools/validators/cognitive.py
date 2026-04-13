"""
First executable subset of the cognitive/navigation validator.

WHY: specs/VALIDATORS_FRAMEWORK.md declares GATE-006 for navigation structure,
progressive disclosure, reading complexity, and notification density. This
module starts with the smallest honest runtime slice over repo-owned HTML
surfaces plus the machine-readable axis profile manifest.
"""

# ruff: noqa: I001
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
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
DEFAULT_PROFILE_MANIFEST = (
    REPO_ROOT / "specs" / "tokens" / "profiles" / "axis-profiles.json"
)
DEFAULT_HTML_PATHS = (
    REPO_ROOT / "examples" / "ui" / "variant-toggle.html",
    REPO_ROOT / "examples" / "ui" / "palette-compare.html",
)
ALLOWED_HUD_COMPLEXITY = {"full", "simple", "minimal"}
ALLOWED_PROFILE_COGNITIVE = {"full HUD", "simple HUD", "minimal HUD"}
IGNORED_TEXT_TAGS = {
    "script",
    "style",
    "svg",
    "defs",
    "filter",
    "fecolormatrix",
    "template",
    "option",
}
WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
SENTENCE_RE = re.compile(r"[.!?]+")
VOWEL_GROUP_RE = re.compile(r"[aeiouy]+", re.I)
HUD_REGION_THRESHOLDS = {
    "minimal": (4, 5),
    "simple": (5, 6),
    "full": (7, 9),
}
HUD_ACTION_THRESHOLDS = {
    "minimal": (2, 3),
    "simple": (3, 4),
    "full": (4, 6),
}
HUD_VISIBLE_CONTROL_THRESHOLDS = {
    "minimal": (6, 8),
    "simple": (8, 10),
    "full": (18, 22),
}
HUD_PANEL_THRESHOLDS = {
    "minimal": (2, 3),
    "simple": (3, 4),
    "full": (12, 15),
}
HUD_METRIC_THRESHOLDS = {
    "minimal": (0, 1),
    "simple": (1, 2),
    "full": (3, 4),
}
HUD_BURDEN_THRESHOLDS = {
    "minimal": (7, 8),
    "simple": (9, 10),
    "full": (12, 14),
}


def _bool_attr(value: str | None) -> bool:
    return value is not None and value.lower() in {"", "true", "1", "yes"}


def _approximate_syllables(word: str) -> int:
    word = word.lower()
    groups = VOWEL_GROUP_RE.findall(word)
    count = len(groups)
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def approximate_grade_level(text: str) -> float:
    words = WORD_RE.findall(text)
    if not words:
        return 0.0
    sentences = max(len(SENTENCE_RE.findall(text)), 1)
    syllables = sum(_approximate_syllables(word) for word in words)
    word_count = len(words)
    return 0.39 * (word_count / sentences) + 11.8 * (syllables / word_count) - 15.59


class CognitiveHTMLParser(HTMLParser):
    """Parse just enough HTML structure for the first cognitive gate subset."""

    def __init__(self) -> None:
        super().__init__()
        self._ignored_depth = 0
        self._nav_stack: list[dict[str, int | str]] = []
        self.nav_contexts: list[dict[str, int | str]] = []
        self.notification_count = 0
        self.has_summary_view = False
        self.hud_modes: list[str] = []
        self.complex_content_marked = False
        self.text_chunks: list[str] = []
        self.region_count = 0
        self.primary_action_count = 0
        self.visible_control_count = 0
        self.panel_group_count = 0
        self.metric_group_count = 0
        self._primary_action_scopes: list[str] = []

    def handle_starttag(
        self, tag: str, attrs_list: list[tuple[str, str | None]]
    ) -> None:
        attrs = dict(attrs_list)
        panel_groups = attrs.get("data-panel-groups")
        if panel_groups and panel_groups.isdigit():
            self.panel_group_count += int(panel_groups)
        metric_groups = attrs.get("data-metric-groups")
        if metric_groups and metric_groups.isdigit():
            self.metric_group_count += int(metric_groups)
        if tag in IGNORED_TEXT_TAGS:
            self._ignored_depth += 1
            return

        hud_mode = attrs.get("data-hud-complexity")
        if hud_mode:
            self.hud_modes.append(hud_mode)
        if _bool_attr(attrs.get("data-cognitive-complex")):
            self.complex_content_marked = True
        if "data-density-region" in attrs:
            self.region_count += 1
        if tag == "details" or _bool_attr(attrs.get("data-summary-view")):
            self.has_summary_view = True
        if (
            attrs.get("role") in {"alert", "status"}
            or "aria-live" in attrs
            or "data-notification" in attrs
        ):
            self.notification_count += 1
        if "data-primary-actions" in attrs:
            self._primary_action_scopes.append(tag)
        if self._primary_action_scopes and tag in {
            "button",
            "select",
            "input",
            "textarea",
        }:
            self.primary_action_count += 1
        if tag in {"a", "button", "summary", "select", "textarea"}:
            self.visible_control_count += 1
        if tag == "input" and attrs.get("type", "text").lower() != "hidden":
            self.visible_control_count += 1

        is_nav_scope = (
            tag == "nav"
            or attrs.get("role") == "navigation"
            or "data-nav-scope" in attrs
        )
        if is_nav_scope:
            self._nav_stack.append(
                {
                    "tag": tag,
                    "item_count": 0,
                    "list_depth": 0,
                    "max_depth": 1,
                }
            )

        if self._nav_stack:
            context = self._nav_stack[-1]
            if tag in {"a", "button", "summary", "select"}:
                context["item_count"] = int(context["item_count"]) + 1
            if tag in {"ul", "ol"}:
                next_depth = int(context["list_depth"]) + 1
                context["list_depth"] = next_depth
                context["max_depth"] = max(int(context["max_depth"]), 1 + next_depth)

    def handle_endtag(self, tag: str) -> None:
        if tag in IGNORED_TEXT_TAGS:
            self._ignored_depth = max(self._ignored_depth - 1, 0)
            return
        if self._nav_stack:
            context = self._nav_stack[-1]
            if tag in {"ul", "ol"} and int(context["list_depth"]) > 0:
                context["list_depth"] = int(context["list_depth"]) - 1
            if tag == context["tag"]:
                self.nav_contexts.append(self._nav_stack.pop())
        if self._primary_action_scopes and tag == self._primary_action_scopes[-1]:
            self._primary_action_scopes.pop()

    def handle_startendtag(
        self, tag: str, attrs_list: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs_list)
        if tag in IGNORED_TEXT_TAGS and self._ignored_depth:
            self._ignored_depth -= 1
        if (
            self._primary_action_scopes
            and dict(attrs_list).get("data-primary-actions") is not None
        ):
            self._primary_action_scopes.pop()

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        text = " ".join(data.split())
        if text:
            self.text_chunks.append(text)


class CognitiveGate(ValidatorGate):
    """GATE-006: first executable subset of cognitive/navigation validation."""

    gate_id = "GATE-006"
    gate_name = "COGNITIVE"
    severity = Severity.WARNING

    def __init__(
        self,
        profile_manifest_path: Path | None = None,
        html_paths: tuple[Path, ...] | None = None,
    ):
        self.profile_manifest_path = profile_manifest_path or DEFAULT_PROFILE_MANIFEST
        self.html_paths = html_paths or DEFAULT_HTML_PATHS

    def _check_profiles(self, result: GateResult) -> None:
        payload = json.loads(self.profile_manifest_path.read_text())
        profiles = payload.get("profiles", {})
        cognitive_values = [
            profile.get("axes", {}).get("cognitive")
            for profile in profiles.values()
            if "axes" in profile
        ]
        invalid = [
            value
            for value in cognitive_values
            if value not in ALLOWED_PROFILE_COGNITIVE
        ]
        result.checks.append(
            CheckResult(
                name="profiles/cognitive_values_declared",
                status=Status.PASS if not invalid else Status.FAIL,
                message=(
                    "All profile cognitive modes use allowed HUD labels"
                    if not invalid
                    else "Invalid cognitive profile modes: "
                    + ", ".join(sorted(invalid))
                ),
                value=float(len(cognitive_values)),
                threshold=float(len(cognitive_values)),
            )
        )

        supports_reduced_density = any(
            value == "minimal HUD" for value in cognitive_values
        )
        result.checks.append(
            CheckResult(
                name="profiles/reduced_density_mode_available",
                status=Status.PASS if supports_reduced_density else Status.FAIL,
                message=(
                    "At least one profile exposes a minimal-HUD cognitive mode"
                    if supports_reduced_density
                    else "Profile manifest lacks a minimal-HUD cognitive mode"
                ),
            )
        )

    def _check_html_surface(self, html_path: Path, result: GateResult) -> None:
        parser = CognitiveHTMLParser()
        parser.feed(html_path.read_text())
        nav_count = max(
            (int(item["item_count"]) for item in parser.nav_contexts), default=0
        )
        nav_depth = max(
            (int(item["max_depth"]) for item in parser.nav_contexts), default=0
        )
        hud_modes = parser.hud_modes
        invalid_hud_modes = [
            mode for mode in hud_modes if mode not in ALLOWED_HUD_COMPLEXITY
        ]
        hud_mode = hud_modes[0] if hud_modes and not invalid_hud_modes else None
        grade_level = approximate_grade_level(" ".join(parser.text_chunks))

        nav_status = (
            Status.WARN
            if nav_count == 0
            else Status.PASS
            if nav_count <= 9
            else Status.FAIL
        )
        nav_message = (
            "No navigation scope declared on the page"
            if nav_count == 0
            else f"Maximum navigation scope size is {nav_count} items"
        )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/navigation_item_count",
                status=nav_status,
                message=nav_message,
                value=float(nav_count),
                threshold=9.0,
            )
        )

        depth_status = (
            Status.WARN
            if nav_depth == 0
            else Status.PASS
            if nav_depth <= 3
            else Status.FAIL
        )
        depth_message = (
            "No navigation nesting declared on the page"
            if nav_depth == 0
            else f"Maximum navigation nesting depth is {nav_depth}"
        )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/nesting_depth",
                status=depth_status,
                message=depth_message,
                value=float(nav_depth),
                threshold=3.0,
            )
        )

        summary_required = parser.complex_content_marked
        summary_status = (
            Status.PASS
            if (not summary_required or parser.has_summary_view)
            else Status.FAIL
        )
        summary_message = (
            "Complex content has a summary or details disclosure"
            if summary_status == Status.PASS
            else "Complex content marker present without summary/details disclosure"
        )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/progressive_disclosure",
                status=summary_status,
                message=summary_message,
            )
        )

        if not hud_modes:
            hud_status = Status.WARN
            hud_message = "No data-hud-complexity declaration found"
        elif invalid_hud_modes:
            hud_status = Status.FAIL
            hud_message = "Invalid HUD complexity values: " + ", ".join(
                sorted(invalid_hud_modes)
            )
        else:
            hud_status = Status.PASS
            hud_message = "Declared HUD complexity modes: " + ", ".join(hud_modes)
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/hud_complexity",
                status=hud_status,
                message=hud_message,
            )
        )

        notification_status = (
            Status.PASS if parser.notification_count <= 3 else Status.FAIL
        )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/concurrent_notifications",
                status=notification_status,
                message=f"Page exposes {parser.notification_count} concurrent notification regions",
                value=float(parser.notification_count),
                threshold=3.0,
            )
        )

        if parser.region_count == 0 or hud_mode is None:
            density_region_status = Status.WARN
            density_region_message = "Missing density-region markers or usable HUD mode"
        else:
            pass_threshold, warn_threshold = HUD_REGION_THRESHOLDS[hud_mode]
            if parser.region_count <= pass_threshold:
                density_region_status = Status.PASS
            elif parser.region_count <= warn_threshold:
                density_region_status = Status.WARN
            else:
                density_region_status = Status.FAIL
            density_region_message = (
                f"{parser.region_count} density region(s) for {hud_mode} HUD "
                f"(target <= {pass_threshold}, warn <= {warn_threshold})"
            )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/density_regions",
                status=density_region_status,
                message=density_region_message,
                value=float(parser.region_count),
                threshold=(
                    float(HUD_REGION_THRESHOLDS[hud_mode][0])
                    if hud_mode is not None
                    else None
                ),
            )
        )

        if parser.primary_action_count == 0 or hud_mode is None:
            action_density_status = Status.WARN
            action_density_message = "Missing primary-action markers or usable HUD mode"
        else:
            pass_threshold, warn_threshold = HUD_ACTION_THRESHOLDS[hud_mode]
            if parser.primary_action_count <= pass_threshold:
                action_density_status = Status.PASS
            elif parser.primary_action_count <= warn_threshold:
                action_density_status = Status.WARN
            else:
                action_density_status = Status.FAIL
            action_density_message = (
                f"{parser.primary_action_count} primary action control(s) for {hud_mode} HUD "
                f"(target <= {pass_threshold}, warn <= {warn_threshold})"
            )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/primary_action_density",
                status=action_density_status,
                message=action_density_message,
                value=float(parser.primary_action_count),
                threshold=(
                    float(HUD_ACTION_THRESHOLDS[hud_mode][0])
                    if hud_mode is not None
                    else None
                ),
            )
        )

        if hud_mode is None:
            visible_control_status = Status.WARN
            visible_control_message = (
                "Missing usable HUD mode for visible-control burden"
            )
        else:
            pass_threshold, warn_threshold = HUD_VISIBLE_CONTROL_THRESHOLDS[hud_mode]
            if parser.visible_control_count <= pass_threshold:
                visible_control_status = Status.PASS
            elif parser.visible_control_count <= warn_threshold:
                visible_control_status = Status.WARN
            else:
                visible_control_status = Status.FAIL
            visible_control_message = (
                f"{parser.visible_control_count} visible control(s) for {hud_mode} HUD "
                f"(target <= {pass_threshold}, warn <= {warn_threshold})"
            )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/visible_control_burden",
                status=visible_control_status,
                message=visible_control_message,
                value=float(parser.visible_control_count),
                threshold=(
                    float(HUD_VISIBLE_CONTROL_THRESHOLDS[hud_mode][0])
                    if hud_mode is not None
                    else None
                ),
            )
        )

        if hud_mode is None:
            panel_status = Status.WARN
            panel_message = "Missing usable HUD mode for declared panel-group density"
        else:
            pass_threshold, warn_threshold = HUD_PANEL_THRESHOLDS[hud_mode]
            if parser.panel_group_count <= pass_threshold:
                panel_status = Status.PASS
            elif parser.panel_group_count <= warn_threshold:
                panel_status = Status.WARN
            else:
                panel_status = Status.FAIL
            panel_message = (
                f"{parser.panel_group_count} declared panel group(s) for {hud_mode} HUD "
                f"(target <= {pass_threshold}, warn <= {warn_threshold})"
            )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/panel_group_density",
                status=panel_status,
                message=panel_message,
                value=float(parser.panel_group_count),
                threshold=(
                    float(HUD_PANEL_THRESHOLDS[hud_mode][0])
                    if hud_mode is not None
                    else None
                ),
            )
        )

        if hud_mode is None:
            metric_status = Status.WARN
            metric_message = "Missing usable HUD mode for declared metric-group density"
        else:
            pass_threshold, warn_threshold = HUD_METRIC_THRESHOLDS[hud_mode]
            if parser.metric_group_count <= pass_threshold:
                metric_status = Status.PASS
            elif parser.metric_group_count <= warn_threshold:
                metric_status = Status.WARN
            else:
                metric_status = Status.FAIL
            metric_message = (
                f"{parser.metric_group_count} declared metric group(s) for {hud_mode} HUD "
                f"(target <= {pass_threshold}, warn <= {warn_threshold})"
            )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/metric_group_density",
                status=metric_status,
                message=metric_message,
                value=float(parser.metric_group_count),
                threshold=(
                    float(HUD_METRIC_THRESHOLDS[hud_mode][0])
                    if hud_mode is not None
                    else None
                ),
            )
        )

        density_burden = (
            parser.region_count
            + parser.primary_action_count
            + parser.notification_count
        )
        if hud_mode is None:
            burden_status = Status.WARN
            burden_message = "Missing usable HUD mode for combined density budget"
        else:
            pass_threshold, warn_threshold = HUD_BURDEN_THRESHOLDS[hud_mode]
            if density_burden <= pass_threshold:
                burden_status = Status.PASS
            elif density_burden <= warn_threshold:
                burden_status = Status.WARN
            else:
                burden_status = Status.FAIL
            burden_message = (
                f"Combined burden {density_burden} for {hud_mode} HUD "
                f"(regions + primary actions + notifications)"
            )
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/combined_density_burden",
                status=burden_status,
                message=burden_message,
                value=float(density_burden),
                threshold=(
                    float(HUD_BURDEN_THRESHOLDS[hud_mode][0])
                    if hud_mode is not None
                    else None
                ),
            )
        )

        if grade_level <= 9.0:
            reading_status = Status.PASS
        elif grade_level <= 13.5:
            reading_status = Status.WARN
        else:
            reading_status = Status.FAIL
        result.checks.append(
            CheckResult(
                name=f"{html_path.name}/reading_level",
                status=reading_status,
                message=f"Approximate reading grade is {grade_level:.1f}",
                value=grade_level,
                threshold=9.0,
            )
        )

    def validate(self, **kwargs) -> GateResult:
        del kwargs
        result = self._make_result()
        self._check_profiles(result)
        for html_path in self.html_paths:
            self._check_html_surface(html_path, result)
        return result


if __name__ == "__main__":
    gate = CognitiveGate()
    result = gate.validate()
    print(result)
    raise SystemExit(0 if result.status != Status.FAIL else 1)
