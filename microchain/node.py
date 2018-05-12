from datetime import datetime
from .blockchain import Blockchain, Block
from .transactions import Transaction
from .exceptions import TransactionInvalidException


class Node(object):

    def __init__(self):
        self.pending_transactions = []
        self.blockchain = Blockchain()

    def validate_transaction(self, transaction):
        return True

    def receive_transaction(self, transaction):
        if self.validate_transaction(transaction):
            self.pending_transactions.append(transaction)
            return len(self.blockchain.chain) + 1
        else:
            raise TransactionInvalidException()

    def mine(self):
        previous_block = self.blockchain.chain[-1]
        previous_block_hash = previous_block.hash()
        nonce = self.calculate_nonce(self.blockchain, previous_block_hash)
        coingen_tx = Transaction("void", "me", 10)
        self.pending_transactions.append(coingen_tx)
        fresh_block = Block(
            previous_block.idx + 1,
            previous_block_hash,
            datetime.now(),
            nonce,
            self.pending_transactions
        )
        self.blockchain.add_block(fresh_block)
        self.pending_transactions = []
        return fresh_block

    @staticmethod    
    def calculate_nonce(blockchain, previous_hash):
        i = 0
        while not blockchain.validate_nonce(i, previous_hash):
            i += 1
        print("Nonce is", i)
        return i


def demo():
    print("init muchain")
    node = Node()
    print("mining...")
    print(node.mine())
    print("From me to you!")
    tx = Transaction("me", "you", 10)
    print("transmiting tx")
    print("tx will be part of block {}".format(
        node.receive_transaction(tx)
    ))
    print("mining...")
    print(node.mine())
    print("Chain:")
    print(node.blockchain.chain)
    print("Transactions in latest node")
    print(node.blockchain.chain[-1].transactions)
    return node
