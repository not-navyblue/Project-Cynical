import discord
from discord.errors import NotFound
from discord.ext.commands.errors import NoPrivateMessage
import cardDefines as cards
import random
import constants

class Battle:
    def __init__(self, channelID: int, fighters: list):
        random.seed(random.randint(-10737418240, 10737418235))
        
        self.channelID = channelID
        
        self.isBattling = False
        self.endBattle = False
        self.fighters = fighters
        self.winner = None
        self.winNum = -1
        self.consecutivePass = 0
        self.playerCards = [[], []] # Deck of usable Cards
        self.lastUsedCard = [None, None]
        self.playerBannedCards = [list(), list()] # Card name, Length of ban (-1 means until the end of battle)
        self.playerStatus = [["none", 0], ["none", 0]] # Status, Duration (0 means none, -1 means until certain conditions occur)
        # "none" - Normal; "protected" - Protect; "protected2" - Psychic Protect; "protected3" - Banishing Shield
        # "poisoned" - Poison; "blocked" - Blocked
        self.playerStats = [[100, 100, 100, 100], [100, 100, 100, 100]] # Attack, Defense, Accuracy, Evasion
        self.playerChainLevel = [0, 0] # For the Cards "Chain" and "Chain Breaker"
        self.playerHP = [200, 200]
        self.playerEnergy = [10, 10]
        self.playerLimitBreak = [False, False] # Did user break its limits?
        self.playerUsedJS = [False, False] # Did user use Jump Scare?
        self.playerUsedProtect = [False, False] # Did user use Protect or Psychic Protect?
        self.playerUsedMute = [False, False] # Did user use Mute?
        self.playerHasHealed = [False, False] # Did user heal?
        self.playerRevival = [False, False] # Is user Revivable?
        self.playerFlinched = [False, False] # Did user flinch?
        self.pHPDeduct = ["0", "0"]
        self.pEnergyDeduct = ["0", "0"]
                                         # set 1  #  # set 2  #  # set 3  #  # set 4  #
        self.playerTurn = random.choice([0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1])
        self.turns = 1
        
        self.outcome = "The battle has just begun!"
        
    def setStatus(self, playerNum: int, status: list):
        self.playerStatus[playerNum] = status

def initBattle(battle: Battle):
    random.seed(random.randint(-10737418240, 10737418235))
    
    regularCardChance = 90 # Chances that a player will get a non-Special Card.
    x = ""; doesNotExist = True; z = 0
    battle.playerTurn = random.randint(0, 1)
    battle.isBattling = True
    SpecialCards1 = []
    
    offC = 0
    defC = 0
    supC = 0
    misC = 0
    classif = list()
    
    for a in cards.SpecialCards_:
        if a == None:
            pass
        else:
            SpecialCards1.append(a)
    
    while not (offC > 0 and defC > 0 and misC > 0):
        offC = 0
        defC = 0
        supC = 0
        misC = 0
        classif = list()
    
        battle.playerCards[0] = [None, None, None, None, None, None, None, None, None]
        
        for a in cards.SpecialCards:
            if battle.fighters[0].id == cards.SpecialCards[a].originalUser:
                battle.playerCards[0][z] = a
                z += 1
            
                classif = cards.SpecialCards[a].classification.split(",", 1)
                
                if "offensive" in classif:
                    offC += 1
                if "defensive" in classif:
                    defC += 1
                if "support" in classif:
                    supC += 1
                if "miscellaneous" in classif:
                    misC += 1
            
        while battle.playerCards[0][8] == None:
            if random.randint(1, 100) <= regularCardChance:
                while doesNotExist:
                    x = random.choice(cards.UniversalCards)
                
                    for y in battle.playerCards[0]:
                        if y == x:
                            doesNotExist = False
                            break
                        
                        if y == None:
                            battle.playerCards[0][z] = x
                            doesNotExist = False
                            z += 1
                        
                            classif = cards.NormalCards[x].classification.split(",", 1)
                
                            if "offensive" in classif:
                                offC += 1
                            if "defensive" in classif:
                                defC += 1
                            if "support" in classif:
                                supC += 1
                            if "miscellaneous" in classif:
                                misC += 1
                        
                            break
                doesNotExist = True
            else:
                while doesNotExist:
                    x = random.choice(SpecialCards1)

                    for y in battle.playerCards[0]:
                        if y == x:
                            doesNotExist = False
                            break
                        
                        if y == None:
                            battle.playerCards[0][z] = x
                            doesNotExist = False
                            z += 1
                        
                            classif = cards.SpecialCards[x].classification.split(",", 1)
                
                            if "offensive" in classif:
                                offC += 1
                            if "defensive" in classif:
                                defC += 1
                            if "support" in classif:
                                supC += 1
                            if "miscellaneous" in classif:
                                misC += 1
                        
                            break
                doesNotExist = True
    
    z = 0
    
    offC = 0
    defC = 0
    supC = 0
    misC = 0
    classif = list()
    
    while not (offC > 0 and defC > 0 and misC > 0):
        offC = 0
        defC = 0
        supC = 0
        misC = 0
        classif = list()
        
        battle.playerCards[1] = [None, None, None, None, None, None, None, None, None]
        
        for a in cards.SpecialCards:
            if battle.fighters[1].id == cards.SpecialCards[a].originalUser:
                battle.playerCards[1][z] = a
                z += 1
                
                classif = cards.SpecialCards[a].classification.split(",", 1)
                
                if "offensive" in classif:
                    offC += 1
                if "defensive" in classif:
                    defC += 1
                if "support" in classif:
                    supC += 1
                if "miscellaneous" in classif:
                    misC += 1
            
        while battle.playerCards[1][8] == None:
            if random.randint(1, 100) <= regularCardChance:
                while doesNotExist:
                    x = random.choice(cards.UniversalCards)
                
                    for y in battle.playerCards[1]:
                        if y == x:
                            doesNotExist = False
                            break
                        
                        if y == None:
                            battle.playerCards[1][z] = x
                            doesNotExist = False
                            z += 1
                        
                            classif = cards.NormalCards[x].classification.split(",", 1)
                
                            if "offensive" in classif:
                                offC += 1
                            if "defensive" in classif:
                                defC += 1
                            if "support" in classif:
                                supC += 1
                            if "miscellaneous" in classif:
                                misC += 1
                        
                            break
                doesNotExist = True
            else:
                while doesNotExist:
                    x = random.choice(SpecialCards1)

                    for y in battle.playerCards[1]:
                        if y == x:
                            doesNotExist = False
                            break
                        
                        if y == None:
                            battle.playerCards[1][z] = x
                            doesNotExist = False
                            z += 1
                        
                            classif = cards.SpecialCards[x].classification.split(",", 1)
                
                            if "offensive" in classif:
                                offC += 1
                            if "defensive" in classif:
                                defC += 1
                            if "support" in classif:
                                supC += 1
                            if "miscellaneous" in classif:
                                misC += 1
                        
                            break
                doesNotExist = True
            
    z = 0

