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