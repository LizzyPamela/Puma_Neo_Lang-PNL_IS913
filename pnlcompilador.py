# PumaNeoLang (PNL) - Reconstrucción Total: Lexer, Parser, Interpreter, Symbols

import re

# -----------------------------
# Lexer (Análisis Léxico)
# -----------------------------
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"<{self.type}:{self.value}>"

class Lexer:
    TOKEN_PATTERNS = [
        (r'\bsi\b', 'IF'),
        (r'\bsino\b', 'ELSE'),
        (r'\bmientras\b', 'WHILE'),
        (r'\bfuncion\b', 'FUNC'),
        (r'\bretornar\b', 'RETURN'),
        (r'\bimprimir\b', 'PRINT'),
        (r'\bverdadero\b|\bfalso\b', 'BOOLEAN'),
        (r'\d+\.\d+', 'FLOAT'),
        (r'\d+', 'NUMBER'),
        (r'".*?"|\'.*?\'', 'STRING'),
        (r'\b[a-zA-Z_]\w*\b', 'IDENTIFIER'),
        (r'[+\-*/%=]', 'OPERATOR'),
        (r'[(){}:,]', 'SYMBOL')
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        pos = 0
        while pos < len(self.code):
            if self.code[pos].isspace():
                pos += 1
                continue
            match = None
            for pattern, type_ in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    value = match.group(0)
                    self.tokens.append(Token(type_, value))
                    pos = match.end()
                    break
            if not match:
                raise SyntaxError(f"Error léxico: carácter inválido '{self.code[pos]}' en posición {pos}")
        return self.tokens


# -----------------------------
# Tabla de Símbolos
# -----------------------------
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, value):
        self.symbols[name] = value

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        raise NameError(f"Variable '{name}' no definida")


# -----------------------------
# Parser (BNF simplificado)
# -----------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token('EOF', '')

    def match(self, *types):
        if self.current().type in types:
            token = self.current()
            self.pos += 1
            return token
        return None

    def expect(self, *types):
        token = self.match(*types)
        if token:
            return token
        raise SyntaxError(f"Se esperaba uno de {types}, se encontró {self.current().type}")

    def parse(self):
        program = []
        while self.current().type != 'EOF':
            program.append(self.statement())
        return program

    def statement(self):
        if self.match('PRINT'):
            expr = self.expression()
            return ('print', expr)
        elif self.match('IDENTIFIER') and self.match('OPERATOR'):
            name = self.tokens[self.pos - 3].value
            expr = self.expression()
            return ('assign', name, expr)
        elif self.match('IF'):
            cond = self.expression()
            self.expect('SYMBOL')  # Espera :
            true_block = self.statement()
            return ('if', cond, true_block)
        else:
            return ('expr', self.expression())

    def expression(self):
        token = self.current()
        if token.type in ('NUMBER', 'FLOAT', 'STRING', 'BOOLEAN'):
            self.pos += 1
            return ('literal', token.value)
        elif token.type == 'IDENTIFIER':
            self.pos += 1
            return ('var', token.value)
        raise SyntaxError(f"Expresión inválida: {token}")


# -----------------------------
# Intérprete
# -----------------------------
class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.symbols = SymbolTable()

    def evaluate(self, node):
        if node[0] == 'literal':
            value = node[1]
            if value in ['verdadero', 'falso']:
                return value == 'verdadero'
            elif value.replace('.', '', 1).isdigit():
                return float(value) if '.' in value else int(value)
            return value.strip('"').strip("'")
        elif node[0] == 'var':
            return self.symbols.get(node[1])

    def execute(self):
        output = []
        for stmt in self.tree:
            if stmt[0] == 'print':
                value = self.evaluate(stmt[1])
                output.append(str(value))
            elif stmt[0] == 'assign':
                self.symbols.define(stmt[1], self.evaluate(stmt[2]))
        return '\n'.join(output)


# -----------------------------
# Ejemplo de uso
# -----------------------------
if __name__ == "__main__":
    code = """
    x = 10
    imprimir("El valor de x es:")
    imprimir(x)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter(tree)
    print(interpreter.execute())