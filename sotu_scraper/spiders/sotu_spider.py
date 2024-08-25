from pathlib import Path
import scrapy


class SotuSpider(scrapy.Spider):
    name = "sotu"
    start_urls = [
        "https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union",
    ]

    def parse(self, response):
        sotu_links = response.css(".table-responsive a::attr(href)")
        yield from response.follow_all(sotu_links, self.parse_sotu)

    def parse_sotu(self, response):
        yield {
            "potus": response.css(".diet-title a::text").get(),
            "date": response.css(".field-docs-start-date-time span::text").get(),
            "categories": response.css(
                ".field-ds-filed-under- + .label-above ~ div a::text"
            ).getall(),
            "speech_html": " ".join(
                response.css(".field-docs-content p::text").getall()
            ),
        }
