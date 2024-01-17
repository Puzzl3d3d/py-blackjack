# DECK
from random import shuffle
SUITS = ("Diamonds", "Hearts", "Spades", "Clubs")
CARDS = ("A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K")
DECK = []
for suit in SUITS:
    for card in CARDS:
        DECK.append([suit, card])
class Deck:
    def __init__(self, shoe_size=6):
        self.shoe = []
        self.discards = []
        for _ in range(shoe_size):
            self.shoe = [*self.shoe, *DECK]
    def __str__(self):
        return self.shoe
    
    def check_shoe(self):
        if len(self.shoe) == 0:
            self.shuffle()
        
    def shuffle(self):
        self.shoe = [*self.shoe, *self.discards]
        self.discards = []
        shuffle(self.shoe)
    def draw(self):
        self.check_shoe()
        card = self.shoe.pop(0)
        self.discards.append(card)
        return card


# CARD RENDERER
import os

os.system('' if os.name == 'nt' else 'color')
os.system('cls' if os.name == 'nt' else 'clear')

card = """
┌────────┐
│ {:<2}   {} │
│        │
│        │
│        │
│ {}   {:>2} │
└────────┘
"""

suitColours = {
    "Hearts": "\033[91m{}\033[00m",
    "Diamonds": "\033[91m{}\033[00m",
    "Clubs": "{}",
    "Spades": "{}"
}
suitEmojis = {"Hearts": "♥", "Clubs": "♣", "Diamonds": "♦", "Spades": "♠"}

def combineStrings(str1, str2, *args, spacing="  ", suit1="Spades", suit2="Spades"):
    combined = ""
    str1 = str1.split("\n")
    str2 = str2.split("\n")

    for i in range(max(len(str1), len(str2))):
        line1 = str1[i] if i < len(str1) else ""
        line2 = str2[i] if i < len(str2) else ""
        combined += f"{suitColours[suit1].format(line1)}{spacing}{suitColours[suit2].format(line2)}\n"
    return combined

def getCardDisplay(suit, value):
    if suit is None or value is None:
        card_back = """
┌────────┐
│╱╲╱╲╱╲╱╲│
│╲╱╲╱╲╱╲╱│
│        │
│╱╲╱╲╱╲╱╲│
│╲╱╲╱╲╱╲╱│
└────────┘
"""
        return card_back
    else:
        value_str = {10: "10", 11: "A", 12: "J", 13: "Q", 14: "K"}.get(value, str(value))
        suitEmoji = suitEmojis[suit]
        return suitColours[suit].format(card.format(value_str, suitEmoji, suitEmoji, value_str))


# HAND
class Hand:
    def __init__(self):
        self.hand = []
    def __str__(self):
        combined = "\n\n\n\n\n\n\n\n"
        for card in self.hand:
            if card == []:
                combined = combineStrings(combined, getCardDisplay(None, None), suit2="Spades") # default as spades for no reason whatsoever
            else:
                combined = combineStrings(combined, getCardDisplay(*card), suit2=card[0])
        return combined
    def __int__(self):
        return self.calculate()

    def add_card(self, card):
        self.hand.append(card)
        return self
    def calculate(self):
        numAces = 0
        hand = 0

        for card in self.hand:
            if card == []: continue
            _suit, value = card
            if value == "A":
                numAces += 1
                continue
            elif isinstance(value, str):
                value = 10
            hand += value

        for _i in range(numAces):
            if hand + 11 > 21:
                hand += 1
            else:
                hand += 11

        return hand
    def reset(self):
        hand = self.hand
        self.hand = []
        return hand
    def can_split(self):
        if len(self.hand) != 2: return
        card1, card2 = self.hand
        return card1[1] == card2[1] or (isinstance(card1[1], str) and isinstance(card2[1], str))
    def split(self):
        if self.can_split():
            return Hand().add_card(self.hand[0]), Hand().add_card(self.hand[-1])


# LEADERBOARD
from urllib import request, parse
import json

base_url = "https://flask.puzzl3d.dev"
api = "/blackjack"
data_endpoint = "/data"
top_endpoint = "/top"

username = None

