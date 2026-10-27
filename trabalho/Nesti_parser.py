from ply import yacc
from Nesti_lexer import tokens

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


# --------------- Programa ------------------------------------------ 
def p_programa(p): 
  '''programa : PROGRAM ID LBRACE declaracoes_variaveis declaracoes_funcoes comandos RBRACE'''
  pass

# --------------- Declaração de variáveis --------------------------- 
def p_declaracoes_variaveis(p): 
  '''declaracoes_variaveis : declaracoes_variaveis declaracao_variavel
                           | empty'''
  pass

def p_declaracao_variavel(p):
  '''declaracao_variavel : tipo ID SEMI
                          | tipo ID ASSIGN expressao SEMI'''
  pass

def p_tipo(p):
  '''tipo : INT
          | BOOL'''
  pass

# ---------- declarações de funções ----------
def p_declaracoes_funcoes(p):
  '''declaracoes_funcoes : declaracoes_funcoes declaracao_funcao
                        | empty'''
  pass

def p_declaracao_funcao(p): 
  '''declaracao_funcao : FUN ID LPAREN lista_parametros RPAREN ARROW tipo_retorno LBRACE declaracoes_variaveis declaracoes_funcoes comandos RBRACE
                       | FUN ID LPAREN RPAREN ARROW tipo_retorno LBRACE declaracoes_variaveis declaracoes_funcoes comandos RBRACE'''
  pass
  

def p_lista_parametros(p): 
  '''lista_parametros : lista_parametros COMMA parametro
                      | parametro'''
  pass

def p_parametro(p): 
  '''parametro : tipo ID'''
  pass

def p_tipo_retorno(p): 
  '''tipo_retorno : INT
                  | BOOL
                  | VOID'''
  pass

# ---------- comandos ----------
def p_comandos(p): 
  '''comandos : comandos comando
              | empty'''
  pass

def p_comando(p): 
  '''comando : atribuicao
             | condicional
             | repeticao
             | retorno
             | leitura
             | escrita
             | chamada_comando'''
  pass

def p_atribuicao(p):
  '''atribuicao : ID ASSIGN expressao SEMI'''
  pass

def p_condicional(p): 
  '''condicional : IF LPAREN expressao RPAREN bloco
                 | IF LPAREN expressao RPAREN bloco ELSE bloco'''

def p_repeticao(p): 
  '''repeticao : WHILE LPAREN expressao RPAREN bloco'''
  pass

def p_bloco(p): 
  '''bloco : LBRACE comandos RBRACE'''
  pass

def p_retorno(p): 
  '''retorno : RETURN SEMI
             | RETURN expressao SEMI'''
  pass

def p_leitura(p): 
  '''leitura : READ LPAREN lista_identificadores RPAREN SEMI'''
  pass

def p_lista_identificadores(p): 
  '''lista_identificadores : lista_identificadores COMMA ID
                           | ID'''
  pass

def p_escrita(p): 
  '''escrita : PRINT LPAREN lista_expressoes RPAREN SEMI'''
  pass

def p_lista_expressoes(p): 
  '''lista_expressoes : lista_expressoes COMMA expressao
                      | expressao'''
  pass

def p_chamada_comando(p): 
  '''chamada_comando : chamada SEMI'''
  pass

def p_chamada(p):
  '''chamada : ID LPAREN lista_expressoes RPAREN
             | ID LPAREN RPAREN'''
  pass

# ---------- expressões ----------
def p_expressao(p): 
  '''expressao : expressao_ou'''
  pass

def p_expressao_ou(p): 
  '''expressao_ou : expressao_ou OR expressao_e
                  | expressao_e'''
                  
def p_expressao_e(p):
  '''expressao_e : expressao_e AND expressao_igualdade
                 | expressao_igualdade'''
  pass

def p_expressao_igualdade(p): 
  '''expressao_igualdade : expressao_igualdade operador_igualdade expressao_relacional
                         | expressao_relacional'''
  pass

def p_operador_igualdade(p):
  '''operador_igualdade : EQ
                        | NE'''
  pass

def p_expressao_relacional(p): 
  '''expressao_relacional : expressao_aditiva
                          | expressao_aditiva operador_relacional expressao_aditiva'''
  pass

def p_operador_relacional(p):
  '''operador_relacional : LT
                         | LE
                         | GT
                         | GE'''
  pass

def p_expressao_aditiva(p): 
  '''expressao_aditiva : expressao_aditiva operador_aditivo expressao_multiplicativa
                       | expressao_multiplicativa'''
  pass

def p_operador_aditivo(p):
  '''operador_aditivo : PLUS
                      | MINUS'''
  pass

def p_expressao_multiplicativa(p): 
  '''expressao_multiplicativa : expressao_multiplicativa operador_multiplicativo expressao_unaria
                              | expressao_unaria'''
  pass

def p_operador_multiplicativo(p): 
  '''operador_multiplicativo : TIMES 
                             | DIVIDE'''
  pass

def p_expressao_unaria(p): 
  '''expressao_unaria : MINUS expressao_unaria
                      | NOT expressao_unaria
                      | expressao_primaria'''
  pass

def p_expressao_primaria(p): 
  '''expressao_primaria : NUMBER
                        | TRUE
                        | FALSE
                        | ID
                        | chamada 
                        | LPAREN expressao RPAREN'''
  pass

# ---------- auxiliares ----------
def p_empty(p): 
  '''empty :'''
  pass 

def p_error(p): 
  pass

parser = yacc.yacc()