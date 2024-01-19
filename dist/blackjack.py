# DECK
from random import shuffle

SUITS = ("Diamonds", "Hearts", "Spades", "Clubs")
CARDS = ("A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K")

# Generate a deck
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

card = """┌────────┐
│ {:<2}   {} │
│        │
│        │
│        │
│ {}   {:>2} │
└────────┘"""

suitColours = {
    "Hearts": "\033[91m{}{}\033[00m",
    "Diamonds": "\033[91m{}{}\033[00m",
    "Clubs": "{}{}\033[00m",
    "Spades": "{}{}\033[00m"
}
suitEmojis = {"Hearts": "♥", "Clubs": "♣", "Diamonds": "♦", "Spades": "♠"}

def combineStrings(str1, str2, *args, spacing="  ", suit1="Spades", suit2="Spades", bg=""):
    combined = ""
    str1 = str1.split("\n")
    str2 = str2.split("\n")

    for i in range(max(len(str1), len(str2))):
        line1 = str1[i] if i < len(str1) else ""
        line2 = str2[i] if i < len(str2) else ""
        combined += f"{suitColours[suit1].format(bg, line1)}{spacing}{suitColours[suit2].format(bg, line2)}\n"
    return combined

def getCardDisplay(suit, value):
    if suit is None or value is None:
        card_back = f"""┌────────┐
│╱╲╱╲╱╲╱╲│
│╲╱╲╱╲╱╲╱│
│        │
│╱╲╱╲╱╲╱╲│
│╲╱╲╱╲╱╲╱│
└────────┘"""
        return card_back
    else:
        value_str = {10: "10", 11: "A", 12: "J", 13: "Q", 14: "K"}.get(value, str(value))
        suitEmoji = suitEmojis[suit]
        return suitColours[suit].format("",card.format(value_str, suitEmoji, suitEmoji, value_str))
    


# HAND
class Hand:
    def __init__(self):
        self.hand = []
        self.stood = False
        self.result = None
        self.bg = ""
    def __str__(self):
        bg = self.bg or ""
        combined = "\n"*7
        for card in self.hand:
            if card == []:
                combined = combineStrings(combined, getCardDisplay(None, None), suit2="Spades", bg=bg) # default as spades for no reason whatsoever
            else:
                combined = combineStrings(combined, getCardDisplay(*card), suit2=card[0], bg=bg)

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
            return len(self.hand) == 2 and Hand().add_card(self.hand[0]), Hand().add_card(self.hand[-1])
# LEADERBOARD
from urllib import request, parse
import json

# if you wanna bomb the api, add "jared_" before it (e.g. "/blackjack/jared_data") please :)
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

import time

cooldown = 60
user = leaderboard.get_user()

dealerHand = Hand()
playerHands = [Hand()]
currentPlayerHand = 0
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
    try:
        position = sorted_data.index(user) + 1
        print(f"Your position in the leaderboard is {leaderboard.ordinal_suffix(position)} with ${data.get(user, {}).get('highest', 100)}!")
    except:
        print(f"You aren't on the leaderboard yet!")
        return None, sorted_data
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
    if playerHands[currentPlayerHand].can_split() and money >= bet*2: choices["Split"] = "p"
    if len(playerHands) > 1:
        choices["Next hand"] = "e"
        choices["Previous hand"] = "q"

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

LOCKED_BG = "\033[100m"
SELECTED_BG = "\033[104m"

def displayHands():
    clear()
    print(f"This game is worth ${bet}")
    print()
    print("You:")
    for hand in playerHands:
        if len(playerHands) > 1 and playerHands[currentPlayerHand] == hand:
            hand.bg = SELECTED_BG
        elif len(playerHands) > 1 and hand.stood or hand.result:
            hand.bg = LOCKED_BG
        else:
            hand.bg = ""
        print(hand)
        print(f"Value: {hand.calculate()}")
        print()
        print()
    print()
    print("Dealer:")
    print(dealerHand)
    print(f"Value: {dealerHand.calculate()}")

def get_result(playerHand):
    if playerHand.result: return                                  playerHand.result
    elif playerHand.calculate() > 21: return                      "Bust"
    elif dealerHand.calculate() > 21: return                      "Win"
    elif playerHand.calculate() == dealerHand.calculate(): return "Push"
    elif playerHand.calculate() > dealerHand.calculate(): return  "Win"
    else: return                                                  "Lose"

def increment_hand_index(increment):
    global currentPlayerHand
    if increment > 0:
        for i in range(len(playerHands)):
            currentPlayerHand = currentPlayerHand+1 if currentPlayerHand < len(playerHands)-1 else 0
            if not playerHands[currentPlayerHand].result and not playerHands[currentPlayerHand].stood: break
    else:
        for i in range(len(playerHands)):
            currentPlayerHand = currentPlayerHand-1 if currentPlayerHand > 0 else len(playerHands)-1
            if not  playerHands[currentPlayerHand].result and not playerHands[currentPlayerHand].stood: break
