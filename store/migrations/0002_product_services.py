# Generated by Django 4.2.8 on 2024-08-18 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="services",
            field=models.TextField(blank=True, null=True),
        ),
    ]
