from django.shortcuts import render
from django.views import View


class BookView(View):
    def get(self, request):
        return render(request, "home.html")
