import os
import sys

import django


progressionmaster_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(progressionmaster_dir, ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "progressionmaster.settings")
django.setup()

from books.models import BookSeries


def populate():
    print(BookSeries.objects.all()[0])


if __name__ == "__main__":
    populate()
