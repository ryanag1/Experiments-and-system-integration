from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource

import asyncio

import json

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):
        self.r_ur = manager.redis
        handler_spec.set_description('テストです。')
        handler_spec.set_as_responsive()
        self.ack_interval = 2
        self.players_transform_position = "GameStage/Players/Transform/Position/"
        self.user_id_url = "GameStage/Players/Id"
        self.players_init_transform_url = "GameStage/Players/Init/Transform/"
        return handler_spec

    #@handler_output
    async def handle(self, event):
        #datadata = event.data
        #data = {'GAME': True, 'str': datadata["str"], 'num': datadata["num"], 'intArray': datadata["intArray"]}
        #data = json.dumps(data)
        #await asyncio.sleep(2)
        #return data
        await self.r_ur.execute('DEL', self.players_transform_position + str(event.data["num"])) # 05/07
        
        self.reids_connection = await self.r_ur.connect_for_blocking(2, 8)
        print("ACKALLPLAYERS")
        with await self.reids_connection as conn:
            try:
                while not await event.session.is_closed():
                    #await asyncio.sleep(self.ack_interval)
                    res = await conn.execute('BLPOP', self.players_transform_position + str(event.data["num"]), 0)
                    #yield data
                    #print(res)
                    #print(type(res))
                    if res:
                        res = json.loads(res[1])
                        yield res
            except Exception as e:
                print(e)
            #finally:
                #await self.r_ur.execute('SREM', self.user_id_url, str(event.data["num"]))
                #await self.r_ur.execute('DEL', self.players_transform_position + str(str(event.data["num"])))
                #await self.r_ur.execute('DEL', self.players_init_transform_url + str(str(event.data["num"])))
            