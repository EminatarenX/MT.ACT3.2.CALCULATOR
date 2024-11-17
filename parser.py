from lark import Lark, Transformer, v_args

grammar = """
start: expr

?expr: term
     | expr "+" term   -> add
     | expr "-" term   -> subtract

?term: factor
     | term "*" factor -> multiply
     | term "/" factor -> divide

?factor: NUMBER        -> number
       | "-" factor    -> neg
       | "(" expr ")"

%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""

parser = Lark(grammar, parser='lalr')

@v_args(inline=True)
class CalculateTree(Transformer):
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

    def number(self, n):
        return float(n)

    def neg(self, n):
        return -n

# Prueba la expresión directamente
try:
    expression = "2 + 3 * (4 - 1)"
    tree = parser.parse(expression)
    result = CalculateTree().transform(tree)
    print("Resultado:", result)
except Exception as e:
    print("Error:", e)


# listo, ahora en la pantalla del html veo Error, y en la consola esto: Resultado después de transformar el árbol: Tree(Token('RULE', 'start'), [81.0]), Tipo: <class 'lark.tree.Tree'>
# 127.0.0.1 - - [14/Nov/2024 08:50:17] "POST /calculate HTTP/1.1" 200 -. 

# esta es la funcion:  function appendToExpression(value) {
#         document.getElementById("display").value += value;
#       }

#       function clearDisplay() {
#         document.getElementById("display").value = "";
#       }

#       function calculate() {
#         const expression = document.getElementById("display").value;
#         fetch("/calculate", {
#           method: "POST",
#           headers: {
#             "Content-Type": "application/json",
#           },
#           body: JSON.stringify({ expression: expression }),
#         })
#           .then((response) => response.json())
#           .then((data) => {
#             if (data.result !== undefined) {
#               document.getElementById("display").value = data.result;
#             } else {
#               document.getElementById("display").value = "Error";
#               console.error("Error:", data.error); // Imprime el error en la consola del navegador
#             }
#           });
#       }