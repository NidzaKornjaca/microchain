from datetime import datetime

class Transaction(object):

    def __init__(self, sender, recipient, amount, timestamp=datetime.now().timestamp()):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp

    def __repr__(self):
        return "{} -> {} = {} @ {}".format(
            self.sender,
            self.recipient,
            self.amount,
            self.timestamp
        )
