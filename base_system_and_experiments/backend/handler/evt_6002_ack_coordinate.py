from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource

import aioredis

import asyncio

import json

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):
        self.r_ur = manager.redis
        handler_spec.set_description('テストです。')
        handler_spec.set_as_responsive()
        self.GameStagePlayers = "GameStage/Players/"
        self.TransformPosition = "/Transform/Position"
        self.players_transform_position = "GameStage/Players/Transform/Position/"
        self.players_transform_position_tmp = "GameStage/Players/Transform/Position/Tmp"
        return handler_spec

    #@handler_output
    async def handle(self, event):
        """datadata = event.data
        data2 = {'GAME': True, 'floatArray': datadata["floatArray"], 'str': datadata["str"], 'num': datadata["num"], 'user_num': datadata["user_num"], 'intArray': datadata["intArray"]}
        data = json.dumps(data2)
        #data = {'floatArray': datadata["floatArray"], 'str': datadata["str"]}
        try:
            for i in range(datadata["user_num"]):
                await self.r_ur.execute('RPUSH', self.players_transform_position + str(i), data)
            await self.r_ur.execute('SET', self.players_transform_position_tmp + str(event.data["num"]), data)
        except Exception as e:
            print(e)
        #data = json.dumps(data)
        #await asyncio.sleep(2)
        return data2"""
        
        
        datadata = event.data
        data2 = {'GAME': True, 'floatArray': datadata["floatArray"], 'str': datadata["str"], 'num': datadata["num"], 'user_num': datadata["user_num"], 'intArray': datadata["intArray"]}
        data = json.dumps(data2)
        #data = {'floatArray': datadata["floatArray"], 'str': datadata["str"]}
        try:
            for i in event.data["intArray"]:
                await self.r_ur.execute('RPUSH', self.players_transform_position + str(i), data)
            await self.r_ur.execute('SET', self.players_transform_position_tmp + str(event.data["num"]), data)
        except Exception as e:
            print(e)
        #data = json.dumps(data)
        #await asyncio.sleep(2)
        return data2
        