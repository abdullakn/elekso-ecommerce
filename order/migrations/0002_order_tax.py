# Generated by Django 3.1.7 on 2021-05-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.FloatField(null=True),
        ),
    ]
