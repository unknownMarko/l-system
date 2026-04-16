"""2D korytnačia grafika pre L-systémy."""

import math
from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


@dataclass
class _State:
    """Stav 2D korytnačky: poloha a orientácia."""

    x: float = 0.0
    y: float = 0.0
    heading: float = 90.0  # stupne; 0 = vpravo, 90 = hore


def _is_draw(c: str) -> bool:
    """A-U, 0-9 — nakresli úsečku."""
    return ("A" <= c <= "U") or ("0" <= c <= "9")


def _is_move(c: str) -> bool:
    """a-u — pohni sa vpred bez kreslenia."""
    return "a" <= c <= "u"


def interpret(word: str, angle: float, step: float = 1.0) -> list[tuple]:
    """Interpretuje slovo L-systému korytnačou grafikou.

    Args:
        word: Slovo na interpretáciu.
        angle: Uhol otočenia v stupňoch.
        step: Dĺžka jedného kroku.

    Returns:
        Zoznam úsečiek [((x1, y1), (x2, y2)), ...].
    """
    state = _State()
    stack: list[_State] = []
    segments: list[tuple] = []

    for c in word:
        if _is_draw(c):
            rad = math.radians(state.heading)
            nx = state.x + step * math.cos(rad)
            ny = state.y + step * math.sin(rad)
            segments.append(((state.x, state.y), (nx, ny)))
            state.x, state.y = nx, ny
        elif _is_move(c):
            rad = math.radians(state.heading)
            state.x += step * math.cos(rad)
            state.y += step * math.sin(rad)
        elif c == "+":
            state.heading += angle
        elif c == "-":
            state.heading -= angle
        elif c == "|":
            state.heading += 180.0
        elif c == "[":
            stack.append(_State(state.x, state.y, state.heading))
        elif c == "]" and stack:
            state = stack.pop()

    return segments


def plot(segments, ax=None, color="black", linewidth=0.5):
    """Vykreslí úsečky na matplotlib axes.

    Args:
        segments: Zoznam úsečiek z interpret().
        ax: Matplotlib axes (voliteľné — vytvorí nové ak None).
        color: Farba čiar.
        linewidth: Šírka čiar.

    Returns:
        Matplotlib axes s vykreslením.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 8))
    if segments:
        lc = LineCollection(segments, colors=color, linewidths=linewidth)
        ax.add_collection(lc)
        ax.autoscale()
    ax.set_aspect("equal")
    ax.axis("off")
    return ax
