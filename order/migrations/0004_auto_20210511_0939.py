# Generated by Django 3.1.7 on 2021-05-11 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210511_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]