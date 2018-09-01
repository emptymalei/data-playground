# -*- coding: utf-8 -*-
import scrapy


class DatasciSpider(scrapy.Spider):
    name = 'datasci'
    allowed_domains = ['www.linkedin.com']
    start_urls = ['https://www.linkedin.com/search/results/people/?keywords=data%20scientist&origin=SWITCH_SEARCH_VERTICAL']


    # rules = (
        # Rule(LinkExtractor(allow=(), restrict_css=('.next',)),
             # callback="parse_item",
             # follow=True),)

    def parse(self, response):
        print('Processing... Page: ' + response.url)
        pass
