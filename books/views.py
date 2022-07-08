from django.shortcuts import render
from django.views import View

from books.models import Book


class BookView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, "home.html", {"books": books})
