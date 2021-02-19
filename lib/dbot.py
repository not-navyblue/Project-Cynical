from discord.ext import commands

# Customized Bot class (subclass of discord.ext.commands.Bot)
class Bot(commands.Bot):
    def __init__(self, command_prefix, help_command = commands.bot._default, description = None, **options):
        super().__init__(command_prefix, help_command = help_command, description = description, **options)
        self.changelogContents = list()
        self.battles = list()
        self.pendingBattles = list() # [[battler11, battler12], [battler21, battler22], ...]
        self.isShuttingDown = False
        self.leaderboards = []
        self.eco = None
        self.noMEE6 = False