class leaderboard:
    @staticmethod
    def get_user():
        global username
        if not os.path.exists("session"):
            with open("session", "w") as file:
                username = input("Username: ")
                file.write(username)
        else:
            with open("session", "r") as file:
                username = file.read().split("\n")[0].strip()
        return username
    @staticmethod
    def get_top():
        try:
            with request.urlopen(f"{base_url}{api}{top_endpoint}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            print("ERROR |",e)
            return {}
    @staticmethod
    def get_data():
        try:
            with request.urlopen(f"{base_url}{api}{data_endpoint}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            return f"An error occurred: {e}"
    @staticmethod
    def get_self_data():
        query_params = parse.urlencode({'name': username or leaderboard.get_user()})
        try:
            with request.urlopen(f"{base_url}{api}{data_endpoint}?{query_params}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            return f"An error occurred: {e}"
    @staticmethod
    def update(value):
        query_params = parse.urlencode({'name': username or leaderboard.get_user(), 'value': value})
        req = request.Request(f"{base_url}{api}{data_endpoint}?{query_params}", method="POST")
        try:
            with request.urlopen(req) as response:
                charset = response.headers.get_content_charset()
                return response.read().decode(charset or 'utf-8')
        except Exception as e:
            return f"An error occurred: {e}"
    @staticmethod
    def ordinal_suffix(position):
        position = int(position)
        if 10 <= position % 100 <= 20:
            suffix = 'th'
        else:
            suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
            suffix = suffixes.get(position % 10, 'th')
        return f"{position}{suffix}"

money = 100
user = leaderboard.get_user()

dealerHand = Hand()
playerHand = Hand()
shoe = Deck(shoe_size=6)
shoe.shuffle()

results = {
    "Push": 0,
    "Lose": -1,
    "Bust": -1,
    "Blackjack": 1.5,
    "Win": 1
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_top():
    data = leaderboard.get_top() or {}
    name = data.get("name", "Nobody")
    value = data.get("value", 0)
    if money > value:
        leaderboard.update(money)
        name = user
        value = money
    return name, value
def get_self_pos():
    data = leaderboard.get_data()
    sorted_data = sorted(data.keys(), key=lambda x: (-data[x].get("highest", 100), data[x].get("last_updated", 0)))
    position = sorted_data.index(user) + 1
    print(f"Your position in the leaderboard is {leaderboard.ordinal_suffix(position)} with ${data.get(user, {}).get("highest", 100)}!")
    return position, sorted_data

def get_bet():
    name,value = get_top()
    print(f"{name} is top of the leaderboard with ${value}!")
    get_self_pos()
    print
    while True:
        try:
            bet = int(input(f"What's your bet (You have ${money})? "))
        except:
            print("Not a valid number")
        else:
            if bet > money:
                print("Not enough money")
            elif bet <= 0:
                print("Too low!")
            else:
                break
    clear()
    return bet
def get_choice():

    choices = {"Hit": "h", "Stand": "s"}
    if money >= bet*2: choices["Double Down"] = "d"
    if playerHand.can_split(): choices["Split"] = "p"

    print("Pick a choice:")
    for name in choices:
        char = choices[name]
        print(f"\t[{char}]: {name}")

    while True:
        try:
            choice = input("What're you gonna do? ")
        except:
            print("Not a valid input")
        else:
            if choice not in choices.values():
                print("Not a valid choice")
            else:
                break
    return choice

def dealer():
    dealerHand.add_card(dealerHand.hidden_card)
    dealerHand.hand.pop(1)
    while dealerHand.calculate() < 17:
        dealerHand.add_card(shoe.draw())

def displayHands():
    clear()
    print(f"This game is worth ${bet}")
    print()
    print("You:")
    print(playerHand)
    print(f"Value: {playerHand.calculate()}")
    print()
    print("Dealer:")
    print(dealerHand)
    print(f"Value: {dealerHand.calculate()}")

def round():
    global bet, money
    global playerHand, dealerHand

    bet = get_bet()

    # Initialise the hands
    playerHand.reset()
    dealerHand.reset()

    playerHand.add_card(shoe.draw())
    playerHand.add_card(shoe.draw())

    dealerHand.add_card(shoe.draw())
    dealerHand.add_card([])
    dealerHand.hidden_card = shoe.draw()

    # Check for dealer blackjack
    if Hand().add_card(dealerHand.hand[0]).add_card(dealerHand.hidden_card) == 21:
        # Check for player blackjack
        if playerHand.calculate() == 21:
            return "Push"
        else:
            return "Lose"
    # Check for player blackjack
    elif playerHand.calculate() == 21:
        return "Blackjack"

    while True:
        displayHands()
        if playerHand.calculate() >= 21: break
        choice = get_choice()
        if choice == "s": # Stand
            break
        
        if choice == "p" and playerHand.can_split(): # Split
            print("Not added that yet lmao")
            continue

        if choice == "d": bet *= 2 # Double down
        if choice == "h" or choice == "d": # Hit / Double down
            playerHand.add_card(shoe.draw())
            if choice == "d": break
    
    displayHands()
    
    if playerHand.calculate() > 21:
        return "Bust"
    
    dealer()

    displayHands()

    if dealerHand.calculate() > 21:
        return "Win"
    if playerHand.calculate() == dealerHand.calculate():
        return "Push"
    elif playerHand.calculate() > dealerHand.calculate():
        return "Win"
    else:
        return "Lose"
    
if __name__ == "__main__":
    while True:
        money = 100

        while True:
            result = round()

            money += bet*results[result]

            print()
            print(f"{result}! You now have ${money}")

            print("-"*15)

            if money <= 0:
                break

        play_again = input("You ran out of money! Play again? ")
        if len(play_again) > 0 and play_again.lower()[0] == "n": break
        clear()

    print("See you again!")
