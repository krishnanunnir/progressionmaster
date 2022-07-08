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
            (
                title,
                author,
                description,
                rating,
                ratings_count,
                has_kindle_unlimited,
                has_audiobook,
                cover_image_url,
            ) = parseAmazonDetails(book.amazon_link)

            book.amazon_rating = rating
            book.has_kindle_unlimited = has_kindle_unlimited
            book.has_audiobook = has_audiobook
            book.cover_image_url = cover_image_url
            book.save()

    def update_from_goodreads(self, request, queryset):
        for book in queryset:
            name, rating, no_of_rating = parseGoodreadsDetail(book.goodreads_link)
            book.goodreads_rating = rating
            book.name = name
            book.save()

    def update_all_fields(self, request, queryset):
        self.update_from_amazon(request, queryset)
        self.update_from_goodreads(request, queryset)

    update_from_amazon.short_description = "Update from Amazon"
    update_from_goodreads.short_description = "Update from goodreads"
    update_all_fields.short_description = "Update all fields"
    has_goodreads_link.boolean = True
    has_amazon_link.boolean = True

    list_display = ("name", "has_goodreads_link", "has_amazon_link")

    actions = ["update_from_amazon", "update_from_goodreads", "update_all_fields"]


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
