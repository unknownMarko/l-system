"""Animácia vývoja L-systému do GIF."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from . import core
from . import turtle2d


def create_gif(
    axiom: str,
    rules: dict[str, str],
    angle: float,
    iterations: int,
    filename: str,
    step: float = 1.0,
    color: str = "black",
    linewidth: float = 0.5,
    figsize: tuple = (8, 8),
    interval: int = 1000,
    dpi: int = 100,
) -> None:
    """Vytvorí animovaný GIF zobrazujúci vývoj L-systému cez iterácie.

    Args:
        axiom: Počiatočné slovo.
        rules: Prepisovacie pravidlá.
        angle: Uhol otočenia v stupňoch.
        iterations: Počet iterácií.
        filename: Cesta k výstupnému GIF súboru.
        step: Dĺžka jedného kroku korytnačky.
        color: Farba čiar.
        linewidth: Šírka čiar.
        figsize: Veľkosť obrázku.
        interval: Čas medzi snímkami v ms.
        dpi: Rozlíšenie výstupu.
    """
    words = core.rewrite(axiom, rules, iterations)
    all_segments = [turtle2d.interpret(w, angle, step) for w in words]

    # Globálne hranice pre konzistentný pohľad naprieč iteráciami
    all_points: list[tuple[float, float]] = []
    for segs in all_segments:
        for (x1, y1), (x2, y2) in segs:
            all_points.extend([(x1, y1), (x2, y2)])

    if all_points:
        xs, ys = zip(*all_points)
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        dx = (xmax - xmin) * 0.1 or 1.0
        dy = (ymax - ymin) * 0.1 or 1.0
        bounds = (xmin - dx, xmax + dx, ymin - dy, ymax + dy)
    else:
        bounds = (-1, 1, -1, 1)

    fig, ax = plt.subplots(figsize=figsize)

    def update(frame: int) -> None:
        ax.clear()
        # Adaptívna šírka čiar — hrubšie pre skoré iterácie, tenšie pre neskoršie
        lw = max(linewidth, linewidth * (iterations - frame + 1))
        turtle2d.plot(all_segments[frame], ax=ax, color=color, linewidth=lw)
        ax.set_xlim(bounds[0], bounds[1])
        ax.set_ylim(bounds[2], bounds[3])
        ax.set_title(f"Iterácia {frame}", fontsize=14)
        ax.set_aspect("equal")
        ax.axis("off")

    anim = FuncAnimation(fig, update, frames=len(words), interval=interval, repeat=True)
    fps = max(1, 1000 // interval)
    anim.save(filename, writer=PillowWriter(fps=fps), dpi=dpi)
    plt.close(fig)
    print(f"  GIF uložený: {filename}")
