from flask import Flask, request, jsonify
from microchain.node import Node

app = Flask(__name__)
node = Node()

@app.route('/')
def index():
    pass

@app.route('/node/introduce', methods=['POST'])
def introduce_node():
    pass

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(
        node.blockchain.chain
    )

@app.route('/block/mined', methods=['POST'])
def block_mined():
    pass
