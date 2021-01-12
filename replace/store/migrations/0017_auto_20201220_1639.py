# Generated by Django 3.1.4 on 2020-12-20 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_bestseller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bestseller',
            old_name='best',
            new_name='name',
        ),
        migrations.CreateModel(
            name='NewProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.produit')),
            ],
        ),
    ]
