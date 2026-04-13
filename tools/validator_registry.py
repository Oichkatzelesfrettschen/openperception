"""
Registry of declared validator gates and broader spec/runtime gap areas.

WHY: The repository has a strong declared validator and accessibility system,
but only a subset is executable today. This module provides one authoritative
place to describe:

- which validator gates are implemented,
- which remain spec-only,
- and which larger system areas are still missing runtime support.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TOKENS_JSON = REPO_ROOT / "tokens" / "color-tokens.json"


@dataclass(frozen=True)
class GateSpec:
    gate_id: str
    gate_name: str
    severity: str
    status: str
    description: str
    module_path: str | None = None
    factory: Callable[[Path | None], object] | None = None
    required_input: str | None = None


@dataclass(frozen=True)
class RuntimeArea:
    name: str
    status: str
    declared_sources: tuple[str, ...]
    runtime_artifacts: tuple[str, ...]
    lacuna: str
    next_step: str


def _contrast_factory(tokens_path: Path | None = None) -> object:
    from validators.contrast import ContrastGate

    return ContrastGate(tokens_path)


def _cvd_factory(tokens_path: Path | None = None) -> object:
    from validators.cvd import CVDGate

    return CVDGate(tokens_path)


def _spatial_factory(tokens_path: Path | None = None) -> object:
    from validators.spatial import SpatialGate

    del tokens_path
    return SpatialGate()


def _seizure_factory(manifest_path: Path | None = None) -> object:
    from validators.seizure import SeizureGate

    if manifest_path is None:
        raise ValueError("Seizure gate requires a manifest path")
    return SeizureGate(manifest_path)


def _temporal_depth_factory(tokens_path: Path | None = None) -> object:
    from validators.temporal_depth import TemporalDepthGate

    del tokens_path
    return TemporalDepthGate()


def _cognitive_factory(tokens_path: Path | None = None) -> object:
    from validators.cognitive import CognitiveGate

    del tokens_path
    return CognitiveGate()


def _achromat_factory(tokens_path: Path | None = None) -> object:
    from validators.achromat import AchromatGate

    return AchromatGate(tokens_path)


def get_gate_specs() -> list[GateSpec]:
    return [
        GateSpec(
            gate_id="GATE-001",
            gate_name="SEIZURE",
            severity="BLOCKING",
            status="partial",
            description="Frame-sequence flash, red-saturation, area, and cumulative-exposure checks.",
            module_path="tools/validators/seizure.py",
            factory=_seizure_factory,
            required_input="seizure_manifest",
        ),
        GateSpec(
            gate_id="GATE-002",
            gate_name="CONTRAST",
            severity="BLOCKING",
            status="implemented",
            description="WCAG contrast validation for token pairs.",
            module_path="tools/validators/contrast.py",
            factory=_contrast_factory,
        ),
        GateSpec(
            gate_id="GATE-003",
            gate_name="CVD",
            severity="WARNING",
            status="implemented",
            description="Color separation validation for CVD-sensitive token roles.",
            module_path="tools/validators/cvd.py",
            factory=_cvd_factory,
        ),
        GateSpec(
            gate_id="GATE-004",
            gate_name="SPATIAL",
            severity="WARNING",
            status="partial",
            description="Static token/CSS/example checks for touch targets, focus affordances, viewport/meta responsiveness, main-layout/mobile-column responsiveness, swatch-grid adaptation, and wrapping control rows.",
            module_path="tools/validators/spatial.py",
            factory=_spatial_factory,
        ),
        GateSpec(
            gate_id="GATE-005",
            gate_name="TEMPORAL_DEPTH",
            severity="WARNING",
            status="partial",
            description="First-pass motion-token and display-profile temporal policy validation.",
            module_path="tools/validators/temporal_depth.py",
            factory=_temporal_depth_factory,
        ),
        GateSpec(
            gate_id="GATE-006",
            gate_name="COGNITIVE",
            severity="WARNING",
            status="partial",
            description="First-pass navigation, summary-view, density-budget, visible-control burden, panel/metric-group, HUD-complexity, notification-density, and reading-level checks.",
            module_path="tools/validators/cognitive.py",
            factory=_cognitive_factory,
        ),
        GateSpec(
            gate_id="GATE-007",
            gate_name="ACHROMAT",
            severity="WARNING",
            status="implemented",
            description=(
                "Luminance contrast for semantic role foregrounds in the mono token variant. "
                "Uses BT.709 relative luminance consistent with GATE-002 CONTRAST. "
                "Threshold: 4.5:1 PASS (WCAG AA normal text), 3.0:1 WARN (large text/non-text UI)."
            ),
            module_path="tools/validators/achromat.py",
            factory=_achromat_factory,
        ),
    ]


def implemented_gate_specs() -> list[GateSpec]:
    return [
        spec for spec in get_gate_specs() if spec.status in {"implemented", "partial"}
    ]


def spec_only_gate_specs() -> list[GateSpec]:
    return [spec for spec in get_gate_specs() if spec.status == "spec_only"]


def get_runtime_areas() -> list[RuntimeArea]:
    return [
        RuntimeArea(
            name="Chromatic validation",
            status="partial",
            declared_sources=(
                "specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md",
                "specs/VALIDATORS_FRAMEWORK.md",
                "specs/tokens/semantic/color-roles.json",
            ),
            runtime_artifacts=(
                "tools/validators/contrast.py",
                "tools/validators/cvd.py",
                "tools/semantic_tokens.py",
                "tokens/semantic-role-tokens.json",
                "tools/contrast_check.py",
                "tools/separation_check.py",
                "tools/experimental_palette_report.py",
            ),
            lacuna=(
                "Contrast, brand-pair separation, expanded first-class semantic-role pairs, and "
                "first-pass semantic/viz redundancy checks are now enforced, but the full declared "
                "semantic universe and richer CVD simulation thresholds are not yet wired into "
                "runtime validation."
            ),
            next_step="Expand first-class semantic token validation to the remaining declared roles and richer CVD thresholds.",
        ),
        RuntimeArea(
            name="Evidence and claims",
            status="partial",
            declared_sources=(
                "specs/EVIDENCE_MATRIX.md",
                "specs/REFERENCES_BIBLIOGRAPHY.md",
            ),
            runtime_artifacts=(
                "specs/CLAIMS_RUNTIME_REGISTRY.json",
                "tools/claims_registry.py",
                "tools/claims_coverage_report.py",
                "tools/check_claims_registry.py",
            ),
            lacuna=(
                "A seeded subset of claims is now machine-linked to validators, tests, "
                "docs, and runtime artifacts, but coverage is still narrow and needs "
                "integrity checks plus broader evidence-matrix expansion."
            ),
            next_step="Expand registry coverage and enforce it with integrity checks.",
        ),
        RuntimeArea(
            name="Axis conflict resolution",
            status="partial",
            declared_sources=("specs/AXIS_OVERLAP_MAP.md",),
            runtime_artifacts=(
                "specs/tokens/profiles/axis-profiles.json",
                "tools/profile_resolver.py",
                "tools/tests/test_profile_resolver.py",
            ),
            lacuna=(
                "A first machine-readable profile manifest and composition helper now exist, "
                "including restrictive cap composition and conflict surfacing for chromatic, "
                "luminance, temporal, spatial, and cognitive axes, but they are not yet "
                "integrated into the shared validator CLI or downstream renderers."
            ),
            next_step="Integrate profile composition with validators and render-cap consumers.",
        ),
        RuntimeArea(
            name="Scaling and display adaptation",
            status="partial",
            declared_sources=(
                "specs/SCALING_MATHEMATICS.md",
                "specs/DISPLAY_ADAPTATION_LAYER.md",
                "specs/DPI_TRANSITION_CONTRACT.md",
                "specs/SCALING_AUTHORITY_MATRIX.md",
                "specs/QUANTIZATION_POLICY.md",
            ),
            runtime_artifacts=(
                "tools/scaling.py",
                "tools/tests/test_scaling.py",
                "specs/tokens/units/logical-pixels.json",
            ),
            lacuna=(
                "A first shared scaling helper now implements effective-scale math, "
                "modular size steps, snap-class quantization, hysteresis, and touch-target "
                "floor enforcement, but display detection, DPI transition handling, and "
                "consumer integration remain unimplemented."
            ),
            next_step="Integrate the scaling helper with validators, profile composition, and renderer/runtime consumers.",
        ),
        RuntimeArea(
            name="Reflow and layout",
            status="partial",
            declared_sources=(
                "specs/LAYOUT_SYSTEM.md",
                "specs/REFLOW_EXCEPTIONS_2D.md",
            ),
            runtime_artifacts=(
                "tools/validators/spatial.py",
                "tools/rendered_spatial_check.py",
                "specs/tokens/layout/spacing.json",
                "tokens/color-tokens.css",
                "examples/ui/variant-toggle.html",
                "examples/ui/palette-compare.html",
            ),
            lacuna=(
                "A first static spatial validator now checks token minima, button target "
                "minima, focus-ring CSS, link underlining, focusable-example hygiene, "
                "viewport/meta responsiveness, main-layout responsiveness, narrow-viewport "
                "column fit, swatch-grid adaptation, and wrapping control rows, and a "
                "separate rendered audit now checks actual overflow and first focus-visibility "
                "risk in Chromium, but it still does not perform exact focus-ring pixel "
                "measurement, target measurement, or reflow-at-scale audits."
            ),
            next_step="Expand the rendered spatial audit into exact focus clipping, target measurement, and deeper reflow checks.",
        ),
        RuntimeArea(
            name="Typography",
            status="partial",
            declared_sources=(
                "specs/TYPOGRAPHY_SYSTEM.md",
                "specs/tokens/typography/font-contract.json",
                "specs/tokens/typography/font-families.json",
            ),
            runtime_artifacts=(
                "tools/validators/typography.py",
                "tools/tests/test_typography.py",
                "examples/ui/variant-toggle.html",
                "examples/ui/palette-compare.html",
            ),
            lacuna=(
                "A first typography verifier now checks font-contract coverage, required "
                "weights, x-height metadata, body font size, body line height, line-length "
                "ceilings, and uppercase tracking on example surfaces, but disambiguation "
                "rendering tests and cross-output enforcement remain unimplemented."
            ),
            next_step="Expand typography verification to rendering-based disambiguation and integrate it into the shared validator surface.",
        ),
        RuntimeArea(
            name="Temporal safety",
            status="partial",
            declared_sources=(
                "specs/VALIDATORS_FRAMEWORK.md",
                "specs/tokens/temporal/motion.json",
                "specs/TEST_MATRIX.md",
            ),
            runtime_artifacts=(
                "tools/validators/seizure.py",
                "tools/validators/temporal_depth.py",
                "tools/tests/test_temporal_depth.py",
                "specs/tokens/temporal/motion.json",
                "tools/PEAT_1.6_Seizure_Analysis.zip",
            ),
            lacuna=(
                "A first frame-sequence seizure gate and a first motion-token/profile policy "
                "gate now exist, but pattern oscillation, video decoding, rendered motion-path "
                "analysis, and richer hardware/display interactions remain unimplemented."
            ),
            next_step="Expand temporal validation into pattern oscillation, rendered motion-path analysis, and direct video analysis.",
        ),
        RuntimeArea(
            name="Cognitive load and navigation",
            status="partial",
            declared_sources=(
                "specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md",
                "specs/VALIDATORS_FRAMEWORK.md",
                "specs/LAYOUT_SYSTEM.md",
            ),
            runtime_artifacts=(
                "tools/validators/cognitive.py",
                "tools/rendered_cognitive_check.py",
                "tools/tests/test_cognitive.py",
                "specs/tokens/profiles/axis-profiles.json",
                "examples/ui/variant-toggle.html",
                "examples/ui/palette-compare.html",
            ),
            lacuna=(
                "A first cognitive validator now checks nav scope size, nesting depth, "
                "progressive disclosure markers, notification density, density-region "
                "budgets, primary action density, visible-control burden, declared panel "
                "and metric-group burden, HUD complexity declarations, and approximate "
                "reading level on repo-owned HTML, and a separate rendered audit now "
                "checks first-screen visible burden in Chromium, but it does not yet "
                "perform user-flow analysis, task-memory checks, or deeper rendered HUD "
                "density measurement."
            ),
            next_step="Expand the rendered cognitive audit into deeper viewport-state and task-flow validation.",
        ),
        RuntimeArea(
            name="Unified validator entrypoint",
            status="partial",
            declared_sources=("specs/VALIDATORS_FRAMEWORK.md",),
            runtime_artifacts=("tools/validate.py",),
            lacuna=(
                "A unified CLI can now execute implemented gates and summarize auxiliary "
                "runtime surfaces, but several gate families are still partial and one "
                "partial gate requires explicit seizure manifests."
            ),
            next_step="Keep expanding partial gates and integrate them more deeply with renderer/runtime consumers.",
        ),
    ]
