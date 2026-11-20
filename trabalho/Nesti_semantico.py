'''
Análise semâmtica da linguagem Nesti

Percorre a AST com o padrão Visitor, usadno a tabela de símbolos t_symbols
para verificar escopos e tipos. Os erros são acumulados em uma lista e a 
análise continua, para que todos sejam reportados de uma vez
'''

from Nesti_visitor import NestiVisitor
from Nesti_tabela_simbolos import TabelaSimbolos, Simbolo

# Registro de ativação da MEPA (slides "Código MEPA: sub-rotinas"):
#   D[k]+0 ...        variáveis locais
#   D[k]-1            link estático (D[k-1])
#   D[k]-2            nível léxico do chamador (k')
#   D[k]-3            link dinâmico (D[k'])
#   D[k]-4            endereço de retorno
#   D[k]-5 ...        argumentos, empilhados na ordem da declaração:
#                     o primeiro fica em D[k]-(4+n) e o último em D[k]-5
#   D[k]-(5+n)        valor de retorno, reservado pelo chamador com AMEM 1
TAMANHO_CONTROLE = 4

class AnalisadorSemantico(NestiVisitor): 

  def __init__(self):
    self.t_symbols = TabelaSimbolos()
    self.erros = []
    self.escopos_fechados = []    # para p modo --tabela
    
  def analisar(self, programa):
    self.visitar(programa)
    return self.erros
  
  # ------- Auxiliares ---------
  def erro(self, lineno, mensagem): 
    self.erros.append(f"Erro semântico na linha {lineno}: {mensagem}")
    
  def instalar(self, simbolo): 
    if not self.t_symbols.instalar(simbolo):
      self.erro(simbolo.lineno, f"'{simbolo.nome}' já foi declarado neste escopo")
  
  def fechar_escopo(self): 
    escopo = self.t_symbols.fechar_escopo()
    self.escopos_fechados.append(escopo)
    return escopo
  
  # -------- Programa e Declarações --------
  def visitar_Programa(self, no): 
    self.t_symbols.abrir_escopo(f"programa {no.nome}")
    for declaracao in no.variaveis: 
      self.visitar(declaracao)
    for funcao in no.funcoes: 
      self.visitar(funcao)
    # comandos: parte A
    escopo = self.fechar_escopo()
    no.num_variaveis = escopo.num_variaveis
    
  def visitar_DeclVariavel(self, no):
    # tipo da inicialização: parte D
    simbolo = Simbolo(no.nome, 'variavel', no.tipo,
                      self.t_symbols.nivel_atual,
                      self.t_symbols.novo_deslocamento(),
                      lineno=no.lineno)
    self.instalar(simbolo)
    no.simbolo = simbolo
  
  def visitar_DeclFuncao(self, no):
    num_parametro = len(no.parametros)
    
    # 1. o nome da função vai para o escopo atual, antes do corpo (permite recursão);
    #    o deslocamento da função é a posição do valor de retorno: -(5 + n)
    funcao = Simbolo(no.nome, 'funcao', no.tipo_retorno,
                     self.t_symbols.nivel_atual + 1,
                     deslocamento=-(num_parametro + TAMANHO_CONTROLE + 1),
                     parametros=[parametro.tipo for parametro in no.parametros],
                     lineno=no.lineno)
    self.instalar(funcao)
    no.simbolo = funcao
    
    # 2. o corpo tem o próprio escopo
    self.t_symbols.abrir_escopo(f"função {no.nome}")
    
    # parâmetro i (a partir de 0): -(n + 4) + i, do primeiro em -(4 + n) ao último em -5
    for i, parametro in enumerate(no.parametros):
      simbolo = Simbolo(parametro.nome, 'parametro', parametro.tipo,
                         self.t_symbols.nivel_atual,
                         -(num_parametro + TAMANHO_CONTROLE) + i,
                         lineno=parametro.lineno)
      self.instalar(simbolo)
      parametro.simbolo = simbolo
    
    for declaracao in no.variaveis: 
      self.visitar(declaracao)
    for funcao_interna in no.funcoes:
      self.visitar(funcao_interna)
    # comando e regras de retorno: partes A e B
    
    escopo = self.fechar_escopo()
    no.num_variaveis = escopo.num_variaveis
  