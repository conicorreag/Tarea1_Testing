from _ast import Call, ClassDef, FunctionDef
import ast
from typing import Any
from ..rule import *


class DuplicatedSetupVisitor(WarningNodeVisitor):
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


    def visit_FunctionDef(self, node):
        method_name = node.name
        method_lines = []

        for method_item in node.body:
            method_item_str = ast.dump(method_item)
            method_lines.append(method_item_str)

        self.all_method_lines[method_name] = method_lines





    # def __init__(self):
    #     super().__init__()
    #     self.setup_lines = {}
    #     self.repetidos = 0
    #     self.duplicated_lines = []

    # def visit_ClassDef(self, node):
    #     n_metodo = 0
    #     for class_item in node.body:
    #         if isinstance(class_item, ast.FunctionDef):
    #             n_metodo += 1
    #             print("Método:", class_item.name)
    #             for method_item in class_item.body:
    #                 if n_metodo == 1:
    #                     self.setup_lines[n_metodo] = []
    #                     self.setup_lines[n_metodo].append(ast.dump(method_item))
    #                 else:
    #                     if ast.dump(method_item) in self.setup_lines[n_metodo-1]:
    #                         self.repetidos += 1
    #                         self.duplicated_lines.append(ast.dump(method_item))
                            

            


        
            

    # def __init__(self):
    #     super().__init__()
    #     self.setup_lines = []
    #     self.duplicated_lines = []
    #     self.in_test_method = False
    #     self.warning_ready = False
    #     self.actual_node_assign = 0
    #     self.repetidos = 0
    #     self.nodos = 0
    #     self.actual_node_func = 0
    #     self.no_mas_repetidos = False
    #     self.asign_final = 0
    #     self.line_expr = 0
    #     self.call_atribute = None
    #     self.call_args = None



    # def visit_FunctionDef(self, node):
    #     print("nodos:", self.nodos)
    #     if isinstance(node, ast.FunctionDef):
    #         self.generic_visit(node)
    #         self.actual_node_func += 1
    #         self.actual_node_assign = 0


    # def visit_Expr(self, node):
    #     if isinstance(node.value, ast.Call):
    #         if self.actual_node_func == 0:
    #             self.line_expr = node.value.lineno
    #             self.call_atribute = node.value.func.attr
    #             self.call_args = ast.dump(node.value)
               
    #         else:
    #             node_args = ast.dump(node.value)
    #             if node.lineno == ((self.line_expr-1)*2) and self.call_atribute == node.value.func.attr and self.no_mas_repetidos == False and node_args == self.call_args:
    #                 self.repetidos += 1
                  

       
    # def visit_Assign(self, node):
    #     print("----entro a nodo assing", self.actual_node_assign, "------")
    #     print("id", node.targets[0].id)
    #     if self.actual_node_func == 0:
    #         self.setup_lines.append((node.targets[0].id, node.value.value))
    #     else:
    #         if self.actual_node_assign < len(self.setup_lines):

    #             if node.targets[0].id == self.setup_lines[self.actual_node_assign][0] and node.value.value == self.setup_lines[self.actual_node_assign][1] and self.no_mas_repetidos == False:
    #                 print("repetido: ", node.targets[0].id, node.value.value)
    #                 if node.targets[0].id not in self.duplicated_lines:
    #                     self.repetidos += 1
    #                     self.duplicated_lines.append(node.targets[0].id)
    #             else:
    #                 self.no_mas_repetidos = True

    #     self.actual_node_assign += 1
    #     self.asign_final = self.actual_node_assign
       



class DuplicatedSetupRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(node)
        if visitor.repetidos>0:
            visitor.addWarning('DuplicatedSetup', visitor.repetidos, "there are " + str(visitor.repetidos) + " duplicated setup statements") 
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'duplicate-setup'
