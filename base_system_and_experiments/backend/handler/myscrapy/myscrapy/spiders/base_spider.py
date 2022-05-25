import scrapy
from bs4 import BeautifulSoup
from ..items import MyscrapyItem

class Parser(object):
    def __init__(self, html: str):
        self._soup = BeautifulSoup(html, 'html.parser')
        
    def parse_title(self):
        return self._soup.find('title').get_text(strip=True)
    
    def parse_links(self):
        return [url.get('href') for url in self._soup.find_all('a')]
    
    def parse_text(self):
        return [text for text in self._soup.get_text().split("\n") if text != ""]

    
class BaseSpider(scrapy.Spider):
    name = "base_spider"
    
    def start_requests(self):
        urls = [
            "http://quotes.toscrape.com/"
            #"https://docs.scrapy.org/en/latest/intro/tutorial.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        parser = Parser(response.text)
        title_text = parser.parse_title()
        links = parser.parse_links()
        texts = parser.parse_text()
        #print("RESULT!!!")
        #print(title_text)
        #print(links)
        #print(texts)
        
        yield MyscrapyItem(
            title=title_text,
            links=links,
            texts=texts
        )