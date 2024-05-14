

from discord import Message
import discord
import discord.ext
import discord.ext.commands
from models.dbcontainer import DbService
from models.models import Guild, User
from discord.basecommand import BaseCommand
import random


class Spin(BaseCommand):
    cost = 2
    wins = [(1/500, 50), (1/50, 20), (1/18, 10), (1/6, 6), (1/2, 2)]
    jackpot_chance = 1/100
    prefix = "bran spin"
    usage = prefix
    freebie_chance = 1/100
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not message.content.startswith(self.prefix):
            return
        output_msg = self.execute_spin(message, dbservice)
        await message.reply(output_msg)
        
    def execute_spin(self, message: Message, dbservice: DbService):
        output_msg = ""
        with dbservice.Session() as session: 
            is_freebie = True if random.uniform(0, 1) < self.freebie_chance else False
            source = session.query(User).filter(User.user_id == str(message.author.id), User.guild_id == str(message.guild.id)).first()
            jackpot = session.query(Guild).filter(Guild.guild_id == str(message.guild.id)).first()
            coin_change = 0

            if source.brancoins < self.cost:
                return ("You ain't got the facilities for that big man")

            if not is_freebie:
                coin_change -= self.cost

            spin_val = random.uniform(0, 1)
            win_val = 0
            for win in self.wins:
                if spin_val < win[0]:
                    win_val = win[1]
                    break
            won_jackpot = spin_val < self.jackpot_chance

            jackpot_value = jackpot.brancoins
            if won_jackpot:
                coin_change += jackpot_value
                jackpot.brancoins = 0
            else:
                jackpot.brancoins += self.cost
                coin_change += win_val

            source.brancoins += coin_change

            if won_jackpot:
                output_msg = (f":rotating_light: :rotating_light: :rotating_light: YOU WON THE JACKPOT OF {jackpot_value} {self.custom_emoji} !!!   :rotating_light: :rotating_light: :rotating_light: ")
            else:
                if not is_freebie:
                    if win_val == 0:
                        output_msg = (f"Paid {self.cost} {self.custom_emoji} ...\nWon nothing... dummy... :clown:")
                    else:
                        output_msg = (f"Paid {self.cost} {self.custom_emoji} ...\nWon {win_val}!!!!:maracas:")
                else:
                    if win_val == 0:
                        output_msg = (f"Paid nothing!!! Fames Jermo has blessed you! ...\nWon nothing... it looks like this blessing is a toxic curse... :cursed:")
                    else:
                        output_msg = (f"Paid nothing!!! Farhan smiles upon you!!\nWon {win_val}!!!! Time to convert!!!!:maracas: <:Prayge:1038601127052193814> :maracas:")

            session.add(jackpot)
            session.add(source)
            session.commit()
        return output_msg
            