if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

from discord.ext import commands
from lib import Constants, dbot
from lib.livedb import LiveDatabase as eco

def has_admin_perms(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)

def is_developer(ctx, bot: commands.Bot):
    return (bot.owner_id == ctx.author.id) or (ctx.author.id in bot.owner_ids)
        
def is_server_valid(ctx):
    return ctx.guild.id in Constants.ServerIDs

async def user_check(ctx, bot: dbot.Bot):
    prefix = ("c-" if Constants.isAlpha else "c+", Constants.bot_mention[Constants.isAlpha])
    
    if bot.isShuttingDown and not ctx.author.bot and ctx.message.content.startswith(prefix):
        await ctx.send("Project Cynical is shutting down. All commands are no longer invoked.")
        return False
    
    
    if ctx.author.bot:
        return False
    
    if not is_server_valid(ctx):
        print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
        return False

    isExist = await bot.eco.user_exists(ctx.author.id)
    
    if not isExist:
        await bot.eco.add_user(id = ctx.author.id)
        
    return True
