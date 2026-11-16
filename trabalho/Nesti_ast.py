'''
- Cada classe representa uma construção com significado no programa
- Delimitadores (parâteses, chaves, ponto e víngula) não geram nós
- Sequência (declarações, comandos, parâmetros, argumentos) são listas Python
- Todo nó guarda a linha (lineno) para as mensagens de erro
- O atributo de classe "campos" lista os atributos que formam a árvore; ele é usado pelo impressor e pelas travessias

'''

class NestiNode:
  '''Classe base de todos os nós da AST'''
  campos = ()
  
  def __init__(self, lineno):
    self.lineno = lineno
    
# ------- Programa e Declarações -----------
class Programa(NestiNode):
  campos = ('nome', 'variaveis', 'funcoes', 'comandos')
  
  def __init__(self, nome, variaveis, funcoes, comandos, lineno):
    super().__init__(lineno)
    self.nome = nome              # str
    self.variaveis = variaveis    # list[DeclVariavel]
    self.funcoes = funcoes        # list[DeclFuncao]
    self.comandos = comandos      # list[comando]
    
class DeclVariavel(NestiNode):
  campos = ('tipo', 'nome', 'inicializacao')
  
  def __init__(self, tipo, nome, inicializacao, lineno):
    super().__init__(lineno)
    self.tipo = tipo                      # 'int' ou 'bool'
    self.nome = nome                      # str
    self.inicializacao = inicializacao    # expressão ou None
    
class DeclFuncao(NestiNode):
  campos = ('nome', 'parametros', 'tipo_retorno', 'variaveis', 'funcoes', 'comandos')
  
  def __init__(self, nome, parametros, tipo_retorno, variaveis, funcoes, comandos, lineno):
    super().__init__(lineno)
    self.nome = nome                    # str
    self.parametros = parametros        # list[Parametro]
    self.tipo_retorno = tipo_retorno    # 'int', 'bool' ou 'void'
    self.variaveis = variaveis          # list[DeclVariavel]
    self.funcoes = funcoes              # list[DeclFuncao]
    self.comandos = comandos            # list[comando]
    
class Parametro(NestiNode):
  campos = ('tipo', 'nome')
  
  def __init__(self, tipo, nome, lineno):
    super().__init__(lineno)
    self.tipo = tipo    # 'int' ou 'bool'
    self.nome = nome    # str
    
# -------- Comandos --------------
class Atribuicao(NestiNode):
  campos = ('nome', 'expressao')
  
  def __init__(self, nome, expressao, lineno):
    super().__init__(lineno)
    self.nome = nome              # str: variável que recebe o valor
    self.expressao = expressao    # expressao
    
class Condicional(NestiNode): 
  campos = ('condicao', 'entao', 'senao')
  
  def __init__(self, condicao, entao, senao, lineno):
    super().__init__(lineno)
    self.condicao = condicao    # expressao
    self.entao = entao          # list[comando]
    self.senao = senao          # list[comando] ou None

class Repeticao(NestiNode):
  campos = ('condicao', 'corpo')
  
  def __init__(self, condicao, corpo, lineno):
    super().__init__(lineno)
    self.condicao = condicao    # expressão
    self.corpo = corpo          # list[comando]
    
class Retorno(NestiNode):
  campos = ('expressao',)
  
  def __init__(self, expressao, lineno):
    super().__init__(lineno)
    self.expressao = expressao   # expressão ou None
    
class Leitura(NestiNode):
  campos = ('nomes',)
  
  def __init__(self, nomes, lineno):
    super().__init__(lineno)
    self.nomes = nomes           # list[str]: variáveis que recebem os valoes 
    
class Escrita(NestiNode):
  campos = ('expressoes',)
  
  def __init__(self, expressoes, lineno):
    super().__init__(lineno)
    self.expressoes = expressoes  # list[expressão]
    
class ComandoChamada(NestiNode): 
  campos = ('chamada',)           # É uma tupla com um elemento: a string 'chamada'
  
  def __init__(self, chamada, lineno):
    super().__init__(lineno)
    self.chamada = chamada        # Chamada (valor de retorno, se houver, é descartado)
    
# ------ Expressões -------------
class OpBinaria(NestiNode):
  '''
  OpBinaria representa todos operadores que atua sobre dois valor
  '''
  campos = ('op', 'esquerda', 'direita')
  
  def __init__(self, op, esquerda, direita, lineno):
    super().__init__(lineno)
    self.op = op                   # '+', '-', '*', '/', '<=', '>', '>=', '==', '!=', '&&', '||'
    self.esquerda = esquerda       # expressão
    self.direita = direita         # expressão

class OpUnaria(NestiNode):
  '''
  OpUnaria representa um operador que atua sobre um só valor
  '''
  campos = ('op', 'operando')
  
  def __init__(self, op, operando, lineno):
    super().__init__(lineno)
    self.op = op                    # '-' ou '!'
    self.operando = operando        # expressão
    
class Literal(NestiNode):
  campos = ('valor', 'tipo')
  
  def __init__(self, valor, tipo, lineno):
    super().__init__(lineno)
    self.valor = valor              # int (números) ou bool (true/false)
    self.tipo = tipo                # 'int' ou 'bool'
    
class Variavel(NestiNode):
  campos = ('nome',)
  
  def __init__(self, nome, lineno):
    super().__init__(lineno)
    self.nome = nome                # str
    
class Chamada(NestiNode):
  campos = ('nome', 'argumentos')
  
  def __init__(self, nome, argumentos, lineno):
    super().__init__(lineno)
    self.nome = nome                 # str: função chamada
    self.argumentos = argumentos     # list[expressão]
