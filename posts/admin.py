from django.contrib import admin

# Register your models here.
from posts.models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["titulo", "autor", "atualizado"]
    list_display_links = ["titulo", ]
    list_filter = ["titulo", "criado", "atualizado", "autor"]
    search_fields = ["titulo", "conteudo"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
