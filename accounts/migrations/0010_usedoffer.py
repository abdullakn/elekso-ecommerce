# Generated by Django 3.1.7 on 2021-05-28 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_normalcoupen'),
        ('accounts', '0009_referalcoupen'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.normalcoupen')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]