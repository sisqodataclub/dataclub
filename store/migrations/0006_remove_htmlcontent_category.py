# Generated by Django 4.2.8 on 2024-08-25 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_htmlcontent_image1"),
    ]

    operations = [
        migrations.RemoveField(model_name="htmlcontent", name="category",),
    ]
