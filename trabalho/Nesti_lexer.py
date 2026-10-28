from ply import lex

# ----------- palavras reservadas ------------
# Chave: o texto como aparece no código-fonte 
# Valor: o tipo de token correspondente

reserved = {
  'program': 'PROGRAM', 
  'fun':     'FUN', 
  'int':     'INT', 
  'bool':    'BOOL', 
  'void':    'VOID', 
  'if':      'IF', 
  'else':    'ELSE', 
  'while':   'WHILE', 
  'return':  'RETURN', 
  'read':    'READ', 
  'print':   'PRINT', 
  'true':    'TRUE', 
  'false':   'FALSE',
}

tokens = [
  # identificador e número
  'ID', 'NUMBER',
  # pontuação
  'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI', 'COMMA', 'ARROW',
  # operadores
  'ASSIGN', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'AND', 'OR', 'NOT',
] + list(reserved.values())

# ------------- identificadores e palavras reservdas ---------------
# Verifica se o texto está no dicionário:
# Se tiver: passa devolve o tipo da palavra 
# Caso contrário: devolve o tipo como ID
# Ao final da função devolve o token com o texto com o type correto
def t_ID(t): 
  r'[a-zA-Z][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value, 'ID')
  return t

'''
PALAVRAS RESERVADAS

Token	    Lexema	  O que representa
PROGRAM	  program	  Início do programa, em programa
FUN	      fun	      Início de uma declaração de função, em declaracao_funcao
INT	      int	      Tipo inteiro, em tipo e tipo_retorno
BOOL	    bool	    Tipo lógico, em tipo e tipo_retorno
VOID	    void	    Função sem valor de retorno; só em tipo_retorno
IF	      if	      Início do comando condicional, em condicional
ELSE	    else	    Parte alternativa do condicional, em condicional
WHILE	    while	    Comando de repetição, em repeticao
RETURN	  return	  Comando de retorno de função, em retorno
READ	    read	    Comando de leitura da entrada padrão, em leitura
PRINT	    print	    Comando de escrita na saída padrão, em escrita
TRUE	    true	    Constante lógica verdadeira, em expressao_primaria
FALSE	    false	    Constante lógica falsa, em expressao_primaria

IDENTIFICADOR E NÚMERO

Token	      Lexema	                O que representa
ID	        [a-zA-Z][a-zA-Z0-9_]*, 	Nome definido pelo programador
NUMBER	    [0-9]+                  Constante inteira sem sinal


PONTUAÇÃO

Token	    Lexema	    O que representa
LPAREN	  (	          Abre parênteses
RPAREN	  )	          Fecha parênteses, nos mesmos lugares
LBRACE	  {	          Abre o corpo do programa, de uma função ou de um bloco
RBRACE	  }	          Fecha o corpo do programa, de uma função ou de um bloco
SEMI	    ;	          Termina declarações de variável e comandos simples
COMMA	    ,	          Separa itens nas listas de parâmetros, identificadores e expressões
ARROW	    ->	        Separa a lista de parâmetros do tipo de retorno: fun f() -> int

OPERADORES

Token	    Lexema	     O que representa
ASSIGN	   =	         Atribuição, em atribuicao e na inicialização de declaracao_variavel
EQ	       ==	         Igualdade; operandos do mesmo tipo (int ou bool), resultado bool
NE	       !=	         Diferença; mesmas regras de EQ
LT	       <	         Menor que; operandos int, resultado bool
LE	       <=	         Menor ou igual; operandos int, resultado bool
GT	       >	         Maior que; operandos int, resultado bool
GE	       >=	         Maior ou igual; operandos int, resultado bool
PLUS	     +	         Soma; operandos int, resultado int
MINUS	     -	         Subtração / Negação aritmética (unário, em expressao_unaria)
TIMES	     *	         Multiplicação; operandos int, resultado int
DIVIDE	   /	         Divisão inteira (Nesti não tem números reais)
AND	       &&	         Conjunção lógica; operandos bool, resultado bool
OR	       ||	         Disjunção lógica; operandos bool, resultado bool
NOT	       !	         Negação lógica (unário); operando bool, resultado bool

'''
