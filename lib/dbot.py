from discord.ext import commands
from .livedb import LiveDatabase
from . import Constants

# Customized Bot class (subclass of discord.ext.commands.Bot)
class Bot(commands.Bot):
    def __init__(self, command_prefix, help_command = commands.bot._default, description = None, **options):
        super().__init__(command_prefix, help_command = help_command, description = description, **options)
        
        self.changelogContents = []
        self.battles = []
        self.pendingBattles = [] # [[battler11, battler12], [battler21, battler22], ...]
        self.leaderboards = []
        
        self.shop_items = []
        
        self.isShuttingDown = False
        self.eco = LiveDatabase(Constants.CurrentDirectory + "/data/")
        self.noMEE6 = False
        
        self.song_queues = [] # [id, queue]