from libcst import parse_module
from libcst.codemod import CodemodContext
from libcst.codemod.visitors import ApplyTypeAnnotationsVisitor


context = CodemodContext()
visitor = ApplyTypeAnnotationsVisitor(context)

stub_file = '../django-stubs/shortcuts.pyi'
source_file = '../django-sources/django/shortcuts.py'

with open(stub_file) as f:
    stub = f.read()

stub_module = parse_module(stub)

visitor.store_stub_in_context(context, stub_module)

with open(source_file) as f:
    source = f.read()

source_module = parse_module(source)
result = visitor.transform_module(source_module)

print(result.code)

