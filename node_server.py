#!/usr/bin/env python3


import hashlib import sha512
import json


class Block:
	# One or more pieces of data (author, content, and timestamp) will be stored in a block.
	# The blocks containing the data are generated frequently and added to the blockchain, each with a unique ID.
	def __init__(self, index, transactions, timestamp):
		self.index = []
		self.transactions = transactions
		self.timestamp = timestamp

	# A function that creates the hash of the block.
	def compute_hash(block):
		block_string = json.dumps(self.__dict__, sort_keys=True)
		return sha512(block_string.encode()).hexdigest()
