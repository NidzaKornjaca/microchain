from datetime import datetime
from hashlib import sha256
from .exceptions import BlockInvalidException

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
        return sha256(string_seed.encode())


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.chain.append(
            Block(0, 0, datetime.now(), 0, [])
        )

    def validate_nonce(self, nonce, previous_block_hash):
        hash_string = "{}{}".format(nonce, previous_block_hash.hexdigest())
        return sha256(hash_string.encode()).hexdigest()[:4] == '0000'

    def validate_block(self, block):
        previous_block = self.chain[block.idx - 1]
        if (
            previous_block.hash().hexdigest() != block.previous_block_hash.hexdigest() or
            not self.validate_nonce(block.nonce, block.previous_block_hash)
        ):
            return False
        return True

    def add_block(self, block):
        if self.validate_block(block):
            self.chain.append(block)
            print("Block added to blockchain")
        else:
            raise BlockInvalidException()
