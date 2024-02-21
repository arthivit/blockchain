from wallet import Wallet
import tkinter as tk
from flask import Flask, jsonify, request
import requests

# wallet

class WalletGui:
    def __init__(self, root):
        self.root = root
        self.root.title("MONTY COIN WALLET")
        

# my balance

        self.balance_label = tk.Label(root, text="Balance: $0", background="DarkSlateGray2", font="Luminari 18")
        self.balance_label.grid(row=0, column=10)

# making transactions from wallet (need to incorporate this with the blockchain server --> create block/make 
# transaction request)
        self.send_button = tk.Button(root, text="Send Crypto", command=self.send_funds, background="pale turquoise", font="Luminari 18")
        self.send_button.grid(row=4)
        self.send_label = tk.Label(root, background="DarkSlateGray2", font="Luminari 18")
        self.send_label.grid(row=5, pady=3)

# my public key, created by Wallet class
        self.pubkey_button = tk.Button(root, text="See Public Key", command=self.see_pubkey, background="pale turquoise", font="Luminari 18")
        self.pubkey_button.grid(row=6, column=0, pady=3)
        self.pubkey_label = tk.Label(root, background="DarkSlateGray2",font="Luminari 18", justify="right")
        self.pubkey_label.grid(row=7, column=0, pady=3)

# my transactions (defined by my public key)
        self.transactions_button = tk.Button(root, text="See My Transactions", command=self.see_transactions, background="pale turquoise", font="Luminari 18")
        self.transactions_button.grid(row=8, column=0, pady=3)

        self.transactions_label = tk.Label(root, background="DarkSlateGray2", font="Luminari 18")
        self.transactions_label.grid(row=9, column=0, pady=3)


# buttons

   
    def send_funds(self):
        self.send_label.config(text="")
        recipient = "example@recipient.com"  # Get recipient from user input
        amount = 10  # Get amount from user input

        # Send request to Flask endpoint
        response = requests.post("http://localhost:5010/send_funds", json={"recipient": recipient, "amount": amount})
        self.update_balance()
        self.send_label.config(text="Funds sent successfully!")
       
   
    def see_pubkey(self):
        response = requests.get("http://localhost:5010/get_public_key")
        pubkey = response.json()
        self.pubkey_label.config(text=f"Public Key: {pubkey}")
        self.pubkey_label.after(3000, lambda: self.pubkey_label.config(text=''))
        
  
    def add_balance(self):
        response = requests.get("http://localhost:5010/add_balance")
        balance = response.json()["balance"]
        self.balance_label.config(text=f"Balance: ${balance}")
    
 
    def see_transactions(self):
        #need to request the blockchain server
        response = requests.get("http://localhost:5001/see_transactions")
        self.transactions_label.config(text=f"{response}")   

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletGui(root)
    root.geometry("600x400")
    root.configure(background='DarkSlateGray2')
    root.mainloop()

