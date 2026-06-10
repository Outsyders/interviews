import csv
import os

"""
Task: Run resilient batch inference over a CSV.

Read inputs.csv, run predict() on every row, and write predictions to out.csv.
One row in the input is malformed and will make predict() raise. A single bad
row must NOT kill the job:
  - catch the failure, log it (print is fine), and keep going
  - at the end, return the number of rows that failed

Implement:
  run_batch(in_path, out_path) -> int   # returns the failure count

out.csv should contain a header (id, prediction) and one row per SUCCESSFUL input.
"""


# --- Provided: a dummy model that raises on un-parseable rows ----------------
def predict(row: dict) -> float:
    # Raises ValueError if a feature isn't a number (e.g. the "BAD" cell).
    f1 = float(row["feature_1"])
    f2 = float(row["feature_2"])
    return f1 * 2 + f2


def run_batch(in_path: str, out_path: str) -> int:
    failures = 0
    with open(in_path, newline="") as fin, open(out_path, "w", newline="") as fout:
        reader = csv.DictReader(fin)
        writer = csv.writer(fout)
        writer.writerow(["id", "prediction"])
        for row in reader:
            try:
                writer.writerow([row["id"], predict(row)])
            except Exception as exc:
                failures += 1
                print(f"skipping row {row.get('id')}: {exc}")
    return failures


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    failures = run_batch(
        os.path.join(here, "inputs.csv"),
        os.path.join(here, "out.csv"),
    )
    print(f"{failures} row(s) failed")
