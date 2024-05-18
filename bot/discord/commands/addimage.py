
from discord import Message
from models.dbcontainer import DbService
from models.models import Guild, Image
from discord.basecommand import BaseCommand

class AdminAddImage(BaseCommand):
    prefix = "bran addimage"
    usage = prefix + " label"
    admin = 114930910884790276
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not self.does_prefix_match(self.prefix, message.content):
            return
        
        if message.author.id != self.admin:
            await message.reply("Unauthorized")
            return
        
        command_breakdown = message.content.split()

        image = Image()
        image.label = str(command_breakdown[2]) 
        image.bin = await message.attachments[0].read()

        with dbservice.Session() as session: 
            session.add(image)
            session.commit()
            await message.reply("done")