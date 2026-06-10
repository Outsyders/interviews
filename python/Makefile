# Interview question repo — organized into sections.
#
# Sections: general | pytorch | mlops
# Each section has source under <section>/, a dependency set in
# requirements/<section>.txt, and tests in tests/test_<section>.txt.
#
# Quick start for a single section (installs its deps, then runs its tests):
#   make pytorch
#
# Override the interpreter if needed:  make pytorch PYTHON=python3

PYTHON ?= python
PIP    := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest -vvv

# Every known section. Used to generate the per-section targets below.
ALL_SECTIONS := general pytorch mlops

# Which sections `install` / `test` act on. Override to pick specific modules:
#   make install SECTIONS=mlops
#   make install SECTIONS="general mlops"
SECTIONS ?= $(ALL_SECTIONS)

.DEFAULT_GOAL := help
.PHONY: help install upgrade-pip test clean $(ALL_SECTIONS) \
        $(addprefix setup-,$(ALL_SECTIONS)) $(addprefix test-,$(ALL_SECTIONS))

help:
	@echo "Sections: $(ALL_SECTIONS)"
	@echo
	@echo "Set up and test one section (installs only that section's deps):"
	@echo "  make general      basic Python questions (no third-party deps)"
	@echo "  make pytorch      PyTorch / ML questions"
	@echo "  make mlops        MLOps questions (k8s, serving, drift, retries)"
	@echo
	@echo "Finer-grained targets:"
	@echo "  make setup-<sec>  install just that section's dependencies"
	@echo "  make test-<sec>   run just that section's tests (no install)"
	@echo
	@echo "Pick specific modules with SECTIONS (default: all):"
	@echo "  make install SECTIONS=mlops"
	@echo "  make install SECTIONS=\"general mlops\""
	@echo "  make test    SECTIONS=pytorch"
	@echo
	@echo "Whole repo:"
	@echo "  make install      install selected sections' dependencies"
	@echo "  make test         run selected sections' tests"
	@echo "  make clean        remove caches and generated files"

upgrade-pip:
	$(PIP) install --upgrade pip

# --- Selected sections (all by default; narrow with SECTIONS=...) -----------
install: upgrade-pip
	@for s in $(SECTIONS); do \
	  echo "==> installing '$$s' dependencies"; \
	  $(PIP) install -r requirements/$$s.txt || exit 1; \
	done

test:
	$(PYTEST) $(foreach s,$(SECTIONS),tests/test_$(s).py)

# --- Per-section: setup deps, then run that section's tests -----------------
# `make <section>` is the one-shot "set up and verify" entry point.
# Generate setup-<sec>, test-<sec>, and <sec> targets for each section.
define section_rules
setup-$(1): upgrade-pip
	$$(PIP) install -r requirements/$(1).txt
test-$(1):
	$$(PYTEST) tests/test_$(1).py
$(1): setup-$(1) test-$(1)
endef
$(foreach s,$(ALL_SECTIONS),$(eval $(call section_rules,$(s))))

clean:
	rm -rf .pytest_cache **/__pycache__ */__pycache__ tests/__pycache__ \
	       mlops/out.csv mlops/__pycache__
