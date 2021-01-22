from cards import Card, SpecialCard
from constants import UserIDs

OffensiveCards = {
    "punch": Card(0, "Punch", 15, 95, 1, "The basic attack.", "No additional effects.", "offensive"),
    "super punch": Card(1, "Super Punch", 30, 75, 3, "Deals more damage than a regular punch.", "Increased critical hit chance.", "offensive"),
    "double slap": Card(3, "Double Slap", 15, 75, 3, "\"Slap like now and subscribe!\" - a certain Italian bassist", "Hits twice. Each slap has a chance of flinching the target.", "offensive"),
    "poison target": Card(6, "Poison Target", -1, 70, 4, "Give them poisoned food or drink, see what happens.", "Poisons the target for 2 - 5 turns. (Target loses HP by 5% at the end of a turn.) Fails if the target has any active status effect.", "offensive"),
    "push": Card(11, "Push", 0, 80, 4, "\"Do you believe in gravity?\" - A JoJo reference", "Has a chance of damaging the target, if the Card's accuracy check passed. Unaffected by Protect. Cannot be critical hit.", "offensive"),
    "sniper shot": Card(12, "Sniper Shot", 35, 60, 7, "Gottem! Wait... oh.", "Increased critical hit damage.", "offensive"),
    "chain breaker": Card(14, "Chain Breaker", 20, 100, 4, "```User 3: lol\nUser 4: lol\nMod: lmao no```\n", "Breaks the target's chain after the move, decreasing Defense equal to target's chain level. Power is multiplied by 50% for each chain level. Fails if the target does not have a chain.", "offensive"),
    "rupture": Card(16, "Rupture", 999, 30, 8, "Cracks open the ground below the target, potentially killing them.", "No additional effects.", "offensive")
}

DefensiveCards = {
    "potion of invisibility": Card(5, "Potion of Invisibility", -1, 100, 3, "Makes you invisible.", "Increases evasion by 5%.", "defensive", True),
    "healing potion": Card(7, "Healing Potion", -1, 100, 2, "Buy the best, all-cure Healing Potion™ for only $69", "Heals the user by 40%. If the user is poisoned, has a chance to cure the user of poisoning. Successive use reduces the Card's accuracy by 25%.", "defensive", True),
    "chain": Card(13, "Chain", -1, 90, 3, "```User 1: lol\nUser 2: lol\nUser 3: lol```\n", "Increases user's Defense by 15%. For each successive use, elevates chain level by 1.", "defensive"),
    "revival": Card(15, "Revival", -1, 60, 3, "lol let's make chat alive again.", "Allows the user to revive and be healed by 50% HP should the user get KO'ed. Fails while user's **Revivable** status is active.", "defensive"),
    "protect": Card(17, "Protect", -1, 90, 4, "\"I protect the hooman\" - cat", "Greatly reduces an opponent's attack damage by 85%. If it's an OHKO attack, it only reduces the user's HP to 1. If it's a status-applying Card, it cancels it. Successive use halves the Card's accuracy. Fails if the user is poisoned.", "defensive")
}

MiscCards = {
    "splash": Card(2, "Splash", -1, 80, 2, "Nothing happens... or was there?", "If the Card hits, has a chance of either flinching the target or dealing 1 HP damage to the target.", "miscellaneous"),
    "jumpscare": Card(4, "Jumpscare", -1, 80, 3, "You scared 'em real good, that's good.", "Flinches the target. Also decreases the target's accuracy by 5%, but increases target's evasion by 10%. Fails when used in succession, when either of the target's Accuracy or Evasion can no longer be changed, or when user is currently Blocked.", "miscellaneous"),
    "warn": Card(8, "Warn", -1, 65, 5, "!warn @target", "Prevents the target from using a Card for 2 turns. (Inflicts the target with the \"Blocked\" status effect.)", "miscellaneous"),
    "mute": Card(9, "Mute", -1, 60, 6, "!tempmute @target 4d", "Forbids the target from using the previous Card again for 2 - 5 turns. Bypasses all forms of protection. Fails if the target hasn't used a Card at least once. Successive use reduces the Card's accuracy by 75%", "miscellaneous"),
    "ban": Card(10, "Ban", -1, 55, 7, "!ban @target", "Flinches the target. Disables the last Card used by the target for the duration of the whole battle, and disables this Card from being re-used by user again for the same duration. Fails if target hasn't used a Card at least once.", "miscellaneous"),
    "pass": Card(1000, "Pass", -1, 100, 0, "Wait, that's illegal", "Skips the user's turn. Alias: `c.pass`", "miscellaneous")
}

