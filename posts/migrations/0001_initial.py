# Generated by Django 2.1.4 on 2019-02-05 14:15

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('sub_titulo', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
                ('conteudo', models.TextField(max_length=1000)),
                ('capa', models.ImageField(blank=True, null=True, upload_to=posts.models.upload_location)),
                ('lancado', models.DateTimeField(auto_now_add=True)),
                ('atualizado', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-atualizado', '-lancado'],
            },
        ),
    ]
