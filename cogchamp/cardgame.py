if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

from typing import Optional
import random
import asyncio

import discord
import libneko
from discord.ext import commands

from cards import cardDefines as cards
from lib.battleRewrite import Battle
from lib import Checks, Constants, Converters, battleRewrite as battles
from lib.dbot import Bot

user_check = Checks.user_check
add = Constants.add
subtract = Constants.subtract
isAlpha = Constants.isAlpha

# Synchronous
def check_if_started(channel: commands.Context.channel, bot: Bot):
    if len(bot.battles) < 1:
        pass
    else:
        for a in bot.battles:
            if a.channelID == channel.id:
                return True
            
    return False
    
def check_if_in_any_battle(member: discord.Member, bot: Bot):
    if len(bot.battles) < 1:
        pass
    else:
        for a in bot.battles:
            if member in a.fighters:
                return True
            
    return False

def check_if_pending(member: discord.Member, bot: Bot):
    if len(bot.pendingBattles) < 1:
        pass
    else:
        for a in bot.pendingBattles:
            if a[0] == member:
                return True
            
    return False

def check_if_challenged(member: discord.Member, bot: Bot):
    if len(bot.pendingBattles) < 1:
        pass
    else:
        for a in bot.pendingBattles:
            if a[1] == member:
                return True
    
    return False

def return_battle(channel: commands.Context.channel, bot: Bot):
    x = 0
    y = len(bot.battles)
    
    if x == y:
        return
    else:
        while x < y:
            if bot.battles[x].channelID == channel.id:
                return bot.battles[x]

def delete_battle(channel: commands.Context.channel, bot: Bot):
    x = 0
    y = len(bot.battles)
    
    if x == y:
        return False
    else:
        while x < y:
            if bot.battles[x].channelID == channel.id:
                bot.battles.remove(bot.battles[x])
                return True

# Asynchronous
async def battle_in(ctx: commands.Context, cardUsed: str, battle: Battle):
    turn = battle.playerTurn
    battle.timeout += 1
    if cardUsed == None:
        return 9
    elif type(cardUsed) is str:
        cardUsed = cardUsed.lower()
        
    isValid = battles.checkIfValid(cardUsed, battle)
    
    if isValid == True:
        if type(cardUsed) is int:
            cardUsed = battle.playerCards[turn][cardUsed - 1].lower()
        
        battle.consecutivePass = 0
        battle.outcome = ""
        battles.what_happens(cardUsed, battle)
        return True
    else:
        if isValid == "no energy":
            if type(cardUsed) is int:
                cardUsed = battle.playerCards[turn][cardUsed - 1].lower()
            cU = cards.AllCards[cardUsed]
            
            return 10
        elif isValid == "out of bounds":
            return 11
        else:
            return 12

