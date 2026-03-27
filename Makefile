# OpenPerception Makefile
# Build orchestration for development, testing, and documentation

# =============================================================================
# Configuration
# =============================================================================
PORT ?= 8000
PANDOC_SRC ?= docs/colorblind-friendly-design-guide.md
OUT_DIR ?= out
VENV_DIR ?= .venv
BOOTSTRAP_PYTHON ?= python3
ifneq ($(wildcard $(VENV_DIR)/bin/python3),)
PYTHON ?= $(abspath $(VENV_DIR)/bin/python3)
else
PYTHON ?= python3
endif
C_BUILD_DIR ?= algorithms/libDaltonLens/build

# =============================================================================
# Phony Targets
# =============================================================================
.PHONY: all help serve oklch contrast-check separation-check seizure-check temporal-depth-check cognitive-check typography-check rendered-spatial-check rendered-cognitive-check check-rendered playwright-install profile-report scale-report validate validate-strict gap-report claims-report claims-check repo-stats repo-stats-check integrity-check task-governance-check source-cache-links-check paper-corpus-check source-assets-check octane-probe check venv \
        test test-python test-tools test-c test-all coverage \
        lint lint-python lint-c format \
        build build-c install-python install-dev \
        pandoc-html pandoc-pdf sphinx-install-theme sphinx-example-html \
        clean clean-all

# =============================================================================
# Default Target
# =============================================================================
all: help

help:
	@echo "OpenPerception Makefile"
	@echo ""
	@echo "Development:"
	@echo "  serve              - Start development server on port $(PORT)"
	@echo "  oklch              - Generate OKLCH color tokens"
	@echo "  contrast-check     - Validate WCAG contrast ratios"
	@echo "  separation-check   - Check CVD color separation"
	@echo "  seizure-check      - Run seizure gate on a frame manifest (set SEIZURE_MANIFEST=path)"
	@echo "  temporal-depth-check - Run the first temporal/depth policy validator"
	@echo "  cognitive-check    - Run the first cognitive/navigation validator"
	@echo "  typography-check   - Run the first typography verifier"
	@echo "  rendered-spatial-check - Run the browser-backed rendered spatial audit"
	@echo "  rendered-cognitive-check - Run the browser-backed rendered cognitive audit"
	@echo "  check-rendered     - Run the optional browser-backed rendered audit lane"
	@echo "  playwright-install - Install Chromium for the selected Playwright environment"
	@echo "  octane-probe       - Verify the clean OctaneBlender headless startup path"
	@echo "  profile-report     - Compose axis/display profiles (set PROFILE_NAMES=a,b)"
	@echo "  scale-report       - Show lp->px quantization report (LP=16 DPI=96 SCALE=1 SNAP_CLASS=layout)"
	@echo "  validate           - Run unified implemented validator gates in strict mode"
	@echo "  validate-strict    - Alias for strict unified validation"
	@echo "  gap-report         - Show declared-vs-runtime gap report"
	@echo "  claims-report      - Show seeded claims-to-runtime coverage report"
	@echo "  claims-check       - Validate the claims registry integrity"
	@echo "  repo-stats         - Regenerate machine-checkable repo stats files"
	@echo "  repo-stats-check   - Validate checked-in repo stats against the current tree"
	@echo "  integrity-check    - Run repo integrity verifiers (claims, stats, corpus, source assets, source cache links, task governance)"
	@echo "  task-governance-check - Validate task ledger and known-issues governance docs"
	@echo "  check              - Run the repo aggregate gate (strict validate, integrity, tools tests, DaltonLens tests)"
	@echo ""
	@echo "Testing:"
	@echo "  test-python        - Run Python tests with pytest"
	@echo "  test-tools         - Run repo-owned tools tests with pytest"
	@echo "  test-c             - Build and run C tests"
	@echo "  test-all           - Run all tests"
	@echo "  test               - Alias for test-all"
	@echo "  coverage           - Run tests with coverage report (>=70% required)"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint-python        - Lint Python code with ruff"
	@echo "  lint-c             - Run cppcheck on C code"
	@echo "  lint               - Run all linters"
	@echo "  format             - Format Python code with black"
	@echo ""
	@echo "Building:"
	@echo "  build-c            - Build libDaltonLens C library"
	@echo "  venv               - Create or refresh the local .venv with dev dependencies"
	@echo "  install-python     - Install DaltonLens-Python in dev mode"
	@echo "  install-dev        - Full dev environment setup (deps + pre-commit)"
	@echo ""
	@echo "Documentation:"
	@echo "  sphinx-install-theme - Install custom Sphinx theme"
	@echo "  sphinx-example-html  - Build example Sphinx docs"
	@echo "  pandoc-html          - Convert docs to HTML with Pandoc"
	@echo "  pandoc-pdf           - Convert docs to PDF with Pandoc"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean              - Remove build artifacts"
	@echo "  clean-all          - Remove all generated files"

