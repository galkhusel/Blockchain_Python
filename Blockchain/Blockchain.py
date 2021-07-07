import hashlib



class Block:
    def __init__(self, index, transactions,previous_block, previous_hash, nonce = 0):

        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.previous_block = previous_block
        self.nonce = nonce
        self.hash = self.compute_hash()


    def compute_hash(self):
    	string_to_hash = hashlib.sha256()
    	string_to_hash.update( str(self.index).encode("utf-8") + 
    		str(self.transactions).encode("utf-8")+ 
    		str(self.previous_hash).encode("utf-8")+ 
    		str(self.nonce).encode("utf-8")
    		)
    	return string_to_hash.hexdigest()



class Block_Chain:
	def __init__(self):

		self.unconfirmed_transactions = []
		self.first_block = self.create_genesis_block()
		self.last_block = self.first_block
		self.difficulty = 2
	def create_genesis_block(self):
		genesis_block = Block(0, [], 0, 0x0)
		return genesis_block

	def add_new_transaction(self, transaction):
	    self.unconfirmed_transactions.append(transaction)


	def proof_of_work(self, block):
 
		computed_hash = block.hash
		while not computed_hash.startswith('0' * self.difficulty):
			block.nonce += 1
			computed_hash = block.compute_hash()
		return computed_hash


	def add_block(self, block, proof):
	        previous_hash = self.last_block.hash
	        if previous_hash != block.previous_hash:
	            return False
	        if not self.is_valid_proof(block, proof):
	            return False
	        block.hash = proof
	        return True
	 
	def is_valid_proof(self, block, block_hash):
	        return (block_hash.startswith('0' * self.difficulty) and
	                block_hash == block.compute_hash())
	 
	def mine(self):
			if not self.unconfirmed_transactions:

				return False
	 
			last_block = self.last_block


			new_block = Block(index=last_block.index + 1,
								transactions=self.unconfirmed_transactions,
								previous_block=last_block,
								previous_hash=last_block.hash)
	 
			proof = self.proof_of_work(new_block)
			self.add_block(new_block, proof)
			self.unconfirmed_transactions = []
			self.last_block = new_block
			return new_block.index