def displayBattle(battle: Battle):
    playerStatusDisplay = ["None", "None"]
    
    a = 0
    b = 1
    while a < 2:
        if a == 0:
            b = 1
        elif a == 1:
            b = 0
            
        if battle.playerStatus[a][0] == "poison":
            playerStatusDisplay[a] = "Poisoned"
        elif battle.playerStatus[a][0] == "blocked":
            playerStatusDisplay[a] = "Blocked"
        elif battle.playerStatus[a][0] == "protected":
            playerStatusDisplay[a] = "Protected (**Protection**)"
        elif battle.playerStatus[a][0] == "protected2":
            playerStatusDisplay[a] = "Protected (**Psyched Protection**)"
        elif battle.playerStatus[a][0] == "protected3":
            playerStatusDisplay[a] = "Protected (**Disabling Aura**)"
        elif battle.playerStatus[a][0] == "none":
            playerStatusDisplay[a] = "OK"
        else:
            playerStatusDisplay[a] = "Error"
        
        if battle.playerRevival[a]:
            playerStatusDisplay[a] += "+"
        
        if battle.playerFlinched[a]:
            playerStatusDisplay[a] += ", Flinched"
            
        if battle.playerStatus[a][0] == "dead":
            playerStatusDisplay[a] = "Defeated"
            battle.endBattle = True
            battle.winner = battle.fighters[b]
            battle.winNum = b
            battle.outcome += f"\n-> {battle.fighters[a].display_name} ({battle.fighters[a]}) " + random.choice(["was defeated in battle!", "got too tired and collapsed!", "couldn't handle it anymore and called for a time out!", "died!"])
        elif battle.playerStatus[a][0] == "surrendered":
            playerStatusDisplay[a] = "Defeated (Surrendered)"
            battle.endBattle = True
            battle.winner = battle.fighters[b]
            battle.winNum = b
            battle.outcome = f"-> {battle.fighters[a].display_name} ({battle.fighters[a]}) has " + random.choice(["surrendered", "retreated", "resigned", "given up"]) + "!"
        
        if battle.playerStatus[a] == ["blocked", 0]:
            battle.playerStatus[a] = ["none", 0]
            
        if battle.playerFlinched[a]:
            battle.playerFlinched[a] = False
            
        a += 1
    
    a = 0 
    
    if battle.consecutivePass >= 4:
        battle.endBattle = True
        battle.outcome += "\n-> The battle has automatically ended!"
    
    embed = discord.Embed(title = f"Card Battle (Turn {battle.turns // 2 + 1} [Total: {battle.turns}])")
    embed.colour = random.randint(0, 0xffffff)
    
    while a < 2:
        value = f"**HP**: {battle.playerHP[a]} / 200 ({battle.pHPDeduct[a]} HP)\n**Energy**: {battle.playerEnergy[a]} / 10 Energy ({battle.pEnergyDeduct[a]} Energy)\n**Status**: {playerStatusDisplay[a]}\n"
        value += "**Cards on Deck**:\n"
        
        isBanned = False
        z = 1
        for x in battle.playerCards[a]:
            if x == battle.playerCards[a][8]:
                break
            
            if len(battle.playerBannedCards[a]) > 0:
                for y in battle.playerBannedCards[a]:
                    if y == None:
                        pass
                    elif y[0] == x:
                        value += f"~~[{z}] {x}~~, ".title()
                        isBanned = True
            
            if not isBanned:
                value += f"**[{z}]** {x}, ".title()
            
            z += 1
            isBanned = False
            
        if len(battle.playerBannedCards[a]) > 0:
            for x in battle.playerBannedCards[a]:
                if x[0] == battle.playerCards[a][8]:
                    if x[1] == -1 or x[1] > 0:
                        value += f"~~[{z}] {battle.playerCards[a][7]}~~".title()
                        isBanned = True
                    else:
                        battle.playerBannedCards.remove(x)
                    
        if not isBanned:
            value += f"**[{z}]** {battle.playerCards[a][8]}".title()
        
        if "limit break" in battle.playerCards[a]:
            value += "\n**Limit Break**: "
            
            if battle.playerLimitBreak[a]:
                value += "Active"
            else:
                value += "Inactive"
        
        embed.add_field(name = f"Player {a + 1}: {battle.fighters[a].display_name} ({battle.fighters[a]})", value = value)
        a += 1
    
    embed.description = "**Previous Turn's Outcome:**\n" + battle.outcome
    
    return embed

def checkIfValid(card, battle: Battle):
    valid = False
    if card == "pass":
        return False
    
    if type(card) is int:
        deckNum = int(card)
        if deckNum < 1 or deckNum > 9:
            return "out of bounds"
        else:
            card = battle.playerCards[battle.playerTurn][deckNum - 1].lower()
    
    for x in battle.playerCards[battle.playerTurn]:
        if card == x:
            if len(battle.playerBannedCards[battle.playerTurn]) > 0:
                a = 0
                for y in battle.playerBannedCards[battle.playerTurn]:
                    if y[a] == card:
                        return False
                    a += 1

                valid = True
            else:
                valid = True
        else:
            valid = False
        
        if valid:
            break
    
    if valid:
        s = 0
        if cards.AllCards[card].id == 1002:
            if cards.AllCards[card].originalUser == battle.fighters[battle.playerTurn].id:
                s = 7
            else:
                s = cards.AllCards[card].energycost
        else:
            s = cards.AllCards[card].energycost
        
        if battle.playerEnergy[battle.playerTurn] - s >= 0:
            return valid
        else:
            return "no energy"
    else:
        return valid

