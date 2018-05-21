from datetime import datetime
from hashlib import sha256
from .exceptions import BlockInvalidException
from .transactions import Transaction

class Block(object):

    def __init__(self, idx, previous_block_hash, timestamp, nonce, transactions = []):
        self.idx = idx
        self.previous_block_hash = previous_block_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce

    def hash(self):
        string_seed = "{}{}{}{}{}".format(
            self.idx,
            self.previous_block_hash,
            self.timestamp,
            self.nonce,
            self.transactions
        )
        return sha256(string_seed.encode()).hexdigest()

    def serialize(self):
        return {
            'idx': self.idx,
            'previous_block_hash': self.previous_block_hash,
            'timestamp': self.timestamp,
            'transactions': [tx.__dict__ for tx in self.transactions],
            'nonce': self.nonce
        }

    @staticmethod
    def deserialize(block):
        transactions = [
            Transaction(**tx)
            for tx in block['transactions']
        ]
        return Block(
            block['idx'],
            block['previous_block_hash'],
            block['timestamp'],
            block['nonce'],
            transactions
        )

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.chain.append(
            Block(0, 0, datetime.now().timestamp(), 0, [])
        )

    def validate_nonce(self, nonce, hash):
        hash_string = "{}{}".format(nonce, hash)
        return sha256(hash_string.encode()).hexdigest()[:4] == '0000'

    def validate_block(self, block):
        previous_block = self.chain[block.idx - 1]
        if (
            previous_block.hash() != block.previous_block_hash or
            not self.validate_nonce(block.nonce, block.hash())
        ):
            return False
        return True

    def add_block(self, block):
        if self.validate_block(block):
            self.chain.append(block)
            print("Block added to blockchain")
        else:
            raise BlockInvalidException()

    def serialize_chain(self):
        return [i.serialize() for i in self.chain]
