
class BaseCommand():
    async def process(self, message):
        raise NotImplementedError("Please Implement this method")