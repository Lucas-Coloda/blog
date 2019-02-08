from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import PostForm
from .models import Post
from django.utils import timezone


def post_list(request):
    queryset_list = Post.objects.filter(rascunho=False).filter(publish__lte=timezone.now()).order_by("-atualizado")
    paginator = Paginator(queryset_list, 10)

    page = request.GET.get('pag')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "lista": queryset,
        "titulo": "Meus posts"
    }
    return render(request, "post_list.html", context)


def post_detail(request, post_slug):
    instancia = get_object_or_404(Post, slug=post_slug)
    context = {
        "titulo": instancia.titulo,
        "objeto": instancia
    }
    if request.user.is_superuser:
        return render(request, "post_detail_super_user.html", context)
    else:
        return render(request, "post_detail.html", context)


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
    return render(request, "post_form.html", context)


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
    return render(request, "post_form.html", context)


def post_delete(request, post_slug=None):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    instancia = get_object_or_404(Post, slug=post_slug)
    instancia.delete()
    messages.success(request, "Deletado")
    return redirect("/posts")
