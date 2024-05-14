

from discord import Message
import discord
import discord.ext
import discord.ext.commands
from discord.VoteType import VoteType
from models.dbcontainer import DbService
from models.models import Match
from discord.basecommand import BaseCommand
from discord.ext.commands import Bot

class ViewVotes(BaseCommand):
    prefix = "bran votes"
    usage = prefix
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not self.does_prefix_match(self.prefix, message.content):
            return
        
        with dbservice.Session() as session: 
            open_matches = session.query(Match).filter(Match.finished == False).all()
            context: discord.ext.commands.Context = await ctx(message)
            bot: Bot = context.bot
            for open_match in open_matches:
                embedVar = await self.generate_embed_for_match(open_match, bot)
                await message.reply(embed=embedVar)

            if len(open_matches) == 0:
                await message.reply("No open matches")

    async def generate_embed_for_match(self, match: Match, bot: Bot):
        embedVar = discord.Embed(title=f"Aram {match.match_id}", color=0xccccff)
        embedVar.set_author(name="Votes", icon_url="https://i.imgur.com/BAWRRXp.png")
        for vote in match.votes:
            discord_user = await bot.fetch_user(vote.voter.user_id)
            embedVar.add_field(name="Voter", value=str(discord_user.display_name), inline=True)
            embedVar.add_field(name="Type", value=str(VoteType(vote.type_of_vote).name), inline=True)
            embedVar.add_field(name="Brancoins", value=str(vote.brancoins), inline=True)
            embedVar.add_field(name="\u200b", value="\u200b", inline=False)
        return embedVar