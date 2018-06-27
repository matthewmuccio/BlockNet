#!/usr/bin/env python3


from hashlib import sha512
import json
import time

from flask import Flask, request
import requests


# A class that represents a Block, which stores one or more pieces of data, in the immutable Blockchain.
class Block:
	# One or more pieces of data (author, content, and timestamp) will be stored in a block.
	# The blocks containing the data are generated frequently and added to the blockchain, each with a unique ID.
	def __init__(self, index, transactions, timestamp, previous_hash):
		self.index = index
		self.transactions = transactions
		self.timestamp = timestamp
		self.previous_hash = previous_hash
		self.nonce = 0

	# A function that creates the hash of the block contents.
	def compute_hash(self):
		block_string = json.dumps(self.__dict__, sort_keys=True)
		return sha512(block_string.encode()).hexdigest()
# End of Block class.


# A class that represents an immutable list of Block objects that are chained together by hashes, a Blockchain.
class Blockchain:
	# Difficulty of PoW algorithm.
	difficulty = 2
	# One or more blocks will be stored and chained together on the Blockchain, starting with the genesis block.
	def __init__(self):
		self.unconfirmed_transactions = [] # Pieces of data that are not yet added to the Blockchain.
		self.chain = [] # The immutable list that represents the actual Blockchain.
		self.create_genesis_block()

	# Generates genesis block and appends it to the Blockchain.
	# The Block has index 0, previous_hash of 0, and a valid hash.
	def create_genesis_block(self):
		genesis_block = Block(0, [], time.time(), "0")
		genesis_block.hash = genesis_block.compute_hash()
		self.chain.append(genesis_block)

	# Verifies the block can be added to the chain, adds it, and returns True or False.
	def add_block(self, block, proof):
		previous_hash = self.last_block.hash
		# Verifies that the previous_hash field of block to be added points to the hash of the latest block,
		# and that the PoW that is provided is correct.
		if (previous_hash != block.previous_hash or not self.is_valid_proof(block, proof)):
			return False
		# Adds new block to the chain after verification.
		block.hash = proof
		self.chain.append(block)
		return True

	# Serves as an interface to add the transactions to the blockchain by adding them
	# and then figuring out the PoW.
	def mine(self):
		# If unconfirmed_transactions is empty, no mining to be done.
		if not self.unconfirmed_transactions:
			return False
		last_block = self.last_block
		# Creates a new block to be added to the chain.
		new_block = Block(last_block.index + 1, \
					self.unconfirmed_transactions, \
					time.time(), \
					last_block.hash)
		# Running PoW algorithm to obtain valid hash and consensus.
		proof = self.proof_of_work(new_block)
		# Verifies block can be added to the chain (previous hash matches, and PoW is valid), and adds it.
		self.add_block(new_block, proof)
		# Empties the list of unconfirmed transactions since they are now added to the blockchain.
		self.unconfirmed_transactions = []
		# Announces to the network once a block has been mined, other blocks can simply verify the PoW and add it to their respective chains.
		announce_new_block(new_block)
		# Returns the index of the block that was just added to the chain.
		return new_block.index

	# Proof of work algorithm that tries different values of nonce in order to get a hash
	# that satisfies the difficulty criteria.
	# Important to note that there is no definite logic to figure out the nonce quickly, simply brute force.
	def proof_of_work(self, block):
		block.nonce = 0
		computed_hash = block.compute_hash()
		while not computed_hash.startswith("0" * Blockchain.difficulty):
			block.nonce += 1
			computed_hash = block.compute_hash()
		return computed_hash

	# Adds a new transaction the list of unconfirmed transactions (not yet in the blockchain).
	def add_new_transaction(self, transaction):
		self.unconfirmed_transactions.append(transaction)

	# Checks if the chain is valid at the current time.
	@classmethod
	def check_chain_validity(cls, chain):
		result = True
		previous_hash = "0"
		for block in chain:
			block_hash = block.hash
			# Removes the hash attribute to recompute the hash again using compute_hash.
			delattr(block, "hash")
			if not cls.is_valid_proof(block, block.hash) or previous_hash != block.previous_hash:
				result = False
				break
			block.hash = block_hash
			previous_hash = block_hash
		return result

	# Checks if block_hash is a valid hash of the given block, and if it satisfies the difficulty criteria.
	@classmethod
	def is_valid_proof(cls, block, block_hash):
		return (block_hash.startswith("0" * Blockchain.difficulty) and block_hash == block.compute_hash())

	# Returns the current last Block in the Blockchain.
	@property
	def last_block(self):
		return self.chain[-1]
