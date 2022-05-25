from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource

import random
import string

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_ur = UserResource(manager.redis)
        #self.ct = None
        #self.pre_ct = None

        handler_spec.set_description('セッションを作ります。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        id = event.data["UserId"]
        ct = event.data["ClientToken"]
        await event.session.set_session_attribute("UserId", id)
        await event.session.set_session_attribute("ClientToken", ct)
        await self.r_ur.expire_delete_active_ct(ct, 10)
        
        output.set("Auth", False)


    async def handle_closed(self, session):
        try:
            #wsid = await session.get_session_attribute('WorkSessionId')
            id = await session.get_session_attribute("UserId")
            #password = await session.get_session_attribute("UserPassword")
            #pn = await session.get_session_attribute('ProjectName')
            ct = await session.get_session_attribute('ClientToken')

            await self.r_ur.expire_delete_active_ct(ct, 10)
            #await self.r_wkr.delete_active_id_for_ct(wid, ct)
            #logger.debug(f"inactivating {wid} for {pn}")
        except:
            pass


