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
        self.ct = None
        self.pre_ct = None

        handler_spec.set_description('ログインします。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("PreviousClientToken", self.ct)
        if not self.ct == None:
            output.set("PreviousRedisClientToken", await self.r_ur.check_existance_active_ct(self.ct))
        output.set("PreviousPreviousClientToken", self.pre_ct)
        if not self.pre_ct == None:
            output.set("PreviousPreviousRedisClientToken", await self.r_ur.check_existance_active_ct(self.pre_ct))


        id = event.data["Username"]
        password  = event.data["Password"]
        if await self.r_ur.check_existance_key("Hakuchu"):
            output.set("Redis", await self.r_ur.check_existance_key("Hakuchu"))
            await self.r_ur.delete_password_for_id("600zoku", "Hakuchu")
        else:
            if not await self.r_ur.check_existance_key("mugi"):
                output.set("Redis", await self.r_ur.check_existance_key("mugi"))
                await self.r_ur.add_password_for_id("600zoku", "mugi")
            if not await self.r_ur.check_existance_key("kome"):
                output.set("Redis", await self.r_ur.check_existance_key("kome"))
                await self.r_ur.add_password_for_id("300kei", "kome")
            if not await self.r_ur.check_existance_key("ikeda"):
                output.set("Redis", await self.r_ur.check_existance_key("ikeda"))
                await self.r_ur.add_password_for_id("ultra", "ikeda")
            if not await self.r_ur.check_existance_key("numata"):
                output.set("Redis", await self.r_ur.check_existance_key("numata"))
                await self.r_ur.add_password_for_id("super", "numata")
            if not await self.r_ur.check_existance_key("pika"):
                output.set("Redis", await self.r_ur.check_existance_key("pika"))
                await self.r_ur.add_password_for_id("great", "pika")
            
            
            #await event.session.set_session_attribute("UserId", "Muki")
            #await event.session.set_session_attribute("UserPassword", "600zoku")

        ret = "user not found"
        if await self.r_ur.check_existance_key(id):
            ret = "password error"
            if await self.r_ur.check_password_for_id(password, id):
                ct = id_generator()
                i = 0
                while await self.r_ur.check_existance_active_ct(ct):
                    ct = id_generator()
                    i += 1
                    if i > 100:
                        output.set("id_generator", "loop_timeout")
                        break
                #output.set("RedisClientToken", await self.r_ur.check_existance_active_ct(ct))
                #output.set("RedisActiveUser", await self.r_ur.check_active_id_for_ct(id, ct))
                await self.r_ur.add_active_id_for_ct(id, ct)
                #await event.session.set_session_attribute("UserId", id)
                #await event.session.set_session_attribute("ClientToken", ct)
                #output.set("RedisClientTokenAFTER", await self.r_ur.check_existance_active_ct(ct))
                #output.set("RedisActiveUserAFTER", await self.r_ur.check_active_id_for_ct(id, ct))
                ret = ct
                self.pre_ct = self.ct
                self.ct = ct

        output.set("RedisKeys", await self.r_ur.fetch_all_key_data_for_id())
        output.set("RedisKeys2", await self.r_ur.fetch_all_key_from_id_for_to_id())
        output.set("ClientToken", ret)

    """async def handle_closed(self, session):
        try:
            #wsid = await session.get_session_attribute('WorkSessionId')
            id = await session.get_session_attribute("UserId")
            #password = await session.get_session_attribute("UserPassword")
            #pn = await session.get_session_attribute('ProjectName')
            ct = await session.get_session_attribute('ClientToken')

            await self.r_ur.expire_delete_active_ct(ct, 30)
            #await self.r_wkr.delete_active_id_for_ct(wid, ct)
            #logger.debug(f"inactivating {wid} for {pn}")
        except:
            pass"""


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))