# End of Blockchain class.


# Flask web application
# Creates a new Flask web app.
app = Flask(__name__)
# The node's copy of the blockchain.
blockchain = Blockchain()
# A set that stores the addresses to other participating members of the network.
peers = set()

# Creates a new endpoint, and binds the function to the URL.
@app.route("/new_transaction", methods=["POST"])
# Submits a new transaction, which adds new data to the blockchain.
def new_transaction():
	tx_data = request.get_json()
	required_fields = ["author", "content"]
	for field in required_fields:
		if not tx_data.get(field):
			return "Invalid transaction data", 404
	tx_data["timestamp"] = time.time()
	blockchain.add_new_transaction(tx_data)
	return "Success", 201

# Creates a new endpoint, and binds the function to the URL.
@app.route("/chain", methods=["GET"])
# Returns the node's copy of the blockchain in JSON format (to display all confirmed transactions/posts).
def get_chain():
	# Ensures that the user's chain is the current (longest) chain.
	consensus()
	chain_data = []
	for block in blockchain.chain:
		chain_data.append(block.__dict__)
	return json.dumps({"length" : len(chain_data), "chain" : chain_data})

# Creates a new endpoint, and binds the function to the URL.
@app.route("/mine", methods=["GET"])
# Requests the node to mine the unconfirmed transactions (if any).
def mine_unconfirmed_transactions():
	result = blockchain.mine()
	if not result:
		return "There are no transactions to mine."
	return "Block #{0} has been mined.".format(result)

# Creates a new endpoint, and binds the function to the URL.
@app.route("/add_nodes", methods=["POST"])
# Adds new peers to the network.
def register_new_peers():
	nodes = request.get_json()
	if not nodes:
		return "Invalid data", 400
	for node in nodes:
		peers.add(node)
	return "Success", 201

# Creates a new endpoint, and binds the function to the URL.
@app.route("/pending_tx")
# Queries unconfirmed transactions.
def get_pending_tx():
	return json.dumps(blockchain.unconfirmed_transactions)

# A simple algorithm to achieve consensus to maintain the integrity of the system.
# If a longer valid chain is found, the chain is replaced with it, and returns True, otherwise nothing happens and returns False.
def consensus():
	global blockchain
	longest_chain = None
	curr_len = len(blockchain.chain)
	# Achieve consensus by checking the JSON fields of every node in the network.
	for node in peers:
		response = requests.get("http://{0}/chain".format(node))
		length = response.json()["length"]
		chain = response.json()["chain"]
		if length > curr_len and blockchain.check_chain_validity(chain):
			curr_len = length
			longest_chain = chain
	if longest_chain:
		blockchain = longest_chain
		return True
	return False

# Creates a new endpoint, and binds the function to the URL.
@app.route("/add_block", methods=["POST"])
# Adds a block mined by a user to the node's chain.
def validate_and_add_block():
	block_data = request.get_json()
	block = Block(block_data["index"], \
			block_data["transactions"], \
			block_data["timestamp", block_data["previous_hash"]])
	proof = block_data["hash"]
	added = blockchain.add_block(block, proof)
	if not added:
		return "The block was discarded by the node.", 400
	return "The block was added to the chain.", 201

# Announces to the network once a block has been mined, should always be called after validate_and_add_block().
# Other blocks can simply verify the PoW and add it to their respective chains.
def announce_new_block(block):
	for peer in peers:
		url = "http://{0}/add_block".format(peer)
		requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))

# Runs the Flask web app.
app.run(port=8000, debug=True)