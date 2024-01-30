# Arthi Vithiananthan - Blockchain Project 1
## What features and functionality did you add to your blockchain? Why? 
Feature-wise, I added two new app routes: 'make_block' and 'my_transactions'. I also changed the parameters of each block to be 'index,' 'time mined,' 'timestamp, 'proof,' 'previous_hash,' 'data,' 'sender,' and 'reciever.' The last three parameters are user inputted (from the request.get_json() function) through Postman.

### make_block
With 'make_block,' I sought out to reflect the process of blocks being added to the ledger from a pool of unconfirmed transactions. The 'make_block' function allows users to "make" their transaction and then have it added to the pool (rather than directly to the chain). Then, I edited the pre-existing 'mine_block' function to add blocks from the pool of unmined blocks to the ledger. If the user tried to mine a block with nothing in the pool, they would recieve an output stating this, rather than just crashing.  
### my_transactions
For 'my_transactions,' I utilized the dictionary quality of the blocks to return an array of all blocks with a case-specific 'sender' value. To do this, I created a loop to iterate through the ledger array, checking the value for the 'sender' key of each block. 

## What is a class in Python/Object-Oriented Programming? What is an endpoint? What is a server? What is Flask? What is Postman doing?
**A class** is the blueprint for a user-created object which includes a constructor, class methods, variables, and more specific components for this special data type. **An API endpoint** is a specific place data can be sent from/recieved at within the API. **A server** is the channel in which data requests are made. Flask is a framework that helps create simple apps. Postman is acting as our API server, and the endpoints are the specific app routes in Postman.

## What you intended to do vs. what you actually completed. What challenges did you face?
I wanted to create a web interface for this project as well, but there was more googling needed (about json, Python-HTML compatibility, etc) than I had time for. I also struggled with some of the json functions which required me to play around for a while with my code to figure out how to make it work. 