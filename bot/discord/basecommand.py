
from envvars import Env


class BaseCommand():
    custom_emoji = "<:brancoin:1231038231198437396>" if Env.is_debug == "false" else "<:test:1230694305937756160>"
    async def process(self, ctx, message):
        raise NotImplementedError("Please Implement this method")