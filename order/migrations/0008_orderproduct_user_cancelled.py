# Generated by Django 3.1.7 on 2021-05-13 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_orderproduct_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='user_cancelled',
            field=models.CharField(default=False, max_length=20, null=True),
        ),
    ]
