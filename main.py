# Built-in Modules
import os
import random
from typing import Optional

# Third-party Modules and APIs
import discord
from discord.errors import DiscordException, Forbidden
from discord.ext import commands, tasks
import asyncio
from dotenv import load_dotenv

# Custom/Developer-defined Modules
import constants, cardDefines as cards, battleRewrite as battles
from battleRewrite import Battle
import Converters, Checks

# Loading the .env file
if load_dotenv():
    print("Environment variables (from the .env file) loaded.")
else:
    print("Failed to load environment variables.")
    quit(1)

# Global Variables
isAlpha = False

# Customized Bot class (subclass of discord.ext.commands.Bot)
class Bot(commands.Bot):
    def __init__(self, command_prefix, help_command = commands.bot._default, description = None, **options):
        super().__init__(command_prefix, help_command = help_command, description = description, **options)
        self.changelogContents = list()
        self.battles = list()
        self.pendingBattles = list() # [[battler11, battler12], [battler21, battler22], ...]
        self.isShuttingDown = False

# Function Definitions
def setChangelog(bot: Bot):
    f = open("changelog", "r")
    bot.changelogContents = f.read().split("\n\n")
    bot.changelogContents.reverse()
    f.close()
    if len(bot.changelogContents) > 0:
        print("Changelog loaded.")
    else:
        print("Changelog failed to load.")
        quit(1)

def createHighScoresFile():
    try:
        os.mkdir(constants.CurrentDirectory + "/data")
    except FileExistsError:
        pass
    except OSError:
        pass
    
    try:
        f = open(constants.CurrentDirectory + "/data/highscores.mhjson", "x")
        f.write('{\n' + f"\t0: {DeveloperID}\n" + '}')
        f.close()
        
        print("highscores.mhjson created.")
    except FileExistsError:
        print("highscores.mhjson loaded.")
    except OSError:
        print("highscores.mhjson loaded.")
        
def isServerValid(ctx):
    try:
        for x in constants.ServerIDs:
            if ctx.guild.id == x:
                raise Exception("message's server is one of the servers allowed")
    except Exception:
        return True
    else:
        return False

def checkIfStarted(channel: commands.Context.channel, bot: Bot):
    if len(bot.battles) < 1:
        pass
    else:
        for a in bot.battles:
            if a.channelID == channel.id:
                return True
            
    return False
    
def checkIfInAnyBattle(member: discord.Member, bot: Bot):
    if len(bot.battles) < 1:
        pass
    else:
        for a in bot.battles:
            if member in a.fighters:
                return True
            
    return False

def checkIfPending(member: discord.Member, bot: Bot):
    if len(bot.pendingBattles) < 1:
        pass
    else:
        for a in bot.pendingBattles:
            if a[0] == member:
                return True
            
    return False

def checkIfChallenged(member: discord.Member, bot: Bot):
    if len(bot.pendingBattles) < 1:
        pass
    else:
        for a in bot.pendingBattles:
            if a[1] == member:
                return True
    
    return False

def returnBattle(channel: commands.Context.channel, bot: Bot):
    x = 0
    y = len(bot.battles)
    
    if x == y:
        return
    else:
        while x < y:
            if bot.battles[x].channelID == channel.id:
                return bot.battles[x]

def deleteBattle(channel: commands.Context.channel, bot: Bot):
    x = 0
    y = len(bot.battles)
    
    if x == y:
        return False
    else:
        while x < y:
            if bot.battles[x].channelID == channel.id:
                bot.battles.remove(bot.battles[x])
                return True

