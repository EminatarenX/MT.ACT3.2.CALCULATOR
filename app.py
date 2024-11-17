from flask import Flask, render_template, request, jsonify
from lark import Lark, Transformer, v_args, Tree

# Define la gramática
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

# Crea el parser
parser = Lark(grammar, parser='lalr')

# Define un transformer para evaluar la expresión
@v_args(inline=True)
class CalculateTree(Transformer):
    def add(self, a, b):
        return float(a) + float(b)
    def subtract(self, a, b):
        return float(a) - float(b)
    def multiply(self, a, b):
        return float(a) * float(b)
    def divide(self, a, b):
        return float(a) / float(b)
    def number(self, n):
        return float(n)
    def neg(self, n):
        return -float(n)
    def start(self, tree):
        return float(tree)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.json['expression']
        # Primero parseamos la expresión
        tree = parser.parse(expression)
        # Luego transformamos el árbol en un resultado numérico
        transformer = CalculateTree()
        result = transformer.transform(tree)
        
        # Aseguramos que el resultado sea un número
        if isinstance(result, (int, float)):
            return jsonify({
                "result": str(result),
                "success": True
            })
        else:
            return jsonify({
                "error": "El resultado no es un número válido",
                "success": False
            })
    except Exception as e:
        print(f"Error en calculate: {str(e)}")  # Para debugging
        return jsonify({
            "error": str(e),
            "success": False
        })

@app.route('/generate_tree', methods=['POST'])
def generate_tree():
    try:
        expression = request.json['expression']
        tree = parser.parse(expression)
        
        # Convertir el árbol a formato JSON para visualización
        def tree_to_dict(tree):
            if isinstance(tree, Tree):
                return {
                    "name": str(tree.data),
                    "children": [tree_to_dict(child) for child in tree.children]
                }
            return {"name": str(tree)}
        
        tree_dict = tree_to_dict(tree)
        return jsonify({
            "tree": tree_dict,
            "success": True
        })
    except Exception as e:
        print(f"Error en generate_tree: {str(e)}")  # Para debugging
        return jsonify({
            "error": str(e),
            "success": False
        })

if __name__ == '__main__':
    app.run(debug=True)