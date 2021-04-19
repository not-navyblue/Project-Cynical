from discord.ext import commands
from discord.ext.commands.errors import BadArgument

class SafeInt(commands.Converter):
    """Converts `str` into `int` safely. Returns the value of the argument itself if conversion failed. """
    async def convert(self, ctx, args: str):
        try:
            return int(str(args))
        except ValueError:
            return args
        
class SafeFloat(commands.Converter):
    """Converts `str` into `int` or `float` depending on the presence of decimal values. Returns the value of the argument itself if conversion failed."""
    async def convert(self, ctx, args: str):
        chaos = 0
        
        try:
            chaos = float(str)
            
            if chaos % 1 == 0:
                return int(chaos)
            else:
                return chaos
        except ValueError:
            return args