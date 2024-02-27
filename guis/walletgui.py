#from wallet import Wallet
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st 
from flask import Flask, jsonify
import requests

# wallet

class WalletGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Wallet")
        self.transaction_data = {
            "sender": '',
            "receiver": '',
            "amount": ''
        }
        self.initpubkey = requests.get("http://localhost:5010/get_public_key")
        self.pubkey = self.initpubkey.json()
        

# my balance to start from the wallet class
        self.initbal = requests.get("http://localhost:5010/get_balance",)
        self.balance = int(self.initbal.json()["balance"])
        self.balance_label = tk.Label(root, text=f"Balance: ${self.balance}", background="pale turquoise", font="AppleMyungjo 22")
        self.balance_label.grid(row=3, column=1)
        
#instructions

        self.instructions = tk.Label(root, text='First pick a node...', background="pale turquoise", font="AppleMyungjo 22")
        self.instructions.grid(row=0, column=1)
        self.node_picker = ttk.Combobox(
                    state="readonly",
                    values=["5001", "5002", "5003", "5004"],
                    background="pale turquoise")

    #node picker
        self.node_picker.grid(row=1, column=1, padx=10)
        self.node_confirm = tk.Button(root, text="Confirm Node", command=self.select_node, background="pale turquoise", font="AppleMyungjo 22")
        self.node_confirm.grid(row=2, column=1, padx=10, pady=5)


# make transaction request
        self.make_button = tk.Button(root, text="Make Transaction", command=self.add_transaction, background="pale turquoise", font="AppleMyungjo 22")
        self.make_button.grid(row=4)
        
    

# see public key
        self.pubkey_button = tk.Button(root, text="See Public Key", command=self.see_pubkey, background="pale turquoise", font="AppleMyungjo 22")
        self.pubkey_button.grid(row=5, column=0, pady=3)
        self.pubkey_label = st.ScrolledText(root, background="pale turquoise", font="AppleMyungjo 22", width=30, height=3)
        self.pubkey_label.grid_forget()

# see my transactions (defined by my public key)
        self.transactions_button = tk.Button(root, text="My Transactions", command=self.see_transactions, background="pale turquoise", font="AppleMyungjo 22")
        self.transactions_button.grid(row=9, column=0, pady=20, padx=10)

    #i sent
        self.transactions_sender = st.ScrolledText(root, background="pale turquoise", font="AppleMyungjo 18", width=30, height=3)
        self.transactions_sender.grid_forget()
       
        
    #i got
        self.transactions_reciever = st.ScrolledText(root, background="pale turquoise", font="AppleMyungjo 18", width=20, height=3)
        self.transactions_reciever.grid_forget()
        
