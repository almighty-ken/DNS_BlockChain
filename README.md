# A Blockchain Implementation of DNS service
## Ken Cheng
## Nov. 2017

### TODO
1. A tutorial on how to install and run this. Supply a sample use case of the system
	- COMPLETED
2. support of `nslookup` and actual DNS packets
	- using `dnslib`, the dns server thread also has access to the `dns_layer` instance and is thus able to use the function lookup to construct replies.
	- the `resolver` class that is passed into the `udp_resolver` class will utilize the `dns_layer` to do actual lookup.
	- as of a proof of concept, this will not be implemented.

### Abstract
DNS service is the perfect candidate for applications of blockchain. DNS requires multiple servers to reach a consensus on the mapping from the domain namespace to the IP namespace. Moreover, DNS servers are often under DDoS attacks, as there are not many publicly trusted servers and each server is already under heavy traffic. Using a blockchain powered network of DNS servers solves all these problems. Each server automatically reaches a consensus of mapping by maintaining exact replicas of the ledger, which is a chain of all the records of mapping entries. Users can trust any node in the network by requesting a proof of work on the blockchain and comparing it with the other nodes, and this allows better load balancing.

### Dependencies
- python                    3.6.3
- dnslib                    0.9.7
- faker                     0.8.6
- flask                     0.12.2

### Implementation
We implement three separate classes in this project. The first class in the `blockchain` class, which is our datastorage solution. The second class is the `name_trans` class, which helps process requests for namespace translation and appending new entries or modifying old entries. This class is basically the interface between the third class and the first class for regular request processsing. The third class is the `server` class, which uses `flask` as a framework to take care of internet requests, and calls corresponding methods in the `name_trans` class and `blockchain` class.

The file `mapping_generator.py` is used to create sample mappings from hostname to ip and port.

For future development, some progress has been made in making this implementation capable of listening to port 53 DNS packets and resolving the requests. Relevant code can be found in `resolver.py` and `sample_tcp.py`.

### Key Insight
Adding transaction to the system will cost the nodes a transaction fee, and you earn money by creating new blocks. This creates the incentive for nodes to mine for new blocks, which solidifies buffered transactions. Each new block grants the node who mined it ten coins, which means on average, a block that contains ten transactions will be cost-efficient. Thus, nodes will attempt to create blocks with less than ten transactions, thus pushing blocks faster, and generating more proof of work. This stabilizes the chain.

### Sample Use Scenario
The node can be started by
```bash
python ./server.py -p 5000
```
where `-p` is the port the server listens on. Multiple nodes can be launched and simulate a real life usecase. The nodes operate on a RESTful API framework. For API documentation, please refer to the Postman API documentation [page](https://documenter.getpostman.com/view/1302497/blockchain-dns/7EHcC3X) generated.

A sample use scenario is supplied below. Assume we have two nodes already launched in port 5000 and 5001.
```bash
# Register node2 with node1
curl --request POST \
  --url http://0.0.0.0:5000/nodes/new \
  --header 'content-type: application/json' \
  --data '{"nodes":["0.0.0.0:5001"]}'

# Register node1 with node2
curl --request POST \
  --url http://0.0.0.0:5001/nodes/new \
  --header 'content-type: application/json' \
  --data '{"nodes":["0.0.0.0:5000"]}'

# Push 2 transactions into the buffer of node1
curl --request POST \
  --url http://0.0.0.0:5000/dns/new \
  --header 'content-type: application/json' \
  --data '{
	"entry1":{"hostname":"www.google.com","ip":"123.123.123.123","port":"1234"},
	"entry2":{"hostname":"www.apple.com","ip":"456.123.123.123","port":"5678"}
}'

# dump the buffer of node1 to confirm
curl --request GET \
  --url http://0.0.0.0:5000/debug/dump_buffer

# now we force node1 to mine block
curl --request GET \
  --url http://0.0.0.0:5000/debug/force_block

# check quota of node1
curl --request GET \
  --url http://0.0.0.0:5000/debug/get_quota

# dump chain of node2, this should be the same as node1's chain
curl --request GET \
  --url http://0.0.0.0:5001/debug/dump_chain
```

Below is the corresponding output we get:
```json
<!-- this is the reward transaction node 1 was granted -->
[
    {
        "block_index": 3,
        "node": "6828d92f6e76427a9093197994bd73ab",
        "reward": 10
    }
]

<!-- the quota returned will be 28 -->

<!-- Now we check node2's chain -->
{
  "chain": [
    {
      "index": 1, 
      "previous_hash": "1", 
      "proof": 100, 
      "source": "6828d92f6e76427a9093197994bd73ab", 
      "timestamp": 1512426204.571512, 
      "transactions": []
    }, 
    {
      "index": 2, 
      "previous_hash": "e61de53374d3a8782b312ab9338cd67aa7a2246d07111551f32145685d506a5e", 
      "proof": 226, 
      "source": "6828d92f6e76427a9093197994bd73ab", 
      "timestamp": 1512426325.6513438, 
      "transactions": [
        {
          "hostname": "www.google.com", 
          "ip": "123.123.123.123", 
          "port": "1234"
        }
      ]
    }, 
    {
      "index": 3, 
      "previous_hash": "84a6e0fa9835e062cd912633a465b210b1ca2ca7a7be7304a130fbdb62cbadc9", 
      "proof": 346, 
      "source": "6828d92f6e76427a9093197994bd73ab", 
      "timestamp": 1512426325.68392, 
      "transactions": [
        {
          "block_index": 2, 
          "node": "6828d92f6e76427a9093197994bd73ab", 
          "reward": 10
        }, 
        {
          "hostname": "www.apple.com", 
          "ip": "456.123.123.123", 
          "port": "5678"
        }
      ]
    }, 
    {
      "index": 4, 
      "previous_hash": "10b7460cb2e8596712b44383040485b59d2138b1f8db7cf87fd435a9fa48560b", 
      "proof": 57, 
      "source": "6828d92f6e76427a9093197994bd73ab", 
      "timestamp": 1512426531.58557, 
      "transactions": [
        {
          "block_index": 3, 
          "node": "6828d92f6e76427a9093197994bd73ab", 
          "reward": 10
        }
      ]
    }
  ], 
  "length": 4
}

```
