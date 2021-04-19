if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

from typing import Optional
import random

import discord
from discord.colour import Color
import libneko
from discord.ext import commands

from lib import Converters, Constants
from lib import dbot

prefix = "c-" if Constants.isAlpha else "c+"
workOutcome = {
    True: ["{0.mention} worked hard enough to garner :coin: {1}.",
           "{0.mention}'s monthly paycheck has soon arrived, with :coin: {1} within the envelope.",
           "{0.mention} earned :coin: {1} while they were working."
           "{0.mention} managed to bag :coin: {1} as a bonus.",
           "{0.mention} used `" + prefix + "work` and got :coin: {1}."],
    False: ["{0.mention} messed up big time.",
            "{0.mention} didn't make it in time to work.",
            "{0.mention} couldn't go to work because there was a " + random.choice(["heavy rain", "snowstorm", "tornado"]) + ".",
            "{0.mention} accidentally messed up the documents.",
            "{0.mention} accidentally created a major bug in the bot's code."]
}

class Economy(commands.Cog, name = "Codename \"Vault\""):
    def __init__(self, bot: dbot.Bot, description: str = "(No description for this category of commands.)"):
        self.bot = bot
        self.description = description
    
    @commands.command(aliases = ("bal", "wallet", "bank"), help = "Display a user's current balance in both their wallet and bank, as well as the total amount.", brief = "Display user's balance.")
    async def balance(self, ctx, user: Optional[discord.Member]):
        uid = 0
        wallet = bank = None
        
        if user == None:
            user = ctx.author
            uid = ctx.author.id
        else:
            uid = user.id
        
        while wallet == None and bank == None:
            wallet = await self.bot.eco.get_money(uid, "wallet")
            bank = await self.bot.eco.get_money(uid, "bank")
            
        total = wallet + bank
    
        embed = libneko.Embed(title = f"{user}'s Balance")
        embed.description = f"**Wallet**: :coin: {wallet}\n**Bank**: :coin: {bank}\n**Total Balance**: :coin: {total}"
        embed.set_thumbnail(url = str(user.avatar_url))
        
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        
        try:
            await ctx.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I am unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")

    @commands.command(help = "Adds a daily monetary reward to the user's account. For every consecutive day, the amount increases, and resets when the streak is broken.", brief = "monies per day")
    async def daily(self, ctx):
        id = ctx.author.id
        amount = 500
        sA = 0
        valid = False
        day = await self.bot.eco.get_dailycd(id)
        
        embed = libneko.Embed(title = "Daily Rewards")
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        
        if type(day) is str:
            valid = False
        elif day == 1:
            await self.bot.eco.edit_streak(id, "add")
            valid = True
        else:
            await self.bot.eco.edit_streak(id, "set")
            valid = True
        
        if valid:
            streak = await self.bot.eco.get_streak(id)
            await self.bot.eco.set_dailycd(id)
            
            sA = (0.33 * (streak - 1))
            amount += int(50 * sA)
            
            await self.bot.eco.edit_money(id, amount, "wallet", "add")
            
            embed.description = f"You have received your daily :coin: {amount}!\n**Streak**: Day {streak} (+:coin: {int(50 * sA)})"
        else:
            embed.description = f"Your daily reward is on cooldown, please try again tomorrow!\n**Cooldown**: {day}"
            
        try:
            await ctx.send(f"{ctx.author.mention}", embed = embed)
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I am unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")      
    
    @commands.command(aliases = ("dep", ), help = "Deposit the specified amount of coins to the bank.", brief = "Deposit coins.")     
    async def deposit(self, ctx, amount: Optional[Converters.SafeInt]):        
        in_wallet = await self.bot.eco.get_money(ctx.author.id, "wallet")

        if amount == None or (amount != "all" and not type(amount) is int):
            await ctx.send(f"{ctx.author.mention}, please enter the amount of coins to withdraw!")
            return
        elif type(amount) is int:
            if amount <= 0:
                await ctx.send(f"{ctx.author.mention}, please enter the amount of coins to withdraw!")
                return
            elif amount > in_wallet:
                await ctx.send(f"{ctx.author.mention}, you don't have that much coins in your bank to withdraw!")
                return
        
        if amount == "all":
            amount = in_wallet
        
        if amount <= 0:
            await ctx.send(f"{ctx.author.mention}, please enter the amount of coins to withdraw!")
            return
        elif amount > in_wallet:
            await ctx.send(f"{ctx.author.mention}, you don't have that much coins in your bank to withdraw!")
            return
            
        await self.bot.eco.edit_money(ctx.author.id, amount, "wallet", "subtract")
        await self.bot.eco.edit_money(ctx.author.id, amount, "bank", "add")
        
        await ctx.send(f"Successfully deposited :coin: {amount} to {ctx.author.mention}'s wallet.")
        
    @commands.command(aliases = ("with", ), help = "Withdraw the specified amount of coins from the bank.", brief = "Withdraw coins.")     
    async def withdraw(self, ctx, amount: Optional[Converters.SafeInt]):        
        in_bank = await self.bot.eco.get_money(ctx.author.id, "bank")

        if amount == None or (amount != "all" and not type(amount) is int):
            await ctx.send(f"{ctx.author.mention}, please enter the amount of coins to withdraw!")
            return
        elif type(amount) is int:
            if amount <= 0:
                await ctx.send(f"{ctx.author.mention}, please enter the amount of coins to withdraw!")
                return
            elif amount > in_bank:
                await ctx.send(f"{ctx.author.mention}, you don't have that much coins in your bank to withdraw!")
                return
        
        if amount == "all":
            amount = in_bank
        
        if amount <= 0:
            await ctx.send(f"{ctx.author.mention}, please enter the amount of coins to withdraw!")
            return
        elif amount > in_bank:
            await ctx.send(f"{ctx.author.mention}, you don't have that much coins in your bank to withdraw!")
            return
            
        await self.bot.eco.edit_money(ctx.author.id, amount, "wallet", "add")
        await self.bot.eco.edit_money(ctx.author.id, amount, "bank", "subtract")
        
        await ctx.send(f"Successfully withdrawed :coin: {amount} from {ctx.author.mention}'s bank.")
    
    @commands.command(aliases = ("job", ), help = "Earn a quick buck or some. Has a cooldown of 15 seconds", brief = "get monies")
    @commands.cooldown(1, 15)
    async def work(self, ctx):        
        isSuccessful = random.choice([True, False, True, False, True, False])
        amount = int(random.randint(15, 50) * random.uniform(0.95, 2.95))
        
        embed = libneko.Embed(title = f"Work {'Successful <:le:808638475229986876>' if isSuccessful else 'Failed <:nogis:808638474646978560>'}")
        
        if isSuccessful:
            embed.color = random.choice([Color.green(), Color.blue(), Color.blurple()])
            embed.add_field(name = "Outcome:", value = random.choice(workOutcome[isSuccessful]).format(ctx.author, amount))
            await self.bot.eco.edit_money(ctx.author.id, amount, "wallet", "add")
        else:
            embed.color = random.choice([Color.red(), Color.orange(), 0xffff00])
            embed.add_field(name = "Outcome:", value = random.choice(workOutcome[isSuccessful]).format(ctx.author))
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
        
        try:
            await ctx.send(f"{ctx.author.mention}", embed = embed)
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I am unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    
    @commands.command(aliases = ("gm", ), hidden = True)
    @commands.is_owner()
    async def give_money(self, ctx, user: Optional[discord.User], amount: Optional[Converters.SafeInt]):
        if user == None:
            await ctx.send("Please add a user to give money to.")
            return
        
        if type(amount) is str:
            await ctx.send("Invalid value.")
            return
            
        if await self.bot.eco.edit_money(user.id, amount, "wallet", "add"):
            await ctx.send(f"Gave :coin: {amount} to {await self.bot.fetch_user(user.id)}")
            print(f" > Added {amount} coins to {user}'s wallet")
        else:
            await ctx.send(f" > Giving the coins failed :(")
            
    @commands.command(aliases = ("tm", ), hidden = True)
    @commands.is_owner()
    async def take_money(self, ctx, user: Optional[discord.User], amount: Optional[Converters.SafeInt]):        
        if user == None:
            await ctx.send("Please add a user to take money from.")
            return
        
        if type(amount) is str:
            await ctx.send("Invalid value.")
            return
            
        if await self.bot.eco.edit_money(user.id, amount, "wallet", "subtract"):
            await ctx.send(f"Removed :coin: {amount} from {await self.bot.fetch_user(user.id)}")
            print(f" > Removed {amount} coins from {user}'s wallet")
        else:
            await ctx.send(f" > Removing the coins from {user}'s wallet failed :(")