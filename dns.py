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
			# mine new block
			"""
			here we assume only the node will full buffer will mine
			once finish mining, broadcast new block to every node
			all other node add new block but keep buffer
			"""
			TODO
		






