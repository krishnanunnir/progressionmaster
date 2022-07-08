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
        is_kindle_unlimited,
        has_audiobook,
        cover_image_url,
    )


print(
    parseAmazonDetails(
        "https://www.amazon.in/Harry-Potter-Philosophers-Stone-Rowling-ebook/dp/B019PIOJYU/ref=sr_1_4?crid=2EVB9XLXDM251&keywords=audiobook&qid=1657284898&s=digital-text&sprefix=audiobook%2Cdigital-text%2C269&sr=1-4"
    )
)
