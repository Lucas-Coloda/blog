from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post


class PostForm(forms.ModelForm):
    data_lancamento = forms.DateField(widget=forms.SelectDateWidget)
    conteudo = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = Post
        fields = [
            "titulo",
            "sub_titulo",
            "capa",
            "conteudo",
            "rascunho",
            "data_lancamento",
        ]
