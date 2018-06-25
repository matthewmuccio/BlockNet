SimpleBlockchainApp
===================
A simple, fully-functional blockchain-based project which implements a public blockchain from scratch and a simple Flask web application to leverage it.

Project
-------
- Objective: to build a simple web application using a public blockchain that allows users to share information over a decentralized network.
- Because the content will be stored on the blockchain, it is immutable and permanent (more below).
- Defining the structure of the data that will be stored on the blockchain:
- A post is a message posted by any user on our application, it must have three properties: content, author, and timestamp.

Process
-------
- Using Flask microframework, create endpoints for different functions of the blockchain, such as adding a transaction.
- Then, run the scripts on multiple machines in order to create a decentralized network.
- Build a simple UI that interacts with the blockchain and stores information for any use case.
- For instance, content sharing, P2P payments, chatting, or e-commerce.

Background
----------
Public blockchain
- A public blockchain network is completely decentralized and open to the public.
- No one entity has control over the network and they are secure in that data cannot be changed once validated on the blockchain.
- Anyone can join and participate.
- Examples: Bitcoin, Ethereum

Private blockchain
- A private blockchain network is primarily used by businesses who need greater privacy, security, and speed of transactions.
- Participants need an invitation to join.
- They operate quite similarly to public blockchains but have access controls that limit who can participate in the network.
- It operates like modern centralized database systems that restrict access to certain users.
- One or more entities control the network.
- Causes users to still have to rely on third-parties to transact.
- Example: Ripple, Hyperledger

Brief History of Bitcoin
- In 2008, a whitepaper was released by an individual or group under the identifier Satoshi Nakamoto
- Titled "Bitcoin: A Peer-to-Peer Electronic Cash System."
- The paper combined cryptographic techniques and a peer-to-peer network without the need to trust a centralized authority to make payments from one person to another.
- It also introduced a distributed system of storing data (blockchain).
- We now know this concept has far wider applicability than just payments, or cryptocurrencies.
- Blockchain technology has exploded across nearly every industry.
- It is now the underlying technology behind:
  - Fully digital cryptocurrencies (i.e., Bitcoin)
  - Distributed copmuting technologies (i.e., Ethereum)
  - Open-source frameworks (i.e., Hyperledger Fabric)

Blockchain Basics
-----------------
Blockchain Technology
- In simplest terms, blockchain is a mechanism for storing digital data.
- The data can literally be anything.
- The data can even be files, it doesn't matter.
- In the case of Bitcoin, it is the transactions (transfers of Bitcoin from one account to another).
- The data is stored in the form of blocks, which are chained together using hashes.
- Storing data in BLOCKs + using hashes to CHAIN them together = blockchain

Characteristics of Blockchain Networks
- All of the "magic" in blockchain comes from the way this data is added and stored in the blockchain.
- This yields some highly desirable and powerful characteristics:
  - Immutability of history
  - Un-hackability of the system
  - Persistence of the data
  - No single point of failure

Development
-----------
1. Store transactions into blocks
- We will be storing our data in JSON, a widely-used format.
- The generic term "data" is often used interchangeably with the term "transactions" on the Internet.
- The transactions in the application are packed into blocks.
- A block can contain one or many transactions.
- The blocks containing the transactions are generated frequently and added to the blockchain.
- Each block will have a unique ID, since there can be multiple blocks.

2. Make the blocks immutable
- We want to detect any kind of tampering in the data stored inside the block.
- In blockchain technology, this is accomplished using a hash function.
- It is a function that takes data of any size and produces data of a fixed sizse from it, which generally works to identify the input.
- The Python Standard Library has a hashlib library with a SHA-256 and SHA-512 hashing function.
- The characteristics of an ideal hash function are:
  - It should be computationally easy to compute.
  - Even a single bit change in data should make the hash change altogether.
  - It should not be possible to guess the input from the output hash.
- We will store the hash of every block in a field inside a Block object to act like a digital fingerprint of data contained in it.
- Note: In most cryptocurrencies, the individual transactions in the block are also hashed, to form a hash tree, and the root of the tree might be used as the hash of the block.
  - However, it is not a necessary requirement for the functioning of the blockchain.

3. Chain the blocks
- The blocks themselves are now set up.
- The blockchain is a collection of blocks, and we must implement it accordingly.
- We could store all of the blocks in a list (array) in Python, but it would not work.
  - It is not sufficient.
  - Someone could intentionally replace a block at a previous index in the collection/list.
- In our current (unfinished) implementation, creating a new block with altered transactions, computing the hash, and replacing it with any older block works and it should not.
- We must maintain the immutability and order of the blocks in some way.
- We need a way to ensure that any change in the past blocks invalidates the entire chain.
- One way to do this is to chain the blocks by the hash.
  - By chaining, I mean to include the hash of the previous block in the current block.
- If the content of any of the previous blocks change, the hash of the block would change, which would lead to a mismatch with the previous_hash field in the next block.
- If every block will be linked to the previous block by the previous_hash field, we must manually generate the very first block ourselves.
- The very first block is called the genesis block, and it is generated manually or by some unique logic, in most cases.
