

from discord import Message
import discord
import discord.ext
import discord.ext.commands
from discord.VoteType import VoteType
from models.dbcontainer import DbService
from models.models import Match, User, Votes
from discord.basecommand import BaseCommand
import random


class AddVote(BaseCommand):

    prefix = "bran vote"
    usage = f"{prefix} [win] [num_coins] [optional: match_id]\n {prefix} [lose] [num_coins] [optional: match_id]"
    async def process(self, ctx, message: Message, dbservice: DbService):
        if not message.content.startswith(self.prefix):
            return
        command_breakdown = message.content.split()

        if command_breakdown[2] == "win" or command_breakdown[2] == "lose":
            await self.add_win_loss_vote(dbservice, command_breakdown[2:], message)

    async def add_win_loss_vote(self, db: DbService, arggs, message: discord.Message):
        vote_type = VoteType.WIN if arggs[0] == "win" else VoteType.LOSE
        num_coins = int(arggs[1])
        match_id = arggs[2] if 2 < len(arggs) else None

        with db.Session() as session:
            source_user = session.query(User).filter(User.user_id == str(message.author.id)).first()
            if source_user.brancoins < num_coins:
                await message.reply("Stop doing gamba broke boi")
                return
            source_user.brancoins -= num_coins

            match_fetch_query = session.query(Match).filter(Match.finished == False)
            if match_id:
                match_fetch_query = match_fetch_query.filter(Match.match_id == match_id)
            target_match = match_fetch_query.first()

            new_vote = Votes()
            new_vote.type_of_vote = vote_type.value
            new_vote.processed = False
            new_vote.voter = source_user
            new_vote.brancoins = num_coins
            target_match.votes.append(new_vote)
            
            session.add(source_user)
            session.add(target_match)
            session.commit()
        await message.reply("Vote placed")