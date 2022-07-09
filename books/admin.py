from django.contrib import admin
from .models import BookSeries, Book
from .helpers import (
    parseAmazonDetails,
    parseGoodreadsDetail,
    parseGoodreadsSeriesDetail,
)

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    def has_goodreads_link(self, instance):
        return True if instance.goodreads_link else False

    def has_amazon_link(self, instance):
        return True if instance.amazon_link else False

    def update_from_amazon(self, request, queryset):
        for book in queryset:
            book_dict = parseAmazonDetails(book.amazon_link)
            book.amazon_rating = book_dict["amazon_rating"]
            book.has_kindle_unlimited = book_dict["has_kindle_unlimited"]
            book.has_audiobook = book_dict["has_audiobook"]
            book.cover_image_url = book_dict["cover_image_url"]
            book.save()

    def update_from_goodreads(self, request, queryset):
        for book in queryset:
            amazon_link = None
            if book.goodreads_link:
                rating, no_of_rating, amazon_link = parseGoodreadsDetail(
                    book.goodreads_link
                )
            if amazon_link:
                book_dict = parseAmazonDetails(amazon_link)
                book.amazon_link = book_dict["amazon_link"]
                book.amazon_rating = book_dict["amazon_rating"]
                book.has_kindle_unlimited = book_dict["has_kindle_unlimited"]
                book.has_audiobook = book_dict["has_audiobook"]
                book.cover_image_url = book_dict["cover_image_url"]
            if not book.goodreads_rating:
                book.goodreads_rating = rating
            if not book.amazon_rating:
                book.amazon_rating
            book.save()

    update_from_amazon.short_description = "Update from Amazon"
    update_from_goodreads.short_description = "Update from goodreads"
    has_goodreads_link.boolean = True
    has_amazon_link.boolean = True

    list_display = ("name", "has_goodreads_link", "has_amazon_link")

    actions = ["update_from_amazon", "update_from_goodreads"]


admin.site.register(Book, BookAdmin)


class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    actions = ["create_book_from_goodreads"]

    def create_book_from_goodreads(self, request, queryset):
        for series in queryset:
            books_list = parseGoodreadsSeriesDetail(series.goodreads_link, series)
            book_instance_list = [Book(**vals) for vals in books_list]
            Book.objects.bulk_create(book_instance_list)

    create_book_from_goodreads.short_description = "Create book from goodreads"


admin.site.register(BookSeries, BookSeriesAdmin)
