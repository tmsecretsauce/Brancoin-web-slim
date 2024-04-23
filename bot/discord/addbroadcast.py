
from discord import Message
from models.dbcontainer import DbService
from models.models import Guild
from discord.basecommand import BaseCommand

class AdminAddBroadcast(BaseCommand):
    prefix = "bran broadcast"
    usage = prefix
    admin = 114930910884790276
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not message.content.startswith(self.prefix):
            return
        
        if message.author.id != self.admin:
            await message.reply("Unauthorized")
            return

        new_broadcast_channel_id = message.channel.id

        with dbservice.Session() as session: 
            guild = session.query(Guild).filter(Guild.guild_id==str(message.guild.id)).first()
            guild.broadcast_channel_id = str(new_broadcast_channel_id)
            session.add(guild)
            session.commit()
            await message.reply("joever")