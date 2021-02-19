import os

UserIDs = {
    "navyblue": 448141184544669716,
    "theAstra": 461410812838281227, 
    "SanskariHydra": 607953377674002463
}

# In order: devServer, Creosphere, testServer
ServerIDs = [789340106233741372, 667327481191333909, 798763455888752651]
# In order: #suggestions-box, #suggestions-list
Suggestions = [806807107646783509, 802117618931859456]

EmoteIndex = {
    "stroke": 0,
    "sick": 1
}

isAlpha = False

level_ranges = {
    "Unranked": range(0, 5), 
    "Troposphere": range(5, 15), 
    "Stratosphere": range(15, 25), 
    "Mesosphere": range(25, 45), 
    "Thermosphere": range(45, 65), 
    "Exosphere": range(65, 100), 
    "Ionosphere": range(100, 2147483648)
}

rank_prefix = {
    "Unranked": "∅", 
    "Troposphere": "Tr", 
    "Stratosphere": "S", 
    "Mesosphere": "M", 
    "Thermosphere": "Th", 
    "Exosphere": "E", 
    "Ionosphere": "I"
}

xp_ranges = {
    "Unranked": [0, 1150], 
    "Troposphere": [1150, 11825], 
    "Stratosphere": [11825, 42000], 
    "Mesosphere": [42000, 200850], 
    "Thermosphere": [200850, 557700], 
    "Exosphere": [557700, 1899250], 
    "Ionosphere": [1899250, -1]
}

bot_mention = {
    True: "<@803859581045309480> ", 
    False: "<@790506033784029195> "
}

CurrentDirectory = os.getcwd()

add = lambda a, b = 1: a + b
subtract = lambda a, b = 1: a - b

number_suffix = {
    1000: "k",
    1000000: "M", 
    1000000000: "B",
    1000000000000: "T",
    1000000000000000: "q",
    1000000000000000000: "Q",
    1000000000000000000000: "s",
    1000000000000000000000000: "S",
    1000000000000000000000000000: "O",
    1000000000000000000000000000000: "N",
    1000000000000000000000000000000000: "D",
    1000000000000000000000000000000000000: "Udc",
    1000000000000000000000000000000000000000: "Ddc",
    1000000000000000000000000000000000000000000: "Tdc",
    1000000000000000000000000000000000000000000000: "qdc",
    1000000000000000000000000000000000000000000000000: "Qdc"
}

def number_format(number: float):
    dividend = 1000
    suffix = number_suffix[dividend]
    
    if number <= 999 and number >= -999:
        return "{:.2f}".format(number)
    
    while True:
        divided = number / dividend
        
        if (divided >= 1 and divided < 1000) or (divided <= -1 and divided > -1000):
            return "{:.2f}{}".format(divided, suffix)
        else:
            try:
                dividend *= 1000
                suffix = number_suffix[dividend]
            except KeyError:
                raise ValueError("value is unsupported: {}".format(number))
