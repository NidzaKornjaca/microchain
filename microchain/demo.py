from .blockchain import Block, Blockchain
from .exceptions import BlockInvalidException
from .node import Node, NeighbourNode
from datetime import datetime


def add_block():
    blockchain = Blockchain()
    print(blockchain.chain)
    prev_block = blockchain.chain[-1]
    prev_hash = prev_block.hash()
    print(prev_hash)
    block = Block(
        prev_block.idx + 1,
        prev_hash,
        datetime.now().timestamp(),
        calculate_nonce(blockchain, prev_hash)
    )
    print("Try to add valid block")
    try_add_block(blockchain, block)
    bad_block = Block(
        prev_block.idx + 1,
        prev_hash,
        datetime.now().timestamp(),
        0
    )
    print("Try to add bad block")
    try_add_block(blockchain, bad_block)

def try_add_block(blockchain, block):
    try:
        blockchain.add_block(block)
    except BlockInvalidException:
        print("Failed - Block rejected")


def calculate_nonce(blockchain, previous_hash):
    i = 0
    while not blockchain.validate_nonce(i, previous_hash):
        i += 1
    print("Nonce is", i)
    return i

def block_sync_demo():
    n = Node()
    addr = 'http://localhost:5000/'
    nn = NeighbourNode(addr)
    n.add_neighbour(addr)
    #force sync
    n.blockchain = nn.get_chain()
    fresh_block = n.mine()
    for i in n.neighbours:
        print(i.tell_block_mined('me', fresh_block))


def advanced_sync_demo():
    n = Node()
    n.add_neighbour('http://localhost:5000/')
    block_sync_demo()
    block_sync_demo()
    n.sync()
    print(n.blockchain.serialize_chain())
    return n
