class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.env = {}
        self.symbol_table = {}
        self.functions = {}

    def run(self):
        for stmt in self.tree:
            self.execute(stmt)

    def execute(self, stmt):
        stype = stmt[0]

        if stype == 'assign':
            _, name, expr = stmt
            value = self.evaluate(expr)
            self.env[name] = value
            self.symbol_table[name] = {'tipo': type(value).__name__, 'valor': value}

        elif stype == 'print':
            _, expr = stmt
            print(self.evaluate(expr))

        elif stype == 'if':
            _, cond, then_body, else_body = stmt
            if self.evaluate(cond):
                for s in then_body:
                    self.execute(s)
            else:
                for s in else_body:
                    self.execute(s)

        elif stype == 'while':
            _, cond, body = stmt
            while self.evaluate(cond):
                for s in body:
                    self.execute(s)

        elif stype == 'func_def':
            _, name, body = stmt
            self.functions[name] = body

        elif stype == 'func_call':
            _, name = stmt
            if name not in self.functions:
                raise RuntimeError(f"Función no definida: {name}")
            for s in self.functions[name]:
                self.execute(s)

        else:
            raise RuntimeError(f"Instrucción desconocida: {stype}")

    def evaluate(self, expr):
        etype = expr[0]
        if etype == 'literal':
            return self.parse_literal(expr[1])
        elif etype == 'var':
            name = expr[1]
            if name not in self.env:
                raise RuntimeError(f"Variable no declarada: {name}")
            return self.env[name]
        elif etype == 'binop':
            _, op, l, r = expr
            lval, rval = self.evaluate(l), self.evaluate(r)
            if op == '+': return lval + rval
            elif op == '-': return lval - rval
            elif op == '*': return lval * rval
            elif op == '/': return lval / rval
            elif op == '%': return lval % rval
            elif op == '>': return lval > rval
            elif op == '<': return lval < rval
            elif op == '>=': return lval >= rval
            elif op == '<=': return lval <= rval
            elif op == '==': return lval == rval
            elif op == '!=': return lval != rval
            else: raise RuntimeError(f"Operador inválido: {op}")
        else:
            raise RuntimeError(f"Expresión desconocida: {etype}")

    def parse_literal(self, value):
        v = value.strip().lower()
        if v == "verdadero": return True
        elif v == "falso": return False
        elif v.startswith('"') and v.endswith('"'):
            return v[1:-1]
        try:
            if '.' in v: return float(v)
            return int(v)
        except ValueError:
            return v

    def get_symbol_table(self):
        return self.symbol_table
