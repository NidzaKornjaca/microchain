from datetime import datetime
import requests
from .blockchain import Blockchain, Block
from .transactions import Transaction
from .exceptions import TransactionInvalidException, BlockInvalidException


class Node(object):

    def __init__(self):
        self.pending_transactions = []
        self.blockchain = Blockchain()
        self.neighbours = set()

    def validate_transaction(self, transaction):
        return True

    def receive_transaction(self, transaction):
        if self.validate_transaction(transaction):
            self.pending_transactions.append(transaction)
            return len(self.blockchain.chain) + 1
        else:
            raise TransactionInvalidException()

    def mine(self):
        raise NotImplementedError()

    @staticmethod
    def calculate_nonce(blockchain, block):
        block.nonce = 0
        raise NotImplementedError()

    def receive_block(self, block):
        self.blockchain.add_block(block)
        for neighbour in self.neighbours:
            neighbour.ask_for_sync()

    def add_neighbour(self, address):
        self.neighbours.add(NeighbourNode(address))

    def serialize_neighbours(self):
        return [i.address for i in self.neighbours]

    def sync(self, force=False):
        raise NotImplementedError()

class NeighbourNode(object):

    def __init__(self, address):
        self.address = address

    def __hash__(self):
        return self.address.__hash__()

    def ask_for_sync(self):
        response = requests.post(self.address + 'sync')
        return response

    def send_block(self, block):
        response = requests.post(
            self.address + 'block/mined',
            json={
                'block': block.serialize()
            }
        )
        return response

    def get_chain(self):
        response = requests.get(self.address + 'chain')
        chain = response.json()
        blockchain = Blockchain()
        blockchain.chain = [Block.deserialize(chain[0])]
        for block in chain[1:]:
            blockchain.add_block(
                Block.deserialize(block)
            )
        return blockchain
