from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "titulo",
            "sub_titulo",
            "capa",
            "conteudo",
            "rascunho",
            "publish",
        ]
