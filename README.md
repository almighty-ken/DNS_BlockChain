# A Blockchain Implementation of DNS service
## Ken Cheng
## Nov. 2017

### TODO
1. A tutorial on how to install and run this. Supply a sample use case of the system
2. support of `nslookup` and actual DNS packets

### Abstract
DNS service is the perfect candidate for applications of blockchain. DNS requires multiple servers to reach a consensus on the mapping from the domain namespace to the IP namespace. Moreover, DNS servers are often under DDoS attacks, as there are not many publicly trusted servers and each server is already under heavy traffic. Using a blockchain powered network of DNS servers solves all these problems. Each server automatically reaches a consensus of mapping by maintaining exact replicas of the ledger, which is a chain of all the records of mapping entries. Users can trust any node in the network by requesting a proof of work on the blockchain and comparing it with the other nodes, and this allows better load balancing.

### Implementation
We implement three separate classes in this project. The first class in the `blockchain` class, which is our datastorage solution. The second class is the `name_trans` class, which helps process requests for namespace translation and appending new entries or modifying old entries. This class is basically the interface between the third class and the first class for regular request processsing. The third class is the `server` class, which uses `flask` as a framework to take care of internet requests, and calls corresponding methods in the `name_trans` class and `blockchain` class.

### Key Insight
Adding transaction to the system will cost the nodes a transaction fee, and you earn money by creating new blocks. This creates the incentive for nodes to mine for new blocks, which solidifies buffered transactions. Each new block grants the node who mined it ten coins, which means on average, a block that contains ten transactions will be cost-efficient. Thus, nodes will attempt to create blocks with less than ten transactions, thus pushing blocks faster, and generating more proof of work. This stabilizes the chain.