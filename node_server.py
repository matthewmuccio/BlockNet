#!/usr/bin/env python3


import hashlib import sha512
import json
import time


# A class that represents a Block, which stores one or more pieces of data, in the immutable Blockchain.
class Block:
	# One or more pieces of data (author, content, and timestamp) will be stored in a block.
	# The blocks containing the data are generated frequently and added to the blockchain, each with a unique ID.
	def __init__(self, index, transactions, timestamp, previous_hash):
		self.index = index
		self.transactions = transactions
		self.timestamp = timestamp
		self.previous_hash = previous_hash

	# A function that creates the hash of the block.
	def compute_hash(self, block):
		block_string = json.dumps(self.__dict__, sort_keys=True)
		return sha512(block_string.encode()).hexdigest()


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

	# Adds a new transaction the list of unconfirmed transactions (not yet in the blockchain).
	def add_new_transaction(self, transaction):
		self.unconfirmed_transactions.append(transaction)

	# Serves as an interface to add the transactions to the blockchain by adding them
	# and then figuring out PoW.
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
		# Returns the index of the block that was just added to the chain.
		return new_block.index

	# Checks if block_hash is a valid hash of the given block, and if it satisfies the difficulty criteria.
	def is_valid_proof(self, block, block_hash):
		return (block_hash.startswith("0" * Blockchain.difficulty) and block_hash == block.compute_hash())

	# Proof of work algorithm that tries different values of nonce in order to get a hash
	# that satisfies the difficulty criteria.
	# Important to note that there is no definite logic to figure out the nonce quickly, simply brute force.
	def proof_of_work(self, block):
		block.nonce = 0
		computed_hash = block.compute_hash()
		while not computed_hash.startswith("0" * Blockchain.difficulty)
			block.nonce += 1
			computed_hash = block.compute_hash()
		return computed_hash

	# Returns the current last Block in the Blockchain.
	@property
	def last_block(self):
		return self.chain[-1]
