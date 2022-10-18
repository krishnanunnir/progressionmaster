from django.contrib import admin
from .models import BookSeries, Book
from .helpers import (
    parseAmazonDetails,
    parseGoodreadsDetail,
    parseGoodreadsSeriesDetail,
)
import logging

logger = logging.getLogger(__name__)
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    def is_goodreads_parsed(self, instance):
        return (
            True
            if instance.goodreads_link
            and instance.goodreads_rating
            and instance.goodreads_rating_count
            else False
        )

    def is_amazon_parsed(self, instance):
        return (
            True
            if instance.amazon_link
            and instance.amazon_rating
            and instance.amazon_rating_count
            else False
        )

    def can_be_public(self, instance):
        if all(
            [
                instance.amazon_link,
                instance.goodreads_link,
                instance.description,
                instance.name,
                instance.author,
            ]
        ):
            return True
        return False

    def update_from_amazon(self, request, queryset):
        for book in queryset:
            try:
                book_dict = parseAmazonDetails(book.amazon_link)
                if book_dict:
                    book.amazon_link = book_dict["amazon_link"]
                    book.amazon_rating = book_dict["amazon_rating"]
                    book.amazon_rating_count = book_dict["amazon_rating_count"]
                    book.has_kindle_unlimited = book_dict["has_kindle_unlimited"]
                    book.has_audiobook = book_dict["has_audiobook"]
                    book.cover_image_url = book_dict["cover_image_url"]
                    book.save()
                    logger.info(f"Updated {book} from Amazon")
                else:
                    logger.info("Nothing to write")
            except Exception as ex:
                logger.exception(f"Couldn't log details for {book.name}")

    def update_from_goodreads(self, request, queryset):
        for book in queryset:
            amazon_link = None
            try:
                if book.goodreads_link:
                    (
                        rating,
                        no_of_rating,
                        book_number,
                        image_url,
                        amazon_link,
                    ) = parseGoodreadsDetail(book.goodreads_link)
                if amazon_link:
                    book.amazon_link = amazon_link
                if rating:
                    book.goodreads_rating = rating
                if book_number:
                    book.book_number = book_number
                if no_of_rating:
                    book.goodreads_rating_count = no_of_rating
                book.cover_image_url = image_url
                book.save()
                logger.info(f"Updated {book} from goodreads")
            except Exception as ex:
                logger.exception(f"Couldn't log details for {book.name}")

    def fill_max_data(self, request, queryset):
        for book in queryset:
            amazon_link = None
            try:
                if book.goodreads_link:
                    (
                        rating,
                        no_of_rating,
                        book_number,
                        image_url,
                        amazon_link,
                    ) = parseGoodreadsDetail(book.goodreads_link)
                if amazon_link:
                    book_dict = parseAmazonDetails(amazon_link)
                    book.amazon_link = book_dict["amazon_link"]
                    book.amazon_rating = book_dict["amazon_rating"]
                    book.amazon_rating_count = book_dict["amazon_rating_count"]
                    book.has_kindle_unlimited = book_dict["has_kindle_unlimited"]
                    book.has_audiobook = book_dict["has_audiobook"]
                if rating:
                    book.cover_image_url = image_url
                    book.goodreads_rating = rating
                    book.goodreads_rating_count = no_of_rating
                book.book_number = book_number
                book.cover_image_url = image_url
                book.save()
                logger.info(f"Updated {book} with max data")
            except Exception:
                logger.exception(f"Couldn't log details for {book.name}")

    update_from_amazon.short_description = "Update from Amazon"
    update_from_goodreads.short_description = "Update from goodreads"
    fill_max_data.short_description = "Fill max data"
    is_goodreads_parsed.boolean = True
    is_amazon_parsed.boolean = True
    can_be_public.boolean = True

    list_display = ("name", "is_goodreads_parsed", "is_amazon_parsed", "can_be_public")

    actions = ["update_from_amazon", "update_from_goodreads", "fill_max_data"]


admin.site.register(Book, BookAdmin)


class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    actions = ["create_book_from_goodreads"]

    def create_book_from_goodreads(self, request, queryset):
        for series in queryset:
            books_list = parseGoodreadsSeriesDetail(series.goodreads_link, series)
            book_instance_list = [Book(**vals) for vals in books_list]
            logger.info(f"Bulk saving {book_instance_list}")
            try:
                Book.objects.bulk_create(book_instance_list)
            except Exception:
                logger.error("Error while saving")
                logger.exception()

    create_book_from_goodreads.short_description = "Create book from goodreads"


admin.site.register(BookSeries, BookSeriesAdmin)
