from ducts.spi import EventHandler
from handler.handler_output import handler_output


import asyncio

import csv

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):

        handler_spec.set_description('pingにpongを返します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        ping_timestamp = event.data["obj"]
        pong_timestamp = "pong " + ping_timestamp[5:]
        output.set("pong", pong_timestamp)