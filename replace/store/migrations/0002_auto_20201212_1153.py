# Generated by Django 3.1.4 on 2020-12-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produit',
            old_name='image',
            new_name='image_1',
        ),
        migrations.AddField(
            model_name='produit',
            name='image_2',
            field=models.ImageField(default=None, upload_to='upload/produit/'),
        ),
    ]