async def battle_out(bot: Bot, ctx: commands.Context, battle: Battle):
    turn = battle.playerTurn
    players = battle.fighters
    embed = battles.displayBattle(battle)
    
    if battle.turns > 1:
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"{ctx.author} has made a move!")
    else:
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
    
    embed.colour = random.randint(0, 0xffffff)
        
    try:
        await ctx.channel.send(content = None, embed = embed)
    except discord.errors.Forbidden:
        await ctx.channel.send(f"{ctx.author.mention}, I am unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
        return
        
    if battle.endBattle:
        winner = battle.winner
        
        if battle.playerStatus[turn][0] == "timeout":
            await ctx.send(f"{players[turn].mention} hasn't used a Card in 3 minutes; ergo, {winner.mention} has been declared as the winner!")
        else:
            if winner == None:
                await ctx.send(f"The battle has ended because both players have not used a single Card within 4 total turns since the last use of a Card.")
                delete_battle(ctx.channel, bot)
                return
            else:
                await ctx.send(f"Congratulations, {winner.mention}! You have stood victorious in this battle that you have fought!")
                
        await battles.update_scores(battle.winNum, battle, bot.eco)
        delete_battle(ctx.channel, bot)
    else:
        thing = f"{players[turn].mention} (Battler {add(turn)})'s turn.\n\n"
        prefix = "c-" if isAlpha else "c+"
        
        if battle.playerCharging[turn][0]:
            thing += f"You are currently charging your power. Please use `{prefix}skip` to skip your turn."
        else:
            thing += f"Type `{prefix}use <Card name / Deck position>` to use a Card, `{prefix}refresh` to pass a turn, or `{prefix}summary` to view the battle summary again."
            
        thing += "\n\n**You have 3 minutes to use a valid Card.**"
        
        await ctx.send(thing)

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

async def battle_timeout(ctx: commands.Context, battle: battles.Battle, bot: Bot):
    timeout = battle.timeout
    turn = battle.playerTurn
    
    if timeout <= 0:
        battle.setStatus(turn, ("timeout", 0))
        await battle_out(bot, ctx, battle)
    else:
        battle.timeout -= 1

# Class
class CardGameRelated(commands.Cog, name = "Card Game Commands"):
    def __init__(self, bot: commands.Bot, description: str = "(No description for this category of commands.)"):
        self.bot = bot
        self.description = description
    
    @commands.command(aliases = ("cards", "list"), help = "Shows the list of Universal and Special Cards available for use.", brief = "Shows the list of Cards.")    
    async def cardlist(self, ctx):
        if not await user_check(ctx, self.bot):
            return

        embed = libneko.Embed(title = "List of Cards (sorted by IDs)")
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
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
                await ctx.channel.send(content = random.choice(["Note: Special Cards have a 5% chance of being added to a User's deck, except for their respective Users which have their own Special Card automatically added into their hand.", "Note: Cards in each of the player's decks in battle are randomized.", "Note: The ranges of stats of a player are 20 - 200 for Attack & Defense, and 50 - 150 for Accuracy and Evasion."]), embed = embed)
            else:
                await ctx.channel.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    
    @commands.command(aliases = ("cinfo", ), help = "Displays some more information about a specific Card.\nArguments: [Card Name / Card ID]", brief = "More Card information")
    async def cardinfo(self, ctx, *, cardID: Optional[Converters.SafeInt]):
        if not await user_check(ctx, self.bot):
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
            moveInfo.power = " -- "
        elif moveInfo.power == 999:
            moveInfo.power = "OHKO"
          
        if moveInfo.id == 11:
            moveInfo.power = "0 or 20 - 50"  
        elif moveInfo.id == 13:
            moveInfo.power = "35 - 70"
        
        embed = libneko.Embed(title = f"More Card Information")
        
        cl = moveInfo.classification.split(",", 1)
        clinfo = ""
        
        if len(cl) == 1:
            clinfo = cl[0].title()
        elif len(cl) == 2:
            clinfo = f"{cl[0].title()} / {cl[1].title()}"
        
        if moveInfo.isSpecial:  
            embed.description = f"**Card Name**: {moveInfo.name} (ID: {moveInfo.id})\n**Classification/s**: {clinfo} [Special]\n**Card Power**: {moveInfo.power}\n**Accuracy**: {moveInfo.accuracy}%\n**Energy Cost**: {moveInfo.energycost} Energy"
        else:
            embed.description = f"**Card Name**: {moveInfo.name} (ID: {moveInfo.id})\n**Classification/s**: {clinfo} [Universal]\n**Card Power**: {moveInfo.power}\n**Accuracy**: {moveInfo.accuracy}%\n**Energy Cost**: {moveInfo.energycost} Energy"
        
        embed.add_field(name = "**Card Description**:", value = f"\"{moveInfo.description}\"")
        embed.add_field(name = "**Battle Effect/s**:", value = moveInfo.effectDesc)
        
        if moveInfo.isSpecial:
            if moveInfo.originalUser != 0:
                try:
                    embed.add_field(name = f"**Special / Additional Effect(s)** ({await self.bot.fetch_user(moveInfo.originalUser)}):", value = f"{moveInfo.originalUserDesc}")
                except discord.NotFound:
                    embed.add_field(name = f"**Special / Additional Effect(s)** (MissingUser#0000):", value = f"{moveInfo.originalUserDesc}")
        
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        
        try:
            await ctx.channel.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, I am unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
         
    @commands.command(aliases = ("fight", ), help = "Initiates a Card Battle with another member. Requires the challenged user to accept the challenge to start the battle.\n(Note: The bot will refuse to initiate a battle if Creo is the one who's challenged while he is offline.)\nArguments: < Mentioned Member > ", brief = "Starts a battle.")
    async def battle(self, ctx, challengee: Optional[discord.Member]):
        if not await user_check(ctx, self.bot):
            return

        if check_if_started(ctx.channel, self.bot): # If there's a battle ongoing in a channel
            await ctx.send(f"{ctx.author.mention}, there is a battle ongoing!")
            return
        elif check_if_in_any_battle(ctx.author, self.bot): # If the user is already in a battle
            await ctx.send(f"{ctx.author.mention}, you are already in a battle!")
            return
        elif not type(challengee) is discord.Member: # If there is no user mentioned
            await ctx.send(f"{ctx.author.mention}, you need to mention another user to battle!")
            return
        elif challengee.id == 170353794134179840 and challengee.status == discord.Status.offline:
            await ctx.send(f"{ctx.author.mention}, you can't do that, that's against the rules!")
            return # If Creo's challenged but he's offline
        elif ctx.author.id == challengee.id and not ctx.guild.id == Constants.ServerIDs[0]: # If the challenger tries to battle itself
            await ctx.send(f"{ctx.author.mention}, you can't battle yourself!")
            return
        elif check_if_in_any_battle(challengee, self.bot): # If a challengee is already in a battle
            await ctx.send(f"{ctx.author.mention}, please challenge another user. They are already in a battle!")
            return
        elif check_if_pending(ctx.author, self.bot): # If you have a pending challenge already
            await ctx.send(f"{ctx.author.mention}, you already have a pending challenge!")
            return
        else:
            self.bot.pendingBattles.append([ctx.author, challengee])
            await ctx.send(f"{challengee.mention}, you are being challenged by {ctx.author.mention}! Reply with `c.accept` within to accept to their challenge!")
            await challenge_timeout(ctx, [ctx.author, challengee], self.bot)
            
    @commands.command(hidden = True, help = "Accepts a challenge.")
    async def accept(self, ctx):
        if not await user_check(ctx, self.bot):
            return

        if check_if_challenged(ctx.author, self.bot):
            if check_if_started(ctx.channel, self.bot):
                await ctx.send("A battle in this channel has already started!")
                return
            
            for a in self.bot.pendingBattles:
                if a[1] == ctx.author:
                    await ctx.send("Battle initiating...")
                    
                    self.bot.battles.append(Battle(ctx.channel.id, a))
                    battles.initBattle(return_battle(ctx.channel, self.bot))
                    
                    battle = return_battle(ctx.channel, self.bot)
                    
                    await battle_out(self.bot, ctx, battle)
                    await asyncio.sleep(180)
                    await battle_timeout(ctx, battle, self.bot)
    
    @commands.command(hidden = True, help = "Use a Card in a Card Battle.")
    async def use(self, ctx, *, cardUsed: Optional[Converters.SafeInt]):
        if not await user_check(ctx, self.bot):
            return

        checkB = None
        battle = return_battle(ctx.channel, self.bot)
        
        if battle == None:
            return
        
        turn = battle.playerTurn
        if battle.fighters[turn].id == ctx.author.id and battle.playerCharging[turn][0]:
            await ctx.send(f"{ctx.author.mention}, you are charging your power for your outcoming attack! Use `c.skip` to skip a turn!")
            return
                    
        elif ctx.author == battle.fighters[turn]:
            checkB = await battle_in(ctx, cardUsed, battle)
            eMessage = None
            
            if checkB == True:
                await battle_out(self.bot, ctx, battle)
                await asyncio.sleep(180)
                await battle_timeout(ctx, battle, self.bot)
            elif checkB == 9:
                eMessage = await ctx.send(f"{ctx.author.mention}, please select a Card!")
            elif checkB == 10:
                if type(cardUsed) is int:
                    cardUsed = battle.playerCards[turn][cardUsed]
                    
                cU = cards.AllCards[cardUsed]
                
                if cU.id == 1002 and cU.originalUser == ctx.author.id:
                    eMessage = await ctx.send(f"{ctx.author.mention}, you don't have enough energy to use that Card! ({7 - battle.playerEnergy[turn]} more Energy needed.)")
                else:
                    eMessage = await ctx.send(f"{ctx.author.mention}, you don't have enough energy to use that Card! ({cU.energycost - battle.playerEnergy[turn]} more Energy needed.)")
            elif checkB == 11:
                eMessage = await ctx.send(f"{ctx.author.mention}, there is no Card in that position!")
            elif checkB == 12:
                eMessage = await ctx.send(f"{ctx.author.mention}, please use another Card! The previous one was either invalid or not in your hand!")
    
            if checkB != True:
                try:
                    await eMessage.delete(delay = 5)
                except discord.errors.NotFound:
                    print(f"Error: {eMessage} already deleted")
    
    @commands.command(aliases = ("rest", "refresh", "pass", "skip"), hidden = True)
    async def restore(self, ctx):
        if not await user_check(ctx, self.bot):
            return

        battle = return_battle(ctx.channel, self.bot)
        
        if battle == None:
            return
        
        turn = battle.playerTurn
        if ctx.author == battle.fighters[turn]:
            battle.consecutivePass += 1
            battle.timeout += 1
            battles.what_happens("restore", battle)
            
            await battle_out(self.bot, ctx, battle)
            await asyncio.sleep(180)
            await battle_timeout(ctx, battle, self.bot)
    
    @commands.command(hidden = True, help = "Display the current summary of the battle.")
    async def summary(self, ctx):
        if not await user_check(ctx, self.bot):
            return

        battle = return_battle(ctx.channel, self.bot)
        
        if battle == None:
            return
        
        if ctx.author in battle.fighters:
            await battle_out(self.bot, ctx, battle)