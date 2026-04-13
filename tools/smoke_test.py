#!/usr/bin/env python3
"""Machine-checkable install smoke tests.

Verifies that the core Python packages, C library build, and
repo tooling are importable and functional after a fresh install.
Run via `make smoke-test` or `python tools/smoke_test.py`.

Exit code 0 means all checks pass.  Exit code 1 means at least one
check failed; each failure is printed to stderr.
"""

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def _check(name: str, ok: bool, detail: str = "") -> bool:
    """Print a PASS/FAIL line and return ok."""
    status = "[PASS]" if ok else "[FAIL]"
    msg = f"{status} {name}"
    if detail:
        msg += f": {detail}"
    print(msg)
    return ok


def check_daltonlens_import() -> bool:
    try:
        import daltonlens  # noqa: F401
        from daltonlens import convert, daltonize, simulate  # noqa: F401

        return _check("daltonlens import", True)
    except ImportError as exc:
        return _check("daltonlens import", False, str(exc))


def check_daltonlens_simulate() -> bool:
    try:
        import numpy as np

        from daltonlens import simulate

        sim = simulate.Simulator_AutoSelect()
        im = np.full((4, 4, 3), 128, dtype=np.uint8)
        out = sim.simulate_cvd(im, simulate.Deficiency.PROTAN, severity=1.0)
        ok = out.shape == (4, 4, 3) and out.dtype == np.uint8
        return _check("daltonlens simulate_cvd (protan, AutoSelect)", ok)
    except Exception as exc:
        return _check("daltonlens simulate_cvd", False, str(exc))


def check_daltonlens_achromat() -> bool:
    try:
        import numpy as np

        from daltonlens import simulate

        sim = simulate.Simulator_Achromat()
        im = np.full((4, 4, 3), 128, dtype=np.uint8)
        out = sim.simulate_cvd(im, simulate.Deficiency.ACHROMAT, severity=1.0)
        ok = out.shape == (4, 4, 3)
        return _check("daltonlens simulate_cvd (achromat)", ok)
    except Exception as exc:
        return _check("daltonlens simulate_cvd (achromat)", False, str(exc))


def check_daltonlens_bcm() -> bool:
    try:
        import numpy as np

        from daltonlens import simulate

        sim = simulate.Simulator_BCM()
        im = np.full((4, 4, 3), 128, dtype=np.uint8)
        out = sim.simulate_cvd(im, simulate.Deficiency.BCM, severity=1.0)
        ok = out.shape == (4, 4, 3)
        return _check("daltonlens simulate_cvd (bcm)", ok)
    except Exception as exc:
        return _check("daltonlens simulate_cvd (bcm)", False, str(exc))


def check_daltonlens_cli() -> bool:
    try:
        from daltonlens.main import DEFICIENCY_FROM_STR, get_simulator

        sim = get_simulator("auto")
        deficiency = DEFICIENCY_FROM_STR["protan"]
        ok = sim is not None and deficiency is not None
        return _check("daltonlens CLI (get_simulator, DEFICIENCY_FROM_STR)", ok)
    except Exception as exc:
        return _check("daltonlens CLI", False, str(exc))


def check_numpy() -> bool:
    try:
        import numpy as np

        arr = np.array([1, 2, 3], dtype=np.float32)
        ok = arr.sum() == 6.0
        return _check("numpy", ok, f"version {np.__version__}")
    except ImportError as exc:
        return _check("numpy", False, str(exc))


def check_pillow() -> bool:
    try:
        import io

        import numpy as np
        from PIL import Image

        arr = np.full((2, 2, 3), 100, dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(arr).save(buf, format="PNG")
        ok = buf.tell() > 0
        return _check("Pillow (PIL.Image round-trip)", ok)
    except ImportError as exc:
        return _check("Pillow", False, str(exc))


def check_c_library_binary() -> bool:
    binary = (
        REPO_ROOT
        / "algorithms"
        / "libDaltonLens"
        / "build"
        / "tests"
        / "test_simulation"
    )
    if not binary.exists():
        print(
            "[SKIP] libDaltonLens C test binary: not built -- run `make build-c` first"
        )
        return True  # SKIP is not a failure; CI build lane handles this separately
    result = subprocess.run([str(binary)], capture_output=True, text=True, timeout=30)
    ok = result.returncode == 0
    detail = "all tests GOOD" if ok else result.stdout[-200:] + result.stderr[-200:]
    return _check("libDaltonLens C test binary", ok, detail)


def check_token_file() -> bool:
    token_path = REPO_ROOT / "tokens" / "color-tokens.json"
    ok = token_path.exists() and token_path.stat().st_size > 0
    return _check("tokens/color-tokens.json exists", ok)


def check_validator_imports() -> bool:
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    try:
        import validator_registry  # noqa: F401
        from validator_registry import get_gate_specs

        specs = get_gate_specs()
        ok = len(specs) >= 6
        return _check(
            "validator_registry (GATE specs)", ok, f"{len(specs)} gates registered"
        )
    except Exception as exc:
        return _check("validator_registry", False, str(exc))
    finally:
        sys.path.pop(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv=None) -> int:
    checks = [
        check_numpy,
        check_pillow,
        check_daltonlens_import,
        check_daltonlens_simulate,
        check_daltonlens_achromat,
        check_daltonlens_bcm,
        check_daltonlens_cli,
        check_token_file,
        check_validator_imports,
        check_c_library_binary,
    ]

    results = [check() for check in checks]
    passed = sum(results)
    total = len(results)
    print(f"\nSmoke test: {passed}/{total} passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
