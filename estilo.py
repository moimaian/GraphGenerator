# SPDX-License-Identifier: GPL-3.0-or-later
"""Tema claro/escuro do GraphGenerator, no mesmo esquema do SolarCalc: uma
paleta Qt 100% explícita (para o claro/escuro ser decidido só pelo app, e
não pelo tema do sistema operacional) mais um QSS base + um QSS extra só no
escuro.

O mecanismo de "classes CSS" imita Gtk.Widget.add_css_class: guardamos as
classes na propriedade dinâmica "class" e usamos o seletor [class~="x"] no
QSS."""
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


def _paleta_clara():
    paleta = QPalette()
    paleta.setColor(QPalette.ColorRole.Window, QColor("#F5F5F0"))
    paleta.setColor(QPalette.ColorRole.WindowText, QColor("#1B1B1B"))
    paleta.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
    paleta.setColor(QPalette.ColorRole.AlternateBase, QColor("#F0F0EC"))
    paleta.setColor(QPalette.ColorRole.Text, QColor("#1B1B1B"))
    paleta.setColor(QPalette.ColorRole.Button, QColor("#E8E8E4"))
    paleta.setColor(QPalette.ColorRole.ButtonText, QColor("#1B1B1B"))
    paleta.setColor(QPalette.ColorRole.ToolTipBase, QColor("#FFFFDC"))
    paleta.setColor(QPalette.ColorRole.ToolTipText, QColor("#1B1B1B"))
    paleta.setColor(QPalette.ColorRole.Highlight, QColor("#5DADE2"))
    paleta.setColor(QPalette.ColorRole.HighlightedText, QColor("#1B1B1B"))
    paleta.setColor(QPalette.ColorRole.PlaceholderText, QColor("#8A8A85"))
    return paleta


def _paleta_escura():
    paleta = QPalette()
    paleta.setColor(QPalette.ColorRole.Window, QColor("#263238"))
    paleta.setColor(QPalette.ColorRole.WindowText, QColor("#CFD8DC"))
    paleta.setColor(QPalette.ColorRole.Base, QColor("#1B262C"))
    paleta.setColor(QPalette.ColorRole.AlternateBase, QColor("#263238"))
    paleta.setColor(QPalette.ColorRole.Text, QColor("#ECEFF1"))
    paleta.setColor(QPalette.ColorRole.Button, QColor("#37474F"))
    paleta.setColor(QPalette.ColorRole.ButtonText, QColor("#ECEFF1"))
    paleta.setColor(QPalette.ColorRole.ToolTipBase, QColor("#37474F"))
    paleta.setColor(QPalette.ColorRole.ToolTipText, QColor("#ECEFF1"))
    paleta.setColor(QPalette.ColorRole.Highlight, QColor("#5DADE2"))
    paleta.setColor(QPalette.ColorRole.HighlightedText, QColor("#1B1B1B"))
    paleta.setColor(QPalette.ColorRole.PlaceholderText, QColor("#78909C"))
    return paleta


def add_css_class(widget, *classes):
    atuais = set((widget.property("class") or "").split())
    atuais.update(classes)
    widget.setProperty("class", " ".join(sorted(atuais)))
    _repolir(widget)


def remove_css_class(widget, *classes):
    atuais = set((widget.property("class") or "").split())
    atuais.difference_update(classes)
    widget.setProperty("class", " ".join(sorted(atuais)))
    _repolir(widget)


def _repolir(widget):
    estilo = widget.style()
    estilo.unpolish(widget)
    estilo.polish(widget)
    widget.update()


