from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import datetime
from django.utils import timezone


class Condutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    modelo_carro = models.CharField(max_length=50)
    numero_posts = models.IntegerField(default=0)
    avatar = models.ImageField(default='forum/images/default.png', blank=True)


class Post(models.Model):
    post_titulo = models.CharField(max_length=50)
    post_texto = models.CharField(max_length=500)
    pub_data = models.DateTimeField('data de publicacao')
    gostos = models.IntegerField(default=0)
    imagem = models.ImageField(blank=True)

    def __str__(self):
        return self.imagem

    def __str__(self):
        return self.post_titulo

    def __str__(self):
        return self.post_texto

    def foi_publicado_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)


class Noticia(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.TextField()
    pub_data = models.DateTimeField('data de publicacao')
    imagem = models.ImageField(blank=True)

    def __str__(self):
        return self.titulo

    def __str__(self):
        return self.texto


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comentario_texto = models.CharField(max_length=200)
    gostos = models.IntegerField(default=0)
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.comentario_texto


class Subcomentario(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    subcomentario_texto = models.CharField(max_length=200)
    gostos = models.IntegerField(default=0)
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.subcomentario_texto
