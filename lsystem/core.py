"""Jadro L-systému: prepisovacie pravidlá D0L-systému."""


def rewrite(axiom: str, rules: dict[str, str], n: int) -> list[str]:
    """Generuje slová L-systému pre iterácie 0 až n.

    Args:
        axiom: Počiatočné slovo (iterácia 0).
        rules: Prepisovacie pravidlá {znak: náhrada}.
        n: Počet iterácií.

    Returns:
        Zoznam slov [iterácia_0, iterácia_1, ..., iterácia_n].
    """
    words = [axiom]
    current = axiom
    for _ in range(n):
        current = "".join(rules.get(c, c) for c in current)
        words.append(current)
    return words
