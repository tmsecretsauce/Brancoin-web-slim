
class BaseCommand():
    custom_emoji = "<:brancoin:1231038231198437396>"
    async def process(self, ctx, message):
        raise NotImplementedError("Please Implement this method")