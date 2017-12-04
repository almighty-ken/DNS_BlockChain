import blockchain as bc
import requests

"""
Define the format of DNS transaction here
dns_transaction = {
	'hostname':hostname,
	'ip':ip,
	'port':port
}
"""

class dns_layer(object):
	def __init__(self, node_identifier):
		"""
		Initialize a blockchain object
		BUFFER_MAX_LEN is the number of entries per block
		"""
		self.blockchain = bc.Blockchain(node_identifier)
		self.BUFFER_MAX_LEN = 20
		self.MINE_REWARD = 10
		self.node_identifier = node_identifier

	def lookup(self,hostname):
		"""
		Goes through all the blocks in the chain to look
		for a matching transaction.

		:param hostname: string, target hostname we are looking for
		:return: a tuple (ip,port)
		"""
		for block in self.blockchain.chain:
			transactions = block['transactions']
			for transaction in transactions:
				# print(transaction)
				if 'hostname' in transaction and transaction['hostname'] == hostname:
					return (transaction['ip'],transaction['port'])
		raise LookupError('No existing entry matching hostname')

	def mine_block(self):
		"""
		here we assume only the node will full buffer will mine
		once finish mining, broadcast resolve to every node
		all other node add new block but keep buffer
		"""
		last_block = self.blockchain.last_block
		last_proof = last_block['proof']
		proof = self.blockchain.proof_of_work(last_proof)

		# Forge the new Block by adding it to the chain
		previous_hash = self.blockchain.hash(last_block)
		block = self.blockchain.new_block(proof, previous_hash)

		# broadcast request for all neighbor to resolve conflict
		self.broadcast_new_block()

		# now add a special transaction that signifies the reward mechanism
		new_transaction = {
		'node':self.node_identifier,
		'block_index':block['index'],
		'reward':self.MINE_REWARD
		}
		self.blockchain.new_transaction(new_transaction)
		return proof

	def broadcast_new_block(self):
		"""
		Broadcast resolve request to all neighbor to force neighbors
		update their chain
		"""
		neighbors = self.blockchain.nodes

		for node in neighbors:
			print(f"Requesting {node} to resolve")
			response = requests.get(f'http://{node}/nodes/resolve')
			# if response.status_code != 200:
			# 	raise ValueError(f'Node {node} responded bad status code')
			# print(f"{node} resolve completed")

		print("Broadcast Complete")

	def new_entry(self,hostname,ip,port):
		"""
		Adds new entry into current transactions in the blockchain.
		Once we reach a full buffer, mine new block.
		:param hostname: string, hostname
		:param ip: string, ip of corresponding hostname
		:param port: int, port of corresponding ip
		""" 
		new_transaction = {
		'hostname':hostname,
		'ip':ip,
		'port':port
		}
		buffer_len = self.blockchain.new_transaction(new_transaction)
		if buffer_len >= self.BUFFER_MAX_LEN or buffer_len >= self.blockchain.quota-self.BUFFER_MAX_LEN:
			self.mine_block()
			
	def dump_chain(self):
		response = {
		'chain': self.blockchain.chain,
		'length': len(self.blockchain.chain)
		}
		return response

	def dump_buffer(self):
		return self.blockchain.current_transactions

	def get_chain_quota(self):
		return self.blockchain.quota

	def register_node(self,addr):
		self.blockchain.register_node(addr)

	def get_network_size(self):
		return len(self.blockchain.nodes)





