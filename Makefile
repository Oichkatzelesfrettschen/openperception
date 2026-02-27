# OpenPerception Makefile
# Build orchestration for development, testing, and documentation

# =============================================================================
# Configuration
# =============================================================================
PORT ?= 8000
PANDOC_SRC ?= docs/colorblind-friendly-design-guide.md
OUT_DIR ?= out
PYTHON ?= python3
C_BUILD_DIR ?= algorithms/libDaltonLens/build

# =============================================================================
# Phony Targets
# =============================================================================
.PHONY: all help serve oklch contrast-check separation-check \
        test test-python test-c test-all coverage \
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
	@echo ""
	@echo "Testing:"
	@echo "  test-python        - Run Python tests with pytest"
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

# =============================================================================
# Testing
# =============================================================================
test: test-all

test-all: test-python test-c
	@echo "All tests completed."

test-python:
	@echo "Running Python tests..."
	cd algorithms/DaltonLens-Python && $(PYTHON) -m pytest tests/ -v --tb=short
	@echo "Python tests completed."

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

install-python:
	@echo "Installing DaltonLens-Python in development mode..."
	pip install -e algorithms/DaltonLens-Python
	@echo "Python package installed."

install-dev:
	@echo "Setting up complete development environment..."
	pip install -r requirements-dev.txt
	pip install -e algorithms/DaltonLens-Python
	pre-commit install
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
	pip install -e python-packages/sphinx-brand-theme

sphinx-example-html:
	@echo "Building example Sphinx project"
	sphinx-build -b html sphinx/example sphinx/example/_build/html

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