SpecialCards = {
    "psychic protect": SpecialCard(1001, "Psychic Protect", -1, 60, 5, "lmao ok.", "Fully protects the user from all attacks for one move. Successive use halves the Card's accuracy. Fails when the user is currently poisoned.", UserIDs["navyblue"], "Accuracy is boosted to 70% and cures poisoning. If the user is not poisoned, adds an extra turn of protection instead.", "defensive", True),
    "the ban hammer": SpecialCard(1002, "The Ban Hammer", 999, 30, 9, "begone.", "Guaranteed to bypass Revival and Protect. Has a chance to bypass Psychic Protect. For each miss or fail, increase user's accuracy by 5%.", UserIDs["theAstra"], "Accuracy is boosted to 55% and Energy cost is reduced to 7 Energy. Increases user's accuracy by 10% instead if the move fails or misses.", "offensive"),
    "the eclipse": SpecialCard(1003, "The Eclipse", -1, 70, 5, "The worlds align and the eclipse falls, spreading darkness around the world.", "Reduces the accuracy of all players in battle (opponent's: 25% / user's: 15%) and the user is healed by 35% the maximum HP. Successive use reduces the Card's accuracy by 25%. Fails if either player's accuracy can no longer be deducted.", UserIDs["SanskariHydra"], "Opponent's accuracy is reduced by 30% and user's accuracy is reduced by 10% instead. User's heals by double the percent any other user heals (70% instead of 35%).", "miscellaneous"),
    "guard break": SpecialCard(1004, "Guard Break", -1, 100, 7, "I'm weak.", "Maximizes user's Evasion but lowers Defense by 75%. Fails if user's stats cannot be lowered or raised further. Once used, this Card can no longer be used for the rest of the battle (essentially Disabling itself).", 0, "No additional effects.", "miscellaneous", True),
    "limit break": SpecialCard(1005, "Limit Break", -1, 100, 10, "UNLIMITED POWER!!!", "Breaks the maximum limit of the user's stats, allowing for abnormally high stats. Once used, this Card can no longer be used for the rest of the battle (essentially Disabling itself).", 0, "No additional effects.", "miscellaneous", True)
}

UniversalCards = []
SpecialCards_ = []
AllCards = dict()
NormalCards = dict()

def initUniversalCards():
    global UniversalCards
    
    # 1 - 10
    UniversalCards.append("punch")
    UniversalCards.append("super punch")
    UniversalCards.append("splash")
    UniversalCards.append("double slap")
    UniversalCards.append("jumpscare")
    UniversalCards.append("potion of invisibility")
    UniversalCards.append("poison target")
    UniversalCards.append("healing potion")
    UniversalCards.append("warn")
    UniversalCards.append("mute")
    
    # 11 - 20
    UniversalCards.append("ban")
    UniversalCards.append("push")
    #UniversalCards.append("sniper shot")
    #UniversalCards.append("chain")
    #UniversalCards.append("chain breaker")
    #UniversalCards.append("revival")
    #UniversalCards.append("rupture")
    #UniversalCards.append("protect")
    
    # 1000 should not be included. 

def initSpecialCards():
    global SpecialCards_
    x = 0
    while x < 1001:
        SpecialCards_.append(None)
        x += 1
        
    SpecialCards_.append("psychic protect")
    SpecialCards_.append("the ban hammer")
    SpecialCards_.append("the eclipse")
    SpecialCards_.append("guard break")
    SpecialCards_.append("limit break")

def initAllCards():
    global OffensiveCards, DefensiveCards, MiscCards, SpecialCards, AllCards, NormalCards
    
    NormalCards = {**OffensiveCards, **DefensiveCards, **MiscCards}
    AllCards = {**NormalCards, **SpecialCards}
    