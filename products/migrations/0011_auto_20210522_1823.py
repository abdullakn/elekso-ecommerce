# Generated by Django 3.1.7 on 2021-05-22 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_productoffer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productoffer',
            old_name='category',
            new_name='product',
        ),
    ]
