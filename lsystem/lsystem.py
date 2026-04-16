"""Hlavná funkcia Lsystem — vypisuje slová a vykresluje grafiku."""

import math

import matplotlib.pyplot as plt

from . import core
from . import turtle2d
from . import turtle3d
from . import animation


def Lsystem(
    axiom: str,
    rules: dict[str, str],
    angle: float,
    iterations: int,
    name: str = "L-systém",
    step: float = 1.0,
    color: str = "black",
    linewidth: float = 0.5,
    save_gif: str | None = None,
    use_3d: bool = False,
    show: bool = True,
) -> list[str]:
    """Hlavná funkcia L-systému: prepísanie, výpis slov a vykreslenie.

    Vypisuje slovo v každej iterácii a zobrazuje viacpanelový obrázok
    s grafickou interpretáciou korytnačou grafikou.

    Args:
        axiom: Počiatočné slovo (axiom).
        rules: Prepisovacie pravidlá.
        angle: Uhol otočenia v stupňoch.
        iterations: Počet iterácií.
        name: Názov L-systému (pre titulok).
        step: Dĺžka jedného kroku.
        color: Farba čiar.
        linewidth: Šírka čiar.
        save_gif: Cesta pre uloženie GIF animácie (None = neukladať).
        use_3d: Použiť 3D korytnačiu grafiku.
        show: Zobraziť obrázok interaktívne.

    Returns:
        Zoznam slov pre iterácie 0..n.
    """
    words = core.rewrite(axiom, rules, iterations)

    # Výpis slov
    print(f"\n{'═' * 60}")
    print(f"  {name}")
    print(f"{'═' * 60}")
    print(f"  Axiom:     {axiom}")
    print(f"  Pravidlá:  {rules}")
    print(f"  Uhol:      {angle}°")
    print(f"  Iterácie:  {iterations}")
    print(f"{'─' * 60}")

    for i, word in enumerate(words):
        if len(word) <= 70:
            display = word
        else:
            display = word[:67] + "..."
        print(f"  [{i}] (dĺžka {len(word):>6d}) {display}")

    print(f"{'─' * 60}")

    # 3D vykreslenie — len posledná iterácia v jednom okne
    if use_3d:
        segs = turtle3d.interpret(words[-1], angle, step)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")
        turtle3d.plot(segs, ax=ax, color=color, linewidth=linewidth)
        ax.set_title(f"{name} — iterácia {iterations}", fontsize=14)
        if save_gif:
            # Pre 3D uložíme PNG namiesto GIF
            png_path = save_gif.rsplit(".", 1)[0] + ".png"
            fig.savefig(png_path, dpi=100, bbox_inches="tight")
            print(f"  PNG uložený: {png_path}")
        if show:
            plt.show()
        else:
            plt.close(fig)
        return words

    # 2D vykreslenie — panely pre každú iteráciu
    cols = min(iterations + 1, 4)
    rows = math.ceil((iterations + 1) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5))
    fig.suptitle(name, fontsize=16, fontweight="bold")

    # Normalizácia axes na 1D pole
    if iterations == 0:
        axes = [axes]
    else:
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, word in enumerate(words):
        segs = turtle2d.interpret(word, angle, step)
        turtle2d.plot(segs, ax=axes[i], color=color, linewidth=linewidth)
        axes[i].set_title(f"Iterácia {i}", fontsize=11)

    # Skrytie prázdnych panelov
    for i in range(len(words), len(axes)):
        axes[i].set_visible(False)

    plt.tight_layout()

    # GIF animácia
    if save_gif:
        animation.create_gif(
            axiom,
            rules,
            angle,
            iterations,
            save_gif,
            step=step,
            color=color,
            linewidth=linewidth,
        )

    if show:
        plt.show()

    return words
