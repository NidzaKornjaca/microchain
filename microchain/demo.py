from .blockchain import Block, Blockchain
from .exceptions import BlockInvalidException
from .node import Node, NeighbourNode
from .transactions import Transaction
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
        0
    )
    _calculate_nonce(blockchain, block)
    print("Try to add valid block")
    _try_add_block(blockchain, block)
    bad_block = Block(
        prev_block.idx + 1,
        prev_hash,
        datetime.now().timestamp(),
        0
    )
    print("Try to add bad block")
    _try_add_block(blockchain, bad_block)

def _try_add_block(blockchain, block):
    try:
        blockchain.add_block(block)
    except BlockInvalidException:
        print("Failed - Block rejected")


def _calculate_nonce(blockchain, block):
    block.nonce = 0
    while not blockchain.validate_nonce(block.nonce, block.hash()):
        block.nonce += 1
    print("Nonce is", block.nonce)
    return block.nonce

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


def block_tx_demo():
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
