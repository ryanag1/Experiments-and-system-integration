import scrapy
from scrapy.crawler import CrawlerProcess

from .spiders.base_spider import BaseSpider


def run(spider):
    process = CrawlerProcess(settings={
        "FEEDS": {
            "result.json": {"format": "json"},
        },
    })
    process.crawl(spider)
    process.start(stop_after_crawl=False)
