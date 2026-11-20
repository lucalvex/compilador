'''
Base do padrão Visitor para percorrer a AST 

Cada fase do compilador (análise semântica, geração de código) é uma 
subclasse com um método visitar_<NomeDaClasse> para cada tipo de nó
'''

class NestiVisitor:
  
  def visitar(self, no): 
    '''Chama o método específico para o tipo do nó'''
    nome_metodo = f'visitar_{type(no).__name__}'
    # busca o método do próprio objeto
    # se não encontrar, chama-se visitar_generico()
    metodo = getattr(self, nome_metodo, self.visitar_generico)    
    return metodo(no)
  
  def visitar_generico(self, no):
    raise NotImplementedError(
      f'{type(self).__name__} não tem o método visitar_{type(no).__name__}'
    )
