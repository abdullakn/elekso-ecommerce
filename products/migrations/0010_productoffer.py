# Generated by Django 3.1.7 on 2021-05-22 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210522_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.IntegerField()),
                ('offer_start', models.DateField()),
                ('offer_end', models.DateField()),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product_table')),
            ],
        ),
    ]
