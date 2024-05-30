from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Post, Condutor, Comentario, Subcomentario, Noticia


def index(request):
    latest_post_list = Post.objects.order_by('-pub_data')[:10]
    context = {'latest_post_list': latest_post_list}
    return render(request, 'forum/index.html', context)


def detalhe(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'forum/detalhe.html', {'post': post})


@login_required(login_url='/forum/login')
def criarpost(request):
    if request.method == 'POST':
        try:
            post_titulo = request.POST.get("titulo")
            post_texto = request.POST.get("texto")
        except KeyError:
            return render(request, 'forum/criarpost.html')
        if post_titulo and post_texto:
            post = Post(post_titulo=post_titulo, post_texto=post_texto, pub_data=timezone.now())
            post.save()
            condutor = Condutor.objects.get(user=request.user)
            condutor.numero_posts += 1
            condutor.save()
            return HttpResponseRedirect(reverse('forum:detalhe', args=(post.id,)))
        else:
            return HttpResponseRedirect(reverse('forum:criarpost'))
    else:
        return render(request, 'forum/criarpost.html')


@login_required(login_url='/forum/login')
def criarcomentario(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        try:
            comentario_texto = request.POST.get("comentario")
        except KeyError:
            return render(request, 'forum/detalhe.html')
        if comentario_texto:
            comentario = Comentario(post=post, comentario_texto=comentario_texto, pub_data=timezone.now())
            comentario.save()
            return HttpResponseRedirect(reverse('forum:detalhe', args=(post.id,)))
        else:
            return HttpResponseRedirect(reverse('forum:detalhe', args=(post.id,)))
    else:
        return render(request, 'forum/detalhe.html',{'post': post})


@login_required(login_url='/forum/login')
def criarsubcomentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    if request.method == 'POST':
        try:
            subcomentario_texto = request.POST.get("subcomentario")
        except KeyError:
            return render(request, 'forum/detalhe.html')
        if subcomentario_texto:
            subcomentario = Subcomentario(comentario=comentario, subcomentario_texto=subcomentario_texto,
                                          pub_data=timezone.now())
            subcomentario.save()
            return HttpResponseRedirect(reverse('forum:detalhe', args=(comentario.post_id,)))
        else:
            return HttpResponseRedirect(reverse('forum:detalhe', args=(comentario.post_id,)))
    else:
        return render(request, 'forum/detalhe.html')


@login_required(login_url='/forum/login')
def gosto_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.gostos += 1
    post.save()
    return HttpResponseRedirect(reverse('forum:detalhe', args=(post_id,)))


@login_required(login_url='/forum/login')
@permission_required('forum.delete_post', login_url='/forum/login')
def removerpost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return render(request, 'forum/removerpost.html')


@login_required(login_url='/forum/login')
@permission_required('forum.delete_comentario', login_url='/forum/login')
def removercomentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    comentario.delete()
    return HttpResponseRedirect(reverse('forum:detalhe', args=(comentario.post_id,)))


@login_required(login_url='/forum/login')
def gosto_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    comentario.gostos += 1
    comentario.save()
    return HttpResponseRedirect(reverse('forum:detalhe', args=(comentario.post_id,)))


def fazerLogin(request):
    if request.method == 'POST':
        user = request.POST.get("username")
        password = request.POST.get("password")
        a = authenticate(username=user, password=password)
        if a is not None:
            login(request, a)
            return HttpResponseRedirect(reverse('forum:index'))
        else:
            return render(request, 'forum/login_error.html')
    else:
        return render(request, 'forum/fazerLogin.html')


def signIn(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    modelo_carro = request.POST.get("modelo_carro")
    nome = request.POST.get("nome")
    apelido = request.POST.get("apelido")
    if username and email and password and modelo_carro is not None:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = nome
        user.last_name = apelido
        user.save()
        condutor = Condutor(user=user, modelo_carro=modelo_carro)
        condutor.save()
        return HttpResponseRedirect(reverse('forum:index'))
    else:
        return render(request, 'forum/signin.html', {'msg_erro': 'Preencher campos em falta.'})


def fazerLogout(request):
    logout(request)
    return render(request, 'forum/logout.html')


@login_required(login_url='/forum/login')
def info(request):
    return render(request, 'forum/info.html')


# Imagens
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def fazer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        post = Post.objects.get(post_titulo=request.post.post_titulo)
        post.imagem = 'media/' + filename
        post.save()
        return render(request, 'forum/fazer_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'forum/fazer_upload.html')


def fazer_upload_avatar(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        condutor = Condutor.objects.get(user=request.user)
        condutor.avatar = 'media/' + filename
        condutor.save()
        return render(request, 'forum/fazer_upload_avatar.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'forum/fazer_upload_avatar.html')


def index_noticia(request):
    latest_noticia_list = Noticia.objects.order_by('-pub_data')[:10]
    context = {'latest_noticia_list': latest_noticia_list}
    return render(request, 'forum/index_noticia.html', context)


@login_required(login_url='/forum/login')
def criarnoticia(request):
    if request.method == 'POST':
        try:
            titulo = request.POST.get("titulo")
            texto = request.POST.get("texto")
        except KeyError:
            return render(request, 'forum/criarnoticia.html')
        if titulo and texto:
            noticia = Noticia(titulo=titulo, texto=texto, pub_data=timezone.now())
            noticia.save()
            return HttpResponseRedirect(reverse('forum:index_noticia'))
        else:
            return HttpResponseRedirect(reverse('forum:criarnoticia'))
    else:
        return render(request, 'forum/criarnoticia.html')
