# Generated by Django 3.1.4 on 2020-12-16 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20201216_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
