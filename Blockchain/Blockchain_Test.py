from Blockchain import Block
from Blockchain import Block_Chain


blockchain = Block_Chain()
blockchain.create_genesis_block()


assert blockchain.unconfirmed_transactions == [] #should be empty list
assert blockchain.first_block.index == 0 #should be None as no transactions have been made
assert blockchain.last_block == blockchain.first_block #should be None as no transactions have been made



blockchain.add_new_transaction( ("me", "you", 100))
assert blockchain.unconfirmed_transactions == [("me", "you", 100)] #added 1 unconfirmed transaction

blockchain.add_new_transaction(( "you", "me", 50))
assert blockchain.unconfirmed_transactions == [("me", "you", 100),("you", "me", 50)] #added 1 unconfirmed transaction


#checking that the transactions have succesfully been added to the first node

blockchain.mine()

assert blockchain.unconfirmed_transactions == [] 
assert blockchain.last_block.index == 1
assert blockchain.last_block.transactions == [("me", "you", 100),("you", "me", 50)]


#adding a second node to the blockchain

blockchain.add_new_transaction( ("me", "you", 100))
blockchain.mine()

assert blockchain.last_block.transactions == [("me", "you", 100)]
assert blockchain.last_block.index == 2
assert blockchain.last_block.previous_hash == blockchain.last_block.previous_block.hash


#adding a second node to the blockchain

blockchain.add_new_transaction( ("you", "me", 25))
blockchain.mine()

assert blockchain.last_block.transactions == [( "you", "me", 25)]
assert blockchain.last_block.index == 3
assert blockchain.last_block.previous_block.index == 2


blockchain2 = Block_Chain()



#-----------------------------volume test unconfirmed transactions------------------------------------------


list_ = []
for x in range(0,1000000):
	blockchain2.add_new_transaction( ("you", "me", x))

assert len(blockchain2.unconfirmed_transactions) == 1000000

blockchain2.mine()
assert len(blockchain2.last_block.transactions) == 1000000


boolean = True
block = blockchain2.last_block
for x in range(0,1000000):
	if block.transactions[x][2] !=  x:
		boolean	= False
		break


assert boolean == True




#-----------------------------volume test mining------------------------------------------

for x in range(0,100):
	blockchain2.add_new_transaction( ("you", "me", x))
	blockchain2.mine()

boolean = True
block = blockchain2.last_block
for x in range(0,100):
	if block.transactions[0][2] != 99 - x:
		boolean	= False
		break
	block = block.previous_block


assert boolean == True
assert blockchain2.last_block.index == 101
