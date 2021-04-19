# Adding the program's working directory to sys.path
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

# Built-in Modules
import os
import asyncio
import traceback
import random

# Third-party Modules and APIs
import discord
from discord import opus
import libneko
from discord.ext import commands
from dotenv import load_dotenv
import mee6_py_api as mee6
#import hjson # unused atm

# Custom/Developer-defined Modules and Cogs
from lib.livedb import LiveDatabase as CynicEconomy
from lib import Constants, Checks
from cards import cardDefines as cards
from lib.dbot import Bot

# Loading the .env file
if load_dotenv():
    print("Environment variables loaded.")
else:
    print("Failed to load environment variables.")
    quit(1)

# Global Variables/Functions
Constants.isAlpha = True
hasLoaded = False

add = Constants.add
subtract = Constants.subtract
number_format = Constants.number_format
isAlpha = Constants.isAlpha
user_check = Checks.user_check

#OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
#NO_OPUS = False

# Function Definitions
# Synchronous Functions
def set_changelog(bot: Bot):
    f = open("changelog", "r")
    bot.changelogContents = f.read().split("\n\n")
    bot.changelogContents.reverse()
    f.close()
    if len(bot.changelogContents) > 0:
        print("Changelog loaded.")
    else:
        print("Changelog failed to load.")
        quit(1)

def sn_ready():
    try:
        f = open(Constants.CurrentDirectory + "/data/.sn", "r")
        f.close()
        
        print(".sn loaded.")
    except FileNotFoundError:
        print(".sn not found.")
        quit(1)

#def load_opus_lib(opus_libs = OPUS_LIBS):
#    if opus.is_loaded():
#        return True

#    for opus_lib in opus_libs:
#        try:
#            opus.load_opus(opus_lib)
#            print("Opus lib loaded.")
#            return
#        except OSError:
#            pass

#    print("Could not find any opus lib. Music functionality is disabled.")
#    NO_OPUS = True

# Asynchronous Functions
async def leaderboards_init(bot: Bot):
    bot.leaderboards = await CreoMee6.levels.get_all_leaderboard_pages(30)
    print("MEE6 Leaderboards loaded.")
    
# Background Tasks
async def leaderboards_update(bot: Bot):
    await bot.wait_until_ready()
    
    while not bot.is_closed(): 
        await asyncio.sleep(90)
        
        try:
            bot.leaderboards = await CreoMee6.levels.get_all_leaderboard_pages(30)
        except:
            pass


# Bot Initialization, Bot-related Variable Declarations, and File-related Function Executions
# (Bot Setup, Part 1 of 4)
try:
    os.mkdir("data")
except:
    pass

if os.getenv("ALPHATEST") != None and isAlpha:
    BotToken = os.getenv("ALPHATEST")
    print("Alpha Bot Token loaded.")
else:
    BotToken = os.getenv("SOYDEVELOPER")
    print("Production Bot Token loaded.")
    isAlpha = False

DeveloperID = int(os.getenv("developerID"))

bot = Bot(
    command_prefix = lambda _, message: message.content[:2] if isAlpha and message.content.lower().startswith("c-") else message.content[:2] if message.content.lower().startswith("c+") and not isAlpha else Constants.bot_mention[isAlpha], 
    status = discord.Status.idle,
    activity = discord.Game("Project Cynical")
)
bot.case_insensitive = True
bot.owner_id = DeveloperID
bot.noMEE6 = True
bot.remove_command('help')

bot.eco = CynicEconomy(Constants.CurrentDirectory + "/data/")
CreoMee6 = mee6.API(Constants.ServerIDs[1])

if not bot.noMEE6:
    bot.loop.run_until_complete(leaderboards_init(bot)) # Ready the MEE6 leaderboards
set_changelog(bot) # Load changelog
sn_ready() # Ready the SN file
bot.loop.run_until_complete(bot.eco.setup_database()) # Ready LiveDB


# Cogs and Commands Setup (Bot Setup, Part 2 of 4)
from cogchamp import misc, cardgame, economy#, music

Cogs = [
    [cardgame.CardGameRelated, "Project Cynical's card game module. The main course of the bot."],
    [economy.Economy, "Project Cynical's economy system, where you can have fun with virtual currency."],
    [misc.Miscellaneous, "Commands that don't fit anywhere else."]#,
    #[music.Music, "Project Cynical's music module. Experimental."]
]

@bot.command(name = "suscommand", hidden = True, help = "when the exception is sus!")
@commands.is_owner()
async def when_the_sus(ctx):
    raise Exception("when the imposter is sus! :sus:")

