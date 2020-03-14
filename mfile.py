from graphviz import Digraph
from mypy.options import Options

source = """
from root.package import MyQuerySet 

MyQuerySet().mymethod()
"""

from mypy import parse

parsed = parse.parse(source, 'myfile.py', None, None, Options())
print(parsed)

graphattrs = {
    "labelloc": "t",
    "fontcolor": "blue",
    # "bgcolor": "#333333",
    "margin": "0",
}

nodeattrs = {
    # "color": "white",
    "fontcolor": "#00008b",
    # "style": "filled",
    # "fillcolor": "#ffffff",
    # "fillcolor": "#006699",
}

edgeattrs = {
    # "color": "white",
    # "fontcolor": "white",
}

graph = Digraph('mfile.py', graph_attr=graphattrs, node_attr=nodeattrs, edge_attr=edgeattrs)
graph.node('__builtins__')

graph.node('django.db.models')
graph.node('django.db.models.fields')

graph.edge('django.db.models', 'django.db.models.fields')
graph.edge('django.db.models', '__builtins__')
graph.edge('django.db.models.fields', '__builtins__')

graph.node('mymodule')
graph.edge('mymodule', 'django.db.models')
graph.edge('mymodule', '__builtins__')
#
# graph.node('ImportFrom', label='ImportFrom(val=root.package, [MyQuerySet])')
# graph.edge('MypyFile', 'ImportFrom')



# graph.node('ClassDef_MyQuerySet', label='ClassDef(name=MyQuerySet)')
# graph.edge('MypyFile', 'ClassDef_MyQuerySet')
#
# graph.node('FuncDef_mymethod', label='FuncDef(name=mymethod)')
# graph.edge('ClassDef_MyQuerySet', 'FuncDef_mymethod')
#
# graph.node('Args', label='Args')
# graph.edge('FuncDef_mymethod', 'Args')
#
# graph.node('Var_self', label='Var(name=self)')
# graph.edge('Args', 'Var_self')
#
# graph.node('Block', label='Block')
# graph.edge('FuncDef_mymethod', 'Block')
#
# graph.node('PassStmt')
# graph.edge('Block', 'PassStmt')

# graph.node('ExpressionStmt')
# graph.edge('MypyFile', 'ExpressionStmt')
#
# graph.node('CallExpr', label='CallExpr(val="MyQuerySet()")')
# graph.edge('ExpressionStmt', 'CallExpr')
#
# graph.node('MemberExpr', label='MemberExpr(val=".mymethod()")')
# graph.edge('CallExpr', 'MemberExpr')
#
# graph.node('CallExpr_outer_Args', label='Args()')
# graph.edge('CallExpr', 'CallExpr_outer_Args')
#
# graph.node('CallExpr_inner', label='CallExpr(val="mymethod()")')
# graph.edge('MemberExpr', 'CallExpr_inner')
#
# graph.node('NameExpr', label='NameExpr(val="mymethod")')
# graph.edge('CallExpr_inner', 'NameExpr')
#
# graph.node('Expression_Args', label='Args()')
# graph.edge('CallExpr_inner', 'Expression_Args')

graph.render(view=True, format='png')


# MypyFile(
#   ClassDef(
#     name=MyQuerySet,
#     FuncDef(
#       name=mymethod,
#       Args(
#         Var(self))
#       Block(PassStmt())
#     )
# )
# ExpressionStmt:6(
#   CallExpr:6(
#     MemberExpr:6(
#       CallExpr:6(
#         NameExpr(MyQuerySet)
#         Args())
#       mymethod)
#     Args())))
