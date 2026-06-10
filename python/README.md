# Developer Interview Template

Structured interview questions, organized into self-contained **sections**. Each
section has its own source folder, its own dependency set, and its own tests, so a
candidate (or interviewer) can set up and run just the part they need.

## Sections

| Section   | Source        | Tests                  | Deps                          | Focus |
|-----------|---------------|------------------------|-------------------------------|-------|
| `general` | `general/`    | `tests/test_general.py`| none (pure Python)            | strings, matrices, LRU cache |
| `pytorch` | `pytorch/`    | `tests/test_pytorch.py`| torch, torchvision, numpy, …  | tensors, datasets, CNNs, mixed precision |
| `mlops`   | `mlops/`      | `tests/test_mlops.py`  | numpy, pandas                 | k8s health, serving, drift, retries, batch jobs |

Each question file has a task docstring and a stub to fill in; provided data and
helpers are already written. The tests ship red — they pass once the stub is
implemented.

## Setup with `make`

Set up and verify a single section in one command (installs only that section's
dependencies, then runs its tests):

```bash
make general      # pure Python, nothing to install
make pytorch
make mlops
```

Finer-grained targets:

```bash
make setup-mlops  # install just this section's deps
make test-mlops   # run just this section's tests (no install)
```

Whole repo:

```bash
make install      # install every section's dependencies
make test         # run all tests
make clean        # remove caches and generated files
make help         # list all targets
```

Override the interpreter if `python` isn't on your PATH:

```bash
make pytorch PYTHON=python3
```

## Layout

```
python/
├── Makefile
├── requirements.txt            # everything (make install)
├── requirements/               # per-section dependency sets
│   ├── base.txt                #   shared (pytest)
│   ├── general.txt
│   ├── pytorch.txt
│   └── mlops.txt
├── general/                    # section source
├── pytorch/
├── mlops/
└── tests/                      # tests/test_<section>.py
```
