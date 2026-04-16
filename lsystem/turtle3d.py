"""3D korytnačia grafika pre L-systémy (bonus rozšírenie).

Rozširuje 2D interpretáciu o tretiu os. Orientácia korytnačky je
definovaná trojicou ortonormálnych vektorov (heading, left, up)
a rotácie sa realizujú Rodriguesovým vzorcom.

Symboly nad rámec 2D:
    &  — sklon dolu (pitch down, rotácia okolo left)
    ^  — sklon hore (pitch up)
    \\  — naklonenie vľavo (roll left, rotácia okolo heading)
    /  — naklonenie vpravo (roll right)
"""

from dataclasses import dataclass, field

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection


def _rotation_matrix(axis: np.ndarray, angle_deg: float) -> np.ndarray:
    """Rotačná matica podľa Rodriguesovho vzorca."""
    angle = np.radians(angle_deg)
    axis = axis / np.linalg.norm(axis)
    K = np.array(
        [
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0],
        ]
    )
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)


@dataclass
class _State:
    """Stav 3D korytnačky: poloha a orientácia (HLU)."""

    pos: np.ndarray = field(default_factory=lambda: np.zeros(3))
    heading: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 1.0, 0.0])
    )  # smer vpred (hore)
    left: np.ndarray = field(
        default_factory=lambda: np.array([-1.0, 0.0, 0.0])
    )
    up: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 1.0])
    )

    def copy(self) -> "_State":
        return _State(
            self.pos.copy(),
            self.heading.copy(),
            self.left.copy(),
            self.up.copy(),
        )

    def rotate(self, axis: np.ndarray, angle: float) -> None:
        R = _rotation_matrix(axis, angle)
        self.heading = R @ self.heading
        self.left = R @ self.left
        self.up = R @ self.up


def _is_draw(c: str) -> bool:
    return ("A" <= c <= "U") or ("0" <= c <= "9")


def _is_move(c: str) -> bool:
    return "a" <= c <= "u"


def interpret(word: str, angle: float, step: float = 1.0) -> list[tuple]:
    """Interpretuje slovo L-systému 3D korytnačou grafikou.

    Args:
        word: Slovo na interpretáciu.
        angle: Uhol otočenia v stupňoch.
        step: Dĺžka jedného kroku.

    Returns:
        Zoznam 3D úsečiek [((x1,y1,z1), (x2,y2,z2)), ...].
    """
    state = _State()
    stack: list[_State] = []
    segments: list[tuple] = []

    for c in word:
        if _is_draw(c):
            new_pos = state.pos + step * state.heading
            segments.append((tuple(state.pos), tuple(new_pos)))
            state.pos = new_pos
        elif _is_move(c):
            state.pos = state.pos + step * state.heading
        elif c == "+":
            state.rotate(state.up, angle)
        elif c == "-":
            state.rotate(state.up, -angle)
        elif c == "&":
            state.rotate(state.left, angle)
        elif c == "^":
            state.rotate(state.left, -angle)
        elif c == "\\":
            state.rotate(state.heading, angle)
        elif c == "/":
            state.rotate(state.heading, -angle)
        elif c == "|":
            state.rotate(state.up, 180)
        elif c == "[":
            stack.append(state.copy())
        elif c == "]" and stack:
            state = stack.pop()

    return segments


def plot(segments, ax=None, color="forestgreen", linewidth=0.8):
    """Vykreslí 3D úsečky.

    Args:
        segments: Zoznam 3D úsečiek z interpret().
        ax: Matplotlib 3D axes (voliteľné).
        color: Farba čiar.
        linewidth: Šírka čiar.

    Returns:
        Matplotlib 3D axes.
    """
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

    if segments:
        lines = [
            [
                (s[0][0], s[0][1], s[0][2]),
                (s[1][0], s[1][1], s[1][2]),
            ]
            for s in segments
        ]
        lc = Line3DCollection(lines, colors=color, linewidths=linewidth)
        ax.add_collection3d(lc)

        all_pts = np.array([p for seg in segments for p in seg])
        for i, setter in enumerate([ax.set_xlim, ax.set_ylim, ax.set_zlim]):
            mn, mx = all_pts[:, i].min(), all_pts[:, i].max()
            margin = (mx - mn) * 0.1 or 1.0
            setter(mn - margin, mx + margin)

    ax.set_axis_off()
    return ax
