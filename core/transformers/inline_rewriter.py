from _ast import Call, FunctionDef, Module, Name
from ast import *
from typing import Any
from core.rewriter import RewriterCommand


class InlineVisitor(NodeVisitor):
    def __init__(self):
        self.variables = {} # Diccionario para variables inicializadas con sus valores
        self.variable_line = {} # Diccionario para variables inicializadas con el valor de la linea en el que se inicializan
        self.used_variables = {} # Diccionario para variables utilizadas con la cantidad de veces que se usan

    def visit_Assign(self, node: Assign):
        self.generic_visit(node)
        if isinstance(node.targets[0], Name):
            variable_name = node.targets[0].id
            self.variables[variable_name] = node.value
            self.variable_line[variable_name] = node.lineno
            if isinstance(node.value, BinOp):
                self._check_and_record_variables(node.value.left)
                self._check_and_record_variables(node.value.right)

    def visit_Call(self, node: Call):
        self.generic_visit(node)
        for arg in node.args:
            self._check_and_record_variables(arg)

    def _check_and_record_variables(self, variable_node):
        if isinstance(variable_node, Name) and variable_node.id in self.variables:
            self.used_variables[variable_node.id] = self.used_variables.get(variable_node.id, 0) + 1
    
    def visit_FunctionDef(self, node: FunctionDef):
        self.generic_visit(node)
        return [self.variables, self.used_variables, self.variable_line]



class InlineTransformer(NodeTransformer):
    def __init__(self):
        super().__init__()
        self.variables = {} # Diccionario para variables inicializadas con sus valores
        self.used_variables = {} # Diccionario para variables utilizadas con la cantidad de veces que se usan
        self.variable_line = {} # Diccionario para variables inicializadas con el valor de la linea en el que se inicializan

    
    def visit_Name(self, node: Name):
        if self.variables and self:
            if isinstance(node.ctx, Load) and node.id in self.used_variables:
                if self.used_variables[node.id] == 1:
                    return self.variables[node.id]
        return node
    
    def visit_Assign(self, node: Assign):
        self.generic_visit(node)
        if isinstance(node.targets[0], Name):
            variable_name = node.targets[0].id
            if variable_name in self.used_variables and self.used_variables[variable_name] == 1:
                return None
        return node
    
    def visit_FunctionDef(self, node: FunctionDef):
        self.variables, self.used_variables, self.variable_line = InlineVisitor().visit(node)
        self.generic_visit(node)
        return node



class InlineCommand(RewriterCommand):
    def apply(self, node):
        new_node = fix_missing_locations(InlineTransformer().visit(node))
        print(dump(new_node))
        return new_node
    
    @classmethod
    def name(self):
        return 'inline'