async def battle_in(ctx: commands.Context, cardUsed: str, battle: Battle):
    turn = battle.playerTurn
    if cardUsed == None:
        await ctx.send(f"{ctx.author.mention}, please select a Card!")
        return False
    elif type(cardUsed) is str:
        cardUsed = cardUsed.lower()
        
    isValid = battles.checkIfValid(cardUsed, battle)
    
    if isValid == True:
        if type(cardUsed) is int:
            cardUsed = battle.playerCards[turn][cardUsed - 1].lower()
        
        battle.consecutivePass = 0
        battles.what_happens(cardUsed, battle)
        return True
    else:
        if isValid == "no energy":
            if type(cardUsed) is int:
                cardUsed = battle.playerCards[turn][cardUsed - 1].lower()
            cU = cards.AllCards[cardUsed]
            
            if cU.id == 1002 and cU.originalUser == ctx.author.id:
                await ctx.send(f"{ctx.author.mention}, you don't have enough energy to use that Card! ({7 - battle.playerEnergy[turn]} more Energy needed.)")
            else:
                await ctx.send(f"{ctx.author.mention}, you don't have enough energy to use that Card! ({cU.energycost - battle.playerEnergy[turn]} more Energy needed.)")
            
            return False
        elif isValid == "out of bounds":
            await ctx.send(f"{ctx.author.mention}, there is no Card in that position!")
            return False
        else:
            await ctx.send(f"{ctx.author.mention}, please use another Card! The previous one was either invalid or not in your hand!")
            return False

