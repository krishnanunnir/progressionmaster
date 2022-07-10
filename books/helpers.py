import string
from bs4 import BeautifulSoup
import requests
import json
import logging

logger = logging.getLogger(__name__)


def parseAmazonDetails(url: string):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    try:
        title_element = soup.find("span", attrs={"id": "productTitle"})
        title = title_element.string.strip().replace(",", "") if title_element else None

        description_element = soup.find(
            "div", attrs={"id": "bookDescription_feature_div"}
        )
        description = description_element.text if description_element else None

        rating_element = soup.find(
            "span", attrs={"class": "reviewCountTextLinkedHistogram"}
        )
        rating = (
            rating_element.get("title").strip().split(" ")[0]
            if rating_element
            else None
        )

        ratings_count_element = soup.find("span", attrs={"id": "acrCustomerReviewText"})
        ratings_count = (
            ratings_count_element.text.split(" ")[0] if ratings_count_element else None
        )
        has_kindle_unlimited = (
            True
            if soup.find("i", attrs={"class": "a-icon-kindle-unlimited"})
            else False
        )
        has_audiobook = (
            True if soup.find("span", attrs={"class": "audible_mm_title"}) else False
        )
        cover_image_element = soup.find("img", attrs={"id": "ebooksImgBlkFront"})
        cover_image_url = (
            cover_image_element.get("src") if cover_image_element else None
        )

        author_element = soup.find("a", attrs={"class": "contributorNameID"})
        author = (
            author_element.string.strip().replace(",", "") if author_element else None
        )

    except Exception as ex:
        logger.error(f"Parsing the data failled for {url}")
        logger.exception("message")

        return None

    book = {
        "amazon_link": webpage.url.rsplit("/", 1)[0],
        "amazon_rating": rating,
        "has_kindle_unlimited": has_kindle_unlimited,
        "amazon_rating_count": int(ratings_count.replace(",", "")),
        "has_audiobook": has_audiobook,
        "cover_image_url": cover_image_url,
    }
    return book


def parseGoodreadsDetail(url: string):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    try:
        share_element = soup.find(
            "div", attrs={"data-react-class": "ReactComponents.ShareDialog"}
        )
        book_props = json.loads(share_element.get("data-react-props", {})).get(
            "previewData"
        )
        rating = book_props.get("rating")
        ratings_count = book_props.get("ratingsCount")
        series_element = soup.find("h2", attrs={"id": "bookSeries"})
        book_number = (
            series_element.text.split(" ")[-1].lstrip("#").rstrip(")\n")
            if series_element
            else None
        )

        image_url = book_props.get("imageUrl")

        amazon_link_element = soup.find("a", attrs={"id": "buyButton"})
        amazon_link = amazon_link_element.get("href")
    except Exception as ex:
        logger.error(f"Parsing the data failled for {url}")
        logger.exception("message")
        return (None, None, None, None)
    return (
        rating,
        ratings_count,
        book_number,
        image_url,
        f"https://www.goodreads.com{amazon_link}",
    )


def parseGoodreadsSeriesDetail(url: string, series):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    books_list = []
    try:
        all_books_element = soup.find_all(
            "div", attrs={"data-react-class": "ReactComponents.SeriesList"}
        )
        for book_element in all_books_element:

            series_props = book_element.get("data-react-props")
            series_json_data = json.loads(series_props)
            for book_all_data in series_json_data["series"]:
                book = book_all_data["book"]
                if book.get("textReviewsCount", 0) == 0:
                    continue
                book_instance = {}
                book_instance["name"] = book.get("title")
                book_instance["description"] = book.get("description", {}).get("html")
                book_instance["author"] = book.get("author", {}).get("name")
                book_instance["goodreads_rating"] = book.get("avgRating")
                book_instance["series"] = series
                book_instance["goodreads_link"] = (
                    f"https://www.goodreads.com{book.get('bookUrl','')}"
                    if book.get("bookUrl")
                    else None
                )
                book_instance["cover_image_url"] = book.get("imageUrl")
                book_instance["goodreads_rating_count"] = book.get("ratingsCount", None)
                books_list.append(book_instance)

    except Exception as ex:
        logger.error(f"Parsing the data failled for {url}")
        logger.exception("message")
        return None
    return books_list