# =============================================================================
# Development
# =============================================================================
serve:
	$(PYTHON) tools/devserver.py --port $(PORT) --dir .

oklch:
	$(PYTHON) tools/gen_oklch_tokens.py

contrast-check:
	$(PYTHON) tools/contrast_check.py

separation-check:
	$(PYTHON) tools/separation_check.py

seizure-check:
	@if [ -z "$(SEIZURE_MANIFEST)" ]; then \
		echo "Set SEIZURE_MANIFEST=/path/to/manifest.json"; \
		exit 1; \
	fi
	$(PYTHON) tools/validators/seizure.py $(SEIZURE_MANIFEST)

temporal-depth-check:
	$(PYTHON) tools/validators/temporal_depth.py

cognitive-check:
	$(PYTHON) tools/validators/cognitive.py

typography-check:
	$(PYTHON) tools/validators/typography.py

rendered-spatial-check:
	$(PYTHON) tools/rendered_spatial_check.py

rendered-cognitive-check:
	$(PYTHON) tools/rendered_cognitive_check.py

check-rendered: rendered-spatial-check rendered-cognitive-check
	@echo "Rendered audit lane completed."

playwright-install:
	$(PYTHON) -m playwright install chromium

octane-probe:
	$(PYTHON) tools/octane_headless_probe.py --blender-executable $(or $(SHOWCASE_BLENDER_BIN),OctaneBlender)

profile-report:
	$(PYTHON) tools/profile_resolver.py $(if $(PROFILE_NAMES),--profiles $(PROFILE_NAMES),)

scale-report:
	$(PYTHON) tools/scaling.py --lp $(or $(LP),16) --dpi $(or $(DPI),96) --scale $(or $(SCALE),1) --snap-class $(or $(SNAP_CLASS),layout) $(if $(PROFILE_NAMES),--profiles $(PROFILE_NAMES),)

validate: validate-strict

validate-strict:
	$(PYTHON) tools/validate.py --strict-warnings

gap-report:
	$(PYTHON) tools/runtime_gap_report.py

claims-report:
	$(PYTHON) tools/claims_coverage_report.py

claims-check:
	$(PYTHON) tools/check_claims_registry.py

repo-stats:
	$(PYTHON) tools/repo_stats.py --output-json docs/generated/repo_stats.json --output-md docs/generated/repo_stats.md

repo-stats-check:
	$(PYTHON) tools/check_repo_stats.py

task-governance-check:
	$(PYTHON) tools/check_task_governance.py

source-cache-links-check:
	$(PYTHON) tools/check_source_cache_links.py

paper-corpus-check:
	$(PYTHON) tools/check_paper_corpus.py

source-assets-check:
	$(PYTHON) tools/check_source_assets.py

integrity-check: claims-check repo-stats-check paper-corpus-check source-assets-check source-cache-links-check task-governance-check
	@echo "All repo integrity checks completed."

check: validate-strict integrity-check test-tools test-python
	@echo "Aggregate repo check completed."

# =============================================================================
# Testing
# =============================================================================
test: test-all

test-all: test-python test-tools test-c
	@echo "All tests completed."

test-python:
	@echo "Running Python tests..."
	cd algorithms/DaltonLens-Python && $(PYTHON) -m pytest tests/ -v --tb=short
	@echo "Python tests completed."

test-tools:
	@echo "Running repo tools tests..."
	$(PYTHON) -m pytest tools/tests/ -v --tb=short
	@echo "Repo tools tests completed."

