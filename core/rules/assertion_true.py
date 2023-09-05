from _ast import Assign
from typing import Any
from ..rule import *
from core.rules.warning import *
import ast


class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.asign = False

    # def visit_Call(self, node: Call):
    #     if node.func.attr == 'assertTrue':
    #         if node.args:
    #             self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
    #     NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node: Assign):
        if isinstance(node, ast.Assign):
             print("-------entro------------")
             if isinstance(node.targets[0], ast.Name):
                # Si el objetivo es una variable (Name), guarda el nombre y el valor asignado.
                variable_name = node.targets[0].id
                assigned_value = node.value
                print("------------AQUIIIII-------------")
                print(assigned_value)
                if isinstance(assigned_value, Constant) and assigned_value.value == True:
                    print("--------yey-------")
                    self.asign = True

    def visit_Call(self, node):
        print("holaaa")
        if isinstance(node.args[0], NameConstant):
            if node.args[0].value == True:
                if node.func.attr == 'assertTrue':
                    self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
        elif isinstance(node.args[0], Name) and node.func.attr == 'assertTrue':
            if self.asign == True:
                self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
         
        NodeVisitor.generic_visit(self, node)
    

class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionTrueVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-true'
