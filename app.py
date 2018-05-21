from flask import Flask, request, jsonify
from microchain.node import Node
from microchain.blockchain import Block
from microchain.exceptions import BlockInvalidException

app = Flask(__name__)
node = Node()

@app.route('/')
def node_info():
    node_info = {
        "chain_len": len(node.blockchain.chain),
        "num_ptx": len(node.pending_transactions),
        "neighbours": node.serialize_neighbours()
    }
    return jsonify(
        node_info
    ), 200


@app.route('/node/introduce', methods=['POST'])
def introduce_node():
    json = request.json
    address = json.get('address')
    if address:
        node.add_neighbour(address)
        return jsonify(
            {
                "msg": "Added to index"
            }
        ), 201
    else:
        return jsonify(
            {
                "msg": "Bad address"
            }, 400
        )


@app.route('/sync', methods=['POST'])
def go_sync():
    node.sync()
    return jsonify(
        {
            "msg": "Synced"
        }
    ), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(
        node.blockchain.serialize_chain()
    ), 200


@app.route('/block/mined', methods=['POST'])
def block_mined():
    json = request.json
    block = json.get('block')
    if not block:
        return jsonify(
            {
                "msg": "Message must contain and 'block' fields"
            }
        ), 400
    block_parsed = Block.deserialize(block)
    try:
        node.receive_block(block_parsed)
    except BlockInvalidException:
        return jsonify(
            {
                "msg": "Adding failed"
            }
        )
    return jsonify(
        {
            "msg": "KTHXBAI"
        }
    ), 200
