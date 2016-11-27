import sys
import ply.lex

tokens = (
    "NUMBER",
    "STRING",
    "OPER",
    "LABEL",
    "LABEL_VAR",
)

t_OPER = "[A-Z]+"
t_LABEL = ":[a-z_\-]+"
t_LABEL_VAR = "\.[a-z_\-]+"

def t_STRING(t):
    '("[^"\\\\]*(?:\\\\.[^"\\\\]*)*")'
    # Taken from http://stackoverflow.com/a/6525975

    t.value = t.value[1:-1]
    return t
    
def t_newline(t):
    "\\n"
    t.lexer.lineno += 1

def t_NUMBER(t):
    "-?[0-9]+"
    t.value = int(t.value)
    return t

t_ignore = " \t"
t_ignore_COMMENT = r"\#.*"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = ply.lex.lex()

def lex(s):
    lexer.input(s)

    tokens = []
    labels = {}

    tokno = 0
    while True:
        tok = lexer.token()
        if tok:
            if tok.type == "LABEL":
                labels[tok.value[1:]] = tokno
            else:
                tokno += 1
                tokens.append(tok)
        else:
            break

    newtoks = []
    for item in tokens:
        if item.type == "LABEL_VAR":
            item.type = "NUMBER"
            item.value = labels[item.value[1:]]
        newtoks.append(item)

    return newtoks
