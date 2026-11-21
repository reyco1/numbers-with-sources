import argparse
import sys

from .check import VERIFIED, check_answer, load_answer


def print_table(results):
    rows = [("STATUS", "CLAIM", "SOURCE", "NOTE")]
    for r in results:
        rows.append((r["status"], r["claim"], r["source"] or "-", r["note"] or "-"))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    for row in rows:
        print("  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip())


def main(argv=None):
    p = argparse.ArgumentParser(prog="numbers_with_sources")
    p.add_argument("answer", help="agent answer as JSON (a list of claims)")
    p.add_argument("data", help="folder of CSV source files")
    p.add_argument("--tolerance", type=float, default=0.0,
                   help="allowed difference between reported and source value")
    args = p.parse_args(argv)

    results = check_answer(load_answer(args.answer), args.data, args.tolerance)
    print_table(results)
    bad = sum(r["status"] != VERIFIED for r in results)
    print(f"\n{len(results) - bad} of {len(results)} verified.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
