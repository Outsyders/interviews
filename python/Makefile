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

SECTIONS := general pytorch mlops

.DEFAULT_GOAL := help
.PHONY: help install upgrade-pip test clean $(SECTIONS) \
        $(addprefix setup-,$(SECTIONS)) $(addprefix test-,$(SECTIONS))

help:
	@echo "Sections: $(SECTIONS)"
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
	@echo "Whole repo:"
	@echo "  make install      install every section's dependencies"
	@echo "  make test         run all tests"
	@echo "  make clean        remove caches and generated files"

upgrade-pip:
	$(PIP) install --upgrade pip

# --- Whole repo -------------------------------------------------------------
install: upgrade-pip
	$(PIP) install -r requirements.txt

test:
	$(PYTEST)

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
$(foreach s,$(SECTIONS),$(eval $(call section_rules,$(s))))

clean:
	rm -rf .pytest_cache **/__pycache__ */__pycache__ tests/__pycache__ \
	       mlops/out.csv mlops/__pycache__
