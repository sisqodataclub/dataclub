# Generated by Django 4.2.8 on 2024-08-26 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0009_alter_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(blank=True, default="", max_length=950, null=True),
        ),
    ]