coverage:
	@echo "Running Python tests with coverage..."
	cd algorithms/DaltonLens-Python && $(PYTHON) -m pytest tests/ -v --tb=short \
		--cov=daltonlens --cov-report=term-missing --cov-report=html:../../htmlcov \
		--cov-fail-under=70
	@echo "Coverage report written to htmlcov/"

benchmark:
	@echo "Running CVD simulation benchmarks..."
	$(PYTHON) benchmarks/run_benchmarks.py
	@echo "Run with --output benchmarks/results/YYYYMMDD.md to save results."

test-c: build-c
	@echo "Running C tests..."
	@if [ -f $(C_BUILD_DIR)/tests/test_simulation ]; then \
		$(C_BUILD_DIR)/tests/test_simulation; \
	else \
		echo "C test binary not found. Build may have failed."; \
		exit 1; \
	fi
	@echo "C tests completed."

# =============================================================================
# Code Quality
# =============================================================================
lint: lint-python lint-c
	@echo "All linting completed."

lint-python:
	@echo "Linting Python code..."
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .
	@echo "Python linting completed."

lint-c:
	@echo "Linting C code..."
	@if command -v cppcheck >/dev/null 2>&1; then \
		cppcheck --enable=warning,style,performance \
			--suppress=missingIncludeSystem \
			--suppress=unusedFunction \
			-I algorithms/libDaltonLens \
			algorithms/libDaltonLens/libDaltonLens.c \
			algorithms/libDaltonLens/libDaltonLens.h; \
	else \
		echo "cppcheck not installed, skipping C lint"; \
	fi
	@echo "C linting completed."

format:
	@echo "Formatting Python code..."
	$(PYTHON) -m black .
	$(PYTHON) -m ruff check --fix .
	@echo "Formatting completed."

# =============================================================================
# Building
# =============================================================================
build-c:
	@echo "Building libDaltonLens..."
	mkdir -p $(C_BUILD_DIR)
	cd $(C_BUILD_DIR) && cmake .. -DCMAKE_BUILD_TYPE=Release
	cd $(C_BUILD_DIR) && cmake --build . --config Release
	@echo "C library build completed."

venv:
	@echo "Bootstrapping local virtual environment in $(VENV_DIR)..."
	$(BOOTSTRAP_PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/python -m pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements-dev.txt
	$(VENV_DIR)/bin/pip install -e algorithms/DaltonLens-Python -e python-packages/sphinx-brand-theme
	@echo "Virtual environment ready. Use $(VENV_DIR)/bin/python or rerun make commands."

install-python:
	@echo "Installing DaltonLens-Python in development mode..."
	$(PYTHON) -m pip install -e algorithms/DaltonLens-Python
	@echo "Python package installed."

install-dev: venv
	@echo "Setting up complete development environment..."
	$(VENV_DIR)/bin/pre-commit install
	@echo "Development environment ready. Run 'make test' to verify."

# =============================================================================
# Documentation
# =============================================================================
$(OUT_DIR):
	mkdir -p $(OUT_DIR)

pandoc-html: | $(OUT_DIR)
	pandoc -s -t html5 --template templates/pandoc/brand.html -o $(OUT_DIR)/pandoc.html $(PANDOC_SRC)

pandoc-pdf: pandoc-html
	@echo "Convert HTML to PDF using wkhtmltopdf (if installed)"
	@if command -v wkhtmltopdf >/dev/null 2>&1; then \
		wkhtmltopdf $(OUT_DIR)/pandoc.html $(OUT_DIR)/pandoc.pdf; \
	else \
		echo "wkhtmltopdf not found; install or use weasyprint."; \
	fi

sphinx-install-theme:
	$(PYTHON) -m pip install -e python-packages/sphinx-brand-theme

sphinx-example-html: sphinx-install-theme
	@echo "Building example Sphinx project"
	$(PYTHON) -m sphinx -b html sphinx/example sphinx/example/_build/html

# =============================================================================
# Cleanup
# =============================================================================
clean:
	rm -rf $(OUT_DIR)
	rm -rf sphinx/example/_build
	rm -rf $(C_BUILD_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup completed."

clean-all: clean
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	@echo "Full cleanup completed."
