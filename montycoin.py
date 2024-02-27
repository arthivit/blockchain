import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import argparse
import tkinter as tk
#from wallet import Wallet
#not totally sure if i need to import this or not

#SERVER FILE
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction_pool = []
        self.create_block(proof=1, previous_hash='0', sender='GENESIS', receiver='BLOCK')
        self.nodes = set()
        
    def create_block(self, proof, previous_hash, sender, receiver):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'sender': sender,
                 'receiver': receiver,
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transaction_pool}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        new_trans = {'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount}
        self.transaction_pool.append(new_trans)
        print(new_trans)
        return len(self.transaction_pool)

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        print(self.nodes)
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            print(node)
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
# Mining a new block
def mine_block():
    if len(blockchain.transaction_pool) == 0:
        response = {'message': 'There are no blocks to mine from transaction pool.'}
        return jsonify(response), 200
    else:
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        transaction = blockchain.transaction_pool[0]
        sender = transaction['sender']
        receiver = transaction['receiver']
        block = blockchain.create_block(proof, previous_hash, sender, receiver)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'sender': block['sender'],
                    'receiver': block['receiver'],
                    'previous_hash': block['previous_hash'],
                    'transactions': block['transactions']}
        blockchain.transaction_pool.remove(transaction)
        return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
# Getting the full Blockchain
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/confirm_chain', methods=['GET'])
# Checking if the Blockchain is valid
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {
            'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


@app.route('/new_transaction', methods=['POST'])
# Adding a new transaction to the Blockchain
def new_transaction():
    json = request.get_json()
    pool_length = blockchain.add_transaction(
        json['sender'], json['receiver'], json['amount'])
    transaction_message = f'This transaction has been added to the pool. Please wait for it to be mined. The pool is {pool_length} transaction(s) long.'
    the_response = {'message': transaction_message}
    print(the_response)
    return jsonify(the_response)
    


@app.route('/connect_node', methods=['POST'])
# Connecting new nodes
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Montycoin Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response)


@app.route('/replace_chain', methods=['GET'])
# Replacing the chain by the longest chain if needed
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response)


@app.route('/see_transactions', methods=['POST'])
def see_transactions():
    sender_list = []
    reciever_list = []
    data = request.get_json()
    key = data.get('Public_Key')
    for block in blockchain.chain:
        if block['sender'] == key:
           sender_list.append(block)
        else:
            if block['receiver'] == key:
                reciever_list.append(block)
    if len(reciever_list) > 0:
        the_response = {'sender_transactions': sender_list, 'reciever_transactions': reciever_list}
    else:
        failed = 'None Found.'
        the_response = {'sender_transactions': sender_list, 'reciever_transactions': failed}

    return jsonify(the_response)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=5001, help='port to listen on')
args = parser.parse_args()

# Running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
#app.run(host='0.0.0.0', port=5001)