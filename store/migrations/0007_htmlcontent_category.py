# Generated by Django 4.2.8 on 2024-08-25 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_remove_htmlcontent_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="htmlcontent",
            name="category",
            field=models.ForeignKey(
                default=4,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.category",
            ),
        ),
    ]
