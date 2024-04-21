

from discord import Message
import discord
from models.dbcontainer import DbService
from models.models import Match, User
from discord.basecommand import BaseCommand
from discord.ext.commands import Bot


class ViewMatches(BaseCommand):
    prefix = "bran viewmatches"
    usage = prefix
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not message.content.startswith(self.prefix):
            return
        
        with dbservice.Session() as session: 
            open_matches = session.query(Match).filter(Match.finished == False).all()
            context = await ctx(message)
            bot: Bot = context.bot

            for open_match in open_matches:
                embedVar = discord.Embed(title="ARAM in progress", description=f"id: {open_match.match_id}", color=0xccccff)
                embedVar.add_field(name="started (UTC)", value=f"{str(open_match.start_time)}", inline=False)
                embedVar.add_field(name="Players:", value="--------", inline=False)
                for match_player in open_match.match_players:
                    discord_id = match_player.league_user.discord_user.user_id
                    discord_user = await bot.fetch_user(discord_id)
                    embedVar.add_field(name=str(discord_user.display_name), value=str(match_player.champion), inline=False)
                await message.reply(embed=embedVar)

            if len(open_matches) == 0:
                await message.reply("No pending matches")