# Generated by Django 3.1.4 on 2020-12-12 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20201212_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sous_categorie',
            name='categorie',
        ),
    ]
