from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource
import uuid

import asyncio

import json

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec,manager):
        self.r_ur = manager.redis
        handler_spec.set_description('テストです。')
        handler_spec.set_as_responsive()
        self.user_id_url = "GameStage/Players/Id"
        self.players_transform_position = "GameStage/Players/Transform/Position/"
        self.players_init_transform_url = "GameStage/Players/Init/Transform/"
        self.players_transform_position_tmp = "GameStage/Players/Transform/Position/Tmp"
        return handler_spec

    #@handler_output
    async def handle(self, event):
        #datadata = event.data
        #self.user_id = str(uuid.uuid4())
        #data = {'GAME': True, 'str': self.user_id}
        #data = json.dumps(data)
        #await asyncio.sleep(2)
        """self.reids_connection = await self.r_ur.connect_for_blocking(2, 8)
        with await self.reids_connection as conn:
            i = 0
            while i < event.data["num"]:
                self.user_id = i
                if await conn.execute('SADD', self.user_id_url, self.user_id):
                    break
                i += 1 
            yield {'GAME': True, 'num': self.user_id}
            try:
                while not await event.session.is_closed():
                    await asyncio.sleep(10)
            except Exception as e:
                print(e)"""
        i = 0
        while i < event.data["num"]:
            user_id = i
            if await self.r_ur.execute('SADD', self.user_id_url, user_id):
                break
            i += 1 
        await event.session.set_session_attribute("UserId", user_id)
        
        login_id = await self.r_ur.execute('SMEMBERS', self.user_id_url)
        login_id = [ int(i) for i in login_id if i != "'" and i != "b" ]
        #print(login_id)
        
        return {'GAME': True, 'num': user_id, 'intArray': login_id}
            
    async def handle_closed(self, session):
        try:
            print("<<<<<CLOSE>>>>>")
            user_id = await session.get_session_attribute('UserId')
            await self.r_ur.execute('SREM', self.user_id_url, user_id)
            await self.r_ur.execute('DEL', self.players_transform_position + str(user_id))
            await self.r_ur.execute('DEL', self.players_init_transform_url + str(user_id))
            await self.r_ur.execute('DEL', self.players_transform_position_tmp + str(user_id))
        except Exception as e:
            print(e)
