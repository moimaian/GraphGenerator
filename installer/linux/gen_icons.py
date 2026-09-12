#!/usr/bin/env python3
"""Gera os ícones do tema hicolor a partir de Midia/GraphGenerator_Icon.png.

    gen_icons.py <origem.png> <dir_hicolor>

Cria <dir_hicolor>/<N>x<N>/apps/graphgenerator.png para N em 16..512, com a
arte centralizada (proporção preservada) num quadrado transparente NxN —
como manda o padrão de ícones do freedesktop."""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt  # noqa: E402
from PySide6.QtGui import QColor, QImage, QPainter  # noqa: E402

TAMANHOS = (16, 24, 32, 48, 64, 128, 256, 512)


def main(origem, dir_hicolor):
    base = QImage(origem)
    if base.isNull():
        sys.exit(f"gen_icons: não consegui abrir {origem}")
    for n in TAMANHOS:
        redim = base.scaled(
            n, n,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        quadro = QImage(n, n, QImage.Format.Format_ARGB32)
        quadro.fill(QColor(0, 0, 0, 0))
        p = QPainter(quadro)
        p.drawImage((n - redim.width()) // 2, (n - redim.height()) // 2, redim)
        p.end()
        pasta = os.path.join(dir_hicolor, f"{n}x{n}", "apps")
        os.makedirs(pasta, exist_ok=True)
        quadro.save(os.path.join(pasta, "graphgenerator.png"), "PNG")
    print(f"gen_icons: {len(TAMANHOS)} ícones em {dir_hicolor}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
