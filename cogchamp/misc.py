if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

from typing import Optional
import random
import asyncio

import discord
import libneko
from discord.ext import commands
from discord.ext.commands.errors import CommandError

from lib import Checks, Constants, Converters, battleRewrite as battles

isAlpha = Constants.isAlpha
rank_prefix = Constants.rank_prefix
level_ranges = Constants.level_ranges
xp_ranges = Constants.xp_ranges
add = Constants.add
subtract = Constants.subtract
number_format = Constants.number_format
user_check = Checks.user_check
                
def sn_add():
    sNum = 0
    
    try:
        f = open(Constants.CurrentDirectory + "/data/.sn", "r")
        sNum = f.read()
        f.close()
        
    except:
        print("Error operation on file '.sn' (6)")
        return -1
    
    sNum = int(sNum)
    sNum += 1
    
    try:
        f = open(Constants.CurrentDirectory + "/data/.sn", "w")
        f.write(str(sNum))
        f.close()
        
        return sNum
    except:
        print("Error operation on file '.sn' (7)")
        return -1

class Miscellaneous(commands.Cog, name = "Miscellaneous Commands"):
    def __init__(self, bot: commands.Bot, description: str = "(No description for this category of commands.)"):
        self.bot = bot
        self.description = description
    
    @commands.command(aliases = ("clist", "commands"), help = "Shows the list of commands of the bot and this message.\nArguments: [Command Name (case sensitive)]", brief = "Shows this help message.")
    async def help(self, ctx, command: Optional[str]):
        if not await user_check(ctx, self.bot):
            return

        embed = libneko.Embed(title = "Commands List")
        embed.colour = random.randint(0, 0xffffff)
        
        prefix = "c-" if isAlpha else "c+"
        
        leCogs = self.bot.cogs
        if not type(command) is str:
            embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
            for b in leCogs:
                cogCommands = leCogs.get(b).get_commands()
                commandinfo = ""
                
                for a in cogCommands:
                    shortHelp = getattr(a, "brief", "(Brief command info not found.)")
                    isHidden = getattr(a, "hidden", False)
                
                    if not isHidden:
                        commandinfo += str(f"\n**{prefix}" + str(a) + f"** - > {shortHelp}")
                    else:
                        pass
                    
                embed.add_field(name = f"**{b}**", value = leCogs.get(b).description + commandinfo)
        else:
            embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
            embed.title = "Specific Command Info"
            commR = self.bot.get_command(command)
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
                
                embed.add_field(name = prefix + str(commR), value = f"{helpMessage}\n\nAlias/es: {aliases}\nBelongs to: **{commCat}**")
        try:
            await ctx.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    
    @commands.command(hidden = True, help = "Allows the user to make a suggestion.")
    async def suggest(self, ctx, *, args: Optional[str]):
        if not await user_check(ctx, self.bot):
            return

        sNum = sn_add()
        if sNum == -1:
            await ctx.send("Command failed!")
            raise CommandError("error in sn file")
        
        embed = libneko.Embed(title = f"Suggestion #{sNum}")
        embed.colour = random.randint(0, 0xffffff)
        
        if ctx.channel.id == Constants.Suggestions[0]:
            await ctx.message.delete()
            
            if args.isspace() or args == "":
                await ctx.send(f"{ctx.author.mention}, please add what to suggest!")
                return
            else:
                embed.description = f"Suggested by {ctx.author}:\n\"{args}\""
                embed.set_footer(icon_url = ctx.author.avatar_url, text = f"\"c.suggest < suggestions > \" is the command.")
                await ctx.send(f"{ctx.author.mention}, your suggestion has been added!")
                await self.bot.get_channel(Constants.Suggestions[1]).send(content = None, embed = embed)
    
    @commands.command(aliases = ("ping", ), help = "Displays the latency of the bot in milliseconds.", brief = "Displays the latency")
    async def latency(self, ctx):
        await ctx.send(f"Latency is currently at {self.bot.latency * 1000:.2f}ms.")

    @commands.command(hidden = True)
    async def test(self, ctx):
        if not (await user_check(ctx, self.bot) and Checks.is_developer(ctx, self.bot)):
            return
        
        embed = libneko.Embed(title = "test")
        embed.add_field(name = "This is YouTube:", value = "[link](https://www.youtube.com)")
        
        try:
            await ctx.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")      
    
    @commands.command(aliases = ("terminate", "turnoff", "killbot", "restart"), hidden = True, help = "Shuts down the self.bot. Optional argument ` -- nowait` skips the 15-second delay. Bot developer only.")
    async def shutdown(self, ctx, s: Optional[str]):
        if not (await user_check(ctx, self.bot) and Checks.is_developer(ctx, self.bot)):
            return

        if s != " -- nowait":
            self.bot.isShuttingDown = True
            await ctx.send("Shutting down in 15 seconds...")
            await self.bot.change_presence(status = discord.Status.dnd, activity = discord.Game("Project Cynical (Shutting down...)"))
            await asyncio.sleep(15)

        await self.bot.change_presence(status = discord.Status.offline)
        await ctx.send("Project Cynical has been terminated.")
        print("Project Cynical has logged out of Discord.")
        await self.bot.logout()

    @commands.command(aliases = ("cl", ), help = "Shows the changelog of the self.bot. Page number is optional. Defaults to the latest version of the self.bot.\nArguments: [\"oldest\" / page number]", brief = "Shows the changelog.")
    async def changelog(self, ctx, *, pageNum: Optional[Converters.SafeInt]):
        if not await user_check(ctx, self.bot):
            return

        embed = libneko.Embed()
        embed.colour = random.randint(0, 0xffffff)
    
        maxPage = len(self.bot.changelogContents)
    
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
        
        embed.description = self.bot.changelogContents[pageNum]
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
        
        try:
            await ctx.send(content = None, embed = embed)
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")

    @commands.group(name = "leaderboards", aliases = ("leaderboard", "lb"), help = "Displays the leaderboards of Top 15 in either the Creosphere's MEE6 leaderboard, or the high scores leaderboard.", brief = "Display the leaderboards.", invoke_without_command = True)
    async def leaderboard_group(self, ctx, tp: Optional[str]):
        if not await user_check(ctx, self.bot):
            return
        
        await ctx.send(f"{ctx.author.mention}, please select a leaderboard. It can be `MEE6` or `highscores` (case-insensitive).")
    
    @leaderboard_group.command(name = "scores")
    async def sub_highscores(self, ctx):
        if not await user_check(ctx, self.bot):
            return
        
        embed = await battles.get_scores(self.bot, self.bot.eco, ctx.author)
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        
        try:
            await ctx.send(content = f"{ctx.author.mention}", embed = embed)
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    
    @leaderboard_group.command(name = "mee6")
    async def sub_mee6(self, ctx, args: Optional[str]):
        if not await user_check(ctx, self.bot):
            return
        
        if self.bot.noMEE6:
            await ctx.send("MEE6 Leaderboards is disabled!")
            return
        
        leaderboard = self.bot.leaderboards
            
        user_details = {}
        for page in leaderboard:
            for player in page['players']:
                if int(player['id']) == ctx.author.id:
                    user_details = player
                    
        try:
            user_level = user_details["level"]
        except:
            user_level = 0
            
        try:
            user_xp = user_details["xp"]
        except:
            user_xp = 0
        
        try:
            user_mc = user_details["message_count"]
        except:
            user_mc = 0
            
        user_name = ctx.author
        user_rank = "∅"
        user_position = 0
        user_league = "Unranked"
        
        level_range = range(100)
        xp_range = [0, 1889250]
        league = "Unranked"
        
        if user_level >= 100:
            user_league = league = "Ionosphere"
        elif user_level >= 65:
            user_league = league = "Exosphere"
        elif user_level >= 45:
            user_league = league = "Thermosphere"
        elif user_level >= 25:
            user_league = league = "Mesosphere"
        elif user_level >= 15:
            user_league = league = "Stratosphere"
        elif user_level >= 5:
            user_league = league = "Troposphere"
        else:
            user_league = league = "Unranked"
            
        user_rank = rank_prefix[league]
        
        if type(args) is str:
            try:
                if args.lower() in ["exosphere", "exo", "65"]:
                    args = "exosphere"
                elif args.lower() in ["ionosphere", "iono", "100"]:
                    args = "ionosphere"
                elif args.lower() in ["thermosphere", "thermo", "45"]:
                    args = "thermosphere"
                elif args.lower() in ["stratosphere", "strato", "15"]:
                    args = "stratosphere"
                elif args.lower() in ["mesosphere", "meso", "25"]:
                    args = "mesosphere"
                elif args.lower() in ["troposphere", "tropo", "5"]:
                    args = "troposphere"
                elif args.lower() in ["unranked", "sphere", "0"]:
                    args = "unranked"

                if args.title() != league:
                    league = args.title()
                else:
                    args = None
            except KeyError:
                args = None

        level_range = level_ranges[league]
        xp_range = xp_ranges[league]

        league_players = []
        top15_players = []
        iterate = 0

        for page in leaderboard:
            for players in page["players"]:
                if players["level"] in level_range:
                    league_players.append(players)

        if len(league_players) <= 0:
            if league == "Unranked":
                await ctx.send(f"There are no members in Creosphere who are Unranked, which is practically impossible.")
            else:
                await ctx.send(f"There are no members in Creosphere who are in the {league} League.")

            return

        for player in league_players:
            if iterate >= 15:
                break
            else:
                top15_players.append(player)
                iterate += 1
                
        embed = libneko.Embed(title = "MEE6 Leaderboards - Creosphere")
        embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Invoked by {ctx.author}")
        embed.colour = random.randint(0, 0xffffff)
        embed.set_thumbnail(url = f"https://cdn.discordapp.com/icons/{leaderboard[0]['guild']['id']}/{leaderboard[0]['guild']['icon']}.gif?size=1024")
        value = ""

        iterate = 1
            
        if xp_range[1] == -1:
            exp_range = f"{number_format(xp_range[0])}+ XP"
        else:
            exp_range = f"{number_format(xp_range[0])} - {number_format(xp_range[1] - 1)} XP"

        for player in top15_players:
            value += f"{iterate}. **{player['username']}#{player['discriminator']}**"

            if iterate == 1:
                value += " :crown:"
            elif len(top15_players) >= 15:
                if iterate <= 3:
                    value += " :sparkles:"
                elif iterate <= 5:
                    value += " :star2:"
                elif iterate <= 7:
                    value += " :star:"
            elif len(top15_players) >= 10:
                if iterate <= 2:
                    value += " :sparkles:"
                elif iterate <= 3:
                    value += " :star2:"
                elif iterate <= 5:
                    value += " :star:"
            elif len(top15_players) >= 6:
                if iterate <= 2:
                    value += " :sparkles:"
                elif iterate <= 3:
                    value += " :star2:"
                elif iterate <= 4:
                    value += " :star:"
            elif len(top15_players) == 5:
                if iterate <= 2:
                    value += " :star2:"
                elif iterate <= 3:
                    value += " :star:"

            value += f": Level {player['level']} ({number_format(player['xp'])} XP / {number_format(player['message_count'])} Messages)\n"

            iterate += 1

        if level_range == range(0, 5):
            embed.add_field(name = f"Top {iterate - 1} -  Unranked ({exp_range}):", value = value)
        else:
            embed.add_field(name = f"Top {iterate - 1} - {league} League ({exp_range}):", value = value)

        description = f"**Full Server Leaderboard**: [Creosphere]({leaderboard[0]['guild']['leaderboard_url']})\n\n"

        if user_league != league:
            league_players = []
            level_range = level_ranges[user_league]

            for page in leaderboard:
                for players in page["players"]:
                    if players["level"] in level_range:
                        league_players.append(players)
                        
        try:
            user_position = league_players.index(user_details) + 1
        except:
            user_position = len(league_players) + 1

        if user_league != league:
            if user_league != "Unranked":
                description += f"**Your Ranking** ({user_league} League):\n{user_rank}-"
            else:
                description += f"**Your Ranking** ({user_league}):\n{user_rank}-"
        else:
            description += "**Your Ranking**:\n"

        if user_position == 1:
            description += f"{user_position}. **{user_name}** :crown:: Level {user_level} ({number_format(user_xp)} XP / {number_format(user_mc)} Messages)"
        else:
            description += f"{user_position}. **{user_name}**: Level {user_level} ({number_format(user_xp)} XP / {number_format(user_mc)} Messages)"
        
        embed.description = description
        
        try:
            await ctx.send(content = f"{ctx.author.mention}", embed = embed)
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention}, the bot is unable to send the requested data! Please grant the bot the \"Embed Links\" permission or ask an admin / moderator to do so.")
    