def doRound():
    global bet, money
    global playerHands, currentPlayerHand, dealerHand

    bet = get_bet()

    # Initialise the hands
    playerHands = [Hand()]
    currentPlayerHand = 0
    playerHand = playerHands[currentPlayerHand]
    dealerHand.reset()

    playerHand.add_card(shoe.draw())
    playerHand.add_card(shoe.draw())

    dealerHand.add_card(shoe.draw())
    dealerHand.add_card([])
    dealerHand.hidden_card = shoe.draw()

    # Check for dealer blackjack
    if Hand().add_card(dealerHand.hand[0]).add_card(dealerHand.hidden_card).calculate() == 21:
        # Check for player blackjack
        if playerHand.calculate() == 21:
            playerHand.result = "Push"
        else:
            playerHand.result = "Lose"
        return
    # Check for player blackjack
    elif playerHand.calculate() == 21:
        playerHand.result = "Blackjack"
        return

    while True:
        if len(playerHands) == 1 and (playerHands[0].calculate() >= 21 or playerHands[0].result or playerHands[0].stood): break
        if len(playerHands) > 1:
            numEnded = 0
            for playerHand in playerHands:
                if playerHand.result or playerHand.stood or playerHand.calculate() >= 21:
                    numEnded += 1
                    playerHand.stood = True
                    if playerHand.calculate() == 21 and len(playerHand.hand) == 2:
                        playerHand.result = "Blackjack"
            if numEnded == len(playerHands):
                break
        displayHands()

        choice = get_choice()
        playerHand = playerHands[currentPlayerHand]

        if choice == "e":
            increment_hand_index(1)
        if choice == "q":
            increment_hand_index(-1)

        if choice == "s": # Stand
            if len(playerHands) == 1: break
            playerHand.stood = True
            continue
        
        if choice == "p" and playerHand.can_split(): # Split
            original_bet = bet / len(playerHands)
            bet += original_bet

            hand1, hand2 = playerHand.split()
            hand1.add_card(shoe.draw())
            hand2.add_card(shoe.draw())
            playerHands[currentPlayerHand] = hand1
            playerHands.append(hand2)

            continue

        if choice == "d": # Double down
            original_bet = bet / len(playerHands)
            bet += original_bet
            playerHand.stood = True
        if choice == "h" or choice == "d": # Hit / Double down
            playerHand.add_card(shoe.draw())
    
    displayHands()
    
    numLosses = 0
    for playerHand in playerHands:
        if playerHand.calculate() > 21:
            playerHand.result = "Bust"
            numLosses += 1
        elif playerHand.calculate() == 21 and len(playerHand.hand) == 2:
            playerHand.result = "Blackjack"
    if numLosses == len(playerHands):
        return
    
    dealer()

    displayHands()

    for playerHand in playerHands:
        playerHand.result = get_result(playerHand)
    
if __name__ == "__main__":
    data = leaderboard.get_self_data()
    money = data.get("current", 100)
    delta = time.time() - data.get("last_updated", 0)
    if money == 0 and delta > cooldown:
        money = 100
        leaderboard.update(money)
    elif money == 0:
        while True:
            clear()
            delta = time.time() - data.get("last_updated", 0)
            if delta > cooldown: break
            else: print(f"You ran out of money! Play again in {round(cooldown-delta)} seconds")
            time.sleep(0.5)
        money = 100
        leaderboard.update(money)

    while True:
        while True:
            doRound()
            original_bet = bet / len(playerHands)

            for playerHand in playerHands:
                result = playerHand.result or "Push" # default to draw
                money += original_bet*results[result]

            leaderboard.update(money)

            print()
            if len(playerHands) == 1:
                print(f"{result}! You now have ${money}")
            else:
                i = 1
                total_result = 0
                for playerHand in playerHands:
                    return_amount = results[playerHand.result]
                    print(f"Hand {i} | {playerHand.result}! You {"kept" if return_amount==0 else ("lost" if return_amount < 0 else "gained")} ${abs(original_bet*return_amount)}!")
                    total_result += original_bet*return_amount
                    i += 1
                print(f"Overall, you {"kept" if total_result==0 else ("lost" if total_result < 0 else "gained")} ${abs(total_result)} and now have ${money}!")

            print("-"*15)

            if money <= 0:
                break

        print(f"You ran out of money! Play again in {cooldown} seconds")
        start = time.time()
        time.sleep(1)
        while True:
            clear()
            delta = time.time() - start
            if delta > cooldown: break
            else: print(f"{round(cooldown-delta)} seconds left!", end="")
            time.sleep(0.5)
        money = 100
        leaderboard.update(money)
