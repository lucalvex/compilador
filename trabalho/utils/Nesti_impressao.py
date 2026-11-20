'''
Nesti_impressao.py — Funções de depuração do compilador Nesti

imprimir_tokens: mostra os tokens reconhecidos pelo léxico.
imprimir_ast: desenha a árvore sintática abstrata com linhas de ligação.
imprimir_tabela: mostra os escopos da tabela de símbolos.

As cores só são usadas quando a saída é o terminal. Quando a saída é
redirecionada para um arquivo, o texto sai sem códigos de cor.
'''
import os
import sys
from Nesti_lexer import lexer, reserved, reiniciar_lexer
from Nesti_ast import NestiNode


# ---------- Cores ----------
USAR_CORES = sys.stdout.isatty()

if USAR_CORES and sys.platform == 'win32':
  os.system('')  # ativa o suporte a códigos de cor no console do Windows

CORES = {
  'classe':    '1;36',  # ciano em negrito: nome do nó
  'linha':     '33',    # amarelo: número da linha
  'campo':     '35',    # magenta: nome do campo
  'valor':     '32',    # verde: valor de um campo simples
  'ramo':      '90',    # cinza: linhas de ligação da árvore
  'reservada': '1;34',  # azul em negrito: palavras reservadas
  'token':     '36',    # ciano: demais tokens
  'erro':      '1;31',  # vermelho em negrito: erros
}

def _cor(texto, tipo):
  '''Envolve o texto com o código de cor do tipo indicado.'''
  if not USAR_CORES:
    return texto
  return f"\033[{CORES[tipo]}m{texto}\033[0m"

# ---------- Tokens ----------
def imprimir_tokens(codigo):
  '''Mostra linha, tipo e valor de cada token e, no final, os erros léxicos.'''
  tipos_reservados = set(reserved.values())
  reiniciar_lexer()
  lexer.input(codigo)
  print(f"{'LINHA':>5}  {'TIPO':<10}  VALOR")
  for tok in lexer:
    linha = _cor(f"{tok.lineno:>5}", 'linha')
    estilo = 'reservada' if tok.type in tipos_reservados else 'token'
    tipo = _cor(f"{tok.type:<10}", estilo)
    print(f"{linha}  {tipo}  {_cor(repr(tok.value), 'valor')}")
  for erro in lexer.erros:
    print(_cor(erro, 'erro'))

# ---------- Árvore sintática ----------
def imprimir_ast(no):
    '''Imprime a árvore com linhas de ligação entre pais e filhos.'''
    print(_descricao(no))
    _imprimir_filhos(no, '')

def _descricao(no):
  '''Monta a linha de um nó: nome da classe, linha e campos simples.'''
  simples = []
  for campo in no.campos:
    valor = getattr(no, campo)
    if not isinstance(valor, (NestiNode, list)):
      simples.append(f"{_cor(campo, 'campo')} = {_cor(repr(valor), 'valor')}")
  classe = _cor(type(no).__name__, 'classe')
  linha = _cor(f"[linha {no.lineno}]", 'linha')
  texto = f"{classe} {linha} {' '.join(simples)}"
  return texto.rstrip()


def _imprimir_filhos(no, prefixo):
  '''Imprime os campos de um nó que são nós ou listas, com as ligações.'''
  filhos = [(campo, getattr(no, campo)) for campo in no.campos
            if isinstance(getattr(no, campo), (NestiNode, list))]

  for i, (campo, valor) in enumerate(filhos):
    ultimo = (i == len(filhos) - 1)
    conector = '└── ' if ultimo else '├── '
    extensao = '    ' if ultimo else '│   '

    if isinstance(valor, list):
      print(f"{_cor(prefixo + conector, 'ramo')}{_cor(campo, 'campo')} ({len(valor)})")
      for j, item in enumerate(valor):
        item_ultimo = (j == len(valor) - 1)
        conector_item = '└── ' if item_ultimo else '├── '
        extensao_item = '    ' if item_ultimo else '│   '
        ramo = _cor(prefixo + extensao + conector_item, 'ramo')
        if isinstance(item, NestiNode):
          print(f"{ramo}{_descricao(item)}")
          _imprimir_filhos(item, prefixo + extensao + extensao_item)
        else:
          print(f"{ramo}{_cor(repr(item), 'valor')}")
    else:
      print(f"{_cor(prefixo + conector, 'ramo')}{_cor(campo, 'campo')}: {_descricao(valor)}")
      _imprimir_filhos(valor, prefixo + extensao)

# ---------- Tabela de símbolos ----------
def imprimir_tabela(escopos):
  '''Mostra o conteúdo de cada escopo, na ordem em que foram fechados.'''
  for escopo in escopos:
    print(_cor(f"Escopo: {escopo.nome} (nível {escopo.nivel})", 'classe'))
    print(f"  {'NOME':<14}{'CATEGORIA':<11}{'TIPO':<6}{'NÍVEL':<7}{'DESLOC':<8}PARÂMETROS")
    for s in escopo.simbolos.values():
      parametros = '' if s.parametros is None else str(s.parametros)
      print(f"  {s.nome:<14}{s.categoria:<11}{s.tipo:<6}{s.nivel:<7}"
            f"{str(s.deslocamento):<8}{parametros}")
    print()