async def battle_out(ctx: commands.Context, battle: Battle):
    turn = battle.playerTurn
    players = battle.fighters
    embed = battles.displayBattle(battle)
    
    if battle.turns > 1:
        embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 64), text = f"{ctx.author} has made a move!")
    else:
        embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 64), text = f"Command requested by {ctx.author}")
    
    embed.colour = random.randint(0, 0xffffff)
        
    try:
        await ctx.channel.send(content = None, embed = embed)
    except discord.errors.Forbidden:
        await ctx.channel.send(f"{ctx.author.mention}, I am unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
        return
        
    if battle.endBattle:
        winner = battle.winner
        
        if battle.playerStatus[turn][0] == "surrendered":
            await ctx.send(f"Due to {players[turn].mention}'s plea of surrender, {winner.mention} has been declared as the winner!")
        else:
            if winner == None:
                await ctx.send(f"The battle has ended because both players have not used a single Card within 4 total turns since the last use of a Card.")
                deleteBattle(ctx.channel, bot)
                return
            else:
                await ctx.send(f"Congratulations, {winner.mention}! You have stood victorious in this battle that you have fought!")
                
        battles.setHighScore(battle.winNum, battle)
        deleteBattle(ctx.channel, bot)
    else:
        await ctx.send(f"It is now {players[turn].mention} (Battler {add(turn)})'s turn.\nUse `c.use <Card name / Deck position>` to use a Card.\nUse `c.refresh` to pass a turn.\nUse `c.surrender` to surrender in this battle.\nUse `c.summary` to view the battle summary again.")

async def challenge_timeout(ctx: commands.Context, fighters: list, bot: Bot):
    await asyncio.sleep(15)
    if len(bot.battles) > 0:
        for a in bot.battles:
            if a.channelID == ctx.channel.id:
                if a.fighters != fighters:
                    bot.pendingBattles.remove(fighters)
                return
                
    bot.pendingBattles.remove(fighters)
    await ctx.send("Battle timed out.")

add = lambda a, b = 1: a + b
subtract = lambda a, b = 1: a - b

# Bot Initialization, Bot-related Variable Declarations, and File-related Function Executions
# (Bot Setup, Part 1 of 4)
if os.getenv("ALPHATEST") != None and isAlpha:
    BotToken = os.getenv("ALPHATEST")
    print("Alpha Bot Token loaded.")
else:
    BotToken = os.getenv("SOYDEVELOPER")
    print("Production Bot Token loaded.")
DeveloperID = int(os.getenv("developerID"))

bot = Bot(command_prefix = lambda _, message: message.content[:2] if message.content.lower().startswith('c.') else 'c.', status = discord.Status.idle)
bot.activity = discord.Game("Project Cynical")
bot.owner_id = DeveloperID
bot.remove_command('help')

setChangelog(bot) # Load changelog
createHighScoresFile() # Load highscores.mhjson


# Cogs and Commands Setup (Bot Setup, Part 2 of 4)
# Miscellaneous Commands
class Miscellaneous(commands.Cog, name = "Miscellaneous Commands"):
    def __init__(self, bot: commands.Bot, description: str = "(No description for this category of commands.)"):
        self.bot = bot
        self.description = description
    
    @commands.command(aliases = ("clist", "commands"), help = "Shows the list of commands of the bot and this message.\nArguments: [Command Name (case sensitive)]", brief = "Shows this help message.")
    async def help(self, ctx, command: Optional[str]):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        embed = discord.Embed(title = "Commands List")
        embed.colour = random.randint(0, 0xffffff)
        
        leCogs = bot.cogs
        if not type(command) is str:
            embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 64), text = f"Command requested by {ctx.author}")
            for b in leCogs:
                cogCommands = leCogs.get(b).get_commands()
                commandinfo = ""
                
                for a in cogCommands:
                    shortHelp = getattr(a, "brief", "(Brief command info not found.)")
                    isHidden = getattr(a, "hidden", False)
                
                    if not isHidden:
                        commandinfo += str("\n**c." + str(a) + f"** -> {shortHelp}")
                    else:
                        pass
                    
                embed.add_field(name = f"**{b}**", value = leCogs.get(b).description + commandinfo)
        else:
            embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 64), text = random.choice([f"Command requested by {ctx.author}", f"Command requested by {ctx.author}", "Arguments with tag brackets (e.g. <args>) are required, and those with square brackets (e.g. [args]) are optional."]))
            embed.title = "Specific Command Info"
            commR = bot.get_command(command)
            commCat = str()
            
            try:
                for a in leCogs:
                    if commR in leCogs.get(a).get_commands():
                        commCat = a
                        raise Exception("cog found")
            except Exception:
                pass
            else:
                commCat = "No Category"
            
            if commR is None:
                await ctx.send(f"Command \"{command}\" not found.")
                return
            else:
                helpMessage = getattr(commR, "help", f"No info given for command \"{commR}\".")
                aliases = getattr(commR, "aliases", "None")
                isHidden = getattr(commR, "hidden", False)
                
                if aliases == []:
                    aliases = "None"
                
                if isHidden:
                    helpMessage += "\n**Note: This is a hidden command. It will not be listed when the list of commands is displayed.**"
                
                embed.add_field(name = "c." + str(commR), value = f"{helpMessage}\n\nAlias/es: {aliases}\nBelongs to: **{commCat}**")
                
        try:
            await ctx.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    
    @commands.command(aliases = ("ping",), help = "Displays the latency of the bot in milliseconds.", brief = "Displays the latency")
    async def latency(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        await ctx.send(f"Latency is currently at {bot.latency * 1000:.2f}ms.")

    @commands.command(aliases = ("terminate", "turnoff", "killbot", "restart"), hidden = True, help = "Shuts down the bot. Optional argument `--nowait` skips the 15-second delay. Bot developer only.")
    @Checks.is_developer(bot)
    async def shutdown(self, ctx, s: Optional[str]):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
    
        if s != "--nowait":
            bot.isShuttingDown = True
            await ctx.send("Shutting down in 15 seconds...")
            await bot.change_presence(status = discord.Status.dnd, activity = discord.Game("Project Cyclical (Shutting down...)"))
            await asyncio.sleep(15)

        await bot.change_presence(status = discord.Status.offline)
        await ctx.send("Project Cynical has been terminated.")
        print("Project Cynical has logged out of Discord.")
        await bot.logout()

    @commands.command(aliases = ("cl",), help = "Shows the changelog of the bot. Page number is optional. Defaults to the latest version of the bot.\nArguments: [\"oldest\" / page number]", brief = "Shows the changelog.")
    async def changelog(self, ctx, *, pageNum: Optional[Converters.SafeInt]):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
    
        embed = discord.Embed()
        embed.colour = random.randint(0, 0xffffff)
    
        maxPage = len(bot.changelogContents)
    
        if type(pageNum) is int:
            pageNum -= 1
        else:
            if pageNum == "oldest":
                pageNum = subtract(maxPage)
            else:
                pageNum = 0
    
        if pageNum < 0 or pageNum > subtract(maxPage):
            await ctx.send(f"{ctx.author.mention}, that is an invalid page number! Range: `1 - {maxPage}`")
            return
    
        if pageNum == 0:
            embed.title = f"Latest Update (page {add(pageNum)} of {maxPage}):"
        elif pageNum == subtract(maxPage):
            embed.title = f"Oldest Version (page {add(pageNum)} of {maxPage}):"
        else:
            embed.title = f"Older Update (page {add(pageNum)} of {maxPage}):"
        
        embed.description = bot.changelogContents[pageNum]
        embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 64), text = f"Command requested by {ctx.author}")
        
        try:
            await ctx.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")

