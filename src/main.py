from deck import Deck;         import os
from hand import Hand;         import time
import leaderboard

cooldown = 60
user, auth = leaderboard.get_user()

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
            bet = float(input(f"What's your bet (You have ${money})? "))
        except:
            print("Not a valid number")
        else:
            bet = round(bet*100)/100
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

            print(leaderboard.update(money))

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
