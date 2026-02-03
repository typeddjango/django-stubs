import libcst
import libcst.matchers as m
from libcst import If, IndentedBlock, BaseSuite
from libcst.codemod import ContextAwareTransformer, CodemodContext

STUB = 'stub.pyi'
IS_3_0 = True


def is_django_3_0(if_node: If) -> bool:
    return m.matches(if_node.test, m.Name(value='DJANGO_3_0'))


class DjangoVersionTransformer(ContextAwareTransformer):
    def leave_IndentedBlock(
            self, original_node: "IndentedBlock", updated_node: "IndentedBlock"
    ) -> "BaseSuite":
        modified_body = []
        for statement in original_node.body:
            if not m.matches(statement, m.If(test=m.Name(value='DJANGO_3_0'))):
                modified_body.append(statement)
                continue

            if_statement = libcst.ensure_type(statement, If)
            if IS_3_0:
                modified_body.extend(if_statement.body.body)
            else:
                if if_statement.orelse is not None:
                    modified_body.extend(if_statement.orelse.body.body)
                else:
                    continue

        return updated_node.with_changes(body=modified_body)


with open(STUB) as f:
    contents = f.read()

tree = libcst.parse_module(contents)
context = CodemodContext()
transformer = DjangoVersionTransformer(context)

modified_tree = tree.visit(transformer)
print(modified_tree.code)
