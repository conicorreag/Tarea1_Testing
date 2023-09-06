from ast import *
from core.rewriter import RewriterCommand


# Este transformador busca todas las variables que se utilizaron una sola vez despues de ser inicializadas, posteriormente elimina estas variables sin modificar la logica del test. Para este efecto, reemplaza la variable a eliminar por la expresion utilizada para inicializar la misma.
class InlineTransformer(NodeTransformer):
    def __init__(self):
        self.variables = {} # guarda en un diccionario las variables inicializadas con su valor
        self.used_variables = {} # guarda en un diccionario las variables utilizadas con la cantidad de veces que se usa

    def visit_Assign(self, node: Assign):
        if isinstance(node.targets[0], Name):
            target_variable = node.targets[0].id
            self.variables[target_variable] = node.value
            print("Variable inicializada: ", target_variable, " = ", node.value)
        NodeTransformer.generic_visit(self,node)
    
    def visit_Name(self, node: Name):
        if isinstance(node.ctx, Load) and node.id in self.variables.keys():
            self.used_variables[node.id] = self.used_variables.get(node.id, 0) + 1
        NodeTransformer.generic_visit(self,node)
    
    def visit_Call(self, node: Call):
        for arg in node.args:
            if arg in self.variables.keys():
                self.used_variables[arg] = self.used_variables.get(arg, 0) + 1
        NodeTransformer.generic_visit(self,node)
    
    def optimize_unused_variables(self, node):
        if isinstance(node, Module):
            new_body = []
            for stmt in node.body:
                if isinstance(stmt, Assign):
                    if isinstance(stmt.value, Name) and isinstance(stmt.value.ctx, Load):
                        if stmt.value.id in self.used_variables and self.used_variables[stmt.value.id] == 1:
                            value = self.variables[stmt.value.id]
                            new_assign = Assign(targets=[Name(id=stmt.targets[0].id, ctx=Store())],
                                                    value=value)
                            new_body.append(new_assign)
                            continue
                new_body.append(stmt)
            node.body = new_body
        return node


class InlineCommand(RewriterCommand):
    def apply(self, node):
        visitor = InlineTransformer()
        new_node = visitor.visit(node)
        new_node = fix_missing_locations(new_node)
        return new_node
    
    @classmethod
    def name(self):
        return 'inline'