#add transaction label/entries
        
        self.add_transaction_label= st.ScrolledText(root, background="pale turquoise", font="AppleMyungjo 22", width=30, height=3)
        self.add_transaction_label.grid_forget()

    #sender
        self.sender_label= tk.Label(root, text="Sender:", background="pale turquoise",font="AppleMyungjo 22" )
        self.sender_label.grid_forget()
        self.sender_key = tk.Label(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.sender_key.grid_forget()

    #receiver
        self.reciever_label = tk.Label(root, text="Reciever:", background="pale turquoise",font="AppleMyungjo 22")
        self.reciever_label.grid_forget()
        self.reciever_entry = tk.Entry(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.reciever_entry.grid_forget()

    #amount
        self.amount_label = tk.Label(root, text="Amount:", background="pale turquoise",font="AppleMyungjo 22")
        self.amount_label.grid_forget()
        self.amount_entry = tk.Entry(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.amount_entry.grid_forget()

        self.send_info_button = tk.Button(root, text="Submit", command=self.send_info, background="pale turquoise", font="AppleMyungjo 22")
        self.send_info_button.grid_forget()

#add balance
    #button
        self.add_balance_button = tk.Button(root, text="Add To Balance", command=self.add_balance, background="pale turquoise", font="AppleMyungjo 22")
        self.add_balance_button.grid(row=6, column=0, pady=3)
    #amount
        self.balamount_label = tk.Label(root, text="Amount to add to balance:", background="pale turquoise",font="AppleMyungjo 22")
        self.balamount_label.grid_forget()
        self.balamount_entry = tk.Entry(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.balamount_entry.grid_forget()

    #method
        self.tradcur_label = tk.Label(root, text="Traditional currency routing number:", background="pale turquoise",font="AppleMyungjo 22")
        self.tradcur_label.grid_forget()
        self.tradcur_entry = tk.Entry(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.tradcur_entry.grid_forget()

    #submit
        self.submit_balance_button = tk.Button(root, text="Submit", command=self.balance_info, background="pale turquoise", font="AppleMyungjo 22")
        self.submit_balance_button.grid_forget()

    


# buttons functions
    def select_node(self):
        self.node = self.node_picker.get()

    def add_transaction(self):
        

        
        self.reciever_label.grid(row=4, column=1)
        self.amount_label.grid(row=6, column=1)

        
        self.reciever_entry.grid(row=5, column=1, padx=70)
        self.amount_entry.grid(row=7, column=1, padx=70)

        self.send_info_button.grid(row=8, column=1)
       
#add transaction continued after submit button pressed
    def send_info(self):
        self.transaction_data = {
            'sender': str(self.pubkey),
            'receiver': str(self.reciever_entry.get()),
            'amount': self.amount_entry.get()
        }
        
        response = requests.post(f'http://localhost:{self.node}/new_transaction', json = self.transaction_data)

        
        self.reciever_label.grid_forget()
        self.amount_label.grid_forget()

        self.amount_entry.grid_forget()
        self.reciever_entry.grid_forget()
        
        self.send_info_button.grid_forget()

        message = response.json()['message']

        trans_amount = int(self.transaction_data["amount"])
        bal_response = requests.post("http://localhost:5010/add_balance", json = {'amount': trans_amount, 'tradcur' : 'n/a'})
        self.balance = int(bal_response.json()["balance"])
        self.balance_label.config(text=f"Balance: ${self.balance}")


        self.add_transaction_label.delete("1.0","end")
        self.add_transaction_label.insert(tk.INSERT, f'{message}')
        self.add_transaction_label.grid(row=5, column=1)
        self.add_transaction_label.after(3000, lambda
        : self.add_transaction_label.grid_forget())
        
        
        

    
        #self.send_label.config(text="Funds sent successfully!")

# show public key
    def see_pubkey(self):
        self.pubkey_label.insert(tk.INSERT, f"Public Key: {self.pubkey}")
        self.pubkey_label.configure(state ='disabled')   #MAKE A LIST
        self.pubkey_label.grid(row=7, column=1, pady=2)
        self.pubkey_label.after(3000, lambda: self.pubkey_label.grid_forget())
    

# add money to balance
    def add_balance(self):
        self.tradcur_label.grid(row=4, column=1)
        self.tradcur_entry.grid(row=5, column=1, padx=100)

        self.balamount_label.grid(row=6, column=1)
        self.balamount_entry.grid(row=7, column=1, padx=70)

        self.submit_balance_button.grid(row=8, column=1, pady=3)
        
        

# add_balance continued after button press  
    def balance_info(self):
        data = {
            "amount": self.balamount_entry.get(),
            "tradcur": self.tradcur_entry.get()
        }

        response = requests.post(f'http://localhost:5010/add_balance', json=data)

        self.tradcur_label.grid_forget()
        self.tradcur_entry.grid_forget()
        self.balamount_label.grid_forget()
        self.balamount_entry.grid_forget()
        self.submit_balance_button.grid_forget()
      
       
        balance = response.json()['balance']
        self.balance_label.config(text=f"Balance: ${balance}")
        message = response.json()['message']

    

    def see_transactions(self):
        thisresponse = requests.get('http://localhost:5010/get_public_key')
        pubkey = str(thisresponse.json())
        
        data = {'Public_Key': pubkey}
        response = requests.post(f'http://localhost:{self.node}/see_transactions', json = data)

        print(response.json())
        receiver = []
        sender = []
        receiver = response.json()['reciever_transactions']
        sender = response.json()['sender_transactions']

        self.transactions_sender.grid(row=5, column=1)
        self.transactions_sender.insert(tk.INSERT,f'Sender Transactions: {sender}')
        self.transactions_sender.after(3000, lambda: self.transactions_sender.grid_forget())
        self.transactions_sender.delete("1.0","end")
        

        self.transactions_reciever.grid(row=6, column=1)
        self.transactions_reciever.insert(tk.INSERT,f'Reciever Transactions: {receiver}')
        self.transactions_reciever.after(3000, lambda: self.transactions_reciever.grid_forget())
        self.transactions_reciever.delete("1.0","end")

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletGui(root)
    root.geometry("600x600")
    root.configure(background='pale turquoise')
    root.mainloop()

