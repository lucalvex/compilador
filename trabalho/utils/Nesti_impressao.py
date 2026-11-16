'''
- Nesti_impressao.py — Funções de depuração do compilador Nesti
- imprimir_tokens: mostra os tokens reconhecidos pelo léxico
- imprimir_ast: desenha a árvore sintática abstrata com linhas de ligação
'''
from Nesti_lexer import lexer
from Nesti_ast import NestiNode

def imprimir_tokens(codigo):
  '''Mostra linha, tipo e valor de cada token reconhecido pelo léxico.'''
  lexer.input(codigo)
  print(f"{'LINHA':>5}  {'TIPO':<10}  VALOR")
  for tok in lexer:
    print(f"{tok.lineno:>5}  {tok.type:<10}  {tok.value!r}")

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
      simples.append(f'{campo} = {valor!r}')
  texto = f"{type(no).__name__} [linha {no.lineno}] {' '.join(simples)}"
  return texto.rstrip # Remove os espaços do final da string

def _imprimir_filhos(no, prefixo):
  '''Imprime os campos de um nó que são nós ou listas, com as ligações.'''
  filhos = [(campo, getattr(no, campo)) for campo in no.campos
            if isinstance(getattr(no, campo), (NestiNode, list))]

  for i, (campo, valor) in enumerate(filhos):
    ultimo = (i == len(filhos) - 1)
    conector = '└── ' if ultimo else '├── '
    extensao = '    ' if ultimo else '│   '

    if isinstance(valor, list):
      print(f"{prefixo}{conector}{campo} ({len(valor)})")
      for j, item in enumerate(valor):
        item_ultimo = (j == len(valor) - 1)
        conector_item = '└── ' if item_ultimo else '├── '
        extensao_item = '    ' if item_ultimo else '│   '
        if isinstance(item, NestiNode):
          print(f"{prefixo}{extensao}{conector_item}{_descricao(item)}")
          _imprimir_filhos(item, prefixo + extensao + extensao_item)
        else:
          print(f"{prefixo}{extensao}{conector_item}{item!r}")
    else:
      print(f"{prefixo}{conector}{campo}: {_descricao(valor)}")
      _imprimir_filhos(valor, prefixo + extensao)