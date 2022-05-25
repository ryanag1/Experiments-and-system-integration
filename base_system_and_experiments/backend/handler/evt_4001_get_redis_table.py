from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource

import asyncio

import csv

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):
        self.r_ur = UserResource(manager.redis)
        handler_spec.set_description('データベースの情報を返します')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        data = await self.r_ur.all_keys()
        for i, item in enumerate(data):
            row = {"KEY": None, "VALUE": None, "TYPE": None, "TTL": None, "LEN": None, "MEMBER": None}
            row["KEY"] = item.decode('utf-8')
            row["TYPE"] = (await self.r_ur.type_data(row["KEY"])).decode('utf-8')
            if row["TYPE"] == "set":
                row["VALUE"] = await self.r_ur.get_set_members(row["KEY"])
                row["VALUE"] = [item.decode('utf-8') for item in row["VALUE"]]
            row["TTL"] = await self.r_ur.get_ttl(row["KEY"])
            data[i] = row
        output.set("RedisData", data)