from ply import yacc
from Nesti_lexer import tokens, lexer
from Nesti_ast import *

'''
Tranformação aplicada seguindo a regra: 

- Direta: sequência copiada sem transformação.
- Padrão 1: { alfa } vira uma lista recursiva à esquerda com empty.
- Padrão 2: [ alfa ] vira duas alternativas, com e sem o trecho.
- Padrão 3: alfa { separador alfa } vira uma lista recursiva à esquerda sem empty.

ALFA representa qualquer trecho da gramática (terminal, não terminal ou
sequência). O separador pode ser ',' (listas) ou um operador
(níveis de expressão, como '||', '&&' e <operador-aditivo>).

A recursão à esquerda foi usada nas listas por ser mais adequada a
parsers LR: cada item é reduzido assim que é lido, sem crescer a pilha.

'''

class ErroSintatico(Exception):
  '''Erro sintático encontrado durante a análise'''
  pass


# --------------- Programa ------------------------------------------ 
def p_programa(p): 
  '''
  programa : PROGRAM ID LBRACE declaracoes_variaveis declaracoes_funcoes comandos RBRACE
  '''
  p[0] = Programa(p[2], p[4], p[5], p[6], p.lineno(1))

# --------------- Declaração de variáveis --------------------------- 
def p_declaracoes_variaveis(p): 
  '''declaracoes_variaveis : declaracoes_variaveis declaracao_variavel
                           | empty'''
  if len(p) == 3:
    p[1].append(p[2]) # acrescenta na lista existente, com o custo constante
    p[0] = p[1]
  else:
    p[0] = []

def p_declaracao_variavel(p):
  '''declaracao_variavel  : tipo ID SEMI
                          | tipo ID ASSIGN expressao SEMI'''
  inicializacao = p[4] if len(p) == 6 else None
  p[0] = DeclVariavel(p[1], p[2], inicializacao, p.lineno(2))

def p_tipo(p):
  '''tipo : INT
          | BOOL'''
  p[0] = p[1]

# ---------- declarações de funções ----------
def p_declaracoes_funcoes(p):
  '''declaracoes_funcoes : declaracoes_funcoes declaracao_funcao
                         | empty'''
  if len(p) == 3:
    p[1].append(p[2])
    p[0] = p[1]
  else:
    p[0] = []  

def p_declaracao_funcao(p): 
  '''declaracao_funcao : FUN ID LPAREN lista_parametros RPAREN ARROW tipo_retorno LBRACE declaracoes_variaveis declaracoes_funcoes comandos RBRACE'''
  p[0] = DeclFuncao(p[2], p[4], p[7], p[9], p[10], p[11], p.lineno(1))

def p_declaracao_funcao_sem_parametros(p):
  '''declaracao_funcao : FUN ID LPAREN RPAREN ARROW tipo_retorno LBRACE declaracoes_variaveis declaracoes_funcoes comandos RBRACE'''
  p[0] = DeclFuncao(p[2], [], p[6], p[8], p[9], p[10], p.lineno(1))
  

def p_lista_parametros(p): 
  '''lista_parametros : lista_parametros COMMA parametro
                      | parametro'''
  if len(p) == 4:
    p[1].append(p[3])
    p[0] = p[1]
  else: 
    p[0] = [p[1]] # cria uma lista com um único elemento

def p_parametro(p): 
  '''parametro : tipo ID'''
  p[0] = Parametro(p[1], p[2], p.lineno(2))

def p_tipo_retorno(p): 
  '''tipo_retorno : INT
                  | BOOL
                  | VOID'''
  p[0] = p[1]

# ---------- comandos ----------
def p_comandos(p): 
  '''comandos : comandos comando
              | empty'''
  if len(p) == 3:
    p[1].append(p[2])
    p[0] = p[1]
  else:
    p[0] = []

def p_comando(p): 
  '''comando : atribuicao
             | condicional
             | repeticao
             | retorno
             | leitura
             | escrita
             | chamada_comando'''
  p[0] = p[1]

def p_atribuicao(p):
  '''atribuicao : ID ASSIGN expressao SEMI'''
  p[0] = Atribuicao(p[1], p[3], p.lineno(1))

def p_condicional(p): 
  '''condicional : IF LPAREN expressao RPAREN bloco
                 | IF LPAREN expressao RPAREN bloco ELSE bloco'''
  senao = p[7] if len(p) == 8 else None
  p[0] = Condicional(p[3], p[5], senao, p.lineno(1))

def p_repeticao(p): 
  '''repeticao : WHILE LPAREN expressao RPAREN bloco'''
  p[0] = Repeticao(p[3], p[5], p.lineno(1))

def p_bloco(p): 
  '''bloco : LBRACE comandos RBRACE'''
  p[0] = p[2]

def p_retorno(p): 
  '''retorno : RETURN SEMI
             | RETURN expressao SEMI'''
  expressao = p[2] if len(p) == 4 else None
  p[0] = Retorno(expressao, p.lineno(1))

def p_leitura(p): 
  '''leitura : READ LPAREN lista_identificadores RPAREN SEMI'''
  p[0] = Leitura(p[3], p.lineno(1))

def p_lista_identificadores(p): 
  '''lista_identificadores : lista_identificadores COMMA ID
                           | ID'''
  if len(p) == 4: 
    p[1].append(p[3])
    p[0] = p[1]
  else:
    p[0] = [p[1]]

