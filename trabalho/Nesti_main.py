import sys
from Nesti_lexer import lexer
from Nesti_parser import parser


def imprimir_tokens(codigo): 
  '''Modo de depuração: mostra cada token reconhecido pelo léxico'''
  lexer.input(codigo)
  print(f"{'LINHA':>5} {'TIPO':<10} VALOR")
  for t in lexer: 
    # :>5 alinha à direita em 5 posições
    # :<10 alinha à esquerda em 10
    # !r mostra o valor com aspas 
    print(f"{t.lineno:>5} {t.type:<10} {t.value!r}")

def main(): 
  argumentos = sys.argv[1:] # pega todos os argumentos, menos o nome do script
  modo_tokens = '--tokens' in argumentos    # return true se a opção foi passada
  arquivos = [a for a in argumentos if not a.startswith('--')] # cria uma lista só com os argumentos que não começam com --
  
  if len(arquivos) != 1:
    print("Uso: python Nesti_main.py <arquivo.nesti>")
    sys.exit(1)  # Essa o programa imediatamente e informa que terminou com erro 
  
  with open(arquivos[0], encoding='utf-8') as arquivo: 
    codigo = arquivo.read()
  
  if modo_tokens: 
    imprimir_tokens(codigo)
    return
    
  parser.parse(codigo, lexer=lexer) # executa a análise sintática
  
if __name__ == '__main__': 
  main()