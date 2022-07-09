from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookView.as_view(), name="index"),
    path("<int:pk>", views.BookSeriesView.as_view(), name="series"),
]
