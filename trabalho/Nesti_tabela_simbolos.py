'''
A tabela é uma pilha de escopos. O escopo global (programa) fica no fundo, com npivel léxico 0; cada funçãi abre um escopo novo, um nível acima do escopo em que foi declarada. Blocos de if/while não criam escopo.
'''

class Simbolo: 
  '''Uma entrada da tabela: tudo o que se sabe sobre um identificador'''
  
  def __init__(self, nome, categoria, tipo, nivel, deslocamento = None, parametros = None, lineno = 0):
    self.nome = nome              
    self.categoria = categoria          # 'variavel', 'parametro' ou 'funcao'
    self.tipo = tipo                    # 'int' ou 'bool'; para funções, o tipo de retorno
    self.nivel = nivel                  # nível léxico
    self.deslocamento = deslocamento    # posição no registro de ativação 
    self.parametros = parametros        # funções: lista com os tipos dos parâmetros
    self.lineno = lineno
    
class Escopo: 
  '''Um nível da pilha: os símbolos declarador num programa ou numa função'''
  
  def __init__(self, nome, nivel):
    self.nome = nome                    # descrição, como "função soma"
    self.nivel = nivel 
    self.simbolos = {}                 # nome -> Simbolo
    self.num_variaveis = 0              # quantas variáveis locais já receberam deslocamento
  
class TabelaSimbolos:
  
  def __init__(self):
    self.escopos = []                   # pilha: escopos[-1] é o escopo atual
    
  def abrir_escopo(self, nome):
    nivel = len(self.escopos)
    self.escopos.append(Escopo(nome, nivel))
  
  def fechar_escopo(self): 
    return self.escopos.pop()

  @property
  def nivel_atual(self): 
    return self.escopos[-1].nivel
  
  def instalar(self, simbolo):
    '''Instala no escopo atual. Devolve False se o nome já existe nele'''
    escopo = self.escopos[-1]
    if simbolo.nome in escopo.simbolos:
      return False
    escopo.simbolos[simbolo.nome] = simbolo
    return True
  
  def buscar(self, nome): 
    '''Procura do escopo atual até o global. Devolver None se não encontrar'''
    for escopo in reversed(self.escopos):
      if nome in escopo.simbolos: 
        return escopo.simbolos[nome]
    return None
  
  def novo_deslocamento(self): 
    '''Reserva o próximo deslocamento para uma variável local'''
    escopo = self.escopos[-1]
    deslocamento = escopo.num_variaveis
    escopo.num_variaveis += 1
    return deslocamento
