from deck import Deck         ;import os
from hand import Hand
import leaderboard

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
