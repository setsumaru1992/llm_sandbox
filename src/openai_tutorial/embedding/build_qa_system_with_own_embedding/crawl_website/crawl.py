import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os

HTTP_URL_PATTERN = r"^http[s]?://.+"
domain = "openai.com"
full_url = "https://openai.com/"

class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hyperlinks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])


def get_hyperlinks(url):
    try:
        with urllib.request.urlopen(url) as response:
            if not response.info().get("Content-Type").startswith("text/html"):
                return []

            html = response.read().decode("utf-8")
    except Exception as e:
        print(e)
        return []
    parser = HyperlinkParser()
    parser.feed(html)
    return parser.hyperlinks


def get_domain_hyperlinks(local_domain, url):
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None

        if re.search(HTTP_URL_PATTERN, link):
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    return list(set(clean_links))


def mkdir_if_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)


crawl_result_dir = os.path.dirname(__file__) + "/text"
processed_dir = os.path.dirname(__file__) + "/processed"


def crawl(url):
    local_domain = urlparse(url).netloc
    crawl_result_dir_with_domain = crawl_result_dir + "/" + local_domain

    queue = deque([url])
    seen = set([url])

    mkdir_if_not_exist(crawl_result_dir)
    mkdir_if_not_exist(crawl_result_dir_with_domain)
    mkdir_if_not_exist(processed_dir)

    while queue:
        url = queue.pop()
        print(url)

        with open(crawl_result_dir_with_domain + "/" + url[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            text = soup.get_text()
            if("You need to enable Javascript to run this app." in text):
                print("Unale to parse page " + url + " due to Javascript being required")
            f.write(text)

        for link in get_domain_hyperlinks(local_domain, url):
            if link not in seen:
                queue.append(link)
                seen.add(link)

crawl(full_url)