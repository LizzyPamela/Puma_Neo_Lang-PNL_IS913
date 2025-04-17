# lexer.py actualizado para Puma.Roar() y Puma.Ya()

import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"<{self.type}:{self.value}>"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0

    def tokenize(self):
        token_specification = [
            ('START',      r'Puma\.Roar\(\):'),
            ('END',        r'Puma\.Ya\(\);'),
            ('FUNC',      r'function'),
            ('NUMBER',     r'\d+(\.\d+)?'),
            ('STRING',     r'".*?"'),
            ('ASSIGN',     r'='),
            ('END_STMT',   r';'),
            ('ID',         r'[a-zA-Z_][a-zA-Z_0-9]*'),
            ('OP',         r'[+\-*/><=!]=?|==|\!=|\*|\/|\%'),
            ('NEWLINE',    r'\n'),
            ('SKIP',       r'[ \t]+'),
            ('SYMBOL',     r'[():]'),
            ('MISMATCH',   r'.')
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line = self.code
        pos = 0
        mo = get_token(line, pos)
        while mo:
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                token = Token('NUMBER', value)
            elif kind == 'STRING':
                token = Token('STRING', value)
            elif kind == 'function':
                token = Token('FUNC', value)
            elif kind == 'ASSIGN':
                token = Token('OPERATOR', value)
            elif kind == 'END_STMT':
                token = Token('SYMBOL', value)
            elif kind == 'ID':
                if value == 'imprimir':
                    token = Token('PRINT', value)
                elif value == 'si':
                    token = Token('IF', value)
                elif value == 'sino':
                    token = Token('ELSE', value)
                elif value == 'mientras':
                    token = Token('WHILE', value)
                elif value == 'verdadero' or value == 'falso':
                    token = Token('BOOLEAN', value)
                else:
                    token = Token('IDENTIFIER', value)
            elif kind == 'OP':
                token = Token('OPERATOR', value)
            elif kind == 'SYMBOL':
                token = Token('SYMBOL', value)
            elif kind == 'START':
                token = Token('START', value)
            elif kind == 'END':
                token = Token('END', value)
            elif kind == 'NEWLINE' or kind == 'SKIP':
                mo = get_token(line, mo.end())
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Error léxico en: {value}")
            self.tokens.append(token)
            pos = mo.end()
            mo = get_token(line, pos)

        return self.tokens