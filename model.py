class Card():

    def __init__(self, color, number, form, fill):
        self.color = color
        self.number = number
        self.form = form
        self.fill = fill

    def __str__(self):
        print(self.color, self.number, self.form, self.fill)


class Deck():

    cards: list[Card]

    def __init__(self):
        # Initialize the deck
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        card = Card(i, j, k, l)
                        self.cards.append(card)


class Game():

    deck: Deck

    def __init__(self):
        deck = Deck()