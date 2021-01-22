from discord.ext import commands

class SafeInt(commands.Converter):
    """Converts `str` into `int` safely. Returns the value of the argument itself if conversion failed. """
    async def convert(self, ctx, args: str):
        try:
            return int(str(args))
        except ValueError:
            return str(args)