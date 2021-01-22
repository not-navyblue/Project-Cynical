class Card:
    """
        The core item of the bot. The one thing that allows users to fight against each other.
        
        Arguments:
            `cardID`: The ID of the Card. Must be below 1000, exclusive.
            `name`: The Card's name.
            `power`: The potency of the Card's power. Ranges from 0 to 80. -1 for Cards with no damage. 999 for OHKO Cards.
            `accuracy`: Whether the Card's effect will occur or not. Ranges from 10% to 100%. OHKO Cards are required to have 30% or less.
            `energycost`: The energy required for a Card to function. Ranges from 0 to 10.
            `description`: Text about the Card.
            `effectDesc`: Information about the Card's effects in battle.
            `appliesToSelf`: Whether it applies only to self or not. `False` by default.
    """
    def __init__(self, cardID: int, name: str, power: int, accuracy: int, energycost: int, description: str, effectDesc: str, classification: str, appliesToSelf: bool = False):
        if cardID < 1000 or (cardID == 1000 and name == "Pass"):
            self.id = cardID
        else:
            raise Exception("Illegal Card ID.")
        self.name = name
        if (power >= -1 and power <= 80) or power == 999:
            self.power = power
        else:
            raise Exception("Illegal Card power value.")   
        if self.power != 999:
            if accuracy >= 10 and accuracy <= 100:
                self.accuracy = accuracy
            else:
                raise Exception(f"Illegal Card accuracy value.")
        else:
            if accuracy >= 10 and accuracy <= 30:
                self.accuracy = accuracy
            else:
                raise Exception("Illegal Card accuracy value.")
        if energycost >= 0 and energycost <= 10:
            self.energycost = energycost
        else:
            raise Exception("Illegal Card energy cost value.")
        self.description = description
        self.effectDesc = effectDesc
        if classification in ["offensive", "defensive", "miscellaneous"]:
            self.classification = classification
        else:
            raise Exception("Illegal Card classification.")
        self.appliesToSelf = appliesToSelf
        self.isSpecial = False
      
class SpecialCard:
    """
        A variation of a generic Card which has better Card stats or effects when used by its specific Original User.
        
        Arguments:
            `cardID`: The ID of the Card. Must be above 1001, inclusive.
            `name`: The Card's name.
            `power`: The potency of the Card's power. Ranges from 0 to 80. -1 for Cards with no damage. 999 for OHKO Cards.
            `accuracy`: Whether the Card's effect will occur or not. Ranges from 10% to 100%. OHKO Cards are required to have 30% or less.
            `energycost`: The energy required for a Card to function. Ranges from 0 to 10.
            `description`: Text about the Card.
            `effectDesc`: Information about the Card's effects in battle.
            `originalUser`: The ID of the Original User.
            `originalUserDesc`: Information about the Card's effects when used by the Original User in battle.
            `appliesToSelf`: Whether it applies only to self or not. `False` by default.
    """
    def __init__(self, cardID: int, name: str, power: int, accuracy: int, energycost: int, description: str, effectDesc: str, originalUser: int, originalUserDesc: str, classification: str, appliesToSelf: bool = False):
        if cardID >= 1001:
            self.id = cardID
        else:
            raise Exception("Illegal Card ID.")
        self.name = name
        if (power >= -1 and power <= 80) or power == 999:
            self.power = power
        else:
            raise Exception("Illegal Card power value.")   
        if self.power != 999:
            if accuracy >= 10 and accuracy <= 100:
                self.accuracy = accuracy
            else:
                raise Exception(f"Illegal Card accuracy value.")
        else:
            if accuracy >= 10 and accuracy <= 30:
                self.accuracy = accuracy
            else:
                raise Exception("Illegal Card accuracy value.")
        if energycost >= 0 and energycost <= 10:
            self.energycost = energycost
        else:
            raise Exception("Illegal Card energy cost value.")
        self.description = description
        self.effectDesc = effectDesc
        self.originalUser = originalUser
        self.originalUserDesc = originalUserDesc
        if classification in ["offensive", "defensive", "miscellaneous"]:
            self.classification = classification
        else:
            raise Exception("Illegal Card classification.")
        self.appliesToSelf = appliesToSelf
        self.isSpecial = True
        