# Generated by Django 5.0.4 on 2024-05-07 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_condutor_delete_utilizador'),
    ]

    operations = [
        migrations.AddField(
            model_name='condutor',
            name='numero_posts',
            field=models.IntegerField(default=0),
        ),
    ]