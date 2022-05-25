from ducts.spi import EventHandler
from handler.handler_output import handler_output


import asyncio

import csv

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):

        handler_spec.set_description('記録します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        obj_list = event.data["obj"]
        for obj in obj_list:
            data = obj.split(';')
            with open('handler/result4.csv', 'a') as f:
                writer = csv.writer(f)
                for row in data:
                    timestamp, rtt = row.split(",")
                    writer.writerow([int(timestamp), int(rtt)])
        output.set("csv", "OK")