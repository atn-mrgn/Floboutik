# Generated by Django 3.1.4 on 2020-12-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_commande_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
