from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from books.models import Book, BookSeries
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)


class BookView(TemplateView):
    template_name = "home.html"

    def get_template_names(self):
        if self.request.GET.get("order"):
            return "_books.html"
        return "home.html"

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data(**kwargs)
        can_be_public = Q(
            amazon_link__isnull=False,
            goodreads_link__isnull=False,
            description__isnull=False,
            name__isnull=False,
            author__isnull=False,
        )
        order = self.request.GET.get("order")
        books = Book.objects.filter(can_be_public, book_number=1)
        if order:
            try:
                books = books.order_by(f"-{order}")
            except Exception:
                logger.error(f"Couldn't sort for-{order}")

        context["books"] = books
        return context


class BookSeriesView(DetailView):
    model = BookSeries
    template_name = "home.html"

    def get_template_names(self):
        if self.request.GET.get("order"):
            return "_books.html"
        return "home.html"

    def get_context_data(self, **kwargs):
        context = super(BookSeriesView, self).get_context_data(**kwargs)
        can_be_public = Q(
            amazon_link__isnull=False,
            goodreads_link__isnull=False,
            description__isnull=False,
            name__isnull=False,
            author__isnull=False,
        )
        books = Book.objects.filter(can_be_public, series=self.kwargs.get("pk"))
        order = self.request.GET.get("order")
        if order:
            try:
                books = books.order_by(f"-{order}")
            except Exception:
                logger.error(f"Couldn't sort for-{order}")
        if books:
            context["books"] = books
        return context
