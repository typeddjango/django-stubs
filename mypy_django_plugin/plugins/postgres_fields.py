from mypy.plugin import Plugin, ClassDefContext


def determine_type_of_array_field(context: ClassDefContext) -> None:
    pass


class PostgresFieldsPlugin(Plugin):
    def get_base_class_hook(self, fullname: str
                            ):
        return determine_type_of_array_field


def plugin(version):
    return PostgresFieldsPlugin
