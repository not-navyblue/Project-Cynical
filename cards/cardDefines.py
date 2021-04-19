if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

from cards.cards import Card, SpecialCard
from lib.Constants import UserIDs

offensiveCards = {
    "punch": Card(0, "Punch", 15, 95, 1, "The basic attack.", "No additional effects.", "offensive"),
    "super punch": Card(1, "Super Punch", 30, 75, 3, "Deals more damage than a regular punch.", "Increased critical hit chance.", "offensive"),
    "double slap": Card(3, "Double Slap", 15, 75, 3, "\"Slap like now and subscribe!\" - a certain Italian bassist", "Hits twice. Each slap has a chance of flinching the target.", "offensive"),
    "push": Card(11, "Push", 0, 80, 4, "\"Do you believe in gravity?\" - A JoJo reference", "Has a chance of damaging the target, if the Card's accuracy check passed. Unaffected by Protection. Damage cannot be increased by critical hit.", "offensive,miscellaneous"),
    "early assault": Card(12, "Early Assault", 30, 65, 5, "(Placeholder text here.)", "The Card's base Power doubles in the first 4 total turns of the battle, and halves by Turn 8 (total). Bound to fail by Turn 12 (total) onwards.", "offensive"),
    "snipe shot": Card(13, "Snipe Shot", 35, 60, 7, "Gottem! Wait... oh.", "Increased critical hit damage.", "offensive"),
    "chain breaker": Card(15, "Chain Breaker", 15, 100, 4, "```\nUser 3: lol\nUser 4: lol\nUser 69: :le:```", "Breaks the target's chain after the move, decreasing Defense equal to target's chain level. Power is multiplied by 75% for each chain level. Fails if the target does not have a chain.", "offensive"),
    "fissure": Card(17, "Fissure", 999, 30, 8, "Cracks open the ground below the target, potentially killing them.", "No additional effects.", "offensive")
}

defensiveCards = {
    "potion of invisibility": Card(5, "Potion of Invisibility", -1, 100, 3, "Makes you invisible.", "Increases evasion by 5%.", "defensive", True),
    "chain": Card(14, "Chain", -1, 80, 3, "```\nUser 1: lol\nUser 2: lol\nUser 3: lol```", "Increases user's Defense by 10%. For each successive use, elevates chain level by 1.", "defensive", True),
    "protect": Card(18, "Protect", -1, 85, 5, "\"I protect the hooman\" - cat", "Greatly reduces an opponent's attack damage by 85%. If it's an OHKO attack, it only reduces the user's HP to 1. If it's a status-applying Card, it cancels it. Lasts one turn. Successive use halves the Card's accuracy. Fails if the user has any status effect.", "defensive", True),
    "banishing shield": Card(19, "Banishing Shield", -1, 40, 7, "!ban @target, but for self-defense", "Any Card used on the user will automatically fail and be Disabled for use for the rest of the battle. This Card can only be used once, and lasts 2 turns only. Fails if both the user and the target have not used any prior Card or when user has any status effect.", "defense,miscellaneous", True),
    "counter": Card(20, "Counter", -1, 60, 6, "no u", "Counters an opponent's attack on one turn, damaging them by 75% the damage the opposing Card dealt, with a chance of additional damage. Fails if the user has any status effect. Does not counter OHKO Cards.", "defensive,offensive", True)
}

SupportCards = {
    "poison target": Card(6, "Poison Target", -1, 70, 4, "Give them poisoned food or drink, see what happens.", "Poisons the target for 2 - 5 turns. (Target loses HP by 5% at the end of a turn.) Fails if the target has any active status effect.", "support,offensive"),
    "healing potion": Card(7, "Healing Potion", -1, 100, 2, "Buy the best, all-cure Healing Potion™ for only $69", "Heals the user by 45%. If the user is poisoned, has a chance to cure the user of poisoning. Successive use reduces the Card's accuracy by 25%.", "support", True),
    "revival": Card(16, "Revival", -1, 60, 7, "lol let's make chat alive again.", "Allows the user to revive and be healed by 50% HP should the user get KO'ed. Fails while user's **Revivable** status is active.", "support,defensive", True),
    "restore": Card(1000, "Restore", -1, 100, 0, "Wait, that's illegal", "Restores the User's energy. Alias: `c.restore`", "miscellaneous,support", True)
}

