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

        handler_spec.set_description('メディアデータ変形')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("")