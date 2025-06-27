from random import shuffle

class Card():

    def __init__(self, color, number, form, fill):
        self.color = color
        self.number = number
        self.form = form
        self.fill = fill

    def __str__(self):
        print(self.color, self.number, self.form, self.fill)


class Deck():
    # Deck of cards yet to be played

    cards: list[Card]

    def __init__(self):
        self.cards = []
        # Initialize the deck
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        card = Card(i, j, k, l)
                        self.cards.append(card)
        shuffle(self.cards)


class Table():
    # Cards on the table

    cards: list[Card]

    def __init__(self):
        self.cards = []


class Pile():
    # Discard pile, cards already played

    cards: list[Card]

    def __init__(self):
        self.cards = []


class Game():

    deck: Deck
    table: Table
    pile: Pile

    def __init__(self):
        self.deck = Deck()
        self.table = Table()
        self.pile = Pile()
        self.deal()

    def deal(self, number=12):
        for _ in range(number):
            card = self.deck.pop()
            self.table.append(card)

    def restart(self):
        self.deck = Deck()
        self.table = Table()
        self.pile = Pile()
        self.deal()