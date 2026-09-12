# Versionamento do GraphGenerator

Mesmo esquema do SolarCalc. A versão segue **MAJOR.MINOR.PATCH** (SemVer)
para o número que importa (o que aparece antes do traço); o `-N` depois do
traço é a *revisão de empacotamento*, no sentido estrito do Debian — só sobe
quando `installer/` muda (control.in, postinst, .desktop, ícones...) sem
nenhuma mudança de código do programa. Toda mudança de código reseta o `-N`
para `-1`.

**Fonte única do número: [`versao.py`](../versao.py)** (`VERSAO = "..."`). É
o mesmo valor que:
- aparece na barra superior do app, ao lado do nome ("Versão 0.1.0-1");
- `installer/build_deb.sh` usa como padrão ao gerar o `.deb`.

`installer/build_deb.sh` recusa rodar se `versao.py` e a primeira linha de
`installer/linux/changelog.Debian` não tiverem o mesmo número — os dois
precisam ser atualizados juntos (ver "Ao gerar um novo `.deb`" abaixo).

```
0.1.0    -1
└─┬─┘    └┬┘
  │       └─ revisão de empacotamento (só installer/ mudou)
  └─ versão do programa (MAJOR.MINOR.PATCH)
```

## Como decidir qual número sobe

A pergunta não é "quanto código mudou" — é **"alguém que já usa o
GraphGenerator hoje vai precisar fazer algo diferente, ou vai ter algo que
parou de funcionar, por causa desta mudança?"**

- **PATCH** (`0.1.0` → `0.1.1`): corrige um bug, sem mudar nenhum
  comportamento que já era esperado.
- **MINOR** (`0.1.0` → `0.2.0`, zera o patch): funcionalidade nova,
  adicionada sem quebrar nada do que já existia.
- **MAJOR** (`0.1.0` → `1.0.0`, zera minor e patch): muda ou remove algo que
  já existia, de um jeito que quem já usa precisa se adaptar (ex.: mudar o
  formato de `~/.config/graphgenerator/config.json` sem migração automática,
  deixar de suportar uma versão de Python/PySide6/SO hoje suportada, mudar
  `/usr/share/graphgenerator` para outro caminho no `.deb`).

Enquanto o MAJOR for `0`, o app está em amadurecimento: mudanças
incompatíveis podem sair como MINOR, mas registre-as com destaque no
changelog. A primeira release considerada estável será a `1.0.0`.

## Ao gerar um novo `.deb`

1. Decida o próximo `MAJOR.MINOR.PATCH` pelas regras acima.
2. Atualize `VERSAO` em `versao.py` para o novo número (com `-1`).
3. Adicione uma entrada no topo de `installer/linux/changelog.Debian`
   (formato Debian padrão: `graphgenerator (X.Y.Z-1) unstable; urgency=low`,
   lista do que mudou, linha `-- Nome <email>  data`) com o **mesmo** número
   do passo 2.
4. Rode `installer/build_deb.sh` (sem argumento já usa o número de
   `versao.py`; ele aborta se o changelog não bater).

Se a mudança for só de empacotamento (ex.: ajustar o `postinst`, um ícone, o
`.desktop`, sem tocar no código), mantenha o `X.Y.Z` e suba só o `-N`
(`0.1.0-1` → `0.1.0-2`).

## Onde o número aparece (não editar à mão)

- `installer/linux/control.in` usa o placeholder `@VERSION@`, preenchido
  pelo `build_deb.sh`.
- A barra superior da interface lê `versao.VERSAO` direto
  (`GraphGenerator.py`).
