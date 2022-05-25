from ducts.spi import EventHandler
from handler.handler_output import handler_output
from handler.redis_resource import UserResource


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
        output.set("UserId", event.data["UserId"])
        output.set("ClientToken", event.data["ClientToken"])
        active_cts = await self.r_ur.fetch_all_active_ct()
        output.set("ActiveCTs", [a_ct.decode("utf-8").replace("ActiveUserIds/ClientToken:", "") for a_ct in active_cts])
        active_users = [await self.r_ur.fetch_active_id_for_ct(a_ct.decode('utf-8').replace("ActiveUserIds/ClientToken:", "")) for a_ct in active_cts]
        output.set("ActiveUserIds", [a_u[0].decode("utf-8") for a_u in active_users])

        """for a_ct in active_cts:
            u_id = await self.r_ur.fetch_active_id_for_ct(a_ct.decode('utf-8').replace("ActiveUserIds/ClientToken:", ""))
            if u_id[0].decode("utf-8") == "Muki" or u_id[0].decode("utf-8") == "Hakuchu":
                await self.r_ur.delete_active_id_for_ct(u_id[0].decode("utf-8"), a_ct.decode('utf-8').replace("ActiveUserIds/ClientToken:", ""))"""
