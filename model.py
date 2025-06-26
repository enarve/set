class Card():

    def __init__(self, color, number, form, fill):
        self.color = color
        self.number = number
        self.form = form
        self.fill = fill

    def __str__(self):
        print(self.color, self.number, self.form, self.fill)