def what_happens(used: str, battle: Battle):
    cardUsed = cards.AllCards[used]
    cardSpecial = cardUsed.isSpecial
    cardID = cardUsed.id
    cardOU = 0
    dpTurn = int()
    battle.pHPDeduct = ["0", "0"]
    battle.pEnergyDeduct = ["0", "0"]
    battle.turns += 1
    pTurn = battle.playerTurn
    noUse = False
    damage = 0
    pHPDtemp = 0
    
    if pTurn == 0:
        dpTurn = 1
    elif pTurn == 1:
        dpTurn = 0
    else:
        return
    
    if battle.playerEnergy[dpTurn] < 10:
        energyplus = random.choice([1, 1, 1, 1, 1, 1, 1, 2, 2, 3])
        battle.playerEnergy[dpTurn] += energyplus
        
        if energyplus > 1:
            if energyplus == 2:
                battle.pEnergyDeduct[dpTurn] = "+2"
            elif energyplus == 3:
                battle.pEnergyDeduct[dpTurn] = "+3"
            
            if battle.playerEnergy[dpTurn] > 10:
                battle.playerEnergy[dpTurn] = 10
        else:
            battle.pEnergyDeduct[dpTurn] = "+1"
    
    battle.outcome = f"=> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** used the Card \"**{cardUsed.name}**\"!"
    
    if used != "restore":
        battle.lastUsedCard[pTurn] = used
    
    if not cardUsed.appliesToSelf and (battle.playerStatus[dpTurn][0] == "protected3" and battle.playerStatus[dpTurn][1] > 0):
        if cardID != 1002:
            battle.playerEnergy[pTurn] -= cardUsed.energycost
            battle.pEnergyDeduct[pTurn] = f"{-cardUsed.energycost}"
        
            battle.playerStatus[dpTurn] = ["none", 0]
            battle.playerBannedCards[pTurn].append([used, -1])

            noUse = True
            battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s **Disabling Aura** has been triggered, causing **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s {used.title()} to fail and be permanently Disabled!"
        
    # Reminder: Attack, Defense, Accuracy, Evasion; Status, Turns Left
    # Minimum/Maximum: 20 - 200 (Attack/Defense) / 50 - 150 (Accuracy/Evasion)
    if not cardSpecial and cardID != 1000 and not noUse:
        battle.playerEnergy[pTurn] -= cardUsed.energycost
        battle.pEnergyDeduct[pTurn] = f"{-cardUsed.energycost}"
        accu = 100
        
        if battle.playerUsedJS[pTurn] and cardID == 4:
            battle.outcome += "\n-> The Card failed because it was attempted to be used in succession!"
            noUse = True
        elif used == "early assault" and battle.turns >= 12:
            battle.outcome += "\n-> It is too late to use this Card now!"
            noUse = True
        elif battle.playerHasHealed[pTurn] and cardID == 7:
            accu = int(accuracyCalc(int(cardUsed.accuracy * 0.75), battle.playerStats[pTurn][2], battle.playerStats[dpTurn][3], cardUsed.appliesToSelf))
        elif battle.playerUsedMute[pTurn] and cardID == 9:
            accu = int(accuracyCalc(int(cardUsed.accuracy * 0.25), battle.playerStats[pTurn][2], battle.playerStats[dpTurn][3], cardUsed.appliesToSelf))
        else:
            accu = int(accuracyCalc(cardUsed.accuracy, battle.playerStats[pTurn][2], battle.playerStats[dpTurn][3], cardUsed.appliesToSelf))

        if random.randint(1, 100) <= accu and not noUse:
            if cardID == 0: # Punch
                if battle.playerStatus[dpTurn][0] != "protected" and battle.playerStatus[dpTurn][0] != "protected2":
                    if normal_criticalHitChance():
                        damage = damageCalc(cardUsed.power * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                        battle.outcome += "\n-> **Critical hit!**"
                    else:
                        damage = damageCalc(cardUsed.power, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    
                    battle.playerHP[dpTurn] -= damage
                    pHPDtemp -= damage
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** punched **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** in the {random.choice(['face', 'gut', 'chest'])} and dealt {damage} HP damage!"
                    del damage
                else:
                    if battle.playerStatus[dpTurn][0] == "protected":
                        if normal_criticalHitChance():
                            damage = damageCalc(cardUsed.power * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                            battle.outcome += "\n-> **Critical hit!**"
                        else:
                            damage = damageCalc(cardUsed.power, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                        
                        battle.playerHP[dpTurn] -= int(damage - damage * 0.85)
                        pHPDtemp -= int(damage - damage * 0.85)
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** punched **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** in the {random.choice(['face', 'gut', 'chest'])}, but **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s **Protect** reduced the damage and it dealt {damage} HP damage!"
                        del damage
                    elif battle.playerStatus[dpTurn] == "protected2":
                        battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
            
            elif cardID == 1: # Super Punch
                if battle.playerStatus[dpTurn][0] != "protected" and battle.playerStatus[dpTurn][0] != "protected2":
                    if increased_criticalHitChance():
                        damage = damageCalc(cardUsed.power * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                        battle.outcome += "\n-> **Critical hit!**"
                    else:
                        damage = damageCalc(cardUsed.power, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    
                    battle.playerHP[dpTurn] -= damage
                    pHPDtemp -= damage
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** gathered power in their fists and punched **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** in the {random.choice(['face', 'gut', 'chest'])}, dealing a whopping {damage} HP damage!"
                    del damage
                else:
                    if battle.playerStatus[dpTurn][0] == "protected":
                        if increased_criticalHitChance():
                            damage = damageCalc(cardUsed.power * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                            battle.outcome += "\n-> **Critical hit!**"
                        else:
                            damage = damageCalc(cardUsed.power, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                            
                        battle.playerHP[dpTurn] -= int(damage - damage * 0.85)
                        pHPDtemp -= int(damage - damage * 0.85)
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** attacked with a powerful punch against **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** in the {random.choice(['face', 'gut', 'chest'])}, but **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s **Protect** reduced the damage and it dealt {damage} HP damage!"
                        del damage
                    elif battle.playerStatus[dpTurn][0] == "protected2":
                        battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
                
            elif cardID == 2: # Splash
                battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** splashed a glass of water towards **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s face!"
                if random.randint(1, 100) <= 66:
                    if random.randint(1, 2) == 1 and battle.playerStatus[dpTurn][0] != "blocked": # 1 is Flinch; 2 is 1 HP damage
                        battle.playerFlinched[dpTurn] = True
                    else:
                        battle.playerHP[dpTurn] -= 1
                        pHPDtemp -= 1
                        battle.outcome += f" **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** was damaged by 1 HP!"
                else:
                    battle.outcome += " But nothing happened."
                    
            elif cardID == 3: # Double Slap
                willFlinch = False
                if normal_criticalHitChance():
                    damage = damageCalc(cardUsed.power * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    battle.outcome += "\n-> **Critical hit!**"
                else:
                    damage = damageCalc(cardUsed.power, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    
                for a in battle.playerHP:
                    a = a # lol
                    
                    if battle.playerStatus[dpTurn][0] != "protected" and battle.playerStatus[dpTurn][0] != "protected2":
                        battle.playerHP[dpTurn] -= damage
                        pHPDtemp -= damage
                    else:
                        if battle.playerStatus[dpTurn][0] == "protected":
                            battle.playerHP[dpTurn] -= int(damage - damage * 0.85)
                            pHPDtemp -= int(damage - damage * 0.85)
                        elif battle.playerStatus[dpTurn][0] == "protected2":
                            battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
                            break
                    
                    if random.randint(1, 100) <= 25 and battle.playerStatus[dpTurn][0] != "blocked":
                        willFlinch = True
                        
                if battle.playerStatus[dpTurn][0] != "protected" and battle.playerStatus[dpTurn][0] != "protected2":
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** got slapped in the face twice by **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** dealing {damage} HP of damage each slap!"
                elif battle.playerStatus[dpTurn][0] == "protected":
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** got slapped in the face twice by **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**, but **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s **Protection** effect reduced the damage and it only dealt {damage} HP damage per slap!"

                if willFlinch:
                    battle.playerFlinched[dpTurn] = True
            
                del willFlinch
                
            elif cardID == 4: # Jump Scare
                if battle.playerUsedJS[pTurn]: # deprecated
                    battle.outcome += "\n-> The Card failed because it was attempted to be used in succession!"
                else:
                    if battle.playerStatus[dpTurn][0] != "protected" and battle.playerStatus[dpTurn][0] != "protected2":
                        if battle.playerUsedJS[pTurn]: # deprecated
                            battle.outcome += "\n-> The Card failed due to a prior use of this Card!"
                        else:
                            if battle.playerStats[dpTurn][2] <= 50 or (battle.playerStats[dpTurn][3] >= 150 and not battle.playerLimitBreak[pTurn]):
                                battle.outcome += f"\n-> The Card failed because **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** can no longer have its stats changed!"
                            elif battle.playerStatus[dpTurn][0] == "blocked":
                                battle.outcome += f"\-> nThe Card failed because **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** was already Blocked!"
                            else:
                                battle.playerFlinched[dpTurn] = True
                                battle.playerUsedJS[pTurn] = True
                            
                                battle.playerStats[dpTurn][2] -= 5
                                if battle.playerStats[dpTurn][2] < 50:
                                    battle.playerStats[dpTurn][2] = 50
                            
                                battle.playerStats[dpTurn][3] += 10
                                if battle.playerStats[dpTurn][3] > 150 and not battle.playerLimitBreak[dpTurn]:
                                    battle.playerStats[dpTurn][3] = 150
                        
                                battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** suddenly jumpscared the heck out of **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** without warning!\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s Accuracy and Evasion changed by -5% and +10% respectively!"
                    else:
                        battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from being jumpscared!"
                    
            elif cardID == 5: # Potion of Invisibility
                if battle.playerStats[pTurn][3] >= 150 and not battle.playerLimitBreak[pTurn]:
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Evasion stat can no longer be increased further!"
                else:
                    battle.playerStats[pTurn][3] += 10
                    
                    if battle.playerStats[pTurn][3] > 150 and not battle.playerLimitBreak[pTurn]:
                        battle.playerStats[pTurn][3] = 150
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** drank a Potion of Invisibility and increased their Evasion stat by 5%!"

            elif cardID == 6: # Poison Target
                if battle.playerStatus[dpTurn][0] == "poison":
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** is already currently poisoned!"
                elif battle.playerStatus[dpTurn][0] == "blocked" or battle.playerStatus[dpTurn][0] == "protected" or battle.playerStatus[dpTurn][0] == "protected2":
                    battle.outcome += f"\nThe Card failed to work because of **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s status overpowering it!"
                else:
                    turns = random.randint(2, 5)
                    battle.playerStatus[dpTurn] = ["poison", turns]
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** consumed a poisoned "+ random.choice(["hamburger", "soda", "spaghetti", "sandwich", "slice of cake", "candy", "water", "garlic bread", "hotdog"]) + f" that was given by **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** and got poisoned for {turns} turns!"
        
            elif cardID == 7: # Healing Potion
                if battle.playerHP[pTurn] >= 200:
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** cannot heal anymore because their HP is full!"
                else:
                    battle.playerHP[pTurn] += (200 * 0.45)
                    battle.playerHasHealed[pTurn] = True
                    
                    if battle.playerHP[pTurn] > 200:
                        battle.playerHP[pTurn] = 200
                
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** drank the Healing Potion™ and was healed by 40% the maximum HP!"
                
                    if battle.playerStatus[pTurn][0] == "poison":
                        if random.randint(1, 100) <= 30:
                            battle.playerStatus[pTurn] == ["none", 0]
                            battle.pHPDeduct[pTurn] = "+60"
                            battle.outcome += f" The potion also cured **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** of their poisoning!"
                    else:
                        battle.pHPDeduct[pTurn] = "+60"
                        battle.outcome += f" The potion also cured **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** of their poisoning!"
            
            elif cardID == 8: # Warn
                if battle.playerStatus[dpTurn][0] == "blocked" or battle.playerStatus[dpTurn][0] == "protected" or battle.playerStatus[dpTurn][0] == "protected2":
                    battle.outcome += f"\nThe Card failed to work because of **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s status overpowering it!"
                else:
                    battle.playerStatus[dpTurn] = ["blocked", 2]
                    
                    battle.outcome += f"\n!warn {battle.fighters[dpTurn].mention} the The"
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** warned **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**, preventing them from using any Card for 2 turns!"
            
            elif cardID == 9: # Mute
                if battle.lastUsedCard[dpTurn] == None:
                    battle.outcome += f"\n-> The Card failed to work because {battle.fighters[dpTurn].display_name} (Battler {dpTurn + 1}) hasn't used a Card at least once!"
                else:
                    battle.playerUsedMute[pTurn] = True
                    randomDuration = random.randint(2, 5)
                    
                    battle.playerBannedCards[dpTurn].append([battle.lastUsedCard[dpTurn], randomDuration])
                    
                    battle.outcome += f"\n!tempmute {battle.fighters[dpTurn].mention} {randomDuration}d the The"
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** has muted **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**, disabling their Card \"{battle.lastUsedCard[dpTurn].title()}\", preventing them from using it for {randomDuration} turns!"
            
            elif cardID == 10: # Ban
                if battle.lastUsedCard[dpTurn] == None:
                    battle.outcome += f"\n-> The Card failed to work because {battle.fighters[dpTurn].display_name} (Battler {dpTurn + 1}) hasn't used a Card at least once!"
                elif "protected" in battle.playerStatus[dpTurn][0]:
                    battle.outcome += f"\n-> {battle.fighters[dpTurn].display_name} (Battler {dpTurn + 1}) protected themselves from the effects of the Card!"
                else:
                    battle.playerFlinched[dpTurn] = True
                    
                    battle.playerBannedCards[dpTurn].append([battle.lastUsedCard[dpTurn], -1])
                    battle.playerBannedCards[pTurn].append(["ban", -1])
            
                battle.outcome += f"\n!ban {battle.fighters[dpTurn].mention} the The"
                battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** has banned **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**, leaving them unable to move for one turn and disabling their Card {battle.lastUsedCard[dpTurn].title()} for use for the rest of the battle! This Card is also now disabled for use for the same duration."

            elif cardID == 11: # Push
                if battle.playerStatus[dpTurn][0] == "protected2":
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
                else:
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** pushed **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** "
                    
                    if random.randint(1, 100) <= 50:
                        damage = damageCalc(random.randint(20, 50), battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    
                        battle.playerHP[dpTurn] -= damage
                        pHPDtemp -= damage
                        
                        battle.outcome += f"on the edge of a cliff and fell, sustaining {damage} HP damage!"
                    else:
                        battle.outcome += f"but nothing happened!"
            
            elif cardID == 12: # Early Assault
                if battle.playerStatus[dpTurn][0] == "protected2":
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
                else:
                    if battle.turns > 4 and battle.turns < 8:
                        if normal_criticalHitChance():
                            damage = damageCalc(cardUsed.power * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                            battle.outcome += "\n-> **Critical hit!**"
                        else:
                            damage = damageCalc(cardUsed.power, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    elif battle.turns <= 4:
                        if normal_criticalHitChance():
                            damage = damageCalc((cardUsed.power * 2) * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                            battle.outcome += "\n-> **Critical hit!**"
                        else:
                            damage = damageCalc((cardUsed.power * 2), battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    elif battle.turns >= 8:
                        if normal_criticalHitChance():
                            damage = damageCalc((cardUsed.power * 0.5) * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                            battle.outcome += "\n-> **Critical hit!**"
                        else:
                            damage = damageCalc((cardUsed.power * 0.5), battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                    
                    if battle.playerStatus[dpTurn][0] == "protected":
                        damage *= 0.15
                        battle.playerHP -= damage
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** immediately attacked **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**, but **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s **Protection** reduced the damage and it only dealt {damage} HP damage!"
                    else:
                        battle.playerHP -= damage
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** immediately attacked **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**, which dealt {damage} HP damage!"

                    pHPDtemp -= damage
                    
            elif cardID == 13: # Snipe Shot
                if battle.playerStatus[dpTurn][0] == "protected2":
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
                else:
                    if normal_criticalHitChance():
                        damage = damageCalc(cardUsed.power * 2, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                        battle.outcome += "\n-> **Critical hit!**"
                    else:
                        damage = damageCalc(cardUsed.power, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                        
                        
                    part = ""
                    
                    if damage >= 60:
                        part = random.choice(["head", "chest", "genitals"])
                    elif damage >= 35 and damage < 60:
                        part = random.choice(["chest", random.choice(["left", "right"]) + "arm"])
                    else:
                        part = random.choice(["left", "right"]) + random.choice(["leg", "foot"])
                    
                    if battle.playerStatus[dpTurn][0] == "protected":
                        damage *= 0.15
                        battle.playerHP -= damage
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** shot **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** in the {part}, but **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s **Protection** reduced the damage and it only dealt {damage} HP damage!"
                    else:
                        battle.playerHP -= damage
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** shot **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** in the {part}, which dealt {damage} HP damage!"
                    
                    pHPDtemp -= damage
                    
            elif cardID == 14: # Chain
                if battle.playerStats[pTurn][1] < 200 or battle.playerLimitBreak[pTurn]:
                    battle.playerStats[pTurn][1] += 10
                    battle.playerChainLevel[pTurn] += 1
                    
                    if battle.playerStats[pTurn][1] > 200 and not battle.playerLimitBreak[pTurn]:
                        battle.playerStats[pTurn][1] = 200
                        
                    if battle.playerChainLevel[pTurn] == 1:
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** started a chain! Their Chain Level is currently at Level {battle.playerChainLevel[pTurn]}!"
                    else:
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** extended their chain! Their Chain Level is currently at Level {battle.playerChainLevel[pTurn]}!"
                else:
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s stats can no longer be increased!"
            
            elif cardID == 15: # Chain Breaker
                if battle.playerChainLevel[dpTurn] > 0:
                    if battle.playerStatus[dpTurn][0] == "protected2":
                        battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
                    else:
                        if normal_criticalHitChance():
                            damage = damageCalc(cardUsed.power * (battle.playerChainLevel[dpTurn] * 0.75) * 1.5, battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])
                            battle.outcome += "\n-> **Critical hit!**"
                        else:
                            damage = damageCalc(cardUsed.power * (battle.playerChainLevel[dpTurn] * 0.75), battle.playerStats[pTurn][0], battle.playerStats[dpTurn][1])

                        battle.playerStats[dpTurn][1] -= 10 * battle.playerChainLevel[dpTurn]
                        battle.playerChainLevel[dpTurn] = 0
                        
                        crack = random.choice(["broke", "shattered", "ruined", "messed up"])
                        
                        if battle.playerStatus[dpTurn][0] == "protected":
                            damage *= 0.15
                            battle.playerHP -= damage
                            battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** {crack} **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s Chain! Their **Protection** reduced the damage and it only dealt {damage} HP damage!"
                        else:
                            battle.playerHP -= damage
                            battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** {crack} **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s Chain, dealing {damage} HP damage!"

                        pHPDtemp -= damage
                        battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s Chain has been reset and their Defense has been reduced!"
                else:
                    battle.outcome += f"\n-> The Card failed to work because the target has no active chain!"
            
            elif cardID == 16: # Revival
                if battle.playerRevival[pTurn]:
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s **Revivable** status is already active!"
                else:
                    battle.playerRevival[pTurn] = True
                    
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** has performed a ritual, allowing them to be revived on the verge of death!\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s **Revivable** status is now active!"
            
            elif cardID == 17: # Fissure
                if battle.playerStatus[dpTurn][0] == "protected2":
                    battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** protected themself from the attack!"
                else:
                    if battle.playerStatus[dpTurn][0] == "protected":
                        pHPDtemp -= (battle.playerHP[dpTurn] - 1)
                        battle.playerHP[dpTurn] = 1
                        battle.outcome += f"\n-> The ground beneath **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** has cracked open! They fell, and survived with only 1 HP left!"
                    else:
                        pHPDtemp -= battle.playerHP[dpTurn]
                        battle.playerHP[dpTurn] = 0
                        battle.outcome += f"\n-> The ground beneath **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** has cracked open! They fell and die within the chasm!"
            
            elif cardID == 18: # Protect
                if battle.playerStatus[pTurn][0] == "none":
                    battle.playerStatus[pTurn] = ["protected", 1]
                    
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** invoked a **Protection** status effect, protecting themselves for one turn!"
                else:
                    battle.outcome += f"\n-> The Card failed to work because the user has an active status effect!"
            
            elif cardID == 19: # Banishing Shield
                if battle.lastUsedCard[pTurn] == None or battle.lastUsedCard[dpTurn] == None:
                    battle.outcome += "\n-> The Card failed to work because both player have not used a Card once!"
                elif battle.playerStatus[pTurn][0] != "none":
                    battle.outcome += "\n-> The Card failed to work because the user has an active status effect!"
                else:
                    battle.playerStatus[pTurn] = ["protected3", 2]
                    battle.playerBannedCards[pTurn].append(["banishing shield", -1])
                    
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** projected an aura that will disable any Card that will target them!"
            
        elif not noUse:
            battle.outcome += "\n-> The Card failed the accuracy check and missed!"
    elif cardSpecial and cardID != 1000 and not noUse:
        cardOU = cardUsed.originalUser
        
        if cardID == 1001: # Psychic Protect
            battle.playerEnergy[pTurn] -= cardUsed.energycost
            battle.pEnergyDeduct[pTurn] = f"{-cardUsed.energycost}"
            accu = 0
                    
            if cardOU == battle.fighters[pTurn].id: # navyblue's Effect
                if battle.playerUsedProtect[pTurn]:
                    accu = accuracyCalc(35, battle.playerStats[pTurn][2], 100, cardUsed.appliesToSelf)
                else:
                    accu = accuracyCalc(70, battle.playerStats[pTurn][2], 100, cardUsed.appliesToSelf)
                    
                if random.randint(1, 100) <= accu:
                    if battle.playerStatus[pTurn][0] == "poison":
                        battle.playerStatus[pTurn] = ["protected2", 1]
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Card cured them of poisoning and protected themself for 1 turn!"
                    elif battle.playerStatus[pTurn][0] == "protected" or battle.playerStatus[pTurn][0] == "protected2":
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s **Protection** is still in effect!"
                    else:
                        battle.playerStatus[pTurn] = ["protected2", 2]
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** protected themself for 2 turns!"
                else:
                    battle.outcome += "\nThe Card failed the accuracy check and missed!"
            else: # Normal User's Effect
                if battle.playerUsedProtect[pTurn]:
                    accuracyCalc(int(cardUsed.accuracy / 2), battle.playerStats[pTurn][2], 100, cardUsed.appliesToSelf)
                else:
                    accuracyCalc(cardUsed.accuracy, battle.playerStats[pTurn][2], 100, cardUsed.appliesToSelf)
                
                if random.randint(1, 100) <= accu:
                    if battle.playerStatus[pTurn][0] == "poison":
                        battle.outcome += "\n-> The Card failed to work due to a status effect overpowering it!"
                    elif battle.playerStatus[pTurn][0] == "protected" or battle.playerStatus[pTurn][0] == "protected2":
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s **Protection** is still in effect!"
                    else:
                        battle.playerStatus[pTurn] = ["protected2", 1]
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** protected themself for 1 turn!"
                else:
                    battle.outcome += "\n-> The Card failed the accuracy check and missed!"
        
        elif cardID == 1002: # The Ban Hammer
            if cardOU == battle.fighters[pTurn].id: # theAstra's Effect
                battle.playerEnergy[pTurn] -= 7
                battle.pEnergyDeduct[pTurn] = f"-7"
                if random.randint(1, 100) <= accuracyCalc(55, battle.playerStats[pTurn][2], battle.playerStats[pTurn][3]):
                    if battle.playerStatus[dpTurn][0] != "protected2":
                        pHPDtemp -= battle.playerHP[dpTurn]
                        battle.playerHP[dpTurn] = 0
                        
                        if battle.playerRevival[dpTurn]:
                            battle.playerRevival[dpTurn] = False
                            
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** " + random.choice(["delivered their verdict", "grasped the deadliest hammer", "took control of the ultimate weapon", "made their final decision"]) + f" and hit **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** with **The Ban Hammer**, which effectively " + random.choice(["decimated", "annihilated", "banished", "destroyed", "defeated", "erased"]) + " them!"
                    else:
                        if random.randint(1, 100) <= 25:
                            pHPDtemp -= battle.playerHP[dpTurn]
                            battle.playerHP[dpTurn] = 0
                            
                            battle.playerStatus[dpTurn] = ["none", 0]
                            if battle.playerRevival[dpTurn]:
                                battle.playerRevival[dpTurn] = False
                            
                            battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** " + random.choice(["delivered their verdict", "grasped the deadliest hammer", "took control of the ultimate weapon", "made their final decision"]) + f" and hit **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** with **The Ban Hammer**, which effectively " + random.choice(["decimated", "annihilated", "banished", "destroyed", "defeated", "erased"]) + " them!"
                        else:
                            battle.outcome += f"\n-> A mysterious protective power channelling through **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s essence protected them from the grasp of **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s **The Ban Hammer**!"
                
                            if battle.playerStats[pTurn][2] >= 150:
                                pass
                            else:
                                battle.playerStats[pTurn][2] += 10
                        
                                if battle.playerStats[pTurn][2] > 150 and not battle.playerLimitBreak[pTurn]:
                                    battle.playerStats[pTurn][2] = 150
                            
                                battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Accuracy Stat increased by 10%!"
                else:
                    battle.outcome += "\n-> The Card failed the accuracy check and missed!"
                    
                    if battle.playerStats[pTurn][2] >= 150:
                        pass
                    else:
                        battle.playerStats[pTurn][2] += 10
                        
                        if battle.playerStats[pTurn][2] > 150 and not battle.playerLimitBreak[pTurn]:
                            battle.playerStats[pTurn][2] = 150
                            
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Accuracy Stat increased by 10%!"
            else: # Normal User's Effect
                battle.playerEnergy[pTurn] -= cardUsed.energycost
                battle.pEnergyDeduct[pTurn] = f"{-cardUsed.energycost}"
                    
                if random.randint(1, 100) <= accuracyCalc(cardUsed.accuracy, battle.playerStats[pTurn][2], battle.playerStats[pTurn][3]):
                    if battle.playerStatus[dpTurn][0] != "protected2":
                        pHPDtemp -= battle.playerHP[dpTurn]
                        battle.playerHP[dpTurn] = 0
                        
                        if battle.playerRevival[dpTurn]:
                            battle.playerRevival[dpTurn] = False
                            
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** " + random.choice(["delivered their verdict", "grasped the deadliest hammer", "took control of the ultimate weapon", "made their final decision"]) + f" and hit **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** with **The Ban Hammer**, which effectively " + random.choice(["decimated", "annihilated", "banished", "destroyed", "defeated", "erased"]) + " them!"
                    else:
                        if random.randint(1, 100) <= 25:
                            pHPDtemp -= battle.playerHP[dpTurn]
                            battle.playerHP[dpTurn] = 0
                            
                            battle.playerStatus[dpTurn] = ["none", 0]
                            if battle.playerRevival[dpTurn]:
                                battle.playerRevival[dpTurn] = False
                                
                            battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** " + random.choice(["delivered their verdict", "grasped the deadliest hammer", "took control of the ultimate weapon", "made their final decision"]) + f" and hit **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** with **The Ban Hammer**, which effectively " + random.choice(["decimated", "annihilated", "banished", "destroyed", "defeated", "erased"]) + " them!"
                        else:
                            battle.outcome += f"\n-> A mysterious protective power channelling through **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})**'s essence protected them from the grasp of **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s **The Ban Hammer**!"
                            
                            if battle.playerStats[pTurn][2] >= 150:
                                pass
                            else:
                                battle.playerStats[pTurn][2] += 5
                        
                                if battle.playerStats[pTurn][2] > 150 and not battle.playerLimitBreak[pTurn]:
                                    battle.playerStats[pTurn][2] = 150
                            
                                battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Accuracy Stat increased by 5%!"
                else:
                    battle.outcome += "\n-> The Card failed the accuracy check and missed!"
                    
                    if battle.playerStats[pTurn][2] >= 150:
                        pass
                    else:
                        battle.playerStats[pTurn][2] += 5
                        
                        if battle.playerStats[pTurn][2] > 150 and not battle.playerLimitBreak[pTurn]:
                            battle.playerStats[pTurn][2] = 150
                            
                        battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Accuracy Stat increased by 5%!"
    
        elif cardID == 1003: # The Eclipse
            battle.playerEnergy[pTurn] -= cardUsed.energycost
            battle.pEnergyDeduct[pTurn] = f"{-cardUsed.energycost}"
            accu = 1
            
            if battle.playerHasHealed[pTurn]:
                accu = accuracyCalc(int(cardUsed.accuracy * 0.75), battle.playerStats[pTurn][2], battle.playerStats[dpTurn][3])
            else:
                accu = accuracyCalc(cardUsed.accuracy, battle.playerStats[pTurn][2], battle.playerStats[dpTurn][3])
            
            if random.randint(1, 100) <= accu:
                if battle.playerStats[dpTurn][2] <= 50 or battle.playerStats[pTurn][2] <= 50:
                    battle.outcome += "\n-> One of the players' accuracy can no longer be reduced further!"
                else:
                    battle.outcome += "\n-> The eclipse has occurred and darkness spreads! "
                    
                    if cardOU == battle.fighters[pTurn].id: # SanskariHydra's Effect
                        battle.playerStats[dpTurn][2] -= 30
                        battle.playerStats[pTurn][2] -= 10
                    
                        if battle.playerStats[dpTurn][2] < 50:
                            battle.playerStats[dpTurn][2] = 50
                        
                        if battle.playerStats[pTurn][2] < 50:
                            battle.playerStats[pTurn][2] = 50
                        
                        battle.playerHP[pTurn] += int(200 * 0.75)
                        battle.playerHasHealed[pTurn] = True
                    
                        if battle.playerHP[pTurn] > 200:
                            battle.playerHP[pTurn] = 200
                            
                        battle.outcome += f"-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** and **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Accuracy stats were reduced by 30% and 10%, respectively. **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** also healed by 70% the maximum HP!"
                    else: # Normal User's Effect
                        battle.playerStats[dpTurn][2] -= 25
                        battle.playerStats[pTurn][2] -= 15
                    
                        if battle.playerStats[dpTurn][2] < 50:
                            battle.playerStats[dpTurn][2] = 50
                        
                        if battle.playerStats[pTurn][2] < 50:
                            battle.playerStats[pTurn][2] = 50
                        
                        battle.playerHP[pTurn] += int(200 * 0.4)
                        battle.playerHasHealed[pTurn] = True
                    
                        if battle.playerHP[pTurn] > 200:
                            battle.playerHP[pTurn] = 200
                            
                        battle.outcome += f"-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** and **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s Accuracy stats were reduced by 25% and 15%, respectively. **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** also healed by 35% the maximum HP!"
            else:
                battle.outcome += "\n-> The Card failed the accuracy check and missed!"
                
        elif cardID == 1004: # Guard Break
            battle.playerEnergy[pTurn] -= cardUsed.energycost
            battle.pEnergyDeduct[pTurn] = f"{-cardUsed.energycost}"
            
            if random.randint(1, 100) <= accuracyCalc(cardUsed.accuracy, battle.playerStats[pTurn][2], 100, cardUsed.appliesToSelf):
                if battle.playerStats[pTurn][1] <= 20 or (battle.playerStats[pTurn][3] >= 150 and not battle.playerLimitBreak[pTurn]):
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s stats cannot be lowered or raised any further!"
                else:
                    battle.playerStats[pTurn][1] -= 75
                    battle.playerStats[pTurn][3] += 150
                    
                    if battle.playerStats[pTurn][1] < 20:
                        battle.playerStats[pTurn] = 20
                    
                    if battle.playerStats[pTurn][3] > 150  and not battle.playerLimitBreak[pTurn]:
                        battle.playerStats[pTurn] = 150
                        
                    battle.playerBannedCards[pTurn].append(["guard break", -1])
                    
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** broke their guard, maximizing their Evasion but harshly lowering their Defense!"
            else:
                battle.outcome += "\n-> The Card failed the accuracy check and missed!"
                
        elif cardID == 1005: # Limit Break
            if battle.lastUsedCard[pTurn] != None:
                battle.playerEnergy[pTurn] -= cardUsed.energycost
                battle.pEnergyDeduct[pTurn] = f"{-cardUsed.energycost}"
            
                if random.randint(1, 100) <= accuracyCalc(cardUsed.accuracy, battle.playerStats[pTurn][2], 100, cardUsed.appliesToSelf):
                    battle.playerLimitBreak[pTurn] = True        
                    battle.playerBannedCards[pTurn].append(["limit break", -1])
                    
                    battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** broke their limit, unlocking their true potential!"
                else:
                    battle.outcome += "\n-> The Card failed the accuracy check and missed!"
            else:
                battle.outcome += "\n-> The Card failed to work!"
                    
    elif used == "restore" and not noUse: # 50% - 1 E; 20% - 2 E; 15% - 3 E; 10% - 4 E; 5% - 5 E
        if battle.playerEnergy[pTurn] < 10:
            energyplus = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5])
            battle.playerEnergy[pTurn] += energyplus
            battle.pEnergyDeduct[pTurn] = f"+{energyplus}"
            
            if energyplus > 1:
                if battle.playerEnergy[pTurn] > 10:
                    battle.playerEnergy[pTurn] = 10
        
        battle.outcome = f"-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** "+ random.choice(["decided to rest!", "decided to take a break for a short time!", "wants to chill down for now!", "bolstered up their morale!"]) + "\n-> **Energy has been restored.**"
    
    if cardID != 4:
        battle.playerUsedJS[pTurn] = False
        
    if not (cardID == 7 or cardID == 1003):
        battle.playerHasHealed[pTurn] = False
        
    if cardID != 9:
        battle.playerUsedMute[pTurn] = False
        
    if cardID == 1001 or cardID == 18:
        battle.playerUsedProtect[pTurn] = True
    else:
        battle.playerUsedProtect[pTurn] = False
    
    a = 0
    while a < 2:
        if len(battle.playerBannedCards[a]) > 0:
            for b in battle.playerBannedCards[a]:
                if b[1] == -1:
                    pass
                else:
                    b[1] -= 1
        
        a += 1
    
    if battle.playerHP[dpTurn] <= 0:
        battle.playerHP[dpTurn] = 0
        if battle.playerRevival[dpTurn]:
            battle.playerRevival[dpTurn] = False
            battle.playerHP[dpTurn] = 100
            pHPDtemp += 100
            battle.outcome += f"\n-> {battle.fighters[dpTurn]}'s **Revival** took effect and revived them from their death!"
        else:
            battle.playerStatus[dpTurn][0] = "dead"
            battle.pHPDeduct[dpTurn] = f"{pHPDtemp}"
            battle.endBattle = True
            return
    
    if "protected" in battle.playerStatus[dpTurn][0]:
        battle.playerStatus[dpTurn][1] -= 1
        if battle.playerStatus[dpTurn][1] <= 0:
            battle.playerStatus[dpTurn] = ["none", 0]
            
    if battle.playerStatus[pTurn][0] == "poison":
        if battle.playerStatus[pTurn][1] - 1 <= 0:
            battle.playerHP[pTurn] -= int(200 * 0.05)
            battle.playerStatus[pTurn] = ["none", 0]
            battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** lost 5% HP due to poisoning!\n-> ****{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})**'s poisoning has been cured.**"
        else:
            battle.playerStatus[pTurn][1] -= 1
            battle.playerHP[pTurn] -= int(200 * 0.05)
            battle.outcome += f"\n-> **{battle.fighters[pTurn].display_name} ({battle.fighters[pTurn]})** lost 5% HP due to poisoning!"
            
        if battle.playerHP[pTurn] <= 0:
            if battle.playerRevival[pTurn]:
                battle.playerRevival[pTurn] = False
                battle.playerHP[pTurn] = 75
                battle.pHPDeduct[pTurn] = f"+75"
                battle.outcome += f"\n-> {battle.fighters[dpTurn]}'s **Revival** took effect and revived them from their death!"
            else:
                battle.playerStatus[pTurn] = ["dead", 0]
                battle.pHPDeduct[pTurn] = f"-{int(200 * 0.05)}"
            return
        else:
            if battle.playerHasHealed[pTurn]:
                if cardID == 7:
                    battle.pHPDeduct[pTurn] = f"+{60 - int(200 * 0.05)}"
                elif cardID == 1003:
                    if cardOU == battle.fighters[pTurn].id:
                        battle.pHPDeduct[pTurn] = f"+{int(200 * 0.7) - int(200 * 0.05)}"
                    else:
                        battle.pHPDeduct[pTurn] = f"+{int(200 * 0.35) - int(200 * 0.05)}"
                        
            else:
                battle.pHPDeduct[pTurn] = f"-{int(200 * 0.05)}"
            
    if pHPDtemp > 0:
        battle.pHPDeduct[dpTurn] = f"+{pHPDtemp}"
    else:
        battle.pHPDeduct[dpTurn] = f"{pHPDtemp}"
        
    if battle.playerFlinched[dpTurn] or battle.playerStatus[dpTurn][0] == "blocked":
        if battle.playerFlinched[dpTurn]:
            battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** flinched and couldn't move!"
        else:
            battle.outcome += f"\n-> **{battle.fighters[dpTurn].display_name} ({battle.fighters[dpTurn]})** couldn't use any Card and skipped a turn!"
            battle.playerStatus[dpTurn][1] -= 1
    else:
        if pTurn == 0:
            battle.playerTurn = 1
        elif pTurn == 1:
            battle.playerTurn = 0
            
    return
            

def damageCalc(power: int, attack: int, defense: int):
    return int(power * (attack / defense) * random.uniform(0.85, 1.15))

def accuracyCalc(accuracyC: int, accuracyP: int, evasion: int, self: bool = False):
    if self:
        accuracy = int(accuracyC * (accuracyP / 100) * random.uniform(0.95, 1.05))
    else:
        accuracy = int(accuracyC * (accuracyP / evasion) * random.uniform(0.95, 1.05))
        
    if accuracy > 100:
        return 100
    elif accuracy < 10:
        return 10
    else:
        return accuracy
    
def normal_criticalHitChance():
    return random.randint(0, 100) <= 20

def increased_criticalHitChance():
    return random.randint(0, 100) <= 40

def setHighScore(number: int, battle: Battle, changeScore: int = 1):
    f = open(constants.CurrentDirectory + "/data/highscores.mhjson", "r", encoding = "utf-8")
    lis = []
    lis2 = list()
    lis3 = list()
    
    for g in f.readlines():
        if g != "{\n" and g != "}":
            lis3 = g.replace("\t", "").replace("\n", "")
            lis.append(lis3.split(": ", 1))
        else:
            lis.append(g)
    del lis3
    f.close()
    
    for l in lis:
        if l != "{\n" and l != "}":
            l = [int(l[0]), int(l[1])]
        lis2.append(l)
    lis = lis2
    del lis2
    
    y = 0
    stri = ""
    isFound = False
    
    for x in lis:
        if x == "}":
            if isFound:
                stri += "}"
            else:
                stri += f"\t{changeScore}: {battle.fighters[number].id}\n" + "}"
        elif x == "{\n":
            stri += "{\n"
        else:
            if x[1] == battle.fighters[number].id:
                lis[y][0] = x[0] + changeScore
                stri += f"\t{lis[y][0]}: {lis[y][1]}\n"
                isFound = True
        y += 1
        
    f = open(constants.CurrentDirectory + "/data/highscores.mhjson", "w", encoding = "utf-8")
    f.write(stri)
    f.close()
    return

async def getHighScores(client: discord.Client, requested: discord.User):
    lis = []
    embed = discord.Embed(title = "CCGbot High Scores")
    f = open(constants.CurrentDirectory + "/data/highscores.mhjson", "r", encoding = "utf-8")
    
    for g in f.readlines():
        if g != "{\n" and g != "}":
            lis2 = g.replace("\n", "").replace("\t", "")
            lis2 = lis2.split(": ", 1)
            lis2[0] = int(lis2[0])
            lis.append(lis2)
            
    mergeSort(lis)
    lis.reverse()
    
    for x in lis:
        x[1] = int(x[1])
    
    num = 1
    s = ""
    
    for profile in lis:
        if num > 10:
            break
        else:
            try:
                s += f"{num}. <@{profile[1]}> ({await client.fetch_user(profile[1])}): {profile[0]} win/s\n"
            except NotFound:
                s += f"{num}. <@{profile[1]}> ([MissingUser]): {profile[0]} win/s\n"
            num += 1
    
    t = ""
    num = 1
    for profile in lis:
        if profile[1] == requested.id:
            try:
                t = f"{num}. <@{profile[1]}> ({await client.fetch_user(profile[1])}): {profile[0]} win/s\n"
                break
            except NotFound:
                t = f"{num}. <@{profile[1]}> ([MissingUser]): {profile[0]} win/s\n"
                break
        
        num += 1
        
    if t == "":
        t = f"{num}. {requested.mention} ({requested}): 0 win/s\n"
    
    embed.add_field(name = "Top 10 Scores", value = s)
    embed.add_field(name = "Your Score:", value = t)
    return embed
    
def mergeSort(arr):
    if len(arr) > 1:
        
        r = len(arr)//2
        leftArr = arr[:r]
        rightArr = arr[r:]
        
        mergeSort(leftArr)
        mergeSort(rightArr)
        
        i = j = k = 0
        while i < len(leftArr) and j < len(rightArr):
            if leftArr[i] < rightArr[j]:
                arr[k] = leftArr[i]
                i += 1
            else:
                arr[k] = rightArr[j]
                j += 1
            k += 1

        while i < len(leftArr):
            arr[k] = leftArr[i]
            i += 1
            k += 1
            
        while j < len(rightArr):
            arr[k] = rightArr[j]
            j += 1
            k += 1
