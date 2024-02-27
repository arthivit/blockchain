#from montycoin import Blockchain
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st 
from flask import Flask, jsonify, request
import requests

class BlockchainGui:
    #make sure to include node_url as a parameter in blockchain's gui/class so it can only interact w the specific node that's being pushed
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain")

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
        self.node = ""
        self.instructions2 = tk.Label(root, text='...then select your functions!', background="pale turquoise", font="AppleMyungjo 22")
        self.instructions2.grid(row=3, column=1, padx=10, pady=10)


#""" BUTTONS """
#mining
        self.mine_button = tk.Button(root, text="Mine Block", command=self.mine_block, background="pale turquoise", font="AppleMyungjo 22")
        self.mine_button.grid(row=5, pady=20)
        self.mine_label = tk.Label(root, background="pale turquoise", font="AppleMyungjo 12")
        self.mine_label.grid(row=5, column=1, pady=20)

#confirm chain (is valid)
        self.isvalid_button = tk.Button(root, text="Confirm Chain?", command=self.is_valid, background="pale turquoise", font="AppleMyungjo 22")
        self.isvalid_button.grid(row=6, padx=10)
        self.isvalid_label = tk.Label(root, background="pale turquoise", font="AppleMyungjo 22")
        self.isvalid_label.grid(row=6, column=1, pady=2)

#get chain
        self.getchain_button = tk.Button(root, text="Get Chain", command=self.get_chain, background="pale turquoise", font="AppleMyungjo 22")
        self.getchain_button.grid(row=7, pady=20)
        self.getchain_label = st.ScrolledText(root, background="pale turquoise", font="AppleMyungjo 22", width=30, height=3)
        self.getchain_label.grid_forget()

#replace chain
        self.replace_chain_button = tk.Button(root, text="Replace Chain?", command=self.replace_chain, background="pale turquoise", font="AppleMyungjo 22")
        self.replace_chain_button.grid(row=8, padx=2)
        self.replace_chain_label = st.ScrolledText(root, background="pale turquoise", font="AppleMyungjo 22", width=30, height=3)
        self.replace_chain_label.grid_forget()
        

#connect node
        self.connect_node_instruction = tk.Label(root, background="pale turquoise", font="AppleMyungjo 22")
        self.connect_node_instruction.grid(row=11, column=1)
        self.node_button = tk.Button(root, text="Connect Node", command=self.connect_node, bg="pale turquoise", font="AppleMyungjo 22")
        self.node_button.grid(row=11, column=0, pady=20)
        self.node_text= st.ScrolledText(root, background="pale turquoise", font="AppleMyungjo 22", width=30, height=3)
        self.node_text.grid_forget()
        

#""" RESPONSES """

    

# button functions

    def select_node(self):
        self.node = self.node_picker.get()


    def mine_block(self):
        self.mine_label.config(text="")
        self.node = self.node_picker.get()
        response = requests.get(f'http://localhost:{self.node}/mine_block')
        print(response)
        block = response.json()
        print(block)
        if block['message'] == 'Congratulations, you just mined a block!':
            self.mine_label.config(text=f"{block}")
        else:
            self.mine_label.config(text=f"{block['message']}")

 

    def get_chain(self):
        self.node = self.node_picker.get()
        data = requests.get(f'http://localhost:{self.node}/get_chain')
        chain = data.json()['chain']
        length = data.json()['length']
        self.getchain_label.insert(tk.INSERT, f"Length: {length} \n Chain: {chain}")
        self.getchain_label.configure(state ='disabled')   #MAKE A LIST
        self.getchain_label.grid(row=7, column=1, pady=2)
        self.add_transaction_label.after(3000, lambda:  self.getchain_label.grid_forget())


    def is_valid(self):
        response = requests.get(f'http://localhost:{self.node}/confirm_chain')
        if response.json()['message'] == "All good. The Blockchain is valid.":
            self.isvalid_label.config(text="All good! Blockchain is valid.")
        else:
            self.isvalid_label.config(text="Uh oh... Blockchain is NOT valid.")
        self.isvalid_label.after(3000, lambda: self.isvalid_label.grid_forget())
    


    def connect_node(self):
        self.connect_node_instruction.config(text='Please enter the nodes in a bracket seperated by commas. Example: [node1, node2, etc]')
        self.node_text.grid(row=7, column=1)
        self.node_text.after(30000, lambda: self.node_text.grid_forget())
        
        data = {
            "nodes": self.node_text.get('1.0', 'end-1c')
        }
        response = requests.get(f'http://localhost:{self.node}/connect_node', data=data)

        message = response.json()['message']
        total_nodes = response.json()['total_nodes']
        self.connect_node_text.config(text=f"{message} {total_nodes}")
        self.connect_node_text.after(30000, lambda: self.connect_node_text.grid_forget())



    def replace_chain(self):
        response = requests.get(f'http://localhost:{self.node}/replace_chain')
        message = response.json()['message']
        if message == 'All good. The chain is the largest one.':
             self.replace_chain_label.insert(tk.INSERT, "All good!")
             
        else:
            self.replace_chain_label.insert(tk.INSERT, "Replaced by longest chain.")
        self.replace_chain_label.grid(row=7, column=1)
        self.replace_chain_label.after(3000, lambda: self.replace_chain_label.grid_forget())

            


if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainGui(root)
    root.geometry("600x700")
    root.configure(background='pale turquoise')
    root.mainloop()

