'''
Análise semâmtica da linguagem Nesti

Percorre a AST com o padrão Visitor, usadno a tabela de símbolos t_symbols
para verificar escopos e tipos. Os erros são acumulados em uma lista e a 
análise continua, para que todos sejam reportados de uma vez

Visitar uma expressão devolve o tipo dela ('int' ou 'bool'). O valor None
indica um erro já reportado; quem o recebe não gera nova mensagem
'''

from Nesti_visitor import NestiVisitor
from Nesti_tabela_simbolos import TabelaSimbolos, Simbolo
from utils.Nesti_impressao import _cor

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

# Regras de tipo dos operadores: operador -> (tipo exigido dos operandos, tipo do resultado)
# Na igualdade, None indica que os operandos podem ser int ou bool, desde que iguais
OPERADORES_BINARIOS = {
  '+':  ('int', 'int'),
  '-':  ('int', 'int'),
  '*':  ('int', 'int'),
  '/':  ('int', 'int'),
  '<':  ('int', 'bool'),
  '<=': ('int', 'bool'),
  '>':  ('int', 'bool'),
  '>=': ('int', 'bool'),
  '==': (None, 'bool'),
  '!=': (None, 'bool'),
  '&&': ('bool', 'bool'),
  '||': ('bool', 'bool'),
}

OPERADORES_UNARIOS = {
  '-': ('int', 'int'),
  '!': ('bool', 'bool'),
}

# Tipos que podem ser lidos, impressos ou usados como valor
TIPOS_DE_VALOR = ('int', 'bool')

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
    self.erros.append(_cor(f"Erro semântico na linha {lineno}: {mensagem}", 'erro'))
    
  def instalar(self, simbolo): 
    if not self.t_symbols.instalar(simbolo):
      self.erro(simbolo.lineno, f"{simbolo.nome}' já foi declarado neste escopo")
  
  def fechar_escopo(self): 
    escopo = self.t_symbols.fechar_escopo()
    self.escopos_fechados.append(escopo)
    return escopo
  
  def exigir_tipo(self, tipo, esperado, lineno, descricao):
    '''Reporta erro se o tipo for conhecido e diferente do esperado'''
    if tipo is not None and tipo != esperado: 
      self.erro(lineno, f"{descricao} deve ser {esperado}, mas é {tipo}")
  
  def buscar_variavel(self, nome, lineno):
    '''Busca um nome que precisa ser variável ou parâmetro. Devolve o símbolo ou None'''
    simbolo = self.t_symbols.buscar(nome)
    if simbolo is None:
      self.erro(lineno, f"'{nome}' não foi declarado")
      return None
    if simbolo.categoria == 'funcao':
      self.erro(lineno, f"'{nome}' é uma função, não uma variável")
      return None
    return simbolo
  
  def visitar_comandos(self, comandos):
    for comando in comandos:
      self.visitar(comando)
  
  # -------- Programa e Declarações --------
  def visitar_Programa(self, no): 
    self.t_symbols.abrir_escopo(f"programa {no.nome}")
    for declaracao in no.variaveis: 
      self.visitar(declaracao)
    for funcao in no.funcoes: 
      self.visitar(funcao)
    self.visitar_comandos(no.comandos)
    escopo = self.fechar_escopo()
    no.num_variaveis = escopo.num_variaveis
    
  def visitar_DeclVariavel(self, no):
    # a inicialização é verificada antes de a variável existir:
    # em "int x = x + 1;", o x da direita não é o que está sendo declarado
    if no.inicializacao is not None:
      tipo = self.visitar(no.inicializacao)
      self.exigir_tipo(tipo, no.tipo, no.lineno,
                       f"a inicialização de '{no.nome}'")
      
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
    
    escopo = self.fechar_escopo()
    no.num_variaveis = escopo.num_variaveis
  
  # ----- Comandos -----------
  def visitar_Atribuicao(self, no):
    simbolo = self.buscar_variavel(no.nome, no.lineno)
    tipo = self.visitar(no.expressao)
    if simbolo is not None:
      self.exigir_tipo(tipo, simbolo.tipo, no.lineno,
                       f"o valor atribuído a '{no.nome}'")
    no.simbolo = simbolo
    
  def visitar_Condicional(self, no):
    tipo = self.visitar(no.condicao)
    self.exigir_tipo(tipo, 'bool', no.lineno, 'a condição do if')
    self.visitar_comandos(no.entao)
    if no.senao is not None:
      self.visitar_comandos(no.senao)
  
  def visitar_Repeticao(self, no):
    tipo = self.visitar(no.condicao)
    self.exigir_tipo(tipo, 'bool', no.lineno, 'a condição do while')
    self.visitar_comandos(no.corpo)
  
  def visitar_Leitura(self, no):
    # toda variável é int ou bool, então basta ela existir e ser uma variável 
    no.simbolos = [self.buscar_variavel(nome, no.lineno) for nome in no.nomes]
  
  def visitar_Escrita(self, no):
    for expressao in no.expressoes:
      tipo = self.visitar(expressao)
      if tipo is not None and tipo not in TIPOS_DE_VALOR:
        self.erro(no.lineno, f'o argumento do print deve ser int ou bool, mas é tipo {tipo}')
  
  # ----- Expressões ----------
  def visitar_Literal(self, no):
    return no.tipo
  
  def visitar_Variavel(self, no):
    simbolo = self.buscar_variavel(no.nome, no.lineno)
    no.simbolo = simbolo
    no.tipo = simbolo.tipo if simbolo is not None else None
    return no.tipo
  
  def visitar_OpUnaria(self, no):
    exigido, resultado = OPERADORES_UNARIOS[no.op]
    tipo = self.visitar(no.operando)
    self.exigir_tipo(tipo, exigido, no.lineno, f"o operando de '{no.op}'")
    no.tipo = resultado
    return resultado
  
  def visitar_OpBinaria(self, no):
    exigido, resultado = OPERADORES_BINARIOS[no.op]
    tipo_esq = self.visitar(no.esquerda)
    tipo_dir = self.visitar(no.direita)
    
    if exigido is None:
      # igualdade e diferença: operandos no mesmo tipo
      if tipo_esq is not None and tipo_dir is not None and tipo_esq != tipo_dir:
        self.erro(no.lineno,
                  f"os operandos de '{no.op}' devem ter o mesmo tipo, mas são {tipo_esq} e {tipo_dir}")
    else: 
      self.exigir_tipo(tipo_esq, exigido, no.lineno, f"o operando esquedo de '{no.op}'")
      self.exigir_tipo(tipo_dir, exigido, no.lineno, f"o operando direito de '{no.op}'")
    no.tipo = resultado
    return resultado