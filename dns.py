import blockchain

"""
Define the format of DNS transaction here
dns_transaction = {
	'hostname':hostname,
	'ip':ip,
	'port':port
}
"""

class dns_layer(object):
	def __init__(self):
		"""
		Initialize a blockchain object
		"""
		blockchain = blockchain.Blockchain()

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
				if transaction['hostname'] == hostname:
					return (transaction['ip'],transaction['port'])
		raise LookupError('No existing entry matching hostname')

	def mine_block(self):
		"""
		here we assume only the node will full buffer will mine
		once finish mining, broadcast resolve to every node
		all other node add new block but keep buffer
		"""
		last_block = blockchain.last_block
		last_proof = last_block['proof']
		proof = blockchain.proof_of_work(last_proof)

		# Forge the new Block by adding it to the chain
		previous_hash = blockchain.hash(last_block)
		block = blockchain.new_block(proof, previous_hash)

		# broadcast request for all neighbor to resolve conflict

	def broadcast_new_block(self):
		"""
		Broadcast resolve request to all neighbor to force neighbors
		update their chain
		"""
		neighbors = self.blockchain.nodes

		for node in neighbors:
			response = requests.get(f'http://{node}/blockchain/resolve')

			if response.status_code != 200:
				raise ValueError(f'Node {node} responded bad status code')

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
		buffer_len = blockchain.new_transaction(new_transaction)
		if buffer_len > BUFFER_MAX_LEN:
			self.mine_block()
			






