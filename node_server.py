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
	def compute_hash(block):
		block_string = json.dumps(self.__dict__, sort_keys=True)
		return sha512(block_string.encode()).hexdigest()


# A class that represents an immutable list of Block objects that are chained together by hashes, a Blockchain.
class Blockchain:
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

	# Returns the current last Block in the Blockchain.
	@property
	def last_block(self):
		return self.chain[-1]
