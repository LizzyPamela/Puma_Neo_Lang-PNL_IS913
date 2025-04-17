# parser_reparable.py
from lexer import Token

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
        raise SyntaxError(f"Se esperaba uno de {types}, se encontró {self.current().type}:{self.current().value}")

    def parse(self):
        program = []
        while self.current().type != 'EOF':
            stmt = self.statement()
            if stmt:
                program.append(stmt)
            else:
                # Avanza y evita bucle infinito si se detecta token inválido
                self.pos += 1
        return program
    
    def peek(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else Token('EOF', '')


    def statement(self):
        current = self.current()
        if current.type == 'PRINT':
            self.match('PRINT')
            self.expect('SYMBOL')  # (
            expr = self.expression()
            self.expect('SYMBOL')  # )
            return ('print', expr)

        elif current.type == 'IDENTIFIER':
            identifier = self.match('IDENTIFIER').value
            if self.match('OPERATOR') and self.tokens[self.pos - 1].value == '=':
                expr = self.expression()
                return ('assign', identifier, expr)

        elif current.type == 'IF':
            self.match('IF')
            condition = self.expression()
            self.expect('SYMBOL')  # :
            if_block = self.block()
            else_block = None
            if self.match('ELSE'):
                self.expect('SYMBOL')  # :
                else_block = self.block()
            return ('if', condition, if_block, else_block)

        elif current.type == 'WHILE':
            self.match('WHILE')
            condition = self.expression()
            self.expect('SYMBOL')  # :
            body = self.block()
            return ('while', condition, body)
       

        elif current.type == 'FUNC':
            self.match('FUNC')
            func_name = self.expect('IDENTIFIER').value
            self.expect('SYMBOL')  # (
            self.expect('SYMBOL')  # )
            self.expect('SYMBOL')  # :
            func_body = self.block()
            return ('func_def', func_name, func_body)

        elif current.type == 'IDENTIFIER' and self.peek().type == 'SYMBOL' and self.peek().value == '(':
            func_name = self.match('IDENTIFIER').value
            self.expect('SYMBOL')  # (
            self.expect('SYMBOL')  # )
            return ('func_call', func_name)


        return None

    def block(self):
        statements = []
        while self.current().type not in ('ELSE', 'EOF', 'IF', 'WHILE', 'FUNC'):
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            else:
                self.pos += 1  # evita bucle si hay tokens inválidos
        return statements

    def expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_expression()
        while self.current().type == 'OPERATOR' and self.current().value in ('==', '!=', '>', '<', '>=', '<='):
            op = self.match('OPERATOR').value
            right = self.parse_expression()
            left = ('binop', op, left, right)
        return left

    def parse_expression(self):
        left = self.parse_term()
        while self.current().type == 'OPERATOR' and self.current().value in ('+', '-'):
            op = self.match('OPERATOR').value
            right = self.parse_term()
            left = ('binop', op, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current().type == 'OPERATOR' and self.current().value in ('*', '/', '%'):
            op = self.match('OPERATOR').value
            right = self.parse_factor()
            left = ('binop', op, left, right)
        return left

    def parse_factor(self):
        token = self.current()
        if token.type in ('NUMBER', 'STRING', 'BOOLEAN'):
            self.pos += 1
            return ('literal', token.value)
        elif token.type == 'IDENTIFIER':
            self.pos += 1
            return ('var', token.value)
        elif token.type == 'SYMBOL' and token.value == '(':
            self.pos += 1
            expr = self.expression()
            self.expect('SYMBOL')  # )
            return expr
        else:
            return None  # ← importante: evita error fatal

