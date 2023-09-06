from ast import *
import ast
from core.rewriter import RewriterCommand


class AssertTrueTransformer(NodeTransformer):
    
    def visit_Call(self, node):
        if node.func.attr == 'assertEquals':
            if node.args[1].value == True:
                variable = node.args[0].id
                return Call(func=Attribute(value=Name(id='self', ctx=Load()), attr='assertTrue', ctx=Load()), args=[Name(id=variable, ctx=Load())], keywords=[])
            
        else:
            return node
        


class AssertTrueCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.

    def apply(self, node):
        new_tree = fix_missing_locations(AssertTrueTransformer().visit(node))
        return new_tree
