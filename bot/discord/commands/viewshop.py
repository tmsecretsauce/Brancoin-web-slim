

import base64
from io import BytesIO
import os
from PIL import Image, ImageFont, ImageDraw
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

    card_width = 349
    card_height = 509
    card_y = 183
    card_coords = [ 
        (55, card_y),
        (433, card_y),
        (811, card_y),
        (1186, card_y),
    ]

    text_margin_x = 20
    text_margin_y = 12
    text_y = 718 + text_margin_y
    text_width = 158
    text_height = 73
    text_coords = [
        (199 + text_margin_x, text_y),
        (582 + text_margin_x, text_y),
        (960 + text_margin_x, text_y),
        (1337 + text_margin_x, text_y),
    ]

    def card_to_image(self, card: Card):
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
        input_data["image_card"] = Image.open(BytesIO(card.image.bin))
        output = CardConstructor(input_data)
        output_card = output.generateCard()
        return Image.open(BytesIO(output_card))

    async def process(self, ctx, message: Message, dbservice: DbService):
        if not self.does_prefix_match(self.prefix, message.content):
            return
        
        card_images = []
        card_costs = []
        with dbservice.Session() as session: 
            shop_items = session.query(Shop).all()
            for shop_item in shop_items:
                card_images.append(self.card_to_image(shop_item.card))
                card_costs.append(shop_item.card.cost)
        
        shop_map = Image.open(os.path.dirname(__file__) + "/../../assets/shopmat.png")
        font = ImageFont.truetype(os.path.dirname(__file__) + "/../../assets/Jersey M54.ttf", 40)
        shop_draw = ImageDraw.Draw(shop_map)
        for idx, card_image in enumerate(card_images):
            shop_map.paste(card_image.resize((self.card_width, self.card_height)), self.card_coords[idx])
            shop_draw.text(self.text_coords[idx], str(card_costs[idx]), (0, 0, 0), font)

        buffered = BytesIO()
        shop_map.save(buffered, format="PNG")
        discord_shop_item = discord.File(BytesIO(buffered.getvalue()), filename="shop.png")
        await message.reply(file=discord_shop_item)