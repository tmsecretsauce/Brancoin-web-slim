

from io import BytesIO
import math
from typing import List
from discord import Message
import discord
from discord.drawutils import DrawUtils
from models.dbcontainer import DbService
from models.models import Card, User
from discord.basecommand import BaseCommand
from PIL import Image


class SelectCard(BaseCommand):
    prefix = "bran summon"
    usage = prefix + " [1,2,3...]"
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not self.does_prefix_match(self.prefix, message.content):
            return
        
        command_breakdown = message.content.split()
        card_idx = int(command_breakdown[2]) - 1
        
        with dbservice.Session() as session: 
            guy = session.query(User).filter(User.user_id == str(message.author.id), User.guild_id == str(message.guild.id)).first()
            if guy and card_idx < len(guy.owned_cards):
                card = guy.owned_cards[card_idx].card
                file = discord.File(DrawUtils.card_to_byte_image(card), filename=f"card.png")
                await message.reply(f"Behold! I'll activate {card.title}!!!", file=file)
            else:
                await message.reply("???")

    def split(self, arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr  = arr[1:]
        arrs.append(arr)
        return arrs