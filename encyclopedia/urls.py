from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.page, name="page"),
    path("encyclopedia/create.html", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random/", views.random_page, name='random')
]
