if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

from discord.ext import commands
from discord.opus import OpusError
from lib import Constants, dbot
from lib.livedb import LiveDatabase as eco

def has_admin_perms(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)
        
def is_server_valid(ctx):
    return ctx.guild.id in Constants.ServerIDs

async def user_check(ctx, bot: dbot.Bot):
    prefix = ("c-" if Constants.isAlpha else "c+", Constants.bot_mention[Constants.isAlpha])
    
    if not is_server_valid(ctx):
        raise UserCheckFailure("attempt to invoke a command in a non-whitelisted server")
    
    if bot.isShuttingDown and not ctx.author.bot and ctx.message.content.startswith(prefix):
        raise BotShuttingDown()
    
    if ctx.author.bot:
        raise AuthorIsBot()
    
    isExist = await bot.eco.user_exists(ctx.author.id)
    
    if not isExist:
        await bot.eco.add_user(id = ctx.author.id)

class UserCheckFailure(commands.CheckFailure):
    def __init__(self, message = None):
        super().__init__(message or 'User checking failed.')
        
class AuthorIsBot(commands.CheckFailure):
    def __init__(self, message = None):
        super().__init__(message or 'The message author is a bot.')
        
class BotShuttingDown(UserCheckFailure):
    def __init__(self, message = None):
        super().__init__(message or 'The bot is shutting down. All commands are not to be invoked.')
        
class NoOpusLoaded(Exception):
    def __init__(self, message = None):
        super().__init__(message or 'There is no opus library loaded.')