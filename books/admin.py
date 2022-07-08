from django.contrib import admin
from .models import BookSeries, Book
from .helpers import parseAmazonDetails, parseGoodreadsDetail

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author")

    actions = ["update_from_amazon", "update_from_goodreads", "update_all_fields"]

    def update_from_amazon(self, request, queryset):
        for book in queryset:
            (
                title_string,
                author_string,
                description,
                rating,
                number_of_rating,
                is_kindle_unlimited,
                has_audiobook,
                cover_image_url,
            ) = parseAmazonDetails(book.amazon_link)

            book.name = title_string
            book.author = author_string
            book.description = description
            book.amazon_rating = rating
            book.has_kindle_unlimited = is_kindle_unlimited
            book.has_audiobook = has_audiobook
            book.cover_image_url = cover_image_url
            book.save()

    def update_from_goodreads(self, request, queryset):
        for book in queryset:
            rating, no_of_rating = parseGoodreadsDetail(book.goodreads_link)
            book.goodreads_rating = rating
            book.save()

    def update_all_fields(self, request, queryset):
        self.update_from_amazon(request, queryset)
        self.update_from_goodreads(request, queryset)

    update_from_amazon.short_description = "Update from Amazon"
    update_from_goodreads.short_description = "Update from goodreads"
    update_all_fields.short_description = "Update all fields"


admin.site.register(Book, BookAdmin)


class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "author")


admin.site.register(BookSeries, BookSeriesAdmin)
