from card_renderer import combineStrings, getCardDisplay

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