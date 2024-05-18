

from io import BytesIO
import PIL
from discord import Message
import discord
import discord.ext
import discord.ext.commands
from models.dbcontainer import DbService
from models.models import Card, Guild, OwnedCard, Shop, User
from discord.basecommand import BaseCommand
import random
from cardmaker import CardConstructor


class Buy(BaseCommand):
    prefix = "bran buy"
    usage = prefix + " [1/2/3/4]"

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
        input_data["image_card"] = PIL.Image.open(BytesIO(card.image.bin))
        output = CardConstructor(input_data)
        output_card = output.generateCard()
        return discord.File(BytesIO(output_card), filename=f"{card.title.replace(' ', '_')}.png")

    async def process(self, ctx, message: Message, dbservice: DbService):
        if not self.does_prefix_match(self.prefix, message.content):
            return
        
        command_breakdown = message.content.split()
        shop_idx = int(command_breakdown[2]) 
        with dbservice.Session() as session: 
            source = session.query(User).filter(User.user_id == str(message.author.id), User.guild_id == str(message.guild.id)).first()
            shop = session.query(Shop).join(Card, Shop.card).order_by(Card.cost.asc(), Card.id.asc()).all()
            selected_shop_item: Shop = shop[shop_idx - 1]

            if source.brancoins < selected_shop_item.card.cost:
                await message.reply("You broke son")

            ownedcard = OwnedCard()
            ownedcard.card = selected_shop_item.card
            source.owned_cards.append(ownedcard)
            source.brancoins -= selected_shop_item.card.cost
            session.add(source)
            
            session.commit()

            await message.reply(f"Congrats on the new card! {self.custom_emoji}", file= self.card_to_image(selected_shop_item.card))
        
        
            