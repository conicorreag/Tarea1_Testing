from _ast import Assign
from ast import *
import ast
from typing import Any
from core.rewriter import RewriterCommand

class ExtractSetupTransformer(NodeTransformer):


    # def __init__(self):
    #     self.duplicate_lines = {}

    # def visit_FunctionDef(self, node):
    #     if node.name != 'setUp':
    #         # Recopila todas las líneas de código en el método actual
    #         lines = [ast.dump(stmt) for stmt in node.body]
    #         code_block = '\n'.join(lines)

    #         # Si el bloque de código ya existe en otro método, guarda su nombre y contenido
    #         if code_block in self.duplicate_lines:
    #             self.duplicate_lines[code_block].append(node.name)
    #         else:
    #             self.duplicate_lines[code_block] = [node.name]

    #     return node

    # def visit_Module(self, node):
    #     # Recorre los nodos del módulo (clases y funciones)
    #     for item in node.body:
    #         if isinstance(item, ast.ClassDef):
    #             # Recorre los métodos de la clase
    #             for method in item.body:
    #                 if isinstance(method, ast.FunctionDef):
    #                     # Si el bloque de código es duplicado, reemplaza el cuerpo del método
    #                     if ast.dump(method) in self.duplicate_lines:
    #                         method.body = [ast.Assign(
    #                             targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=stmt.split('=')[0], ctx=ast.Store())],
    #                             value=ast.parse(stmt.split('=')[1]).body[0].value,
    #                         ) for stmt in ast.dump(method).split('\n')]
        
    #     print(ast.dump(node))
    #     return node









    
#     def __init__(self):
#         super().__init__()
#         self.setup_lines = []
#         self.actual_func_node = 0
#         self.actual_node_assign = 0
#         self.final_setup = []  
#         self.no_mas_repetidos = False

#     def visit_FunctionDef(self, node):
#         self.generic_visit(node)
#         self.actual_func_node += 1
#         self.actual_node_assign = 0
#         if self.no_mas_repetidos == True or len(self.setup_lines)==len(self.final_setup):
#             print("holaaa2")
#             body_setup = []
#             for setup in self.final_setup:
#                 body_setup.append(Assign(targets=[Attribute(value=Name(id='self', ctx=Load()), attr=setup["id"], ctx=Store())], value=Constant(value=setup["value"])), )
            
#             return FunctionDef(name='setUp',
#             args=arguments(args=[arg(arg='self')], defaults=[], kwonlyargs=[], kw_defaults=[],
#                            vararg=None, kwarg=None, posonlyargs=[]),
#             body=body_setup,
#             decorator_list=[],
#             returns=None)
        




#     def visit_Assign(self, node):
#         print("entrooooooo")
#         if self.actual_func_node == 0:
#             self.setup_lines.append({"id": node.targets[0].id, "value": node.value.value})
#         else:
#             if self.actual_node_assign < len(self.setup_lines):
#                 if node.targets[0].id == self.setup_lines[self.actual_node_assign]["id"] and node.value.value == self.setup_lines[self.actual_node_assign]["value"] and self.no_mas_repetidos == False:
#                     self.final_setup.append({"id": node.targets[0].id, "value": node.value.value})
#                     self.actual_node_assign += 1
#                 else:
#                     self.no_mas_repetidos = True
#         print("holaaaa")
#         for s in self.final_setup:
#             print(s)
        
       



class ExtractSetupCommand(RewriterCommand):
    
    def apply(self, ast):
        # La funcion fix_missing_locations se utiliza para recorrer los nodos del AST y actualizar ciertos atributos
        # (e.g., número de línea) considerando ahora la modificacion
        new_tree = fix_missing_locations(ExtractSetupTransformer().visit(ast))
        return new_tree

    @classmethod
    def name(cls):
        return 'extract-setup'
