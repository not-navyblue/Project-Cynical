from discord.ext import commands

def has_admin_perms(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)

def is_developer(bot: commands.Bot):
    def predicate(ctx):
        return (bot.owner_id == ctx.author.id) or (ctx.author.id in bot.owner_ids)
    return commands.check(predicate)