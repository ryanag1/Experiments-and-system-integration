from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource

import asyncio

import json

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):
        handler_spec.set_description('テストです。')
        handler_spec.set_as_responsive()
        return handler_spec

    #@handler_output
    async def handle(self, event):
        datadata = event.data
        data = {'GAME': True, 'str': datadata["str"], 'num': datadata["num"], 'intArray': datadata["intArray"]}
        #data = json.dumps(data)
        #await asyncio.sleep(2)
        return data