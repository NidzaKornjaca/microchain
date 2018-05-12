from flask import Flask, request, jsonify
from microchain.node import Node

app = Flask(__name__)
node = Node()

@app.route('/')
def node_info():
    node_info = {
        "chain_len": len(node.blockchain.chain),
        "num_ptx": len(node.pending_transactions)
    }
    return jsonify(
        node_info
    )

@app.route('/node/introduce', methods=['POST'])
def introduce_node():
    pass

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(
        node.blockchain.serialize_chain()
    )

@app.route('/block/mined', methods=['POST'])
def block_mined():
    pass
