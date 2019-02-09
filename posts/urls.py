from django.contrib import admin
from django.urls import path

from .views import (
    post_list,
    post_detail,
    post_create,
    post_update,
    post_delete
)

urlpatterns = [
    path('', post_list, name="list"),
    path('<slug:post_slug>/', post_detail, name='detail'),
    path('add', post_create),
    path('<slug:post_slug>/edit/', post_update, name="update"),
    path('<slug:post_slug>/delete/', post_delete),
]
