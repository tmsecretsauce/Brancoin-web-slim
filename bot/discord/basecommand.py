
import enum
from envvars import Env


class BaseCommand():
    custom_emoji = "<:brancoin:1233204357550575636>" if Env.is_debug == "false" else "<:test:1230694305937756160>"
    async def process(self, ctx, message):
        raise NotImplementedError("Please Implement this method")
    
    def does_prefix_match(self, prefix: str, message: str):
        split_prefix = prefix.split()
        split_message = message.split()
        if len(split_message) < len(split_prefix):
            return False
        for idx, segment_prefix in enumerate(split_prefix):
            if segment_prefix != split_message[idx]:
                return False
        return True
