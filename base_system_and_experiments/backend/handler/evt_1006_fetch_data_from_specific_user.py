from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource

import asyncio

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_ur = UserResource(manager.redis)
        self.ct = None
        self.pre_ct = None
        
        self.loop_end = False

        handler_spec.set_description('ログインします。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        u_id = event.data["UserId"]
        output.set("UserId", event.data["UserId"])
        output.set("ClientToken", event.data["ClientToken"])
        i = 0
        await event.session.set_session_attribute("UserId", "Muki")
        await event.session.set_session_attribute("UserPassword", "600zoku")
        #await self.r_ur.delete_data_key(u_id)
        #await self.r_ur.delete_from_key(u_id)
        
        while True:
            if self.loop_end:
                break
            await asyncio.sleep(3)
            i += 1
            if i == 200:
                break

            if await self.r_ur.check_existance_data_for_id(u_id):
                data = await self.r_ur.fetch_data_for_id(u_id)
                output.set("Message", data[0].decode('utf-8'))
                await self.r_ur.delete_data_for_id(data[0].decode('utf-8'), u_id)
            """else:
                output.set("Message", "no message")"""

            if await self.r_ur.check_existance_from_id_for_to_id(u_id):
                from_u_id = await self.r_ur.fetch_from_id_for_to_id(u_id)
                output.set("FromUserId", from_u_id[0].decode('utf-8'))
                await self.r_ur.delete_from_id_for_to_id(from_u_id[0].decode('utf-8'), u_id)
                
                break
            """else:
                output.set("FromUserId", "no from userId")"""
        

        """for a_ct in active_cts:
            u_id = await self.r_ur.fetch_active_id_for_ct(a_ct.decode('utf-8').replace("ActiveUserIds/ClientToken:", ""))
            if u_id[0].decode("utf-8") == "Muki" or u_id[0].decode("utf-8") == "Hakuchu":
                await self.r_ur.delete_active_id_for_ct(u_id[0].decode("utf-8"), a_ct.decode('utf-8').replace("ActiveUserIds/ClientToken:", ""))"""

    """async def handle_closed(self, session):
        self.loop_end = True"""