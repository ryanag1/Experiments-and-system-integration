from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource


class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_ur = UserResource(manager.redis)

        handler_spec.set_description('ログインします。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        to_u_id, from_u_id, data = self.add_data_for_specific_user(**event.data)
        output.set("ToUserId", to_u_id)
        output.set("FromUserId", from_u_id)
        output.set("Data", data)
        #output.set("DataType", type(data))
        await self.r_ur.delete_data_for_id(data, to_u_id)
        await self.r_ur.delete_from_id_for_to_id(from_u_id, to_u_id)
        await self.r_ur.add_data_for_id(data, to_u_id)
        await self.r_ur.add_from_id_for_to_id(from_u_id, to_u_id)
        output.set("checkExistsData", await self.r_ur.check_existance_data_for_id(to_u_id))
        output.set("checkExistsKey", [ key.decode("utf-8") for key in await self.r_ur.fetch_all_key_data_for_id() ] )
        output.set("checkExistsFromUsers", await self.r_ur.check_existance_from_id_for_to_id(to_u_id))
        output.set("checkExistsFromUserKey", [ key.decode("utf-8") for key in await self.r_ur.fetch_all_key_from_id_for_to_id()] )


    def add_data_for_specific_user(self, ToUserId, FromUserId, Message):
        return ToUserId, FromUserId, Message




        """for a_ct in active_cts:
            u_id = await self.r_ur.fetch_active_id_for_ct(a_ct.decode('utf-8').replace("ActiveUserIds/ClientToken:", ""))
            if u_id[0].decode("utf-8") == "Muki" or u_id[0].decode("utf-8") == "Hakuchu":
                await self.r_ur.delete_active_id_for_ct(u_id[0].decode("utf-8"), a_ct.decode('utf-8').replace("ActiveUserIds/ClientToken:", ""))"""
