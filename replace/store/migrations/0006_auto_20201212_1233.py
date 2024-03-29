# Generated by Django 3.1.4 on 2020-12-12 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_categorie_sous_categorie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorie',
            name='sous_categorie',
        ),
        migrations.AddField(
            model_name='sous_categorie',
            name='categorie',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.categorie'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.categorie'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='sous_categorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.sous_categorie'),
        ),
    ]
