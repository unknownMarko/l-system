"""Definície známych L-systémov a vlastného návrhu."""

EXAMPLES: dict[str, dict] = {
    # ── Známe L-systémy ──────────────────────────────────────────────
    "koch_snowflake": {
        "name": "Kochova vločka",
        "axiom": "F++F++F",
        "rules": {"F": "F-F++F-F"},
        "angle": 60,
        "iterations": 4,
        "color": "royalblue",
    },
    "sierpinski_triangle": {
        "name": "Sierpinského trojuholník",
        "axiom": "F-G-G",
        "rules": {"F": "F-G+F+G-F", "G": "GG"},
        "angle": 120,
        "iterations": 6,
        "color": "darkred",
    },
    "dragon_curve": {
        "name": "Dračia krivka",
        "axiom": "FX",
        "rules": {"X": "X+YF+", "Y": "-FX-Y"},
        "angle": 90,
        "iterations": 12,
        "color": "darkorange",
    },
    "fractal_plant": {
        "name": "Fraktálová rastlina",
        "axiom": "X",
        "rules": {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        "angle": 25,
        "iterations": 6,
        "color": "forestgreen",
    },
    # ── Vlastný L-systém ─────────────────────────────────────────────
    "pentagonal_snowflake": {
        "name": "Pentagonálna vločka (vlastný)",
        "axiom": "F+F+F+F+F",
        "rules": {"F": "F-F++F-F"},
        "angle": 72,
        "iterations": 3,
        "color": "purple",
        "description": (
            "Aplikácia Kochovej konštrukcie na pravidelný päťuholník "
            "namiesto trojuholníka. Výsledkom je vločka s 5-násobnou "
            "symetriou — pentagonálny fraktál."
        ),
    },
    # ── 3D L-systém (bonus) ──────────────────────────────────────────
    "tree_3d": {
        "name": "3D strom",
        "axiom": "A",
        "rules": {"A": "F[+A][-A][&A][^A]"},
        "angle": 22.5,
        "iterations": 5,
        "color": "forestgreen",
        "3d": True,
        "description": (
            "Trojrozmerný fraktálový strom. Vetvy sa rozširujú do "
            "štyroch smerov — yaw (±) a pitch (&^) — čím vzniká "
            "priestorová koruna."
        ),
    },
}
