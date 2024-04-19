
from mimetypes import guess_type
import random

from discord import Message
from models.dbcontainer import DbService
from models.models import User
from discord.basecommand import BaseCommand


class Discover(BaseCommand):
    chance_of_free_coin = 1 / 5
    custom_emoji = "<:brancoin:1230681818068418580>"
    async def process(self, message: Message, dbservice: DbService):
        if random.uniform(0, 1) < self.chance_of_free_coin:
            with dbservice.Session() as session: 
                guy = session.query(User).filter(User.user_id == str(message.author.id), User.guild_id == str(message.guild.id)).first()
                guy.brancoins = guy.brancoins + 1
                session.add(guy)
                session.commit()
            await message.add_reaction(self.custom_emoji)   