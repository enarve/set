from random import shuffle
from math import ceil

class Card():

    def __init__(self, id, color, number, form, fill):
        self.id = id
        self.color = color
        self.number = number
        self.form = form
        self.fill = fill

    def __str__(self):
        print(self.id)


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
                        id = len(self.cards)
                        card = Card(id, i, j, k, l)
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
    
    def get_card(self, id):
        try:
            id = int(id)
            card = next(card for card in self.cards if card.id == id)
            return card
        except:
            print(f"Error while searching for card with id {id}.")

class Set():
    
    cards = list[Card]

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
    set: Set
    pile: Pile

    def __init__(self):
        self.deck = Deck()
        self.table = Table()
        self.set = Set()
        self.pile = Pile()
        self.deal()

    def compare(self, cards):
        print(cards)
        if len(cards) == 3:
            return self.compare_conditions(cards)
        else:
            return False
    
    def compare_conditions(self, cards):
        # Compare if all equal or all different

        # Colors
        ecolor = (cards[0].color == cards[1].color) and (cards[1].color == cards[2].color)
        dcolor = (cards[0].color != cards[1].color) and (cards[1].color != cards[2].color) and (cards[0].color != cards[2].color)

        # Number
        enumber = (cards[0].number == cards[1].number) and (cards[1].number == cards[2].number)
        dnumber = (cards[0].number != cards[1].number) and (cards[1].number != cards[2].number) and (cards[0].number != cards[2].number)

        # Form
        eform = (cards[0].form == cards[1].form) and (cards[1].form == cards[2].form)
        dform = (cards[0].form != cards[1].form) and (cards[1].form != cards[2].form) and (cards[0].form != cards[2].form)

        # Fill
        efill = (cards[0].fill == cards[1].fill) and (cards[1].fill == cards[2].fill)
        dfill = (cards[0].fill != cards[1].fill) and (cards[1].fill != cards[2].fill) and (cards[0].fill != cards[2].fill)

        condition = (ecolor or dcolor) and (enumber or dnumber) and (eform or dform) and (efill or dfill)
        return condition

    def take_set(self, cards):
        for card in cards:
            self.table.cards.remove(card)
            self.set.cards.append(card)

    def move_set_to_pile(self):
        if self.set.cards:
            self.pile.cards += self.set.cards
            self.set.cards = []
            return True
        else:
            return False
        
    def take_set_and_replace(self, cards):
        for card in cards:
            # remove card
            index = self.table.cards.index(card)
            self.table.cards.remove(card)
            self.set.cards.append(card)

            # add new card
            if self.deck.cards:
                new_card = self.deck.cards.pop()
                self.table.cards.insert(index, new_card)

    def deal(self, number=12):
        for _ in range(number):
            if self.deck.cards:
                card = self.deck.cards.pop()
                self.table.cards.append(card)

    def restart(self):
        self.deck = Deck()
        self.table = Table()
        self.pile = Pile()
        self.deal()