from django.urls import path

from . import views

urlpatterns = [
    path("books/", views.BookView.as_view(), name="index"),
    path("series/<int:pk>", views.BookSeriesView.as_view(), name="series"),
]
