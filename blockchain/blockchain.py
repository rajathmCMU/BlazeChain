#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 20:17:04 2021

@author: rajath
"""


# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify
 
# Create Chain
class Blockchain:
 
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
 
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
 
    def get_previous_block(self):
        return self.chain[-1]
 
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):    
        previous_block = chain[0]               #previous_block = chain[0] = block1 = dict = therefore
        block_index = 1                            #previous_block = dict  
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
 
# Mining - PoW
# Creating flask Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
 
# Creating a Blockchain obj
blockchain = Blockchain()
 
# Mining new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()        #1st block : i=1, time, p=1, ph=0, hash = 23523
    previous_proof = previous_block['proof']                #2nd block :i=2, time, p=00003435,  ph = 23523, hash = 4243
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congrats nibba, you mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200
 
# Getting the entire Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
 
# Checking if Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    check = blockchain.is_chain_valid(blockchain.chain)
    if check:
        response = {'message' : 'Chain is valid'}
    else : 
        response = {'message' : 'Chain is invalid'}
    return jsonify(response), 200


# Run app
app.run(host = '0.0.0.0', port = 5000)