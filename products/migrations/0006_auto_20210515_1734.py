# Generated by Django 3.1.7 on 2021-05-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210515_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_table',
            name='storage',
            field=models.CharField(choices=[('32 GB', '32 GB'), ('64 GB', '64 GB'), ('128 GB', '128 GB'), ('256 GB', '256 GB'), ('512 GB', '512 GB')], max_length=20),
        ),
    ]
