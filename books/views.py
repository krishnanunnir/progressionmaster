from django.shortcuts import render
from django.views import View

from books.models import Book
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)


class BookView(View):
    def get(self, request):
        can_be_public = Q(
            amazon_link__isnull=False,
            goodreads_link__isnull=False,
            description__isnull=False,
            name__isnull=False,
            author__isnull=False,
        )
        books = Book.objects.filter(can_be_public, book_number=1)
        return render(request, "home.html", {"books": books})
