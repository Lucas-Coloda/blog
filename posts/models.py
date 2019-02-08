from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings


# Create your models here.
# MVC model view conroler


def upload_location(intance, filename):
    return "%s/%s" % (intance.slug, filename)


class Post(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    titulo = models.CharField(max_length=150)
    sub_titulo = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    conteudo = models.TextField(max_length=3000)
    capa = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    rascunho = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    lancado = models.DateTimeField(auto_now=False, auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return "/posts/%s/" % self.slug

    class Meta:
        ordering = ["-atualizado", "-lancado"]


def create_slug(intance, new_slug=None):
    slug = slugify(intance.titulo)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(intance, new_slug=new_slug)
    return slug


def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciver, sender=Post)
