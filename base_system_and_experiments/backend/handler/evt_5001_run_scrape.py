from urllib import request
from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource

import asyncio
#from concurrent.futures import ThreadPoolExecutor

from requests_html import HTMLSession
import json

#from my_scrapy.my_scrapy import run_process
#from myscrapy.myscrapy.spiders.base_spider import BaseSpider
#from handler.scrapy_resourse import test
from handler.scrapy_resourse import run_process
from handler.scrapy_resourse import BaseSpider

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):
        handler_spec.set_description('スクレイピングを実行します。')
        handler_spec.set_as_responsive()
        return handler_spec
    
    def fire_and_forget(f):
        def wrapped(*args, **kwargs):
            asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)
        return wrapped
    
    #@fire_and_forget
    #def run_scrapy(spider):
        #run_process.run(spider)
        
    #async def run_scraping(self):
        #loop = asyncio.get_running_loop()
        #with ProcessPoolExecutor() as pool:
            #result = await loop.run_in_executor(pool, request)
            #return result
    def request_text(self, r):
        text = r.html.text
        word_list = text.split("\n")
        return word_list
    
    def request_link(self, r):
        link_list = r.html.links
        return link_list
        
    @fire_and_forget
    def request(self):
        asession = HTMLSession()
        url = "http://quotes.toscrape.com/"
        r = asession.get(url)
        result = self.request_text(r)
        d = {}
        for i, res in enumerate(result):
            d[i] = res
        with open('handler/result6.json', 'w') as f:
            json.dump(d, f, indent=4)
                

    @handler_output
    async def handle(self, event, output):
        self.request()
        output.set("RESULT", "result")