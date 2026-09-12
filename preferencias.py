# SPDX-License-Identifier: GPL-3.0-or-later
"""Preferências de interface do GraphGenerator (idioma e tema), persistidas
em ~/.config/graphgenerator/config.json para serem recuperadas na próxima
inicialização. Na primeira execução (nenhuma preferência salva ainda), os
padrões são: idioma Português e tema escuro.

Mesmo esquema do SolarCalc: funciona igual em Linux e Windows, já que
os.path.expanduser("~") resolve para o HOME do usuário nos dois sistemas."""
import json
import os

# GRAPHGENERATOR_CONFIG_DIR permite apontar para um config.json isolado (usado
# em testes/desenvolvimento), sem arriscar sobrescrever a configuração real
# do usuário em ~/.config/graphgenerator.
_CONFIG_DIR = os.environ.get("GRAPHGENERATOR_CONFIG_DIR") or os.path.join(
    os.path.expanduser("~"), ".config", "graphgenerator"
)
_CONFIG_PATH = os.path.join(_CONFIG_DIR, "config.json")

IDIOMA_PADRAO = "pt"
TEMA_ESCURO_PADRAO = True

idioma_atual = IDIOMA_PADRAO
tema_escuro_ativo = TEMA_ESCURO_PADRAO


def carregar():
    """Lê as preferências salvas em disco (chamar uma vez, na inicialização
    do app)."""
    global idioma_atual, tema_escuro_ativo
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        conteudo = {}

    idioma_atual = conteudo.get("idioma", IDIOMA_PADRAO)
    tema_escuro_ativo = conteudo.get("tema_escuro", TEMA_ESCURO_PADRAO)


def _salvar():
    try:
        os.makedirs(_CONFIG_DIR, exist_ok=True)
        with open(_CONFIG_PATH, "w", encoding="utf-8") as arquivo:
            json.dump(
                {"idioma": idioma_atual, "tema_escuro": tema_escuro_ativo},
                arquivo,
                ensure_ascii=False,
                indent=2,
            )
    except OSError:
        # Persistência é uma conveniência — se o disco recusar a escrita, o
        # app continua funcionando normalmente só sem lembrar dos valores.
        pass


def definir_idioma(idioma):
    global idioma_atual
    idioma_atual = idioma
    _salvar()


def definir_tema_escuro(ativo):
    global tema_escuro_ativo
    tema_escuro_ativo = bool(ativo)
    _salvar()
