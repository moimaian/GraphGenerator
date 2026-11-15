# SPDX-License-Identifier: GPL-3.0-or-later
"""Versão do GraphGenerator — única fonte de verdade.

É importada tanto pela interface (mostrada na barra superior, ao lado do
nome: "Versão X.Y.Z-N") quanto por qualquer script de empacotamento futuro
(.deb/.exe), que deve usá-la como padrão ao gerar o instalador.

Segue o mesmo esquema do SolarCalc: MAJOR.MINOR.PATCH (SemVer) para o número
que importa (antes do traço); o "-N" depois do traço é a revisão de
empacotamento (sobe só quando algo em torno do app muda — ícone, instalador,
.desktop — sem nenhuma mudança de código do programa; toda mudança de código
reseta o "-N" para "-1").

Como decidir qual número sobe:
- PATCH: corrige um bug sem mudar nenhum comportamento esperado.
- MINOR: funcionalidade nova, sem quebrar nada do que já existia.
- MAJOR: muda ou remove algo que já existia, de um jeito que quem já usa
  precisa se adaptar (ex.: mudar o formato de um arquivo salvo por uma
  versão antiga sem migração automática).

Enquanto o MAJOR for 0, o app está em amadurecimento: mudanças incompatíveis
podem sair como MINOR, mas devem ser destacadas na descrição da mudança. A
primeira release considerada estável será a 1.0.0.
"""

VERSAO = "0.1.1-1"
