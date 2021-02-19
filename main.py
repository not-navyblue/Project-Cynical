# Adding the program's working directory to sys.path
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

# Built-in Modules
import os
import asyncio

# Third-party Modules and APIs
import discord
from dotenv import load_dotenv
import mee6_py_api as mee6
import hjson

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
add = Constants.add
subtract = Constants.subtract
number_format = Constants.number_format
isAlpha = Constants.isAlpha
user_check = Checks.user_check

hasLoaded = False

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

# Asynchronous Functions
async def leaderboards_init(bot: Bot):
    bot.leaderboards = await CreoMee6.levels.get_all_leaderboard_pages(30)
    print("MEE6 Leaderboards loaded.")
    
# Background Tasks
async def leaderboards_update(bot: Bot):
    await bot.wait_until_ready()
    iteration = 1
    
    while not bot.is_closed(): 
        await asyncio.sleep(60)
        
        try:
            bot.leaderboards = await CreoMee6.levels.get_all_leaderboard_pages(30)
        except:
            print(f"MEE6 Leaderboards update failed. (Update #{iteration})")
        
        iteration += 1


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

bot = Bot(command_prefix = lambda _, message: message.content[:2] if isAlpha and message.content.lower().startswith("c-") else message.content[:2] if message.content.lower().startswith("c+") and not isAlpha else Constants.bot_mention[isAlpha], status = discord.Status.idle)
bot.activity = discord.Game("Project Cynical")
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


# Cogs Setup (Bot Setup, Part 2 of 4)
from cogchamp import misc, cardgame, economy

Cogs = [
    [cardgame.CardGameRelated, "Commands of Project Cynical's Card Game module."],
    [economy.Economy, "Commands of Project Cynical's economy system."],
    [misc.Miscellaneous, "Commands that don't fit anywhere else."]
]

# Event Overrides, Cog Registrations, and Background Task Creations (Bot Setup, Part 3 of 4)
# Event Overrides
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

async def on_guild_join(guild):
    if not guild.id in Constants.ServerIDs:
        print(f"An attempt to add the bot in non-whitelisted server \"{guild}\" ({guild.id}) has been made")
        await guild.leave()
    else:
        print(f"The bot has joined the server \"{guild}\" ({guild.id})")

async def on_guild_remove(guild):
    print(f"The bot has left the server \"{guild}\" ({guild.id})")

bot.event(on_ready)
bot.event(on_guild_join)
bot.event(on_guild_remove)
# bot.event(on_command_error)

# Cog Registrations
for x in Cogs:
    bot.add_cog(x[0](bot, x[1]))

#bot.add_cog(CardGameRelated(bot, ))
#bot.add_cog(Economy(bot, ))
#bot.add_cog(Miscellaneous(bot, ))

# Background Task Creations
if not bot.noMEE6:
    bot.loop.create_task(leaderboards_update(bot))


# Bot Execution (Bot Setup, Part 4 of 4)
bot.run(BotToken)
