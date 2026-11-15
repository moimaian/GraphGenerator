#!/usr/bin/env bash
# Monta o GraphGenerator.deb — pacote Debian/Ubuntu do GraphGenerator.
#
#   installer/build_deb.sh
#
# O .deb pronto é gravado na RAIZ do repositório (./GraphGenerator.deb), ao
# lado do README — não há pasta dist/. A pasta installer/ contém só a
# "receita" de empacotamento.
#
# A versão vem de versao.py (fonte única — ver installer/VERSIONING.md).
# Este script ABORTA se versao.py e a primeira linha de
# installer/linux/changelog.Debian não tiverem o mesmo número: os dois
# precisam ser atualizados juntos a cada mudança que altere a versão.
#
# Requisitos de quem constrói: dpkg-deb, fakeroot, python3 + PySide6
# (só para gerar os ícones). Não precisa de root.
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
LIN="$RAIZ/installer/linux"
APP=/usr/share/graphgenerator
VER="$(python3 -c "import sys; sys.path.insert(0, '$RAIZ'); import versao; print(versao.VERSAO)")"
VER_CHANGELOG="$(sed -n '1s/^graphgenerator (\(.*\)).*/\1/p' "$LIN/changelog.Debian")"

if [ "$VER" != "$VER_CHANGELOG" ]; then
    echo "build_deb.sh: versao.py ($VER) e o topo de" >&2
    echo "              installer/linux/changelog.Debian ($VER_CHANGELOG) estão em" >&2
    echo "              versões diferentes — atualize os dois antes de empacotar" >&2
    echo "              (ver installer/VERSIONING.md)." >&2
    exit 1
fi

SAIDA="$RAIZ/GraphGenerator.deb"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

echo ">> GraphGenerator $VER  ->  $SAIDA"
mkdir -p "$STAGE/DEBIAN" \
         "$STAGE$APP" \
         "$STAGE/usr/bin" \
         "$STAGE/usr/share/applications" \
         "$STAGE/usr/share/pixmaps" \
         "$STAGE/usr/share/doc/graphgenerator"

# --- arquivos do app --------------------------------------------------
# App de arquivo único (GraphGenerator.py) + módulos irmãos (versionamento,
# idioma, preferências, tema) + a arte em Midia/.
cp "$RAIZ/GraphGenerator.py" "$RAIZ/versao.py" "$RAIZ/i18n.py" \
   "$RAIZ/preferencias.py" "$RAIZ/estilo.py" "$STAGE$APP/"
cp -r "$RAIZ/Midia" "$STAGE$APP/"
[ -f "$RAIZ/README.md" ] && cp "$RAIZ/README.md" "$STAGE$APP/"
[ -f "$RAIZ/LICENSE" ] && cp "$RAIZ/LICENSE" "$STAGE$APP/"
find "$STAGE$APP" -name __pycache__ -type d -prune -exec rm -rf {} +
find "$STAGE$APP" -name '*.pyc' -delete

# --- lançador /usr/bin/graphgenerator ---------------------------------
# Roda com o python do venv criado pelo postinst (graphgenerator-setup), não
# com o python3 do sistema: distros recentes bloqueiam "pip install" global
# (PEP 668). Dentro de um venv, o bootstrap embutido no GraphGenerator.py
# (que serve a quem roda direto do código-fonte) detecta que já está num
# ambiente isolado e não faz mais nada.
cat > "$STAGE/usr/bin/graphgenerator" <<EOF
#!/bin/sh
VENV=/usr/lib/graphgenerator/venv
if [ ! -f "\$VENV/.graphgenerator-ok" ]; then
    MSG="GraphGenerator: o ambiente Python ainda nao foi preparado. Com internet, rode no terminal:  sudo graphgenerator-setup"
    echo "\$MSG" >&2
    if [ -n "\${DISPLAY:-}\${WAYLAND_DISPLAY:-}" ]; then
        if command -v zenity >/dev/null 2>&1; then zenity --error --no-markup --text="\$MSG" 2>/dev/null || true
        elif command -v notify-send >/dev/null 2>&1; then notify-send "GraphGenerator" "\$MSG" || true
        fi
    fi
    exit 1
fi
exec "\$VENV/bin/python3" $APP/GraphGenerator.py "\$@"
EOF

# --- graphgenerator-setup (cria/repara o venv; chamado pelo postinst) ---
install -m 0755 "$LIN/graphgenerator-setup" "$STAGE/usr/bin/graphgenerator-setup"

# --- .desktop (Menu) -----------------------------------------------
cp "$LIN/graphgenerator.desktop" "$STAGE/usr/share/applications/graphgenerator.desktop"

# --- ícones -------------------------------------------------------
python3 "$LIN/gen_icons.py" "$RAIZ/Midia/GraphGenerator_Icon.png" "$STAGE/usr/share/icons/hicolor"
cp "$STAGE/usr/share/icons/hicolor/256x256/apps/graphgenerator.png" "$STAGE/usr/share/pixmaps/graphgenerator.png"

# --- doc: copyright + changelog ---------------------------------
cp "$LIN/copyright" "$STAGE/usr/share/doc/graphgenerator/copyright"
gzip -9 -n -c "$LIN/changelog.Debian" > "$STAGE/usr/share/doc/graphgenerator/changelog.Debian.gz"

# --- permissões conforme a policy -----------------------------
find "$STAGE" -type d -exec chmod 0755 {} +
find "$STAGE" -type f -exec chmod 0644 {} +
chmod 0755 "$STAGE/usr/bin/graphgenerator" "$STAGE/usr/bin/graphgenerator-setup" "$STAGE$APP/GraphGenerator.py"

# --- DEBIAN/control + scripts -------------------------------
SIZE_KB="$(du -sk "$STAGE" | cut -f1)"
sed -e "s/@VERSION@/$VER/" -e "s/@SIZE@/$SIZE_KB/" "$LIN/control.in" > "$STAGE/DEBIAN/control"
install -m 0755 "$LIN/postinst" "$STAGE/DEBIAN/postinst"
install -m 0755 "$LIN/postrm"   "$STAGE/DEBIAN/postrm"

# --- empacota ---------------------------------------------
fakeroot dpkg-deb --build --root-owner-group "$STAGE" "$SAIDA"

echo
dpkg-deb --info "$SAIDA"
echo ">> pronto: $SAIDA  ($(du -h "$SAIDA" | cut -f1))"
echo "   instalar:  sudo apt install \"$SAIDA\""
echo "   (ou:       sudo dpkg -i \"$SAIDA\" && sudo apt -f install)"
if command -v lintian >/dev/null 2>&1; then
    echo
    echo ">> lintian (ignorando dir-or-file-in-opt / opcionais):"
    lintian --suppress-tags dir-or-file-in-opt,no-manual-page "$SAIDA" || true
fi
