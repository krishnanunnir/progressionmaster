from django.urls import path

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.BookView.as_view(), name="index"),
    path("series/<int:pk>", views.BookSeriesView.as_view(), name="series"),
    path("about/", TemplateView.as_view(template_name="about.html")),
]
