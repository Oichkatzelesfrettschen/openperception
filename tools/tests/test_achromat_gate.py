"""Unit tests for GATE-007 AchromatGate (tools/validators/achromat.py)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from validators.achromat import AchromatGate
from validators.base import Status


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_tokens(mono_brand: dict, mono_viz_categorical: list | None = None) -> dict:
    """Build a minimal color-tokens.json payload with only the mono variant."""
    categorical = mono_viz_categorical or ["#374151", "#6B7280", "#6B7280", "#374151"]
    return {
        "default": {
            "gray": {"900": "#111827", "0": "#FFFFFF"},
            "brand": {"primary": "#4F46E5", "surface": "#FFFFFF"},
            "viz": {"categorical": categorical, "markers": [], "dashes": []},
        },
        "mono": {
            "gray": {"900": "#111827", "0": "#FFFFFF"},
            "brand": mono_brand,
            "viz": {
                "categorical": categorical,
                "markers": ["circle", "triangle"],
                "dashes": [[0, 0], [6, 3]],
            },
        },
    }


def _write_tokens(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "color-tokens.json"
    p.write_text(json.dumps(data))
    return p


# ---------------------------------------------------------------------------
# TestAchromatGatePass
# ---------------------------------------------------------------------------

class TestAchromatGatePass:
    """All foreground colors have high contrast against white surface."""

    def test_high_contrast_foregrounds_all_pass(self, tmp_path):
        """Dark-on-white palette: every semantic foreground exceeds 4.5:1."""
        brand = {
            "text":         "#111827",  # ~17.7:1
            "primary":      "#374151",  # ~10.3:1
            "primaryStrong": "#111827", # ~17.7:1
            "accent":       "#374151",  # ~10.3:1
            "accentStrong": "#111827",  # ~17.7:1
            "link":         "#374151",  # ~10.3:1
            "surface":      "#FFFFFF",
        }
        tokens_path = _write_tokens(tmp_path, _make_tokens(brand))
        gate = AchromatGate(tokens_path)
        result = gate.validate()

        fg_checks = [
            c for c in result.checks
            if "on surface" in c.name
        ]
        assert len(fg_checks) == 6
        for check in fg_checks:
            assert check.status == Status.PASS, (
                f"{check.name}: {check.message}"
            )

    def test_gate_id_and_name(self, tmp_path):
        brand = {"text": "#111827", "surface": "#FFFFFF"}
        tokens_path = _write_tokens(tmp_path, _make_tokens(brand))
        gate = AchromatGate(tokens_path)
        result = gate.validate()
        assert result.gate_id == "GATE-007"
        assert result.gate_name == "ACHROMAT"

    def test_status_pass_when_all_fg_pass(self, tmp_path):
        """When all fg checks pass and no categorical collapse, overall status is PASS."""
        brand = {
            "text":         "#111827",
            "primary":      "#111827",
            "primaryStrong": "#111827",
            "accent":       "#374151",
            "accentStrong": "#111827",
            "link":         "#111827",
            "surface":      "#FFFFFF",
        }
        # Categorical with enough contrast between [0] and [1]
        categorical = ["#111827", "#FFFFFF", "#374151", "#6B7280"]
        tokens_path = _write_tokens(
            tmp_path, _make_tokens(brand, categorical)
        )
        gate = AchromatGate(tokens_path)
        result = gate.validate()
        assert result.status == Status.PASS, str(result)


# ---------------------------------------------------------------------------
# TestAchromatGateFail
# ---------------------------------------------------------------------------

class TestAchromatGateFail:
    """Palettes that must trigger FAIL checks."""

    def test_low_contrast_primary_fails(self, tmp_path):
        """brand.primary at gray-300 (#D1D5DB) gives ~1.6:1 on white -- FAIL."""
        brand = {
            "text":         "#111827",
            "primary":      "#D1D5DB",  # ~1.6:1 on white
            "primaryStrong": "#111827",
            "accent":       "#374151",
            "accentStrong": "#111827",
            "link":         "#111827",
            "surface":      "#FFFFFF",
        }
        tokens_path = _write_tokens(tmp_path, _make_tokens(brand))
        gate = AchromatGate(tokens_path)
        result = gate.validate()

        primary_check = next(
            c for c in result.checks if "brand.primary on surface" in c.name
        )
        assert primary_check.status == Status.FAIL
        assert result.status == Status.FAIL

    def test_missing_mono_variant_fails(self, tmp_path):
        """If mono variant is absent, the gate must return FAIL."""
        data = {
            "default": {
                "gray": {"900": "#111827"},
                "brand": {"primary": "#4F46E5", "surface": "#FFFFFF"},
                "viz": {"categorical": [], "markers": [], "dashes": []},
            }
        }
        tokens_path = _write_tokens(tmp_path, data)
        gate = AchromatGate(tokens_path)
        result = gate.validate()
        assert result.status == Status.FAIL


# ---------------------------------------------------------------------------
# TestAchromatGateWarn
# ---------------------------------------------------------------------------

class TestAchromatGateWarn:
    """Borderline palettes that should trigger WARN checks."""

    def test_medium_contrast_primary_warns(self, tmp_path):
        """brand.primary at #888888 gives ~3.5:1 on white -- WARN zone [3.0, 4.5)."""
        brand = {
            "text":         "#111827",
            "primary":      "#888888",  # ~3.5:1 on white -- in WARN zone
            "primaryStrong": "#111827",
            "accent":       "#374151",
            "accentStrong": "#111827",
            "link":         "#111827",
            "surface":      "#FFFFFF",
        }
        tokens_path = _write_tokens(tmp_path, _make_tokens(brand))
        gate = AchromatGate(tokens_path)
        result = gate.validate()

        primary_check = next(
            c for c in result.checks if "brand.primary on surface" in c.name
        )
        assert primary_check.status == Status.WARN

    def test_categorical_collapse_warns(self, tmp_path):
        """When categorical[0] == categorical[1] a WARN is emitted."""
        brand = {
            "text":     "#111827",
            "primary":  "#374151",
            "primaryStrong": "#111827",
            "accent":   "#374151",
            "accentStrong": "#111827",
            "link":     "#374151",
            "surface":  "#FFFFFF",
        }
        categorical = ["#374151", "#374151", "#6B7280", "#D1D5DB"]
        tokens_path = _write_tokens(
            tmp_path, _make_tokens(brand, categorical)
        )
        gate = AchromatGate(tokens_path)
        result = gate.validate()

        collapse_check = next(
            c for c in result.checks if "collapse" in c.name
        )
        assert collapse_check.status == Status.WARN

    def test_missing_token_warns_not_fails(self, tmp_path):
        """A missing optional fg token emits WARN, not FAIL."""
        brand = {
            "text":    "#111827",
            # primary, accent, etc. absent
            "surface": "#FFFFFF",
        }
        tokens_path = _write_tokens(tmp_path, _make_tokens(brand))
        gate = AchromatGate(tokens_path)
        result = gate.validate()

        missing_checks = [
            c for c in result.checks
            if c.status == Status.WARN and "Missing token" in c.message
        ]
        assert len(missing_checks) > 0


# ---------------------------------------------------------------------------
# TestAchromatGateWithRealTokens
# ---------------------------------------------------------------------------

class TestAchromatGateWithRealTokens:
    """Integration test: run against the actual repo tokens."""

    def test_real_tokens_do_not_fail(self):
        """After gen_mono_tokens.py, GATE-007 must not return FAIL."""
        repo_root = Path(__file__).resolve().parents[2]
        tokens_path = repo_root / "tokens" / "color-tokens.json"
        if not tokens_path.exists():
            pytest.skip("color-tokens.json not found")

        gate = AchromatGate(tokens_path)
        result = gate.validate()

        failed = [c for c in result.checks if c.status == Status.FAIL]
        assert not failed, (
            "GATE-007 FAIL checks found:\n"
            + "\n".join(f"  {c.name}: {c.message}" for c in failed)
        )

    def test_real_tokens_primary_contrast_passes(self):
        """brand.primary in the mono variant must pass WCAG AA (4.5:1)."""
        repo_root = Path(__file__).resolve().parents[2]
        tokens_path = repo_root / "tokens" / "color-tokens.json"
        if not tokens_path.exists():
            pytest.skip("color-tokens.json not found")

        gate = AchromatGate(tokens_path)
        result = gate.validate()

        primary_check = next(
            (c for c in result.checks if "brand.primary on surface" in c.name), None
        )
        assert primary_check is not None, "brand.primary check not found"
        assert primary_check.status == Status.PASS, (
            f"brand.primary contrast fails: {primary_check.message}"
        )

    def test_real_tokens_text_contrast_passes(self):
        """brand.text in the mono variant must pass WCAG AA (4.5:1)."""
        repo_root = Path(__file__).resolve().parents[2]
        tokens_path = repo_root / "tokens" / "color-tokens.json"
        if not tokens_path.exists():
            pytest.skip("color-tokens.json not found")

        gate = AchromatGate(tokens_path)
        result = gate.validate()

        text_check = next(
            (c for c in result.checks if "brand.text on surface" in c.name), None
        )
        assert text_check is not None, "brand.text check not found"
        assert text_check.status == Status.PASS, (
            f"brand.text contrast fails: {text_check.message}"
        )
