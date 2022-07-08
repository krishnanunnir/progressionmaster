import string
from bs4 import BeautifulSoup
import requests
import json


def parseAmazonDetails(url: string):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    try:
        title_element = soup.find("span", attrs={"id": "productTitle"})
        title_string = title_element.string
        title = title_string.strip().replace(",", "")

        description_element = soup.find(
            "div", attrs={"id": "bookDescription_feature_div"}
        )
        description = description_element.text

        rating_element = soup.find(
            "span", attrs={"class": "reviewCountTextLinkedHistogram"}
        )
        rating = rating_element.attrs.get("title").strip().split(" ")[0]

        ratings_count_elment = soup.find("span", attrs={"id": "acrCustomerReviewText"})
        ratings_count = ratings_count_elment.text.split(" ")[0]
        has_kindle_unlimited = (
            True
            if soup.find("i", attrs={"class": "a-icon-kindle-unlimited"})
            else False
        )
        has_audiobook = (
            True if soup.find("span", attrs={"class": "audible_mm_title"}) else False
        )
        cover_image_element = soup.find("img", attrs={"id": "ebooksImgBlkFront"})
        cover_image_url = cover_image_element.attrs.get("src")

        author_element = soup.find("a", attrs={"class": "contributorNameID"})
        author_string = author_element.string
        author = author_string.strip().replace(",", "")

    except Exception as ex:
        print("couldn't parse the data" + ex)
        return None
    return (
        title,
        author,
        description,
        rating,
        ratings_count,
        has_kindle_unlimited,
        has_audiobook,
        cover_image_url,
    )


def parseGoodreadsDetail(url: string):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    try:
        name = soup.find("span", attrs={"itemprop": "name"}).text.strip()
        rating = soup.find("span", attrs={"itemprop": "ratingValue"}).text.strip()
        ratings_count = soup.find("meta", attrs={"itemprop": "ratingCount"}).text
    except Exception as ex:
        print("couldn't parse the data" + ex)
        return None
    return (name, rating, ratings_count)


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

            series_props = book_element.attrs.get("data-react-props")
            series_json_data = json.loads(series_props)
            for book_all_data in series_json_data["series"]:
                book = book_all_data["book"]
                book_instance = {}
                book_instance["name"] = book["title"]
                book_instance["description"] = book["description"]["html"]
                book_instance["author"] = book["author"]["name"]
                book_instance["goodreads_rating"] = book["avgRating"]
                book_instance["series"] = series
                book_instance[
                    "goodreads_link"
                ] = f"https://www.goodreads.com{book['bookUrl']}"
                books_list.append(book_instance)

    except Exception as ex:
        print("couldn't parse the data" + ex)
        return None
    return books_list
