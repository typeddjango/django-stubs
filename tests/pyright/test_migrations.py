from .base import run_pyright


def test_integer_with_choices() -> None:
    results = run_pyright(
        """\
from django.db import migrations, models

migrations.AlterField(
    model_name="test_model",
    name="test_field",
    field=models.CharField(
        choices=[
            ("foo", "Foo"),
            ("bar", "Bar"),
        ],
        default=None,
        max_length=3,
        null=True,
    ),
)

migrations.AddField(
    model_name="test_model",
    name="test_related_field",
    field=models.ForeignKey(
        blank=True,
        default=None,
        null=True,
        on_delete=models.deletion.PROTECT,
        related_name="test_fields",
        to="some.other.Model",
    ),
)
"""
    )
    # NOTE: Those would fail when _ST/_GT were set to covariant/contravariant
    assert results == []
