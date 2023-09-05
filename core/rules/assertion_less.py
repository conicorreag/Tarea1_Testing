from _ast import FunctionDef
from typing import Any
from ..rule import *
import ast

class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()
        self.assert_less = True

    def visit_FunctionDef(self, node: FunctionDef):
        self.assert_less = True
        if isinstance(node, ast.Expr) and isinstance(ast.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == 'assertTrue':
            self.assert_less = False
        NodeVisitor.generic_visit(self, node)
        if self.assert_less == True:
            self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')   


class AssertionLessTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionLessVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-less'