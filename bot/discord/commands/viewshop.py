

import base64
import datetime
from io import BytesIO
import os
from PIL import Image, ImageFont, ImageDraw
from discord import Message
import discord
from sqlalchemy import func
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
        
        
        with dbservice.Session() as session: 
            if session.query(Shop).filter(Shop.date_added == datetime.date.today()).count() < 4:
                print("no shop, populating")
                featured_cards = session.query(Card).filter(Card.featured == True).all()
                drawn_cards = []
                drawn_cards.append(session.query(Card).filter(Card.shoppable == True, Card.cost <= 100).order_by(func.random()).first())
                drawn_cards.append(session.query(Card).filter(Card.shoppable == True, Card.cost > 100, Card.cost <= 500).order_by(func.random()).first())
                drawn_cards.append(session.query(Card).filter(Card.shoppable == True, Card.cost > 100).order_by(func.random()).first())
                drawn_cards.append(session.query(Card).filter(Card.shoppable == True, Card.cost > 1000).order_by(func.random()).first())
                drawn_cards.append(session.query(Card).filter(Card.shoppable == True).order_by(func.random()).first())
                drawn_cards.append(session.query(Card).filter(Card.shoppable == True).order_by(func.random()).first())

                filtered_drawn_cards = list(filter(lambda x: x is not None, drawn_cards))
                
                cards_to_add = []
                for featuredCard in featured_cards:
                    cards_to_add.append(featuredCard)
                while len(cards_to_add) < 4:
                    newShopCard = Shop()
                    cards_to_add.append(filtered_drawn_cards.pop(0))
                while len(cards_to_add) < 4:
                    cards_to_add.append(cards_to_add[0])

                for card_to_add in cards_to_add:
                    if card_to_add:
                        newShopCard = Shop()
                        print(card_to_add)
                        newShopCard.card = card_to_add
                        newShopCard.date_added = datetime.date.today()
                        session.add(newShopCard)

                session.commit()

        card_images = []
        card_costs = []
        with dbservice.Session() as session: 
            shop_items = session.query(Shop).join(Card, Shop.card).filter(Shop.date_added == datetime.date.today()).order_by(Card.cost.asc(), Card.id.asc()).limit(4).all()
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

        