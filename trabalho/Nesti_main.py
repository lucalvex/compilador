import sys
from Nesti_lexer import lexer, reiniciar_lexer, verificar_lexico
from Nesti_parser import parser, ErroSintatico
from Nesti_semantico import AnalisadorSemantico
from utils.Nesti_impressao import imprimir_tokens, imprimir_ast, imprimir_tabela

OPCOES_VALIDAS = {'--tokens', '--ast', '--tabela'}
USO = "Uso: python Nesti_main.py <arquivo.nesti> [--tokens] [--ast] [--tabela]"

def falhar(erros):
  '''Imprime os erros e encerra o compilador indicando falha.'''
  for erro in erros:
    print(erro)
  sys.exit(1)  # Essa o programa imediatamente e informa que terminou com erro 
  
# TODO:TROCAR O ARGV - temos que usar o modo de redirecionamento 
def main(): 
  argumentos = sys.argv[1:] # pega todos os argumentos, menos o nome do script
  opcoes = [a for a in argumentos if a.startswith('--')]
  arquivos = [a for a in argumentos if not a.startswith('--')]
  arquivos = [a for a in argumentos if not a.startswith('--')] # cria uma lista só com os argumentos que não começam com --
  
  desconhecidas = [o for o in opcoes if o not in OPCOES_VALIDAS]
  if desconhecidas:
    falhar([f"Opção desconhecida: {', '.join(desconhecidas)}", USO])
    
  if len(arquivos) != 1:
    falhar([USO])
  
  modo_tokens = '--tokens' in opcoes
  modo_ast = '--ast' in opcoes
  modo_tabela = '--tabela' in opcoes
  
  with open(arquivos[0], encoding='utf-8') as arquivo: 
    codigo = arquivo.read()
  
  if modo_tokens: 
    imprimir_tokens(codigo)
    return
  
  # 1. análise léxica: lê o arquivo inteiro antes do parser, para mostrar
  #    todos os erros léxicos e não gerar erros sintáticos falsos
  erros = verificar_lexico(codigo)
  if erros:
    falhar(erros)
  
  # 2. análise sintática e construção da AST
  reiniciar_lexer()  # o input() do PLY não zera o contador de linhas
  try: 
    ast = parser.parse(codigo, lexer=lexer) # executa a análise sintática
  except ErroSintatico as erro:
    falhar([str(erro)])
  
  if modo_ast: 
    imprimir_ast(ast)
  
  # 3. análise semântica
  analisador = AnalisadorSemantico()
  erros = analisador.analisar(ast)

  if modo_tabela:
    imprimir_tabela(analisador.escopos_fechados)

  if erros:
    falhar(erros)
  
if __name__ == '__main__': 
  main()