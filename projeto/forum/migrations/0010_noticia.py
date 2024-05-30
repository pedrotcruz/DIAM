# Generated by Django 5.0.4 on 2024-05-12 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_subcomentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('texto', models.TextField()),
                ('pub_data', models.DateTimeField(verbose_name='data de publicacao')),
                ('imagem', models.ImageField(blank=True, upload_to='')),
            ],
        ),
    ]