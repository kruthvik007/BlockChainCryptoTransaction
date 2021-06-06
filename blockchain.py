#!/usr/bin/python
# -*- coding:utf-8 -*-

from hashlib import sha256


# function to hash the values that uses hash value of the previous block
def update_hash(*args):
    hashing_text = ""
    h = sha256()
    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    # returning the hash value
    return h.hexdigest()


# class to create a block
class Block:
    data = None
    hash = None
    nonce = 0
    # 64 bit hash of the previous data 
    previous_hash = "0" * 64

    # number is the block number
    def __init__(self, data, number=0):
        self.data = data
        self.number = number

    # hashing the values
    def hash_block(self):
        return update_hash(
            self.previous_hash,
            self.number,
            self.data,
            self.nonce
        )

    # function is used  when the print function is called
    def __str__(self):
        return str("\nBlock#: %s\nHash:\t\t%s\nPrevious Hash:  %s\nData: %s\nNonce: %s\n"
                   % (self.number,
                      self.hash_block(),
                      self.previous_hash,
                      self.data,
                      self.nonce
                      )
                   )


# class to chain all the blocks
class Blockchain:
    # difficulty is the number of zeros in the front of the hash, more the difficulty, stronger the blockchain
    difficulty = 4

    def __init__(self, chain=None):
        if chain is None:
            chain = []
        self.chain = chain

    # adding the block
    def add(self, block):
        self.chain.append(block)

    def mine(self, block):
        # checks if there is previous hash, if present, then it uses that to mine the next block
        try:
            block.previous_hash = self.chain[-1].hash_block()
        except IndexError:
            pass

        while True:
            if block.hash_block()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

    # to check if the block is present or not
    def isValid(self):
        # checking if the hash value has the first difficulty number of digits
        # and the previous hash is the same as the next block's hash
        # by looping through the block chain
        for i in range(1, len(self.chain)):
            previous = self.chain[i].previous_hash
            current = self.chain[i - 1].hash_block()
            if previous != current or current[:self.difficulty] != "0" * self.difficulty:
                return False
        return True


# main runner code
blockchain = Blockchain()
database = []
while True:
    choice = int(input("Press 1 for adding data to block chain \nPress 2 to print the block chain \nPress 3 for "
                       "checking if the chain is valid or not \nPress 4 for modifying any value in the blockchain "
                       "\nPress 5 to Exit \n"))
    if choice == 1:
        data_to_be_added = str(input("Enter the data to be added in the blockchain:- "))
        database.append(data_to_be_added)
        blockchain.mine(Block(data_to_be_added, database.index(data_to_be_added) + 1))
    elif choice == 2:
        for block in blockchain.chain:
            print(block)
    elif choice == 3:
        if blockchain.isValid():
            print("The blockchain is valid\n")
        else:
            print("The blockchain is not valid\n")
    elif choice == 4:
        position = -1
        while position < 0 or position > len(database):
            position = int(input("Enter the block number for which you want to modify"))
        string = str(input("Enter the modifying value:- "))
        temp = blockchain.chain[position - 1].data
        blockchain.chain[position - 1].data = string
        blockchain.mine(blockchain.chain[position])
        if blockchain.isValid():
            print("\nThe blockchain is valid\n")
        else:
            print("\nThe blockchain is not valid now\n")
        print("After the change, the block chain is:- ")
        for i in range(len(blockchain.chain) - 1):
            print(blockchain.chain[i])
        print("The database is set back to previous state when the blockchain was valid")
        database[position - 1] = temp
        blockchain = Blockchain()
        for data in database:
            blockchain.mine(Block(data, database.index(data) + 1))
        for block in blockchain.chain:
            print(block)
    elif choice > 4:
        print("Thank you....Visit again later")
        exit()
