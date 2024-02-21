from montycoin import Blockchain
import tkinter as tk
from tkinter import ttk
from flask import Flask, jsonify, request
import requests

class BlockchainGui:
    #make sure to include node_url as a parameter in blockchain's gui/class so it can only interact w the specific node that's being pushed
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain")

        self.instructions = tk.Label(root, text="First pick a node, then select your functions!", background="pale turquoise", font="AppleMyungjo 22")
        self.instructions.grid(row=0, column=1)
        self.node_picker = ttk.Combobox(
                    state="readonly",
                    values=["5001", "5002", "5003", "5004"],
                    background="pale turquoise",
                    font='AppleMyungjo 22'
        )
        self.node_picker.grid(row=5, column=1, pady=2)
        self.node_confirm = tk.Button(root, text="Confirm Node", command=self.select_node, background="pale turquoise", font="AppleMyungjo 22")
        self.node_confirm.grid(row=6, column=1)
        self.node = ""

#add transactions
    #sender
        self.sender_label= tk.Label(root, text="Sender:", background="pale turquoise",font="AppleMyungjo 22", )
        self.sender_label.grid(row=7, column=1)
        self.sender_entry = tk.Entry(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.sender_entry.grid(row=7, column=2)

    #reciever
        self.reciever_label = tk.Label(root, text="Reciever:", background="pale turquoise",font="AppleMyungjo 22")
        self.reciever_label.grid(row=8, column=1)
        self.reciever_entry = tk.Entry(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.reciever_entry.grid(row=8, column=2)

    #amount
        self.amount_label = tk.Label(root, text="Amount:", background="pale turquoise",font="AppleMyungjo 22")
        self.amount_label.grid(row=9, column=1)
        self.amount_entry = tk.Entry(root, bg="pale turquoise", font="AppleMyungjo 22")
        self.amount_entry.grid(row=9, column=2)

    #add transaction button
        self.add_transaction_button = tk.Button(root, text="Add Transaction", command=self.add_transaction, bg="pale turquoise", font="AppleMyungjo 22")
        self.add_transaction_button.grid(row=10, columnspan=2, column=1, pady=5)
        self.add_transaction_label= tk.Label(root,background="pale turquoise",font="AppleMyungjo 22", justify="right")
        self.add_transaction_label.grid(row=11, column=1,pady=2)


#mining
        self.mine_button = tk.Button(root, text="Mine Block", command=self.mine_block, background="pale turquoise", font="AppleMyungjo 22")
        self.mine_button.grid(row=5, pady=2)
        self.mine_label = tk.Label(root, background="pale turquoise", font="AppleMyungjo 22")
        self.mine_label.grid(row=6, pady=2)


#get chain
        self.getchain_button = tk.Button(root, text="Get Chain", command=self.get_chain, background="pale turquoise", font="AppleMyungjo 22")
        self.getchain_button.grid(row=7, pady=2)
        self.getchain_label = tk.Label(root, background="pale turquoise", font="AppleMyungjo 22")
        self.getchain_label.grid(row=8, pady=2)
        

#confirm chain
        self.isvalid_button = tk.Button(root, text="Confirm Chain?", command=self.is_valid, background="pale turquoise", font="AppleMyungjo 22")
        self.isvalid_button.grid(row=9, pady=2)
        self.isvalid_label = tk.Label(root, background="pale turquoise", font="AppleMyungjo 22")
        self.isvalid_label.grid(row=10, pady=2)  


#replace chain
        self.replace_chain_button = tk.Button(root, text="Replace Chain?", command=self.replace_chain, background="pale turquoise", font="AppleMyungjo 22")
        self.replace_chain_button.grid(row=11, pady=2, column=0)
        self.replace_chain_label = tk.Label(root, background="pale turquoise",font="AppleMyungjo 22", justify="right")
        self.replace_chain_label.grid(row=12, column=0, pady=2)


# my transactions (defined by my public key)
        self.transactions_button = tk.Button(root, text="See My Transactions", command=self.see_transactions, background="pale turquoise", font="AppleMyungjo 22")
        self.transactions_button.grid(row=12, column=1, pady=2)

        #i sent
        self.transactions_label_sender = tk.Label(root, background="pale turquoise", font="AppleMyungjo 22")
        self.transactions_label_sender.grid(row=13, column=2, pady=2)
        
        #i got
        self.transactions_label_reciever = tk.Label(root, background="pale turquoise", font="AppleMyungjo 22")
        self.transactions_label_reciever.grid(row=14, column=2, pady=2) 
    

#connect node
        self.node_button = tk.Button(root, text="Connect Node", command=self.connect_node, bg="pale turquoise", font="AppleMyungjo 22")
        self.node_button.grid(row=13, column=0, pady=2)
        self.node_text= tk.Text(root, bg="pale turquoise")
        self.node_text.grid_forget()



# button functions

    def select_node(self):
        self.node = self.node_picker.get()


    def mine_block(self):
        self.mine_label.config(text="")
        self.node = self.node_picker.get()
        response = requests.get(f'http://localhost:{self.node}/mine_block')
        self.mine_label.config(text="Block mined successfully!")



    def get_chain(self):
        self.node = self.node_picker.get()
        data = requests.get(f'http://localhost:{self.node}/get_chain')
        chain = data['chain']
        length = data['length']
        self.getchain_label.config(text=f"Length: {length} /n Chain: {chain}") #MAKE A LIST
        


    def is_valid(self):
        response = requests.get(f'http://localhost:{self.node}/confirm_chain')
        if response == "All good. The Blockchain is valid.":
            self.isvalid_label.config(text="All good!")
        else:
            self.isvalid_label.config(text="Uh oh... Blockchain is NOT valid.")
    


    def add_transaction(self):
        data = {
            "sender": self.sender_entry.get(),
            "reciever": self.reciever_entry.get(),
            "amount": self.amount_entry.get()
        }
        
        response = requests.post(f'http://localhost:{self.node}/add_transaction', data=data)
        
        self.reciever_entry.delete(0, tk.END)
        self.sender_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        message = response['message']
        self.add_transaction_label.config(text=message)
        self.add_transaction_label.after(3000, lambda: self.add_transaction_label.config(text=''))



    def connect_node(self):
        self.connect_node_instruction.config(text='Please enter the nodes in a bracket seperated by commas. Example: [node1, node2, etc]')
        self.node_text.grid(row=15, column=0)
        
        data = {
            "nodes": self.node_text.get('1.0', 'end-1c')
        }
        response = requests.get(f'http://localhost:{self.node}/connect_node', data=data)

        message = response['message']
        total_nodes = response['total_nodes']
        self.connect_node_text.config(text=f"{message} {total_nodes}")



    def replace_chain(self):
        response = requests.get(f'http://localhost:{self.node}/replace_chain')
        if response["message"] == 'All good. The chain is the largest one.':
            self.replace_chain_label.config(text="All good!")
        else:
            self.replace_chain_label.config(text="Replaced by longest chain.")
        self.replace_chain_label.after(3000, lambda: self.replace_chain_label.config(text=''))

    def see_transactions(self):
        response = requests.get(f'http://localhost:{self.node}/see_transactions')

        reciever = response['reciever_transactions']
        sender = response['sender_transactions']

        self.transactions_label_sender.config(text=f'Sender Transactions: {sender}')
        self.transactions_label_sender.after(3000, lambda: self.transactions_label_sender.config(text=''))

        self.transactions_label_reciever.config(text=f'Reciever Transactions: {reciever}')
        self.transactions_label_reciever.after(3000, lambda: self.transactions_label_reciever.config(text=''))
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainGui(root)
    root.geometry("600x700")
    root.configure(background='pale turquoise')
    root.mainloop()

