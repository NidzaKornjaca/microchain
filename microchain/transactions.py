from datetime import datetime

class Transaction(object):

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = datetime.now()

    def __repr__(self):
        return "{} -> {} = {}".format(
            self.sender,
            self.recipient,
            self.amount
        )
