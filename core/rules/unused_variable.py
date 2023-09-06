from _ast import Assign
from typing import Any
from ..rule import *


class UnusedVariableVisitor(WarningNodeVisitor):
    def __init__(self):
        super().__init__()
        self.variables = {}
        self.used_variables = set()
        self.functions_info = []
    
    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if isinstance(target, Name):
                self.variables[target.id] = target.lineno
        NodeVisitor.generic_visit(self, node)
    
    def visit_Name(self, node: Name):
        if isinstance(node.ctx, Load):
            self.used_variables.add(node.id)
        NodeVisitor.generic_visit(self, node)
    
    def visit_FunctionDef(self, node: FunctionDef):
        self.current_function = node
        self.used_variables = set()
        self.variables = {}
        NodeVisitor.generic_visit(self, node)
        self.functions_info.append([self.variables, self.used_variables])


class UnusedVariableTestRule(Rule):
    def analyze(self, node):
        visitor = UnusedVariableVisitor()
        visitor.visit(node)
        for function in visitor.functions_info:
            for variable in (function[0].keys() - function[1]):
                visitor.addWarning('UnusedVariable', function[0][variable], f'variable {variable} has not been used')

        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'not-used-variable'
