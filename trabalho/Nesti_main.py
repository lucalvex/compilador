import sys
from Nesti_lexer import lexer
from Nesti_parser import parser, ErroSintatico
from utils.Nesti_impressao import imprimir_tokens, imprimir_ast


def imprimir_tokens(codigo): 
  '''Modo de depuração: mostra cada token reconhecido pelo léxico'''
  lexer.input(codigo)
  print(f"{'LINHA':>5} {'TIPO':<10} VALOR")
  for t in lexer: 
    # :>5 alinha à direita em 5 posições
    # :<10 alinha à esquerda em 10
    # !r mostra o valor com aspas 
    print(f"{t.lineno:>5} {t.type:<10} {t.value!r}")

# TODO:TROCAR O ARGV - temos que usar o modo de redirecionamento 
def main(): 
  argumentos = sys.argv[1:] # pega todos os argumentos, menos o nome do script
  modo_tokens = '--tokens' in argumentos    # return true se a opção foi passada
  modo_ast = '--ast' in argumentos
  arquivos = [a for a in argumentos if not a.startswith('--')] # cria uma lista só com os argumentos que não começam com --
  
  if len(arquivos) != 1:
    print("Uso: python Nesti_main.py <arquivo.nesti> [--tokens] [--ast]")
    sys.exit(1)  # Essa o programa imediatamente e informa que terminou com erro 
  
  with open(arquivos[0], encoding='utf-8') as arquivo: 
    codigo = arquivo.read()
  
  if modo_tokens: 
    imprimir_tokens(codigo)
    return
  
  try: 
    ast = parser.parse(codigo, lexer=lexer) # executa a análise sintática
  except ErroSintatico as erro:
    print(erro)
    sys.exit(1)
  
  if modo_ast: 
    imprimir_ast(ast)
  
if __name__ == '__main__': 
  main()