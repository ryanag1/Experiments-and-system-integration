# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter


class MyscrapyPipeline:
    
    def open_spider(self, spider):
        #self.link_to_expoter = {}
        self.exporter = None
        
    def close_spider(self, spider):
        #for exporter, json_file in self.link_to_exporter.values():
            #exporter.finish_exporting()
            #json_file.close()
        self.exporter[0].finish_exporting()
        self.exporter[1].close()
            
    def _exporter_for_item(self, item):
        #adapter = ItemAdapter(item)
        #link = adapter['links']
        #if link not in self.link_to_exporter:
            #json_file = open(f'{link}.json, 'wb')
        json_file = open('result.json', 'wb')
        exporter = JsonLinesItemExporter(json_file)
        exporter.start_exporting()
        #self.link_to_exporter[link] = (exporter, link_file)
        #return link_to_exporter[link][0]
        self.exporter = (exporter, json_file)
        return self.exporter[0]
    
    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