@bot.command(name = "announcelog", aliases = ("alog", ), help = "Sends the changelog.")
@commands.is_owner()
async def announce_changelog(ctx: commands.Context):
    cl_ctx = ctx
    
    cl_ctx.command = bot.get_command("changelog")
    cl_ctx.channel = await bot.fetch_channel(803960072363048991)
    
    await ctx.send("Sent the changelog. \:)")
    await bot.invoke(cl_ctx)

# Event Listeners, Cog Registrations, and Background Task Creations (Bot Setup, Part 3 of 4)
# Event Listeners
@bot.listen()
async def on_ready():
    global hasLoaded
    
    if not hasLoaded:
        cards.initUniversalCards(); cards.initSpecialCards(); cards.initAllCards() # Load all the Cards
        print('Project Cynical is live on Discord as bot user {0.user}'.format(bot))
        hasLoaded = True
    else:
        print("Project Cynical has reconnected to Discord as bot user {0.user}".format(bot))
    
async def on_command_error(ctx, error): # deprecated
    print(f"{ctx.author} attempted to invoke invalid command: {error}")

@bot.before_invoke
async def message_check(ctx: commands.Context):
    await user_check(ctx, bot)
    
    #if ctx.command.cog == music.Music and NO_OPUS:
    #    raise Checks.NoOpusLoaded()

@bot.listen()
async def on_command_error(ctx: commands.Context, error):
    if hasattr(ctx.command, "on_error"):
        return
        
    error = getattr(error, 'original', error)
        
    if isinstance(error, commands.CommandNotFound):
        message = await ctx.send(f"{ctx.author.mention}, that command is not found!")
        await message.delete(delay = 10)
    
    elif isinstance(error, commands.CommandOnCooldown):
        message = await ctx.send(f"{ctx.author.mention}, that command is on cooldown for {error.retry_after:,.0f} seconds!")
        await message.delete(delay = 10)

    elif isinstance(error, commands.DisabledCommand):
        message = await ctx.send(f"{ctx.author.mention}, that command is disabled!")
        await message.delete(delay = 10)
        
    elif isinstance(error, commands.NotOwner):
        message = await ctx.send(f"{ctx.author.mention}, you may not use that command!")
        await message.delete(delay = 10)

    elif isinstance(error, commands.MissingPermissions):
        message = await ctx.send(f"{ctx.author.mention}, you do not have the permissions necessary to invoke this command!")
        await message.delete(delay = 10)
    
    elif isinstance(error, Checks.AuthorIsBot):
        pass
    
    elif isinstance(error, Checks.NoOpusLoaded):
        message = await ctx.send(f"{ctx.author.mention}, the music module is disabled because the Opus library is not loaded!")
        await message.delete(delay = 10)
    
    elif isinstance(error, Checks.BotShuttingDown):
        await ctx.send(f"{error}")

    elif isinstance(error, Checks.UserCheckFailure):
        message = await ctx.send(f"User check failed due to: `{error}`.")
        
        if ctx.guild.id in Constants.ServerIDs:
            await message.delete(delay = 10)
        else:
            ctx.guild.leave()
    
    else:
        print(f"Ignoring exception in command {ctx.command}:", file = sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
        
        embedError = libneko.Embed(title = f"Ignoring exception in command {ctx.command}:", description = "")
        embedError.color = random.randint(0x000000, 0xffffff)
        for line in traceback.TracebackException(
            type(error), error, error.__traceback__, limit = None).format(chain = True):
            embedError.description += line
        
        channel = await bot.fetch_channel(814357796035624980)
        try:
            await channel.send(content = "An error had occurred!", embed = embedError)
        except:
            await channel.send("An error had occurred! Please check the server console.")
        await ctx.send("Something went wrong! Please try again later.")
        
    return
    
@bot.listen()
async def on_guild_join(guild):
    if not guild.id in Constants.ServerIDs:
        print(f"An attempt to add the bot in non-whitelisted server \"{guild}\" ({guild.id}) has been made")
        await guild.leave()
    else:
        print(f"The bot has joined the server \"{guild}\" ({guild.id})")

@bot.listen()
async def on_guild_remove(guild):
    print(f"The bot has left the server \"{guild}\" ({guild.id})")

# Cog Registrations
for x in Cogs:
    bot.add_cog(x[0](bot, x[1]))

# Background Task Creations
if not bot.noMEE6:
    bot.loop.create_task(leaderboards_update(bot))


# Bot Execution (Bot Setup, Part 4 of 4)
bot.run(BotToken)
