import string
from bs4 import BeautifulSoup
import requests


def parseAmazonDetails(url: string):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    try:
        title = soup.find("span", attrs={"id": "productTitle"})
        title_value = title.string

        title_string = title_value.strip().replace(",", "")
        description_html = soup.find("div", attrs={"id": "bookDescription_feature_div"})
        description = description_html.text

        rating_text = soup.find(
            "span", attrs={"class": "reviewCountTextLinkedHistogram"}
        )
        rating = rating_text.attrs.get("title").strip().split(" ")[0]
        number_of_rating_element = soup.find(
            "span", attrs={"id": "acrCustomerReviewText"}
        )
        number_of_rating = number_of_rating_element.text.split(" ")[0]
        is_kindle_unlimited = (
            True
            if soup.find("i", attrs={"class": "a-icon-kindle-unlimited"})
            else False
        )
        has_audiobook = (
            True if soup.find("span", attrs={"class": "audible_mm_title"}) else False
        )
        cover_image = soup.find("img", attrs={"id": "ebooksImgBlkFront"})
        cover_image_url = cover_image.attrs.get("src")
        author = soup.find("a", attrs={"class": "contributorNameID"})
        author_value = author.string

        author_string = author_value.strip().replace(",", "")
    except Exception as ex:
        print("couldn't parse the data" + ex)
        return None
    return (
        title_string,
        author_string,
        description,
        rating,
        number_of_rating,
        is_kindle_unlimited,
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
        rating = soup.find("span", attrs={"itemprop": "ratingValue"}).text.strip()
        number_of_rating = soup.find("meta", attrs={"itemprop": "ratingCount"}).text
    except Exception as ex:
        print("couldn't parse the data" + ex)
        return None
    return (rating, number_of_rating)
