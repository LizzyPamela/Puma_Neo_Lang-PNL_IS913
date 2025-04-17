#  PumaNeoLang (PNL)
![Logo](PNL-max.png)

**PumaNeoLang (PNL)** es un lenguaje de programación diseñado para combinar facilidad de aprendizaje con potencia en la manipulación y análisis de datos. Inspirado en la simplicidad de Python y la expresividad de lenguajes funcionales, PNL busca proporcionar una sintaxis limpia, clara y altamente intuitiva, enfocada en automatización de tareas, procesamiento de datos y análisis estadístico. Su diseño lo hace ideal para desarrolladores principiantes y expertos que buscan realizar manipulaciones de datos sin una curva de aprendizaje pronunciada.. El sistema incluye un **léxico personalizado**, **parser**, **intérprete**, **generador de código Python**, y una **IDE gráfica** amigable y potente.

---

##  Características principales

-  Análisis léxico, sintáctico y semántico.
-  Interprete funcional con control de flujo (`si`, `mientras`).
-  Soporte para funciones definidas por el usuario (`funcion nombre():`).
-  Tipos de datos: `int`, `float`, `string`, `bool`.
-  Tabla de símbolos integrada.
-  Manejo de errores léxicos, sintácticos y semánticos.
-  Librerías básicas (`tabla("archivo.csv")`, operaciones estadísticas).
-  Generación de código Python equivalente.
-  IDE visual con botones para ejecutar, ver tokens, AST, símbolos, y exportar código.

---

## Estructura del Proyecto

Archivo	Descripción
- lexer.py	Analiza el código fuente y genera tokens.
- parser.py	Convierte los tokens en un árbol sintáctico (AST).
- interpreter.py	Ejecuta directamente el AST.
- generator.py	Traduce el AST a código Python.
- ide.py	Interfaz gráfica con funcionalidades integradas.
- interpreter_with_symbol_table.py	Intérprete extendido con semántica y tabla de símbolos.
- PNL-min.png / PNL-max.png	Logo del lenguaje para uso en la interfaz.

---

## Cómo ejecutar
- Instala Python 3.10 o superior.
- Ejecuta el archivo ide.py:
- Escribe tu código PNL dentro del entorno gráfico.
- Usa los botones para:
-   Ejecutar el código
-   Ver tokens
-   Ver árbol sintáctico
-   Ver tabla de símbolos
-   Exportar a Python

---

## Requisitos
- Python 3.x
- Librerías: tkinter, pandas (solo si usas tabla("archivo.csv"))

---
## Sintaxis del lenguaje
pnl
Puma.Roar():
    x = 10
    si x > 5:
        imprimir("Mayor a cinco")

    funcion saludar():
        imprimir("Hola")

    saludar()
Puma.Ya();



## Autora
Lizzy Pamela Mejía Mejía
lpmejiam@unah.hn

## Versión
**IS-913 Final Release 04.25 (LPMM)**