def p_escrita(p): 
  '''escrita : PRINT LPAREN lista_expressoes RPAREN SEMI'''
  p[0] = Escrita(p[3], p.lineno(1))

def p_lista_expressoes(p): 
  '''lista_expressoes : lista_expressoes COMMA expressao
                      | expressao'''
  if len(p) == 4:
    p[1].append(p[3])
    p[0] = p[1]
  else: 
    p[0] = [p[1]]

def p_chamada_comando(p): 
  '''chamada_comando : chamada SEMI'''
  p[0] = ComandoChamada(p[1], p[1].lineno)

def p_chamada(p):
  '''chamada : ID LPAREN lista_expressoes RPAREN
             | ID LPAREN RPAREN'''
  argumentos = p[3] if len(p) == 5 else []
  p[0] = Chamada(p[1], argumentos, p.lineno(1))

# ---------- expressões ----------
def p_expressao(p): 
  '''expressao : expressao_ou'''
  p[0] = p[1]

def p_expressao_ou(p): 
  '''expressao_ou : expressao_ou OR expressao_e
                  | expressao_e'''
  if len(p) == 4:
    p[0] = OpBinaria(p[2], p[1], p[3], p[1].lineno) # p[1].lineno é a linha do operando esquerdo, ou seja, a linha onde a expressão começa. Poderiamos usar p.lineno(2), porque OR e AND são tokens, mas, nos próximos núveis, o operador vem de um não terminal e p.lineno(2) devolveria 0. Por isso iremos padronizar usando p[1].lineno em todos os lugares
  else: 
    p[0] = p[1]
                  
def p_expressao_e(p):
  '''expressao_e : expressao_e AND expressao_igualdade
                 | expressao_igualdade'''
  if len(p) == 4: 
    p[0] = OpBinaria(p[2], p[1], p[3], p[1].lineno)
  else:
    p[0] = p[1]

def p_expressao_igualdade(p): 
  '''expressao_igualdade : expressao_igualdade operador_igualdade expressao_relacional
                         | expressao_relacional'''
  if len(p) == 4:
    p[0] = OpBinaria(p[2], p[1], p[3], p[1].lineno)
  else: 
    p[0] = p[1]

def p_operador_igualdade(p):
  '''operador_igualdade : EQ
                        | NE'''
  p[0] = p[1]

def p_expressao_relacional(p): 
  '''expressao_relacional : expressao_aditiva
                          | expressao_aditiva operador_relacional expressao_aditiva'''
  if len(p) == 4:
    p[0] = OpBinaria(p[2], p[1], p[3], p[1].lineno)
  else:
    p[0] = p[1]

def p_operador_relacional(p):
  '''operador_relacional : LT
                         | LE
                         | GT
                         | GE'''
  p[0] = p[1]

def p_expressao_aditiva(p): 
  '''expressao_aditiva : expressao_aditiva operador_aditivo expressao_multiplicativa
                       | expressao_multiplicativa'''
  if len(p) == 4: 
    p[0] = OpBinaria(p[2], p[1], p[3], p[1].lineno)
  else: 
    p[0] = p[1]

def p_operador_aditivo(p):
  '''operador_aditivo : PLUS
                      | MINUS'''
  p[0] = p[1]

def p_expressao_multiplicativa(p): 
  '''expressao_multiplicativa : expressao_multiplicativa operador_multiplicativo expressao_unaria
                              | expressao_unaria'''
  if len(p) == 4: 
    p[0] = OpBinaria(p[2], p[1], p[3], p[1].lineno)
  else: 
    p[0] = p[1]

def p_operador_multiplicativo(p): 
  '''operador_multiplicativo : TIMES 
                             | DIVIDE'''
  p[0] = p[1]

def p_expressao_unaria(p): 
  '''expressao_unaria : MINUS expressao_unaria
                      | NOT expressao_unaria
                      | expressao_primaria'''
  if len(p) == 3: 
    p[0] = OpUnaria(p[1], p[2], p.lineno(1))
  else: 
    p[0] = p[1]

def p_expressao_primaria_numero(p):
  '''expressao_primaria : NUMBER'''
  p[0] = Literal(p[1], 'int', p.lineno(1))

def p_expressao_primaria_booleano(p):
  '''expressao_primaria : TRUE
                        | FALSE'''
  p[0] = Literal(p[1] == 'true', 'bool', p.lineno(1))

def p_expressao_primaria_variavel(p):
  '''expressao_primaria : ID'''
  p[0] = Variavel(p[1], p.lineno(1))

def p_expressao_primaria_chamada(p):
  '''expressao_primaria : chamada'''
  p[0] = p[1]

def p_expressao_primaria_parenteses(p):
  '''expressao_primaria : LPAREN expressao RPAREN'''
  p[0] = p[2]

# ---------- auxiliares ----------
def p_empty(p): 
  '''empty :'''
  pass 

def p_error(p): 
  if p is None: 
    raise ErroSintatico(
      f"Erro sintático na linha {lexer.lineno}: fim de arquivo inesperado."
    )
  raise ErroSintatico(
    f"Erro sintático na linha {p.lineno}: token inesperado {p.value!r}"
  )

parser = yacc.yacc()