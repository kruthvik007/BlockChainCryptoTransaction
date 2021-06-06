from hashlib import sha256
import json
import pprint


# function to hash the data sent (transaction)
def calculate_hash(previous_hash, data, nonce):
    data = str(previous_hash) + str(data) + str(nonce)
    data = data.encode()
    hashing = sha256(data)
    return hashing.hexdigest()


# class to create a block
class Block:
    def __init__(self, transaction_data, previous_hash=''):
        self.transaction_data = transaction_data
        if previous_hash == 'I am the First Block':
            self.previous_hash = '0' * 64
        else:
            self.previous_hash = previous_hash

        self.nonce = 0
        self.hash = calculate_hash(previous_hash, transaction_data, self.nonce)

    # mining of the block based on difficulty by increasing nonce
    def mine_block(self, difficulty):
        difficultyCheck = "0" * difficulty
        while self.hash[:difficulty] != difficultyCheck:
            self.hash = calculate_hash(self.previous_hash, self.transaction_data, self.nonce)
            self.nonce = self.nonce + 1


# function to get the first block data....just a string
def genesis_block():
    basic_genesis_block = Block("I am the First Block")
    return basic_genesis_block


# class to chain the blocks
class Blockchain:
    def __init__(self):
        self.chain = [genesis_block()]
        self.difficulty = 3
        self.pendingTransaction = []
        self.reward = 10

    # is used to get the last box in the chain that is used to get the previous hash
    def get_last_block(self):
        return self.chain[len(self.chain) - 1]

    # mining of all pending transactions into 1 block
    def mining_pending_transactions(self, minerRewardAddress):
        # in reality not all of the pending transaction go into the block the miner gets to pick which one to mine
        new_block = Block(self.pendingTransaction)
        new_block.mine_block(self.difficulty)
        new_block.previous_hash = self.get_last_block().hash

        print("Previous Block's Hash: " + new_block.previous_hash)
        testChain = []
        for transaction_data in new_block.transaction_data:
            temp = json.dumps(transaction_data.__dict__, indent=5, separators=(',', ': '))
            testChain.append(temp)
        pprint.pprint(testChain)

        self.chain.append(new_block)
        print("Block's Hash: " + new_block.hash)
        print("Block added")
        if minerRewardAddress == 'default':
            self.reward = 0
        else:
            self.reward = 10
        rewardTrans = Transaction("System", minerRewardAddress, self.reward)
        self.pendingTransaction.append(rewardTrans)
        self.pendingTransaction = []

    # function to check if the blockchain is valid or not by checking current block's hash and previous block's hash
    def isValid(self):
        for x in range(1, len(self.chain)):
            currentBlock = self.chain[x]
            previous_hash = self.chain[x - 1].hash

            if currentBlock.previous_hash != previous_hash:
                return "The Chain is not valid!"
        return "The Chain is valid and secure"

    # function to add the transaction in pending transaction list
    def create_transaction(self, transaction):
        self.pendingTransaction.append(transaction)

    # function to get balance of a person by checking all the transactions
    def get_balance(self, walletAddress):
        balance = 0
        for block in self.chain:
            if block.previous_hash == "":
                # don't check the first block as it has no data
                continue
            for transaction in block.transaction_data:
                if transaction.from_wallet == walletAddress:
                    balance -= transaction.amount
                if transaction.to_wallet == walletAddress:
                    balance += transaction.amount
        return balance


# class to create a transaction between 2 people for a specific amount
class Transaction:
    def __init__(self, from_wallet, to_wallet, amount):
        self.from_wallet = from_wallet
        self.to_wallet = to_wallet
        self.amount = amount

    # function for printing the data
    def __str__(self):
        # str(self.__class__) + ": " +
        return str(self.__dict__)


# main runner code
RPS_money = Blockchain()
while True:
    print("Select an option:- ")
    choice = int(input("1.Mine currency\n2.Check Balance\n3.Send money\n4.Check transactions\n5.Check if chain is "
                       "valid or not\n6.Exit\n"))
    if choice == 1:
        person = str(input("Who is mining?"))
        RPS_money.mining_pending_transactions(person)
        print("")
        print("10 coins are added to", person)
        print("")
    elif choice == 2:
        person = str(input("Whose balance is to be checked?"))
        RPS_money.mining_pending_transactions("default")
        print("")
        print(person + " has " + str(RPS_money.get_balance(person)) + " Coins on their account")
        print("")
    elif choice == 3:
        from_who = str(input("Who is sending money? "))
        to_who = str(input("Who is receiving money? "))
        money = -1
        while money < 0:
            money = float(input("How much money is to be transferred? "))
        RPS_money.create_transaction(Transaction(from_who, to_who, money))
        print("")
        print("Money has been transferred\n")
    elif choice == 4:
        chain_list = RPS_money.chain
        RPS_money.mining_pending_transactions("default")
        print("")
        print("Block 1 :- ")
        count = 2
        print(chain_list[0].transaction_data)
        for i in chain_list[1:]:
            print("Block ", count, ":- ")
            if type(i.transaction_data) == list:
                print("Previous hash:- ", i.previous_hash)
                print("Current hash :- ", i.hash)
                print(*i.transaction_data, sep='\n')
                print("")
            else:
                print(i.transaction_data)
            count = count + 1
        print("")
    elif choice == 5:
        if RPS_money.isValid():
            print("The chain is valid")
        else:
            print("The chain is invalid")
        print("")
    elif choice > 5:
        print("Thank You....Visit again later")
        exit()
    else:
        print("Invalid Option")