MiscCards = {
    "splash": Card(2, "Splash", -1, 80, 2, "Nothing happens... or was there?", "If the Card hits, has a chance of either flinching the target or dealing 1 HP damage to the target.", "miscellaneous"),
    "jumpscare": Card(4, "Jumpscare", -1, 80, 3, "=)", "Flinches the target. Also decreases the target's accuracy by 5%, but increases target's evasion by 10%. Fails when used in succession, when either of the target's Accuracy or Evasion can no longer be changed, or when user is currently Blocked.", "miscellaneous"),
    "warn": Card(8, "Warn", -1, 60, 5, "!warn @target", "Prevents the target from using a Card for 2 turns. (Inflicts the target with the \"Blocked\" status effect.)", "miscellaneous"),
    "mute": Card(9, "Mute", -1, 50, 6, "!tempmute @target 4d", "Forbids the target from using the previous Card again for 2 - 5 turns. Bypasses all forms of protection. Fails if the target hasn't used a Card at least once. Successive use reduces the Card's accuracy by 75%", "miscellaneous"),
    "banishing slam": Card(10, "Banishing Slam", -1, 40, 7, "!ban @target", "Disables the last Card used by the target for the duration of the whole battle, and disables this Card from being re-used by user again for the same duration. Fails if target hasn't used a Card at least once. **Does not actually deal damage.**", "miscellaneous"),
    "inversion": Card(21, "Inversion", -1, 70, 5, "Egassem a si siht", "Any stat changes to the user will be inverted for 1 - 3 turns.", "miscellaneous", True)
}

SpecialCards = {
    "psychic protect": SpecialCard(1001, "Psychic Protect", -1, 60, 6, "lmao ok.", "Fully protects the user from almost all attacks for one move. Successive use halves the Card's accuracy. Fails when the user is currently poisoned.", UserIDs["navyblue"], "Accuracy is boosted to 70% and cures poisoning. If the user is not poisoned, adds an extra turn of protection instead.", "defensive,support", True),
    "the ban hammer": SpecialCard(1002, "The Ban Hammer", 999, 30, 9, "begone.", "Guaranteed to bypass **Revival**, **Protection**, and **Disabling Aura**, and has a chance to bypass **Psyched Protection**. For each miss or fail, increase user's accuracy by 5%.", UserIDs["theAstra"], "Accuracy is boosted to 55% and Energy cost is reduced to 7 Energy. Increases user's accuracy by 10% instead if the move fails or misses.", "offensive"),
    "the eclipse": SpecialCard(1003, "The Eclipse", -1, 70, 5, "The worlds align and the eclipse falls, spreading darkness around the world.", "Reduces the accuracy of all players in battle (opponent's: 25 / user's: 15) and the user is healed by 40% the maximum HP. Successive use reduces the Card's accuracy by 25%. Fails if either player's accuracy can no longer be deducted.", UserIDs["SanskariHydra"], "Opponent's accuracy is reduced by 30 and user's accuracy is reduced by 10 instead. User's heals by double the percent any other user heals (70% instead of 35%).", "defensive,support"),
    "guard break": SpecialCard(1004, "Guard Break", -1, 100, 7, "I'm weak.", "Maximizes user's Evasion but lowers Defense by 70. Fails if user's stats cannot be lowered or raised further. Once used, this Card can no longer be used for the rest of the battle (essentially Disabling itself).", 0, "No additional effects.", "defensive,miscellaneous", True),
    "limit break": SpecialCard(1005, "Limit Break", -1, 100, 10, "UNLIMITED POWER!!!", "Breaks the maximum limit of the user's stats, but erases 50% of the user's maximum HP. Once used, this Card can no longer be used for the rest of the battle (essentially Disabling itself). Fails if the User hasn't used a prior Card or if the user has less than 50% of the maximum HP.", 0, "No additional effects.", "miscellaneous", True)
}

UniversalCards = []
FreeCards = []
SpecialCards_ = []
AllCards = dict()
NormalCards = dict()

def initUniversalCards():
    global UniversalCards
    
    # 1 - 20
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
    UniversalCards.append("banishing slam")
    UniversalCards.append("push")
    UniversalCards.append("early assault")
    UniversalCards.append("snipe shot")
    UniversalCards.append("chain")
    UniversalCards.append("chain breaker")
    UniversalCards.append("revival")
    UniversalCards.append("fissure")
    UniversalCards.append("protect")
    UniversalCards.append("banishing shield")
    
    # 21 - 40
    UniversalCards.append("counter")
    #UniversalCards.append("inversion")
    
    # 1000 should not be included. 

def init_FreeCards():
    global FreeCards
    
    UniversalCards.append("punch")
    UniversalCards.append("splash")
    UniversalCards.append("jumpscare")
    UniversalCards.append("healing potion")
    UniversalCards.append("push")
    UniversalCards.append("protect")

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
    global offensiveCards, defensiveCards, MiscCards, SpecialCards, AllCards, NormalCards
    
    NormalCards = {**offensiveCards, **defensiveCards, **SupportCards, **MiscCards}
    AllCards = {**NormalCards, **SpecialCards}
    