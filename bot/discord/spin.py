

from discord import Message
import discord
import discord.ext
import discord.ext.commands
from models.dbcontainer import DbService
from models.models import Jackpot, User
from discord.basecommand import BaseCommand
import random


class Spin(BaseCommand):
    cost = 1
    wins = [(1/20, 30), (1/10, 4), (1/4, 2)]
    jackpot_chance = 1/100
    prefix = "bran spin"
    usage = prefix
    freebie_chance = 1/100
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not message.content.startswith(self.prefix):
            return
        
        is_freebie = True if random.uniform(0, 1) < self.freebie_chance else False

        with dbservice.Session() as session: 
            source = session.query(User).filter(User.user_id == str(message.author.id), User.guild_id == str(message.guild.id)).first()
            jackpot = session.query(Jackpot).filter(Jackpot.guild_id == str(message.guild.id)).first()

            if source.brancoins < self.cost:
                await message.reply("You ain't got the facilities for that big man")
                return

            if not is_freebie:
                source.brancoins -= self.cost
                jackpot.brancoins += self.cost

            spin_val = random.uniform(0, 1)
            win_val = 0
            for win in self.wins:
                if spin_val < win[0]:
                    win_val = win[1]
                    break
            
            source.brancoins += win_val
            
            if not is_freebie:
                if win_val == 0:
                    await message.reply(f"Paid {self.cost} {self.custom_emoji} ...\nWon nothing... dummy... :clown:")
                else:
                    await message.reply(f"Paid {self.cost} {self.custom_emoji} ...\nWon {win_val}!!!!:maracas:")
            else:
                if win_val == 0:
                    await message.reply(f"Paid nothing!!! Fames Jermo has blessed you! ...\nWon nothing... it looks like this blessing is a toxic curse... :cursed:")
                else:
                    await message.reply(f"Paid nothing!!! Farhan smiles upon you!!\nWon {win_val}!!!! Time to convert!!!!:maracas: <:prayge:827970344865890324> :maracas:")

            if random.uniform(0, 1) < self.jackpot_chance:
                await message.reply(f":rotating_light: :rotating_light: :rotating_light: YOU WON THE JACKPOT OF {jackpot.brancoins} {self.custom_emoji} !!! :rotating_light: :rotating_light: :rotating_light: ")
                jackpot.brancoins = 0
            
            session.add(jackpot)
            session.add(source)
            session.commit()
            