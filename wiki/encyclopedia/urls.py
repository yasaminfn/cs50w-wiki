from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:filename>/", views.entry, name = "markdown_page"),
    path("search/", views.search, name ="search"),
    path("newpage/", views.newpage, name="new_page"),
    path("edit/", views.edit, name="edit_entry"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("rand_page", views.rand_page, name="rand_page"),
]
