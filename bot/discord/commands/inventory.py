

from discord import Message
import discord
from models.dbcontainer import DbService
from models.models import User
from discord.basecommand import BaseCommand


class Inventory(BaseCommand):
    prefix = "bran inv"
    usage = prefix
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not self.does_prefix_match(self.prefix, message.content):
            return
        
        with dbservice.Session() as session: 
            guy = session.query(User).filter(User.user_id == str(message.author.id), User.guild_id == str(message.guild.id)).first()
            if guy:
                card_csv = []
                for owned_card in guy.owned_cards:
                    card_csv.append(owned_card.card.title)
                await message.reply(f"WIP. For now I'll give you a list: {', '.join(card_csv)}")
            else:
                await message.reply("Who are you?")