import ast
import logging
import numpy as np

class MathExpressionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.x = np.arange(1,4)
    
    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.Call):
            return self.visit_Call(node)
        elif isinstance(node, ast.Name):
            return self.visit_Name(node)
        elif isinstance(node, ast.BinOp):
            return self.visit_BinOp(node)
        elif isinstance(node, ast.Constant):
            return self.visit_Constant(node)
        else:
            logging.error(f"Unallowed node type: {type(node)}")

        return None
    
    def visit_Constant(self, node):
        try:
            return float(node.value)
        except:
            raise ValueError(f"{node.value} is not a float")

    def visit_Name(self, node):
        if node.id == "x":
            return self.x
        else:
            raise ValueError(f"Unknown variable ({node.id})")
    
    def visit_BinOp(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if isinstance(node.op,ast.Add):
            return left_value + right_value
        elif isinstance(node.op,ast.Sub):
            return left_value - right_value
        elif isinstance(node.op,ast.Mult):
            return left_value * right_value
        elif isinstance(node.op,ast.Div):
            return left_value / right_value
        elif isinstance(node.op,ast.Pow):
            return left_value + right_value
        else:
            raise ValueError(f"Unkwown operation ({node.op})")

    def visit_Call(self, node):
        args_values = []
        for argo in node.args:
            args_values.append(self.visit(argo))

        func = node.func.id
        if func == "sin":
            return np.sin(*args_values)
        else:
            raise ValueError(f"Unknown function name ({func})")




formula = "sin(x**2)+2"

try:
    parsed_formula = ast.parse(formula, mode='eval')
except SyntaxError:
    print("Invalid formula")
else:
    mathos = MathExpressionVisitor()
    val = mathos.visit(parsed_formula)
    print("Valid formula")
    print(val)
