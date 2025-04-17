# PumaNeoLang (PNL) - IDE Estilizado con resaltado de errores y funciones para abrir/guardar archivos

import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel, Label, PhotoImage, filedialog
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from pprint import pformat
from generator import CodeGenerator
import io
import sys
import os

class PNL_IDE:
    def __init__(self, root):
        self.root = root
        self.root.title("PumaNeoLang IDE")
        self.root.configure(bg="#ffc700")
        self.root.geometry("950x700")

        try:
            self.root.iconphoto(False, tk.PhotoImage(file="PNL-min.png"))
        except Exception:
            pass

        header = tk.Frame(root, bg="#ffc700")
        header.pack(fill=tk.X, pady=(0, 0))

        title_frame = tk.Frame(header, bg="#ffc700")
        title_frame.pack(side=tk.LEFT, padx=10, pady=(10, 0))

        title = tk.Label(title_frame, text="PumaNeoLang - Lenguaje para Análisis y Compiladores", font=("Times New Roman", 14, "bold"), bg="#ffc700", fg="black")
        title.pack(anchor="w")

        subtitle = tk.Label(title_frame, text="Diseño de Compiladores (IS-913) I-PAC 2025", font=("Times New Roman", 12), bg="#ffc700", fg="black")
        subtitle.pack(anchor="w")

        author = tk.Label(title_frame, text="Autora: Lizzy Pamela Mejía Mejía", font=("Times New Roman", 11, "italic"), bg="#ffc700", fg="black")
        author.pack(anchor="w")

        try:
            logo = PhotoImage(file="PNL-max.png")
            self.logo_img = logo.subsample(4, 4)
            logo_label = tk.Label(header, image=self.logo_img, bg="#ffc700", bd=1, relief="solid")
            logo_label.pack(side=tk.RIGHT, padx=(10, 20), pady=10)
        except Exception:
            logo_label = tk.Label(header, text="[Logo]", bg="#ffc700", fg="black")
            logo_label.pack(side=tk.RIGHT, padx=(10, 20), pady=10)

        button_frame = tk.Frame(root, bg="#ffc700")
        button_frame.pack(fill=tk.X, pady=(0, 2))

        tk.Button(button_frame, text="▶ Ejecutar", command=self.run_code, bg="#222", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="[] Tokens", command=self.show_tokens, bg="#222", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="\ Árbol Sintáctico", command=self.show_ast, bg="#222", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📋 Ver Tabla de Símbolos", command=self.show_symbols, bg="#222", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="⚙️ Generar Python", command=self.generate_python, bg="#222", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="💾 Guardar", command=self.save_file, bg="#222", fg="white", font=("Arial", 10)).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="📂 Abrir", command=self.open_file, bg="#222", fg="white", font=("Arial", 10)).pack(side=tk.RIGHT, padx=5)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=110, height=16, font=("Courier New", 12), bg="#fffaf0")
        self.text_area.pack(padx=10, pady=5)

        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=110, height=12, font=("Courier New", 12), state=tk.DISABLED, bg="#f4f4f4")
        self.output_area.pack(padx=10, pady=(0, 10))

        footer = Label(root, text="IS-913 Final Release 04.25 (LPMM)", bg="#ffc700", fg="black", font=("Times New Roman", 10, "italic"))
        footer.pack(pady=(0, 5))

    def run_code(self):
        code = self.text_area.get("1.0", tk.END).strip()
        self.text_area.tag_remove("error", "1.0", tk.END)
        if not code:
            messagebox.showwarning("Advertencia", "El código está vacío.")
            return

        if not (code.startswith("Puma.Roar():") and code.endswith("Puma.Ya();")):
            messagebox.showerror("Error de estructura", "El código debe iniciar con 'Puma.Roar():' y finalizar con 'Puma.Ya();'")
            return

        code_body = code[len("Puma.Roar():"):].strip()
        if code_body.endswith("Puma.Ya();"):
            code_body = code_body[:-len("Puma.Ya();")].strip()

        try:
            lexer = Lexer(code_body)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            tree = parser.parse()

            buffer = io.StringIO()
            sys.stdout = buffer

            interpreter = Interpreter(tree)
            self.latest_interpreter = interpreter
            interpreter.run()

            sys.stdout = sys.__stdout__
            output = buffer.getvalue()

            self.output_area.config(state=tk.NORMAL)
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, output)
            self.output_area.config(state=tk.DISABLED)

        except Exception as e:
            sys.stdout = sys.__stdout__
            self.output_area.config(state=tk.NORMAL)
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, str(e))
            self.output_area.config(state=tk.DISABLED)
            self.highlight_error(str(e))

    def highlight_error(self, error_msg):
        import re
        match = re.search(r"en: (.*)", error_msg)
        if match:
            token = match.group(1).strip()
            start = "1.0"
            while True:
                pos = self.text_area.search(token, start, tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(token)}c"
                self.text_area.tag_add("error", pos, end)
                self.text_area.tag_config("error", background="red", foreground="white")
                start = end

    def show_tokens(self):
        try:
            code = self.text_area.get("1.0", tk.END).strip()
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            self.show_popup("Tokens", '\n'.join(str(t) for t in tokens))
        except Exception as e:
            messagebox.showerror("Error en tokenización", str(e))

    def show_ast(self):
        try:
            code = self.text_area.get("1.0", tk.END).strip()
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            tree = parser.parse()
            self.show_popup("Árbol Sintáctico (AST)", pformat(tree))
        except Exception as e:
            messagebox.showerror("Error en análisis sintáctico", str(e))

    def show_popup(self, title, content):
        window = Toplevel(self.root)
        window.title(title)
        window.configure(bg="#ffc700")
        text_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=25, font=("Courier New", 11), bg="#fffaf0")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=10, pady=10)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pnl", filetypes=[("Archivos PumaNeoLang", "*.pnl")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get("1.0", tk.END))

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos PumaNeoLang", "*.pnl")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, f.read())

    def show_symbols(self):
        if not hasattr(self, 'latest_interpreter') or self.latest_interpreter is None:
            messagebox.showinfo("Tabla de Símbolos", "Primero ejecuta un programa válido para generar la tabla.")
            return
        table = self.latest_interpreter.get_symbol_table()
        if not table:
            content = "(La tabla de símbolos está vacía)"
        else:
            content = "\n".join([f"\tTabla de símbolos\n\n{k} -> tipo: {v['tipo']}, |      valor: {v['valor']}" for k, v in table.items()])
        self.show_popup("Tabla de Símbolos", content)
        
    def generate_python(self):
        try:
            code = self.text_area.get("1.0", tk.END).strip()

            if not (code.startswith("Puma.Roar():") and code.endswith("Puma.Ya();")):
                messagebox.showerror("Error de estructura", "El código debe iniciar con 'Puma.Roar():' y finalizar con 'Puma.Ya();'")
                return

            code_body = code[len("Puma.Roar():"):].strip()
            if code_body.endswith("Puma.Ya();"):
                code_body = code_body[:-len("Puma.Ya();")].strip()

            lexer = Lexer(code_body)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            tree = parser.parse()

            generator = CodeGenerator(tree)
            python_code = generator.generate()

            ruta = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Archivo Python", "*.py")])
            if ruta:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(python_code)
                messagebox.showinfo("Éxito", "Código Python generado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar código Python: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PNL_IDE(root)
    root.mainloop()