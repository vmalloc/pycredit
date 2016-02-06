import datetime


class Card(object):

    def __init__(self, card_id):
        super(Card, self).__init__()
        self.id = card_id

    def __repr__(self):
        return '<Card {}>'.format(self.id)


class Charge(object):

    def __init__(self, amount, card, payee, date, charge_date, payment_number=1, num_payments=None):
        super(Charge, self).__init__()
        self.amount = amount
        self.card = card
        self.payee = payee
        assert isinstance(date, datetime.date)
        assert isinstance(charge_date, datetime.date)
        self.date = date
        self.charge_date = charge_date
        self.payment_number = payment_number
        self.num_payments = num_payments

    def __repr__(self):
        return '[On {}: {} to {}]'.format(
            self.card.id, self.amount, self.payee)
