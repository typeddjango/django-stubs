from libcst import parse_module
from libcst.codemod import CodemodContext
from libcst.codemod.visitors import ApplyTypeAnnotationsVisitor

from pathlib import Path

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

context = CodemodContext()
visitor = ApplyTypeAnnotationsVisitor(context)

stubs_dir = '../django-stubs'
sources_dir = '../django-sources/django'

stubs_dict = {}
sources_dict = {}

stubs_pathlist = Path(stubs_dir).rglob('*.pyi')
sources_pathlist = Path(sources_dir).rglob('*.py')

for path in stubs_pathlist:
    str_path = str(path)
    
    stubs_dict[str_path.split('/', 2)[-1].split('.')[0]] = str_path

for path in sources_pathlist:
    str_path = str(path)

    key = str_path.split('/', 3)[-1].split('.')[0]

    if key in stubs_dict:
        sources_dict[key] = str_path

for key in stubs_dict:

    with open(stubs_dict[key]) as file:
        stub = file.read()

    stub_module = parse_module(stub)
    visitor.store_stub_in_context(context, stub_module)
    
    try:
        with open(sources_dict[key]) as file:
            source = file.read()
    except:
        prRed('No corresponding file for stub: ' + stubs_dict[key])
        continue

    source_module = parse_module(source)
    result = visitor.transform_module(source_module)
    
    try:
        file=open(sources_dict[key], 'w')
        file.write(result.code)
        file.close()
        prGreen(sources_dict[key])
    except:
        prRed('Error saving file: ' + sources_dict[key])
