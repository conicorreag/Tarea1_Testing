from _ast import FunctionDef
from typing import Any
from ..rule import *
import ast

class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()
        self.assert_less = True
 

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr in ('assertTrue', 'assertEquals'):
                    self.assert_less = False
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.assert_less = True
        self.generic_visit(node)
        if self.assert_less:
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