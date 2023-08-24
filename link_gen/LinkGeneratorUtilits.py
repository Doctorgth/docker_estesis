from time import sleep, time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from proxy import get_proxy

use_proxy=False
def set_use_proxy(value):# если поставить True то подключение всех страниц через классы этого файла будет по прокси
    global use_proxy
    use_proxy=value
class LinkGen():
    def __init__(self):
        pass

    def create_soup(self, url):  # качает страницу для работы локально
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def create_soup_js(self, url):  # качает с применением браузера, для обхода антидодоса
        chrome_options = Options()
        #chrome_options.add_argument('--proxy-server=143.244.60.116:8443')

        global use_proxy
        if use_proxy:
            chrome_options.add_argument('--proxy-server='+get_proxy())


        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

        chrome_options.add_argument("--headless")
        # chrome_options.add_argument('--user-agent={0}'.format(user_agent))
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        if use_proxy:
            sleep(20)
        sleep(5)
        html = driver.page_source
        """
        with open("index.html", "w") as file:
            file.write(html)
        """

        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        return soup

    def generate_links_no_abstract(self, url, Use_Js=False):  # тащит все ссылки со страница, ожидает ссылку
        right_url = create_main_page_link(url)  # на конкретно раздел с новостями
        soup = ""
        ret = []
        if Use_Js:
            soup = self.create_soup_js(url)
        else:
            soup = self.create_soup(url)
        a_tags = soup.find_all("a")

        for a_tag in a_tags:

            parsed_url = a_tag.get("href")

            if parsed_url is not None:

                if not (parsed_url.startswith("http")) and not (parsed_url.startswith("#")):
                    if not parsed_url.startswith("/"):
                        ret.append(right_url + "/" + parsed_url)
                    else:
                        ret.append(right_url + parsed_url)
        return list(set(ret))

    def generate_links_no_abstract_for_search(self, url, search_type,
                                              Use_Js=False):  # тащит все ссылки со страница, ожидает ссылку
        right_url = create_main_page_link(url)  # на конкретно раздел с новостями
        soup = ""
        ret = []
        if Use_Js:
            soup = self.create_soup_js(url)
        else:
            soup = self.create_soup(url)
        a_tags = soup.find_all("a")

        for a_tag in a_tags:
            parsed_url = a_tag.get("href")
            parsed_text = a_tag.text
            if parsed_url is not None:
                if (parsed_url.startswith("http")) and not search_type in parsed_url:
                    # if not parsed_url.startswith("/"):
                    ret.append(parsed_url)
                    parsed_texts = parsed_text.split(">")
                    for parsed_text in parsed_texts:
                        if parsed_text.startswith("http") and not search_type in parsed_text:
                            ret.append(parsed_text)
                    # else:
                    # ret.append(right_url + parsed_url)

            pass

        return list(set(ret))

    def generate_links_abstract(self, url,
                                Use_Js=False):  # Принимает ссылку на сайт и ищет там сам ссылки на раздел новости
        urls = find_news_url(url)  # затем обходит найденые ссылки и с каждой из них тащит все что нашел
        ret = []  # без дубликатов
        right_url = create_main_page_link(url)
        for url in urls:
            if Use_Js:
                soup = self.create_soup_js(url)
            else:
                soup = self.create_soup(url)
            a_tags = soup.find_all("a")

            for a_tag in a_tags:
                parsed_url = a_tag.get("href")
                if parsed_url is not None:
                    if not (parsed_url.startswith("http")) and not (parsed_url.startswith("#")):
                        if not parsed_url.startswith("/"):
                            ret.append(right_url + "/" + parsed_url)
                        else:
                            ret.append(right_url + parsed_url)

        return list(set(ret))


def create_main_page_link(
        url):  # применяется для получения основной ссылки на сайт, т.к все найденые ссылки в формате /new/231
    ret = ""
    count = 0
    for i in url:
        ret += i
        if i == "/":

            count += 1
            if count >= 3:
                break
    return ret[:-1]


def check_key_words(st, key_w_m):  # Проверяет строку на вхождение в неё ключевых слов
    for i in key_w_m:
        if i in st:
            return True
    return False


def find_news_url(url):  # ищет все url которвые как либо связанны с разделом новостей
    x = LinkGen()
    urls = x.generate_links_no_abstract(url)
    ret = []
    key_w = ["new", "event", "press", "novosti", "all"]
    for i in urls:
        if check_key_words(i, key_w):
            ret.append(i)
    return list(set(ret))
