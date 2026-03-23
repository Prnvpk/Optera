# Generated manually for Render/Postgres compatibility.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storeapp", "0003_orders"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="gmail",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="users",
            name="number",
            field=models.CharField(max_length=15),
        ),
    ]
