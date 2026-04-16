#!/usr/bin/env python3
"""Demonštrácia L-systémov — hlavný spúšťací skript.

Spustenie:
    python main.py            # Vykreslí všetky príklady + GIF animácie
    python main.py --no-show  # Len uloží obrázky a GIF, nezobrazuje interaktívne
"""

import argparse
import os

import matplotlib
import matplotlib.pyplot as plt

from lsystem import Lsystem
from lsystem.examples import EXAMPLES


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonštrácia L-systémov")
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Neukazovať interaktívne okná, len uložiť výstupy",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Adresár pre výstupné súbory (default: output/)",
    )
    args = parser.parse_args()

    if args.no_show:
        matplotlib.use("Agg")

    os.makedirs(args.output_dir, exist_ok=True)
    show = not args.no_show

    # ── 2D príklady ──────────────────────────────────────────────────
    examples_2d = {k: v for k, v in EXAMPLES.items() if not v.get("3d")}

    for key, ex in examples_2d.items():
        gif_path = os.path.join(args.output_dir, f"{key}.gif")
        Lsystem(
            axiom=ex["axiom"],
            rules=ex["rules"],
            angle=ex["angle"],
            iterations=ex["iterations"],
            name=ex["name"],
            color=ex.get("color", "black"),
            save_gif=gif_path,
            show=show,
        )

    # ── 3D príklad (bonus) ───────────────────────────────────────────
    examples_3d = {k: v for k, v in EXAMPLES.items() if v.get("3d")}

    for key, ex in examples_3d.items():
        out_path = os.path.join(args.output_dir, f"{key}.png")
        Lsystem(
            axiom=ex["axiom"],
            rules=ex["rules"],
            angle=ex["angle"],
            iterations=ex["iterations"],
            name=ex["name"],
            color=ex.get("color", "forestgreen"),
            use_3d=True,
            save_gif=out_path,
            show=show,
        )

    print(f"\n{'═' * 60}")
    print(f"  Hotovo! Výstupy uložené v: {args.output_dir}/")
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
