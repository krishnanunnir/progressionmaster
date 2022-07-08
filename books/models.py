from django.db import models
import urllib.request
from django.core.exceptions import ValidationError
from django.core.files import File
import os


class BookSeries(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    book_number = models.IntegerField(null=True, blank=True)
    series = models.ForeignKey(
        "BookSeries", on_delete=models.CASCADE, null=True, blank=True
    )
    amazon_link = models.URLField(null=True, blank=True)
    goodreads_link = models.URLField(null=True, blank=True)
    read_online_link = models.URLField(null=True, blank=True)
    amazon_rating = models.FloatField(null=True, blank=True)
    goodreads_rating = models.FloatField(null=True, blank=True)
    has_audiobook = models.BooleanField(null=True, blank=True)
    has_kindle_unlimited = models.BooleanField(null=True, blank=True)
    cover_image_url = models.URLField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    is_public = models.BooleanField(default=False)

    def get_remote_image(self):
        if self.cover_image_url and not self.cover_image:
            result = urllib.request.urlretrieve(self.cover_image_url)
            self.cover_image.save(
                os.path.basename(self.cover_image_url), File(open(result[0]))
            )
            self.save()

    def clean(self):
        if not self.amazon_link or self.goodreads_link:
            raise ValidationError("You must specify either amazon or goodreads link")

    def save(self, *args, **kwargs):
        if getattr(self, "_cover_image_url_changed", True):
            self.cover_image = self.get_remote_image()
        super(Book, self).save(*args, **kwargs)
