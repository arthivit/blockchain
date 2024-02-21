from tinyec.ec import SubGroup, Curve
import secrets
from flask import Flask, jsonify, request
import requests



class Wallet:
    def __init__(self):
        self.transactionsList = []
        self.balance = 100

        #cryptography ECDH
        field = SubGroup(p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
        g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8), n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
        h=0x1)
        curve = Curve(a=0x0, b=0x7, field=field, name='secp256k1')
        self.privateKey = secrets.randbelow(curve.field.n)
        self.rawPublicKey = self.privateKey * curve.g
        self.publicKey = '0' + str(2 + self.rawPublicKey.y % 2) + str(hex(self.rawPublicKey.x)[2:])
    
       

    
    def return_pubkey(self):
        pubkey = self.publicKey
        return pubkey

    def return_balance(self):
        return self.balance

      #find transactions with my public key
      #add them to my balance?
      #Blockchain.get_chain()

      ##represent transactions with my public key (seperated by sender and reciever?) in wallet


wallet = Wallet()

app = Flask(__name__)



@app.route('/get_public_key', methods=['GET'])
def get_public_key():
    public_key = wallet.return_pubkey()
    response = str(public_key)
    return jsonify(response)

@app.route('/get_balance')
def get_balance():
    mybalance = wallet.return_balance()
    return jsonify({"balance": mybalance})

@app.route('/send_funds', methods=['POST'])
def send_funds():
    data = request.json
    recipient = data.get("recipient key")
    amount = data.get("amount")

    if recipient and amount:
        wallet.balance -= amount
        return "Funds sent successfully!", 200
    else:
        return "Invalid request", 400

@app.route('/add_balance', methods=['POST'])
def add_balance():
   data = request.json
   amount = data.get("amount")
   tradnum = data.get("traditional currency")

   if tradnum and amount:
      wallet.balance += amount
      return "Funds added successfully!", 200
   else:
      return "Invalid request", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
        
        
