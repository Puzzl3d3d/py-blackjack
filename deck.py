from random import choice, shuffle

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

if __name__ == "__main__":
    deck = Deck()
    print(deck)
