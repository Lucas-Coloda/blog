from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from .forms import PostForm
from .models import Post
from django.utils import timezone
from blog.utils import load_pages


def post_list(request):
    if request.user.is_superuser:
        queryset_list = Post.posts.user_posts(request.user).order_by("-atualizado")
        page_html = "super_user/post_list.html"
    else:
        queryset_list = Post.posts.public().order_by("-atualizado")
        page_html = "common_user/post_list.html"

    queryset = load_pages(request, queryset_list)
    context = {
        "lista": queryset,
        "titulo": "Meus posts"
    }
    return render(request, page_html, context)


def post_detail(request, post_slug):
    instancia = get_object_or_404(Post, slug=post_slug)
    context = {
        "titulo": instancia.titulo,
        "objeto": instancia
    }
    if request.user.is_superuser:
        return render(request, "super_user/post_detail.html", context)
    else:
        if instancia.rascunho or instancia.data_lancamento == timezone.now():
            raise Http404
        else:
            return render(request, "common_user/post_detail.html", context)


def post_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    formulario = PostForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        instancia = formulario.save(commit=False)
        instancia.autor = request.user
        instancia.save()
        messages.success(request, "Item criado", extra_tags='html_safe')
        return HttpResponseRedirect(instancia.get_absolute_url())
    else:
        messages.error(request, "Não criado")
    context = {
        "titulo": "Novo post",
        "formulario": formulario
    }
    return render(request, "forms/post_form.html", context)


def post_update(request, post_slug=None):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    instancia = get_object_or_404(Post, slug=post_slug)
    formulario = PostForm(request.POST or None, request.FILES or None, instance=instancia)
    if formulario.is_valid():
        instancia = formulario.save(commit=False)
        instancia.save()
        messages.success(request, "Salvo", extra_tags='html_safe')
        return HttpResponseRedirect(instancia.get_absolute_url())
    else:
        messages.error(request, "Nao salvo")
    context = {
        "titulo": instancia.titulo,
        "formulario": formulario,
        "objeto": instancia
    }
    return render(request, "forms/post_form.html", context)


def post_delete(request, post_slug=None):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    instancia = get_object_or_404(Post, slug=post_slug)
    instancia.delete()
    messages.success(request, "Deletado")
    return redirect("/posts")
