from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup
from django.utils.text import slugify
from django.db.utils import IntegrityError

from pkg.client.client import HttpClient
from loguru import logger as log
from shop.models import Category, Product


class ParserMareety:
    domain = "https://mareety.com/"
    cookies = {
        "pll_language": "uz"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) "
                      "Gecko/20100101 Firefox/111.0"
    }

    def get_http_client(
            self,
            url: str,
            json_data: any = None,
            data: any = None,
    ):
        client = HttpClient(
            url=url,
            headers=self.headers,
            cookies=self.cookies,
            json_data=json_data,
            data=data,
        )
        return client

    @staticmethod
    def _parse_object(text: str, url: str, category: Category) -> dict:
        soup = BeautifulSoup(text, "lxml")
        title = soup.find("h1", attrs={"class": "product_title"})
        if title:
            title = title.text.strip()
        price_tag = soup.find("p", attrs={"class": "price"})
        price = 0.0
        if price_tag:
            price_tag = price_tag.text
            if price_tag:
                price_list = [
                    float(s) for s in price_tag.split() if s.isdigit()
                ]
                for p in price_list:
                    price += p

        image_url = soup.find("img", attrs={"class": "wp-post-image"})
        if image_url:
            image_url = image_url.get("src")

        description = ""
        description_tag = soup.find("div", attrs={"id": "tab-description"})
        if description_tag:
            description_tag = description_tag.find("p")
        if description_tag:
            description = description_tag.text.strip()

        slug = slugify(title)

        return {
            "title": title,
            "price": price,
            "image": image_url,
            "description": description,
            "slug": slug,
            "url": url,
            "category": category
        }

    def _parse_products_by_urls(self, product_urls: List[dict]):
        for item in product_urls:
            client = self.get_http_client(url=item.get("url"))
            response = client.http_get()
            if not response:
                return []
            data = client.http_get_text(response)
            obj = self._parse_object(
                data, item.get("url"), category=item.get("category")
            )
            try:
                product = Product.objects.create(**obj)
                log.debug(product)
            except IntegrityError:
                continue

    def _parse_products_by_category(self, category: Category) -> List[dict]:
        product_urls = []
        for p in range(1, 50):
            url = category.url
            if p != 1:
                url = url + f"page/{p}/"
            client = self.get_http_client(url=url)
            response = client.http_get()
            if not response:
                return product_urls
            data = client.http_get_text(response)
            soup = BeautifulSoup(data, "lxml")
            ul_products = soup.find("ul", attrs={"class": "products"})
            if not ul_products:
                break
            li_product_container = ul_products.find_all("li")
            if li_product_container:
                for lpc in li_product_container:
                    product_url = lpc.find("a")
                    if product_url:
                        product_url = product_url.get("href")
                        product_urls.append(
                            {"url": product_url, "category": category}
                        )
        return product_urls

    def _get_categories(self):
        categories = Category.objects.all()
        if not categories:
            categories = self._parse_categories()
        return categories

    def _parse_categories(self):
        client = self.get_http_client(url=self.domain)
        response = client.http_get()
        if not response:
            return []
        data = client.http_get_text(response)
        soup = BeautifulSoup(data, "lxml")
        a_tags = soup.find_all(
            "a",
            attrs={
                "id": "zakazzvonka"
            }
        )
        categories = []
        for a in a_tags:
            c_name = a.text.strip()
            c_url = a.get('href')
            c_slug = slugify(c_name)
            try:
                category = Category.objects.create(
                    name=c_name,
                    slug=c_slug,
                    url=c_url,
                )
                categories.append(category)
            except IntegrityError:
                continue
        return categories

    def _parse_products_by_categories(self):
        categories = self._get_categories()

        product_urls = []
        futures = []
        with ThreadPoolExecutor(max_workers=len(categories)) as ex:
            for category in categories:
                futures.append(ex.submit(
                    self._parse_products_by_category, category
                ))

        for f in as_completed(futures):
            product_urls += f.result()
        self._parse_products_by_urls(product_urls)

    def runner(self):
        self._parse_products_by_categories()
