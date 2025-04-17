# Generador de código Python desde el AST de PumaNeoLang

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.output = []

    def generate(self):
        for stmt in self.ast:
            self.translate(stmt, indent=0)
        return "\n".join(self.output)

    def translate(self, node, indent=0):
        ind = '    ' * indent
        stype = node[0]

        if stype == 'assign':
            _, name, expr = node
            self.output.append(f"{ind}{name} = {self.translate_expr(expr)}")

        elif stype == 'print':
            _, expr = node
            self.output.append(f"{ind}print({self.translate_expr(expr)})")

        elif stype == 'if':
            _, cond, then_body, else_body = node
            self.output.append(f"{ind}if {self.translate_expr(cond)}:")
            for stmt in then_body:
                self.translate(stmt, indent + 1)
            if else_body:
                self.output.append(f"{ind}else:")
                for stmt in else_body:
                    self.translate(stmt, indent + 1)

        elif stype == 'while':
            _, cond, body = node
            self.output.append(f"{ind}while {self.translate_expr(cond)}:")
            for stmt in body:
                self.translate(stmt, indent + 1)

        elif stype == 'func_def':
            _, name, body = node
            self.output.append(f"{ind}def {name}():")
            for stmt in body:
                self.translate(stmt, indent + 1)

        elif stype == 'func_call':
            _, name = node
            self.output.append(f"{ind}{name}()")

    def translate_expr(self, expr):
        etype = expr[0]

        if etype == 'literal':
            val = expr[1]
            if val.lower() == 'verdadero':
                return 'True'
            elif val.lower() == 'falso':
                return 'False'
            return val
        elif etype == 'var':
            return expr[1]
        elif etype == 'binop':
            _, op, left, right = expr
            return f"({self.translate_expr(left)} {op} {self.translate_expr(right)})"
        else:
            return '/*EXPR*/'
