import scrapy
from ..items import JessopItem
from scrapy.loader import ItemLoader


class MyspySpider(scrapy.Spider):
    name = "myspy"
    allowed_domains = ["www.jessops.com"]
    start_urls = ["https://www.jessops.com/drones"]

    def parse(self, response):
        for product in response.css("div.details-pricing"):
            il = ItemLoader(item=JessopItem(), selector=product)

            il.add_css("name", "a")
            il.add_css("link", "a::attr(href)")
            il.add_css("price", "p.price.larger")
            il.add_css("discount", "span.save")
            il.add_css("availability", "li.false")
            il.add_css("specs", "ul.f-list.j-list li")
            yield il.load_item()

        next_page = response.css(
            "ul.f-pagination.f-margin-large-top a::attr(href)"
        ).get()
        if next_page is not None:
            # yield response.follow(next_page, callback=self.parse)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