# Card Game-related Commands
class CardGameRelated(commands.Cog, name = "Card Game Commands"):
    def __init__(self, bot: commands.Bot, description: str = "(No description for this category of commands.)"):
        self.bot = bot
        self.description = description
    
    @tasks.loop(minutes = 1, seconds = 30, count = 1)
    async def turn_timeout(self, ctx: commands.Context):
        pass
    
    @commands.command(aliases = ("leaderboard", "scores", "highscores", "highscore", "lb"), help = "Displays the leaderboard of Top 10 highest scores, as well as the user's score separately.", brief = "Display the leaderboards.")
    async def leaderboards(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        embed = await battles.getHighScores(bot, ctx.author)
        embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 64), text = f"Command requested by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        
        try:
            await ctx.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    
    @commands.command(aliases = ("cards", "list"), help = "Shows the list of Universal and Special Cards available for use.", brief = "Shows the list of Cards.")    
    async def cardlist(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        embed = discord.Embed(title = "List of Cards (sorted by IDs)")
        embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 32), text = f"Command requested by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        
        stri = ""
        for x in cards.UniversalCards:
            stri += f"ID {cards.NormalCards[x].id}: {cards.NormalCards[x].name} (Energy Cost: {cards.NormalCards[x].energycost} Energy)\n"
        embed.add_field(name = "Normal Cards: ", value = stri)
        del stri
        
        stri = ""
        for x in cards.SpecialCards_:
            if x == None:
                pass
            else:
                stri += f"ID {cards.SpecialCards[x].id}: {cards.SpecialCards[x].name} (Energy Cost: {cards.SpecialCards[x].energycost} Energy)\n"
        embed.add_field(name = "Special (User-specific) Cards: ", value = stri)
        embed.colour = random.randint(0, 0xffffff)
        del stri

        try:
            if random.randint(1, 100) <= 30:
                await ctx.channel.send(content = random.choice(["Note: Special Cards have a 25% chance of being added to a User's deck, except for their respective Users which have their own Special Card automatically added into their hand.", "Note: Cards in each of the player's decks in battle are randomized.", "Note: The ranges of stats of a player are 20 - 200 for Attack & Defense, and 50 - 150 for Accuracy and Evasion."]), embed = embed)
            else:
                await ctx.channel.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    
    @commands.command(aliases = ("cinfo", "info"), help = "Displays some more information about a specific Card.\nArguments: [Card Name / Card ID]", brief = "More Card information")
    async def cardinfo(self, ctx, *, cardID: Optional[Converters.SafeInt]):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        moveInfo = None
        if type(cardID) is str:
            cardID = cardID.lower()
        elif type(cardID) is int:
            pass
        else:
            await ctx.channel.send(f"{ctx.author.mention}, please enter the name or ID of a Card!")
            return
        
        if type(cardID) is int:
            for x in cards.UniversalCards:
                try:
                    c = cards.UniversalCards[cardID]
                except:
                    pass
                else:
                    for a in cards.NormalCards:
                        if a == c:
                            moveInfo = cards.NormalCards[c]
                            
            for x in cards.SpecialCards_:
                try:
                    c = cards.SpecialCards_[cardID]
                    
                    if c == None:
                        raise Exception("pass")
                except:
                    pass
                else:
                    moveInfo = cards.SpecialCards[c]
        else:
            for o in cards.AllCards:
                if o == cardID:
                    moveInfo = cards.AllCards[o]
                
        if moveInfo == None:
            await ctx.channel.send(f"{ctx.author.mention}, there is no Card with that name or ID!")
            return
        elif moveInfo.id == 1000:
            await ctx.channel.send(f"{ctx.author.mention}, there is no Card with that name or ID!")
            return
        
        if moveInfo.power == -1:
            moveInfo.power = "--"
        elif moveInfo.power == 999:
            moveInfo.power = "OHKO"
          
        if moveInfo.id == 11:
            moveInfo.power = "0 or 20 - 50"  
        elif moveInfo.id == 13:
            moveInfo.power = "35 - 70"
        
        embed = discord.Embed(title = f"More Card Information")
        
        if moveInfo.isSpecial:  
            embed.description = f"**Card Name**: {moveInfo.name} (ID: {moveInfo.id})\n**Classification**: {moveInfo.classification.title()} [Special]\n**Power**: {moveInfo.power}\n**Accuracy**: {moveInfo.accuracy}\n**Energy Cost**: {moveInfo.energycost}"
        else:
            embed.description = f"**Card Name**: {moveInfo.name} (ID: {moveInfo.id})\n**Classification**: {moveInfo.classification.title()} [Universal]\n**Power**: {moveInfo.power}\n**Accuracy**: {moveInfo.accuracy}\n**Energy Cost**: {moveInfo.energycost}"
        
        embed.add_field(name = "**Card Description**:", value = f"\"{moveInfo.description}\"")
        embed.add_field(name = "**Battle Effect/s**:", value = moveInfo.effectDesc)
        
        if moveInfo.isSpecial:
            if moveInfo.originalUser != 0:
                try:
                    embed.add_field(name = f"**Special / Additional Effect(s)** ({await bot.fetch_user(moveInfo.originalUser)}):", value = f"{moveInfo.originalUserDesc}")
                except discord.NotFound:
                    embed.add_field(name = f"**Special / Additional Effect(s)** (MissingUser#0000):", value = f"{moveInfo.originalUserDesc}")
        
        embed.set_footer(icon_url = discord.User.avatar_url_as(ctx.author, size = 32), text = f"Command requested by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        
        try:
            await ctx.channel.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, I am unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
         
    @commands.command(aliases = ("fight",), help = "Initiates a Card Battle with another member. Requires the challenged user to accept the challenge to start the battle.\n(Note: The bot will refuse to initiate a battle if Creo is the one who's challenged while he is offline.)\nArguments: <Mentioned Member>", brief = "Starts a battle.")
    async def battle(self, ctx, challengee: Optional[discord.Member]):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        if checkIfStarted(ctx.channel, bot): # If there's a battle ongoing in a channel
            await ctx.send(f"{ctx.author.mention}, there is a battle ongoing!")
            return
        elif checkIfInAnyBattle(ctx.author, bot): # If the user is already in a battle
            await ctx.send(f"{ctx.author.mention}, you are already in a battle!")
            return
        elif not type(challengee) is discord.Member: # If there is no user mentioned
            await ctx.send(f"{ctx.author.mention}, you need to mention another user to battle!")
            return
        elif challengee.id == 170353794134179840 and challengee.status == discord.Status.offline:
            await ctx.send(f"{ctx.author.mention}, you can't do that, that's against the rules!")
            return # If Creo's challenged but he's offline
        elif ctx.author.id == challengee.id: # If the challenger tries to battle itself
            await ctx.send(f"{ctx.author.mention}, you can't battle yourself!")
            return
        elif checkIfInAnyBattle(challengee, bot): # If a challengee is already in a battle
            await ctx.send(f"{ctx.author.mention}, please challenge another user. They are already in a battle!")
            return
        elif checkIfPending(ctx.author, bot): # If you have a pending challenge already
            await ctx.send(f"{ctx.author.mention}, you already have a pending challenge!")
            return
        else:
            bot.pendingBattles.append([ctx.author, challengee])
            await ctx.send(f"{challengee.mention}, you are being challenged by {ctx.author.mention}! Reply with `c.accept` within to accept to their challenge!")
            await challenge_timeout(ctx, [ctx.author, challengee], bot)
            
    @commands.command(hidden = True, help = "Accepts a challenge.")
    async def accept(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        if checkIfChallenged(ctx.author, bot):
            if checkIfStarted(ctx.channel, bot):
                await ctx.send("A battle in this channel has already started!")
                return
            
            for a in bot.pendingBattles:
                if a[1] == ctx.author:
                    await ctx.send("Battle initiating...")
                    
                    bot.battles.append(Battle(ctx.channel.id, a))
                    battles.initBattle(returnBattle(ctx.channel, bot))
                    bot.pendingBattles.remove(a)
                    
                    await battle_out(ctx, returnBattle(ctx.channel, bot))
    
    @commands.command(hidden = True, help = "Use a Card in a Card Battle.")
    async def use(self, ctx, *, cardUsed: Optional[Converters.SafeInt]):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        battle = returnBattle(ctx.channel, bot)
        
        if battle == None:
            return
        
        turn = battle.playerTurn
        if ctx.author == battle.fighters[turn]:
            if await battle_in(ctx, cardUsed, battle):
                await battle_out(ctx, battle)
    
    @commands.command(aliases = ("rest", "restore", "pass", "skip"), hidden = True)
    async def refresh(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        battle = returnBattle(ctx.channel, bot)
        
        if battle == None:
            return
        
        turn = battle.playerTurn
        if ctx.author == battle.fighters[turn]:
            battle.consecutivePass += 1
            battles.what_happens("restore", battle)
            await battle_out(ctx, battle)
    
    @commands.command(aliases = ("resign",), hidden = True, help = "Surrender in a Card Battle. This will result to opposition victory.")
    async def surrender(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        battle = returnBattle(ctx.channel, bot)
        
        if battle == None:
            return
        
        turn = battle.playerTurn
        if ctx.author == battle.fighters[turn]:
            battle.setStatus(turn, ["surrendered", 0])
            await battle_out(ctx, battle)
    
    @commands.command(hidden = True, help = "Display the current summary of the battle.")
    async def summary(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        battle = returnBattle(ctx.channel, bot)
        
        if battle == None:
            return
        
        if ctx.author in battle.fighters:
            await battle_out(ctx, battle)
    
    @commands.command(hidden = True)
    @Checks.is_developer(bot)
    async def resetscore(self, ctx):
        if not isServerValid(ctx):
            print(f"{ctx.author} attempted to send a command on non-whitelisted server \"{ctx.guild}\"")
            return
        
        try:
            f = open(constants.CurrentDirectory + "/data/highscores.mhjson", "w")
            f.write('{\n' + f"\t0: {DeveloperID}\n" + '}')
            f.close()
            
            await ctx.send("Reset successful.")
        except OSError:
            await ctx.send("Reset failed.")
            return
    

# Event Overrides and Cog Registrations (Bot Setup, Part 3 of 4)
# Event Overrides
async def on_ready():
    cards.initUniversalCards(); cards.initSpecialCards(); cards.initAllCards() # Load all the Cards
    print('Project Cynical is live as {0.user}.'.format(bot))
    
async def on_command_error(ctx, error): # deprecated
    print(f"{ctx.author} attempted to invoke invalid command: {error}")

async def on_command(ctx):
    if bot.isShuttingDown and ctx.author != bot.user and ctx.message.content.startswith("c."):
        await ctx.send("Project Cynical is shutting down. All commands are no longer invoked.")
        return

bot.event(on_ready)
#bot.event(on_command_error)
bot.event(on_command)

# Cog Registrations
bot.add_cog(CardGameRelated(bot, "Commands that are related to the main feature of Project Cynical."))
bot.add_cog(Miscellaneous(bot, "Commands that don't fit anywhere else."))


# Bot Execution (Bot Setup, Part 4 of 4)
bot.run(BotToken)
