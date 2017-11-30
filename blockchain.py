"""
Implementation referenced from https://github.com/dvf/blockchain
Modified to fit the DNS scenario
"""

import hashlib
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import json

class Blockchain(object):
	def __init__(self):
		"""
		Initializes the class

		Current_transactions is the buffer for new transactions
		before a new block is created

		Chain is the chain of blocks (ledger) storing all data

		Nodes is a set keeping track of all the other nodes.
		This is required since we need to broadcast information to other nodes
		"""
		self.current_transactions = []
		self.chain = []
		self.nodes = set()

		# create the genesis block
		# this is a hardcoded block which serves as the first block
		# it contains no data
		self.new_block(previous_hash = '1', proof=100)

	def register_node(self, address):
		"""
		Add a new node to the list of nodes

		:param address: Address of new node in network.
		"""
		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc)

	@property
	def last_block(self):
		"""
		A property method to return the trailing block in the chain
		"""
		return self.chain[-1]

	@property
	def buffered_transaction(self):
		"""
		A property method to return a list of buffered transactions that
		are not yet written into blocks
		"""
		return self.current_transactions

	@staticmethod
	def hash(block):
		"""
		Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # sort the dictionary to assert the hash is consistent
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof,proof):
    	"""
    	Validates the Proof
    	In our scenario, there is no need of incentive to create new block
    	Therefore, POW should be easy to satisfy
    	We use prefix=="00" as criteria

        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] = "00"

    @staticmethod
    def salt_generator():
    	num = 0
    	while True:
    		yield num
    		num += 1

    def proof_of_work(self, last_proof):
    	"""
    	A proof of work algo. Iterate over different values of salt
		See which salt satisfies valid_proof
		"""
		salt_gen = self.salt_generator()
		salt = next(salt_gen)
		while not self.valid_proof(last_proof,salt):
			salt = next(salt_gen)

		return salt













