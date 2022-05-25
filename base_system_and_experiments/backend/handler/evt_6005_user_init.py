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
        self.players_init_transform_url = "GameStage/Players/Init/Transform/"
        self.user_id_url = "GameStage/Players/Id"
        self.players_transform_position_tmp = "GameStage/Players/Transform/Position/Tmp"
        self.loginout_interval = 5
        return handler_spec

    #@handler_output
    async def handle(self, event):
        await event.session.set_session_attribute("UserId", event.data["num"])
        
        
        login_id = await self.r_ur.execute('SMEMBERS', self.user_id_url)
        login_id = [ int(i) for i in login_id if i != "'" and i != "b" ]
        
        data = {'GAME': True, 'num': event.data["num"], 'user_num': event.data["user_num"], 'floatArray': event.data["floatArray"], 'intArray': login_id}
        data = json.dumps(data)
        await self.r_ur.execute('SET', self.players_transform_position_tmp + str(event.data["num"]), data)
        
        for id in login_id:
            if id == event.data["num"]:
                data = {'GAME': True, 'num': id, 'floatArray': event.data["floatArray"], 'str': 'Login', 'intArray': login_id}
            else:
                data2 = await self.r_ur.execute('GET', self.players_transform_position_tmp + str(id))
                data2 = json.loads(data2)
                data = {'GAME': True, 'num': id, 'floatArray': data2["floatArray"], 'str': 'Login', 'intArray': login_id}
            yield data
        
                
        print("USERLOGIN")
        
        while not await event.session.is_closed():
            await asyncio.sleep(self.loginout_interval)
            tmp_login_id = await self.r_ur.execute('SMEMBERS', self.user_id_url)
            tmp_login_id = [ int(i) for i in tmp_login_id if i != "'" and i != "b" ]
            
            new_logout_id = list(set(login_id) - set(tmp_login_id))
            new_login_id = list(set(tmp_login_id) - set(login_id))
                
            if len(new_login_id) != 0:
                login_id = tmp_login_id
                for id in new_login_id:
                    data2 = await self.r_ur.execute('GET', self.players_transform_position_tmp + str(id))
                    data2 = json.loads(data2)
                    data = {'GAME': True, 'num': id, 'floatArray': data2["floatArray"], 'str': 'Login', 'intArray': login_id}
                    yield data
            
            if len(new_logout_id) != 0:
                login_id = tmp_login_id
                for id in new_logout_id:
                    #data2 = await self.r_ur.execute('GET', self.players_transform_position_tmp + str(id))
                    #data2 = json.loads(data2)
                    data = {'GAME': True, 'num': id, 'floatArray': [0, 0], 'str': 'Logout', 'intArray': login_id}
                    yield data
                    
        """login_id = await self.r_ur.execute('SMEMBERS', self.user_id_url)
        login_id = [ int(i) for i in login_id if i != "'" and i != "b" ]
                    
                    
        datadata = event.data
        data2 = {'GAME': True, 'num': datadata["num"], 'user_num': datadata["user_num"], 'floatArray': datadata["floatArray"], 'intArray': login_id}
        self.user_id = data2["num"]
        await event.session.set_session_attribute("UserId", event.data["num"])
        data = json.dumps(data2)
        print("USERNUM")
        print(datadata["user_num"])
        try:
            for i in range(datadata["user_num"]):
                await self.r_ur.execute('RPUSH', self.players_init_transform_url + str(i), data)
            #await self.r_ur.execute('RPUSH', self.players_transform_position + "1", data)
        except Exception as e:
            print(e)
        
        self.reids_connection = await self.r_ur.connect_for_blocking(2, 8)
        with await self.reids_connection as conn:
            try:
                i = 0
                while i < event.data["user_num"]:
                    res = await conn.execute('BLPOP', self.players_init_transform_url + str(event.data["num"]), 0)
                    if res:
                        i += 1
                        res = json.loads(res[1])
                        yield res
                await conn.execute('DEL', self.players_init_transform_url + str(event.data["num"]))
            except Exception as e:
                print(e)"""
        #data = json.dumps(data)
        #await asyncio.sleep(2)"""
        #return data2
        
    async def handle_closed(self, session):
        try:
            print("<<<<<CLOSE 2>>>>>")
            #user_id = await session.get_session_attribute('UserId')
            #await self.r_ur.execute('DEL', self.players_init_transform_url + str(user_id))
        except Exception as e:
            print(e)