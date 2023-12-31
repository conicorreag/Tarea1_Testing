from _ast import Assign, Call
from ast import *
import ast
from typing import Any
from core.rewriter import RewriterCommand


class DuplicatedSetupVisitor(NodeVisitor):
    #  Implementar Clase

    def __init__(self):
        super().__init__()
        self.method_lines = {}  # Un diccionario para rastrear las líneas de cada método
        self.all_method_lines = {}  # Un diccionario para rastrear todas las líneas de cada método
        self.duplicated_lines = []  # Lista de líneas repetidas en todos los métodos
        self.repetidos = 0
        self.no_mas = False

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        if self.all_method_lines:
            first_method_name, first_method_lines = next(iter(self.all_method_lines.items()))
            for line in first_method_lines:
                is_duplicated = all(line in method_lines for method_lines in self.all_method_lines.values())
                if is_duplicated and self.no_mas == False:
                    self.duplicated_lines.append(line)
                    self.repetidos += 1
                else: 
                    self.no_mas = True
        return self.duplicated_lines



    def visit_FunctionDef(self, node):
        method_name = node.name
        method_lines = []

        for method_item in node.body:
            method_item_str = ast.dump(method_item)
            method_lines.append(method_item_str)

        self.all_method_lines[method_name] = method_lines



class ExtractSetupTransformer(NodeTransformer):

    def __init__(self):
        super().__init__()
        self.duplicated_lines = []
        self.duplicated_variables = []
        self.duplicated_values = []
        
    def visit_ClassDef(self, node):
      
        self.duplicated_lines = DuplicatedSetupVisitor().visit(node)
        self.generic_visit(node)
        if self.duplicated_lines:
            new_method = FunctionDef(name='setUp', 
                                    args=arguments(posonlyargs=[], args=[arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[]),
                                    body=[], decorator_list=[])
            for i in range(0, len(self.duplicated_lines)):
                line = Assign(targets=[Attribute(value=Name(id='self', ctx=Load()), attr=self.duplicated_variables[i], ctx=Store())], value=self.duplicated_values[i])
                new_method.body.append(line)

            node.body.insert(0, new_method)
    
        return node


    def visit_FunctionDef(self, node):
        lines_remove = []

        for m in range(0, len(node.body)):
            method_item_str = ast.dump(node.body[m])
            if method_item_str in self.duplicated_lines:
                lines_remove.append(node.body[m])
                if isinstance(node.body[m], ast.Assign):
                    variable = node.body[m].targets[0].id
                    self.duplicated_variables.append(variable)
                    value = node.body[m].value
                    self.duplicated_values.append(value)

        for i in lines_remove:
            node.body.remove(i)
     
        self.generic_visit(node)
        return node
    


    def visit_Call(self, node):
        for i in range(0, len(node.args)):
            if isinstance(node.args[i], ast.Name):
                if node.args[i].id in self.duplicated_variables:
                    node.args[i] = Attribute(value=Name(id='self', ctx=Load()), attr=node.args[i].id, ctx=Load())
            elif isinstance(node.args[i], ast.Call):
                if node.args[i].func.value.id in self.duplicated_variables:
                    node.args[i] = Call(func=Attribute(value=Attribute(value=Name(id='self', ctx=Load()), attr=node.args[i].func.value.id, ctx=Load()), attr=node.args[i].func.attr, ctx=Load()), args=[], keywords=[])


        return node
        



class ExtractSetupCommand(RewriterCommand):
    
    def apply(self, ast):
        # La funcion fix_missing_locations se utiliza para recorrer los nodos del AST y actualizar ciertos atributos
        # (e.g., número de línea) considerando ahora la modificacion
        new_tree = fix_missing_locations(ExtractSetupTransformer().visit(ast))
        
        return new_tree

    @classmethod
    def name(cls):
        return 'extract-setup'
