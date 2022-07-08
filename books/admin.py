from django.contrib import admin
from .models import BookSeries, Book
from .helpers import parseAmazonDetails

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author")

    actions = ["update_from_amazon"]

    def update_from_amazon(self, request, queryset):
        for book in queryset:
            (
                title_string,
                author_string,
                is_kindle_unlimited,
                has_audiobook,
                cover_image_url,
            ) = parseAmazonDetails(book.amazon_link)

            book.name = title_string
            book.author = author_string
            book.has_kindle_unlimited = is_kindle_unlimited
            book.has_audiobook = has_audiobook
            book.cover_image_url = cover_image_url
            book.save()

    update_from_amazon.short_description = "Update from Amazon"


admin.site.register(Book, BookAdmin)


class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "author")


admin.site.register(BookSeries, BookSeriesAdmin)
