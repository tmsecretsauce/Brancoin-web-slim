

from discord import Message
import discord
from models.dbcontainer import DbService
from models.models import Jackpot, Match, User
from discord.basecommand import BaseCommand
from discord.ext.commands import Bot


class ViewJackpot(BaseCommand):
    prefix = "bran jackpot"
    usage = prefix
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not message.content.startswith(self.prefix):
            return
        
        with dbservice.Session() as session: 
            jackpot = session.query(Jackpot).filter(Jackpot.guild_id == str(message.guild.id)).first()
            await message.reply(f"Jackpot is currently {jackpot.brancoins} {self.custom_emoji}")