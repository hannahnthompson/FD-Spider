import scrapy
from scrapy.spiders import SitemapSpider


class FreshDirectSpider(SitemapSpider):
    name = "freshdirect_sitemap"
    allowed_domains = ["freshdirect.com"]

    # List the sitemap URLs here
    sitemap_urls = [
        "https://www.freshdirect.com/sitemap/sitemap_product_index.xml"
    ]
    sitemap_rules = [
    (r'https://www\.freshdirect\.com/.*/p/[\w-]+', 'parse_product'),  # Adjust the regex to match product URLs
    ]
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "DOWNLOAD_DELAY": 2,  # Delay 2 seconds between requests
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        }
    

    def parse_product(self, response):
        """
        Parse individual product pages and extract desired data.
        """
        self.logger.info(f"Scraping product page: {response.url}")
        product_name = response.xpath("//h1/text()").get() or "N/A" # Adjust the xpath to match product name html
        product_price = response.xpath("//span[@class='price']/text()").get() or "N/A" # Adjust the xpath to match product price html
        yield {
            "url": response.url,
            "name": product_name.strip() if product_name else "N/A",
            "price": product_price.strip() if product_price else "N/A",
        }