# --- QSS base: sempre aplicado, claro ou escuro -----------------------------
QSS_BASE = """
QLabel[class~="title-2"] { font-size: 15pt; font-weight: bold; }
QLabel[class~="dim-label"] { color: #6E6E6E; }
QLabel[class~="versao-cabecalho"] { color: #8A8A8A; }

QPushButton[class~="bandeira-btn"] { padding: 0px 2px; font-size: 15px; }
QPushButton[class~="flat"] {
    background-color: transparent; border: none; padding: 4px 8px;
}
QPushButton[class~="flat"]:hover { background-color: rgba(0, 0, 0, 0.06); }

QPushButton[class~="suggested-action"] {
    background-color: #5DADE2; color: #1B1B1B; border: 1px solid #3E8FCB;
    border-radius: 4px; padding: 5px 14px; font-weight: bold;
}
QPushButton[class~="suggested-action"]:hover { background-color: #85C1EA; }

/* Grupos de campos (QGroupBox): título em negrito "montado sobre" a linha da
   borda (o fundo palette(window) recorta a borda atrás do texto). */
QGroupBox {
    border: 1px solid #D0D0CB; border-radius: 8px;
    margin-top: 12px; padding: 16px 12px 12px 12px; font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 12px; top: 1px; padding: 0px 5px;
    background-color: palette(window);
}

/* Separador horizontal discreto sob a barra superior. */
QFrame[frameShape="4"] {
    min-height: 2px; max-height: 2px; background: transparent;
    border: none; border-top: 1px solid #D0D0CB; border-bottom: 1px solid #FFFFFF;
}

QLineEdit, QComboBox {
    border: 1px solid #C2C2BC;
    border-radius: 4px;
    background-color: palette(base);
    padding: 3px 6px;
    min-height: 20px;
}
QComboBox QAbstractItemView {
    background-color: palette(base);
    selection-background-color: #5DADE2;
    selection-color: #1B1B1B;
    outline: none;
}

QListWidget {
    border: 1px solid #C2C2BC; border-radius: 4px;
    background-color: palette(base);
}
QListWidget::item:selected { background-color: #5DADE2; color: #1B1B1B; }

QTableWidget {
    border: 1px solid #C2C2BC;
    background-color: palette(base);
    gridline-color: #D0D0CB;
}
QTableWidget QHeaderView::section {
    background-color: #E8E8E4; border: 1px solid #D0D0CB;
    padding: 4px; font-weight: bold;
}
"""

# --- QSS extra: só quando o tema escuro está ativo --------------------------
QSS_ESCURO = """
QWidget { background-color: #263238; color: #CFD8DC; }
QLabel[class~="dim-label"] { color: #78909C; }
QLabel[class~="versao-cabecalho"] { color: #78909C; }

QFrame { background-color: #263238; border-color: #37474F; }
QFrame[frameShape="4"] { border-top: 1px solid #1B262C; border-bottom: 1px solid #37474F; }

QPushButton {
    background-color: #37474F; color: #ECEFF1;
    border: 1px solid #455A64; border-radius: 4px; padding: 4px 10px;
}
QPushButton:hover { background-color: #455A64; }
QPushButton:pressed { background-color: #263238; }
QPushButton:disabled { background-color: #2E3B41; color: #607D8B; border-color: #37474F; }
QPushButton[class~="flat"] { background-color: transparent; border-color: transparent; }
QPushButton[class~="flat"]:hover { background-color: #37474F; }

QLineEdit, QComboBox {
    background-color: #37474F; color: #ECEFF1; border: 1px solid #455A64;
    border-radius: 4px; padding: 3px 6px;
}
QLineEdit:disabled { background-color: #2E3B41; color: #607D8B; border-color: #37474F; }
QComboBox QAbstractItemView {
    background-color: #37474F; color: #ECEFF1;
    selection-background-color: #1B262C; selection-color: #ECEFF1;
    border: 1px solid #455A64; outline: none;
}

QCheckBox { color: #CFD8DC; }
QCheckBox::indicator {
    width: 16px; height: 16px;
    background-color: #37474F; border: 1px solid #455A64; border-radius: 3px;
}
QCheckBox::indicator:checked { background-color: #5DADE2; border-color: #5DADE2; }

QGroupBox { border: 1px solid #37474F; }

QListWidget {
    background-color: #37474F; color: #ECEFF1; border: 1px solid #455A64;
}
QListWidget::item:selected { background-color: #1B262C; color: #ECEFF1; }

QTableWidget {
    background-color: #1B262C; color: #ECEFF1;
    border: 1px solid #455A64; gridline-color: #37474F;
}
QTableWidget QHeaderView::section {
    background-color: #37474F; color: #ECEFF1; border: 1px solid #455A64;
}

QDialog { background-color: #263238; color: #CFD8DC; }
QMenu { background-color: #37474F; color: #ECEFF1; border: 1px solid #455A64; }
QMenu::item:selected { background-color: #1B262C; }
"""


def aplicar_tema(escuro):
    app = QApplication.instance()
    if app is None:
        return
    app.setPalette(_paleta_escura() if escuro else _paleta_clara())
    app.setStyleSheet(QSS_BASE + (QSS_ESCURO if escuro else ""))
