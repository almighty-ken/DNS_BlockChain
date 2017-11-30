from flask import Flask, jsonify, request
import json
import dns

"""
This layer takes care of DNS request and reponse packets
Additionally support packets adding new entries, which should require
authentication. Other routes implement methods required to maintain
integrity and consistency of the blockchain.
"""

# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the DNS resolver object
dns_resolver = dns_layer()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    # default port for DNS should be 53
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)