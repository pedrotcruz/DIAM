from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    # index
    path("", views.index, name="index"),
    # detalhe
    path('<int:post_id>', views.detalhe, name='detalhe'),
    # criar post
    path("criarpost", views.criarpost, name='criarpost'),
    # remover post
    path('<int:post_id>/removerpost', views.removerpost, name='removerpost'),
    # remover comentario
    path('<int:comentario_id>/removercomentario', views.removercomentario, name='removercomentario'),
    # gosto post
    path('<int:post_id>/gosto_post', views.gosto_post, name='gosto_post'),
    # login
    path("login", views.fazerLogin, name='fazerLogin'),
    # signin
    path('signin', views.signIn, name='signin'),
    # logout
    path('logout', views.fazerLogout, name='logout'),
    # info
    path('info', views.info, name='info'),
    # comentario
    path('<int:post_id>/criarcomentario', views.criarcomentario, name='criarcomentario'),
    # gosto comentario
    path('<int:comentario_id>/gosto_comentario', views.gosto_comentario, name='gosto_comentario'),
    # upload de imagens
    path('fazer_upload', views.fazer_upload, name='fazer_upload'),
    # upload de imagens avatar
    path('fazer_upload_avatar', views.fazer_upload_avatar, name='fazer_upload_avatar'),
    # subcomentario
    path('<int:comentario_id>/criarsubcomentario', views.criarsubcomentario, name='criarsubcomentario'),
    # index noticias
    path('index_noticia', views.index_noticia, name='index_noticia'),
    # criar noticia
    path("criarnoticia", views.criarnoticia, name='criarnoticia'),
]
