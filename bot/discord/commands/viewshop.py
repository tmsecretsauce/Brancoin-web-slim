

import base64
from io import BytesIO
import PIL
from discord import Message
import discord
from models.dbcontainer import DbService
from models.models import Card, Shop, User
from discord.basecommand import BaseCommand
from discord.ext.commands import Bot
from cardmaker import CardConstructor


class ViewShop(BaseCommand):
    prefix = "bran shop"
    usage = prefix

    def card_to_image_bytes(self, card: Card):
        input_data = {
            "card": card.card_style,
            "Title": card.title,
            "attribute": card.attribute,
            "Level": int(card.level),
            "Type": card.type,
            "Descripton": str(card.description).replace('\\n','\n'),
            "Atk": card.atk,
            "Def": card.defe
            }
        input_data["image_card"] = PIL.Image.open(BytesIO(card.image.bin))
        output = CardConstructor(input_data)
        output_card = output.generateCard()
        return BytesIO(base64.b64decode(output_card))

    async def process(self, ctx, message: Message, dbservice: DbService):
        if not self.does_prefix_match(self.prefix, message.content):
            return
        
        with dbservice.Session() as session: 
            shop_items = session.query(Shop).all()
            discord_files = []
            for shop_item in shop_items:
                file_byte = shop_item.card
                discord_files.append(discord.File(self.card_to_image_bytes(file_byte), filename=shop_item.card.image.label+".png"))
            context = await ctx(message)
            bot: Bot = context.bot
            
            await message.reply(files=discord_files)