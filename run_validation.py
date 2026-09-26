#!/usr/bin/env python3
"""Compare a MYSTRAN F06 against the packaged reference F06."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DISPL_HEADER = re.compile(r"D I S P L A C E M E N T S")
EIGEN_HEADER = re.compile(r"R E A L\s+E I G E N V A L U E S")
GRID_LINE = re.compile(
    r"^\s*(\d+)\s+(\d+)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?|0\.0)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?|0\.0)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?|0\.0)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?|0\.0)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?|0\.0)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?|0\.0)"
)
EIGEN_LINE = re.compile(
    r"^\s*(\d+)\s+\d+\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?)\s+"
    r"([+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?)"
)

def _f(s: str) -> float:
    if s.strip() in {"0.0", "0.", "0"}:
        return 0.0
    return float(s)

def parse_f06(path: Path) -> dict:
    text = path.read_text(errors="replace").splitlines()
    displ = {}
    eigens = {}
    mode = None
    subcase = 1
    for line in text:
        if "OUTPUT FOR SUBCASE" in line:
            parts = line.split()
            for p in reversed(parts):
                if p.isdigit():
                    subcase = int(p)
                    break
        if DISPL_HEADER.search(line):
            mode = "displ"
            continue
        if EIGEN_HEADER.search(line):
            mode = "eigen"
            continue
        if mode == "displ":
            m = GRID_LINE.match(line)
            if m:
                gid = int(m.group(1))
                vals = [_f(m.group(k)) for k in range(3, 9)]
                displ[(subcase, gid)] = vals
            elif line.strip() == "" and displ:
                mode = None
        elif mode == "eigen":
            m = EIGEN_LINE.match(line)
            if m:
                eigens[int(m.group(1))] = (_f(m.group(2)), _f(m.group(4)))
            elif line.strip().startswith(">>") or "OUTPUT FOR EIGENVECTOR" in line:
                mode = None
    return {"displacements": displ, "eigenvalues": eigens}

def close(a: float, b: float, rtol: float, atol: float) -> bool:
    return abs(a - b) <= max(atol, rtol * max(abs(a), abs(b)))

def compare(got: dict, ref: dict, rtol: float, atol: float) -> list:
    fails = []
    for key, ref_vals in ref["displacements"].items():
        if key not in got["displacements"]:
            fails.append(f"missing displacement subcase={key[0]} gid={key[1]}")
            continue
        for i, (gv, rv) in enumerate(zip(got["displacements"][key], ref_vals)):
            if not close(gv, rv, rtol, atol):
                comp = "T1 T2 T3 R1 R2 R3".split()[i]
                fails.append(f"DISP SC{key[0]} GID{key[1]} {comp}: got {gv:.6e} ref {rv:.6e}")
    for mode, (lam, hz) in ref["eigenvalues"].items():
        if mode not in got["eigenvalues"]:
            fails.append(f"missing eigenvalue mode {mode}")
            continue
        gl, gh = got["eigenvalues"][mode]
        if not close(gl, lam, rtol, atol):
            fails.append(f"EIGEN mode {mode} lambda: got {gl:.6e} ref {lam:.6e}")
        if not close(gh, hz, rtol, atol):
            fails.append(f"EIGEN mode {mode} Hz: got {gh:.6e} ref {hz:.6e}")
    return fails

def main() -> int:
    ap = argparse.ArgumentParser(description="MYSTRAN validation helper")
    ap.add_argument("--f06", type=Path)
    ap.add_argument("--reference", type=Path)
    ap.add_argument("--extract", type=Path)
    ap.add_argument("--rtol", type=float, default=5e-5)
    ap.add_argument("--atol", type=float, default=1e-8)
    args = ap.parse_args()
    if args.extract:
        data = parse_f06(args.extract)
        print(f"displacements: {len(data['displacements'])} grid rows")
        for (sc, gid), v in list(data["displacements"].items())[:12]:
            print(f"  SC{sc} GID{gid}: {v}")
        print(f"eigenvalues: {len(data['eigenvalues'])} modes")
        for mode, (lam, hz) in data["eigenvalues"].items():
            print(f"  mode {mode}: lambda={lam:.6e}  f={hz:.6e} Hz")
        return 0
    if not args.f06 or not args.reference:
        ap.error("need --f06 and --reference, or --extract")
    fails = compare(parse_f06(args.f06), parse_f06(args.reference), args.rtol, args.atol)
    if fails:
        print(f"FAIL ({len(fails)} differences)")
        for line in fails[:50]:
            print(" ", line)
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
