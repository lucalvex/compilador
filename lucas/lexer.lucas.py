import ply.lex as lex

p_reservadas = {
    'iniciar': 'INICIAR'
    'finalizar': 'FINAL'
    'robo': 'ROBO'
    'andar': 'ANDAR'
    'parar': 'PARAR'
    'girar': 'GIRAR'
}

tokens =  ('ID', 'NUM', 'ATRIB')+tuple(p_reservadas.values())

# Definição de uma exp regular de um NUM
def t_NUM(t):
    r'[0-9]+(\.[0-9]+)?
    t.value = float(t.value)
    return t

# Definição de uma exp regular de um ID
def t_ID(t): 
    r'[a-z][a-zA-Z0-9]*'
    t.type = p_reservadas.get(t.value, 'ID')
    return t

def t_comment(t): 
    r'//[^/n]*'
    pass

def t_newline(t): 
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t): 
    print("ERRO: Símbolo ilegal '%s'" % t.value[0])
    t.lexer.skip(1) # retorno o t e retrocede para o valor anterior 

scanner = lex.lex()


