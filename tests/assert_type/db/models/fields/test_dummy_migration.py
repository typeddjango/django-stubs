# Regression test for false positives like this due to incomplete `Field` annotations.
# Type annotations must provide the type vars otherwise they get inferred as `Field[Any, Any, Literal[False]]` in some
# contexts, which is usually wrong. Annotations accepting any field should use `Field[Any, Any, Any]`
from __future__ import annotations

from typing import TYPE_CHECKING

import django.db.models.deletion
from django.db import migrations, models

if TYPE_CHECKING:
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor
    from django.db.migrations.state import StateApps


def forwards(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    pass


def backwards(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("corporate", "0037_customerplanoffer"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerplanoffer",
            name="sent_invoice_id",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="customerplanoffer",
            name="sent_invoice_id",
            field=models.CharField(max_length=512, null=True),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name="customerplanoffer",
            old_name="sent_invoice_id",
            new_name="invoice_id",
        ),
        migrations.RemoveField(
            model_name="customerplanoffer",
            name="invoice_id",
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("stripe_invoice_id", models.CharField(max_length=255, unique=True)),
                ("status", models.SmallIntegerField()),
                (
                    "customer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="corporate.customer"),
                ),
            ],
            options={"db_table": "invoice"},
        ),
        migrations.RenameModel(old_name="Invoice", new_name="StripeInvoice"),
        migrations.AlterModelTable(name="stripeinvoice", table="billing_stripe_invoice"),
        migrations.AlterModelTableComment(name="stripeinvoice", table_comment="Stripe invoices"),
        migrations.AlterModelOptions(
            name="stripeinvoice",
            options={"ordering": ["-id"], "verbose_name": "Stripe invoice"},
        ),
        migrations.AlterModelManagers(
            name="stripeinvoice",
            managers=[("objects", models.Manager())],
        ),
        migrations.AlterUniqueTogether(
            name="stripeinvoice",
            unique_together={("stripe_invoice_id", "customer")},
        ),
        migrations.AlterIndexTogether(
            name="stripeinvoice",
            index_together={("status", "customer")},
        ),
        migrations.AlterOrderWithRespectTo(
            name="stripeinvoice",
            order_with_respect_to="customer",
        ),
        migrations.AddIndex(
            model_name="stripeinvoice",
            index=models.Index(fields=["stripe_invoice_id"], name="invoice_stripe_idx"),
        ),
        migrations.RenameIndex(
            model_name="stripeinvoice",
            new_name="invoice_stripe_id_idx",
            old_name="invoice_stripe_idx",
        ),
        migrations.RemoveIndex(
            model_name="stripeinvoice",
            name="invoice_stripe_id_idx",
        ),
        migrations.AddConstraint(
            model_name="stripeinvoice",
            constraint=models.UniqueConstraint(fields=["stripe_invoice_id"], name="invoice_stripe_id_uniq"),
        ),
        migrations.AlterConstraint(
            model_name="stripeinvoice",
            name="invoice_stripe_id_uniq",
            constraint=models.UniqueConstraint(fields=["stripe_invoice_id", "customer"], name="invoice_stripe_id_uniq"),
        ),
        migrations.RemoveConstraint(
            model_name="stripeinvoice",
            name="invoice_stripe_id_uniq",
        ),
        migrations.RunSQL(
            sql="UPDATE billing_stripe_invoice SET status = 0 WHERE status IS NULL",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunPython(
            code=forwards,
            reverse_code=backwards,
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL("CREATE INDEX legacy_idx ON billing_stripe_invoice(status)"),
            ],
            state_operations=[
                migrations.AddIndex(
                    model_name="stripeinvoice",
                    index=models.Index(fields=["status"], name="legacy_idx"),
                ),
            ],
        ),
        migrations.DeleteModel(name="StripeInvoice"),
    ]
