import scrapy


class PhonescraperSpider(scrapy.Spider):
    name = "PhoneScraper"
    # allowed_domains = ["www.ebay.co.uk"]
    start_urls = [
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=Iphone&_sacat=0"
    ]

    def parse(self, response):
        products_links = response.css("a.s-item__link::attr(href)").getall()
        for product_link in products_links:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_page,
                meta={"Product_Link": product_link},
            )

        # Pagination
        next_page = response.css(
            "a[aria-label='Go to next search page']::attr(href)"
        ).get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_page(self, response):
        product_link = response.meta["Product_Link"]
        product_title = response.css("h1.x-item-title__mainTitle span::text").get()
        product_price = response.css(
            'span[itemprop="price"] span.ux-textspans::text'
        ).get()
        product_img = " | ".join(
            response.css(
                "button.ux-image-filmstrip-carousel-item img::attr(src)"
            ).getall()
        )

        yield {
            "Product_Link": product_link,
            "Product_Title": product_title,
            "Product_Price": product_price,
            "Product_Images": product_img,
        }
