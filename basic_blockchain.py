### Create a Blockchain ###

# Import Libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify, request, render_template


### Build Blockchain

class Blockchain: 
    
    def __init__(self): 
        self.chain = []
        self.pool = []
        self.create_block(data = 'GENESIS BLOCK', sender = 'ARTHI', reciever= 'POSTMAN' )
        self.mine_block()
        
        
    def create_block(self, data, sender, reciever): 
        block = {'pool index': len(self.pool) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'data': data,
                 'sender': sender,
                 'reciever': reciever}
        self.pool.append(block)
        return block
    
    def mine_block(self):
        if (len(self.chain)<1):
            previous_hash = 0
            proof = 1
        else:
            previous_block = blockchain.get_previous_block()
            previous_proof = previous_block['proof']
            proof = blockchain.proof_of_work(previous_proof)
            previous_hash = blockchain.hash(previous_block)
        transaction = self.pool.pop((0))
        futureBlock = {
                 'index': len(self.chain) + 1,
                 'time mined': str(datetime.datetime.now()),
                 'timestamp': transaction['timestamp'],
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'data': transaction['data'],
                 'sender': transaction['sender'],
                 'reciever': transaction['reciever']}
        self.chain.append(futureBlock)
        return futureBlock
    
    def get_previous_block(self): 
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof): 
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else: 
                new_proof += 1
        return new_proof
    
    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys = True).encode()
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
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

### Mine Blockchain

# Create Web App
app = Flask(__name__)

# Create Blockchain
blockchain = Blockchain()


#creating a block
@app.route('/make_block', methods = ['POST'])
def make_block():
    info = request.get_json()
    sender = info.get('sender')
    reciever = info.get('reciever')
    data = info.get('data')
    myBlock = blockchain.create_block(data, sender, reciever)
    response = {'message': 'Your block is waiting to be approved...',
                'timestamp': myBlock['timestamp'],
                'sender': myBlock['sender'],
                'reciever': myBlock['reciever'],
                'data': myBlock['data']
                }
    return jsonify(response), 200
  

    
# Mine a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    if len(blockchain.pool) < 1:
        response = {'message': 'No blocks to mine from pool.'}
        return jsonify(response), 200
    else:
        block = blockchain.mine_block()
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash']}
        return jsonify(response), 200

# Get a full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Confirm chain is valid
@app.route('/confirm_chain', methods = ['GET'])
def confirm_chain():
    response = {'valid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200

#my transactions
@app.route('/my_transactions', methods = ['POST'])
def my_transactions():
    myTransactions = []
    data = request.get_json()
    myName = data.get('myName')
    i = 0
    while i < len(blockchain.chain):
        current = blockchain.chain[i]
        if myName != current['sender']:
            i+=1
        else:
              myTransactions.append(current)
              i+=1
    response = {'my transactions': myTransactions,
                'number of transactions': len(myTransactions)}
    return jsonify(response), 200
     

# Run app
app.run(host = '0.0.0.0', port = 5010)
    







