# SPDX-License-Identifier: GPL-3.0-or-later
"""Textos da interface em PT-BR / EN. A janela principal guarda o idioma
atual (ver preferencias.py) e usa t(chave, idioma) para os textos fixos da
barra superior e do formulário principal.

Escopo desta tradução (ver README/commit para detalhes): a barra superior e
os rótulos/botões estáticos do formulário. Os nomes técnicos que também são
chaves de lógica (tipos de gráfico, paleta, modo de tendência) e as
mensagens de validação dentro de generate_chart continuam só em inglês, para
não arriscar dessincronizar texto de interface com strings usadas em
comparações no código."""

IDIOMA_PADRAO = "pt"

_TEXTOS = {
    # --- Barra superior ------------------------------------------------
    "app_titulo": {"pt": "GraphGenerator", "en": "GraphGenerator"},
    "app_versao": {"pt": "Versão {versao}", "en": "Version {versao}"},
    "tema_escuro": {"pt": "Tema escuro", "en": "Dark theme"},
    "tooltip_bandeira_pt": {"pt": "Português", "en": "Português"},
    "tooltip_bandeira_en": {"pt": "English", "en": "English"},

    # --- Formulário principal -------------------------------------------
    "campo_titulo": {"pt": "Título:", "en": "Title:"},
    "campo_arquivo": {"pt": "Arquivo de entrada (CSV/XLSX):", "en": "Input file (CSV/XLSX):"},
    "botao_selecionar_arquivo": {"pt": "Selecionar arquivo…", "en": "Select data file…"},
    "opcional": {"pt": "Opcional", "en": "Optional"},

    "campo_dimensoes": {"pt": "Dimensões:", "en": "Dimensions:"},
    "campo_selecionar_colunas": {"pt": "Selecionar colunas:", "en": "Select Columns:"},
    "campo_x": {
        "pt": "Valores de X (categóricos/numéricos):",
        "en": "X values (Categorical/Numerical):",
    },
    "campo_y": {"pt": "Valores de Y (só numéricos):", "en": "Y values (Only Numerical):"},
    "campo_z": {"pt": "Valores de Z (só numéricos):", "en": "Z values (Only Numerical):"},

    "campo_tipo_grafico": {"pt": "Tipo de gráfico:", "en": "Chart type:"},
    "campo_resolucao": {"pt": "Resolução (dpi):", "en": "Resolution (dpi):"},
    "campo_tendencia": {"pt": "Linha de tendência:", "en": "Select trendline:"},
    "check_legenda": {"pt": "Mostrar legenda", "en": "Show legend"},
    "check_rotulo": {"pt": "Mostrar valores nos pontos", "en": "Show label mark"},

    "campo_cores": {"pt": "Cores:", "en": "Colors:"},
    "botao_escolher_cor": {"pt": "Escolher cor…", "en": "Pick color…"},

    "campo_rotulo_x": {"pt": "Rótulo do eixo X:", "en": "X-axis label:"},
    "campo_rotulo_y": {"pt": "Rótulo do eixo Y:", "en": "Y-axis label:"},
    "campo_rotulo_z": {"pt": "Rótulo do eixo Z:", "en": "Z-axis label:"},

    "botao_gerar": {"pt": "Gerar gráfico", "en": "Generate chart"},
}


def t(chave, idioma, **kwargs):
    valor = _TEXTOS.get(chave, {}).get(idioma)
    if valor is None:
        valor = _TEXTOS.get(chave, {}).get(IDIOMA_PADRAO, chave)
    return valor.format(**kwargs) if kwargs else valor
