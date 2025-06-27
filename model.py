from random import shuffle
from math import ceil

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

    def get_rows(self):
        return ceil(len(self.cards) / self.get_columns())

    def get_columns(self):
        return 4


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

    def compare(self, *cards):
        if len(cards == 3):
            return self.compare_conditions(cards)
        else:
            return False
    
    def compare_conditions(self, *cards):
        # Compare if all equal or all different

        # Colors
        ecolor = cards[0].color == cards[1].color and cards[1].color == cards[2].color
        dcolor = cards[0].color != cards[1].color and cards[1].color != cards[2].color

        # Number
        enumber = cards[0].number == cards[1].number and cards[1].number == cards[2].number
        dnumber = cards[0].number != cards[1].number and cards[1].number != cards[2].number

        # Form
        eform = cards[0].form == cards[1].form and cards[1].form == cards[2].form
        dform = cards[0].form != cards[1].form and cards[1].form != cards[2].form

        # Fill
        efill = cards[0].fill == cards[1].fill and cards[1].fill == cards[2].fill
        dfill = cards[0].fill != cards[1].fill and cards[1].fill != cards[2].fill

        condition = (ecolor or dcolor) and (enumber or dnumber) and (eform or dform) and (efill or dfill)
        return condition

    def deal(self, number=12):
        for _ in range(number):
            card = self.deck.cards.pop()
            self.table.cards.append(card)

    def restart(self):
        self.deck = Deck()
        self.table = Table()
        self.pile = Pile()
        self.deal()