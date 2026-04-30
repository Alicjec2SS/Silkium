# A block contains:
# Một block chứa:
'''
hash của node trước đó
epoch
hash(seller, buyer, item, quantity)
chữ kí của buyer cho đống hash trên
chữ kí của seller cho đống hash trên
code

'''
from __future__ import annotations
from dataclasses import dataclass
from lib.helper import sha256
import json


### STATES
SELL = 1 #mở bán
STOP = 2 #không bán nữa = xóa đơn bán
ADJUST = 3#chỉnh sửa món hàng



#quy định: user id chính là hash(signature_public_key)
@dataclass(frozen=True)
class TransactionBlock:
    def __init__(
        self,
        previous_block,
        epoch,
        information_hash,
        buyer_signed_information_hash,
        seller_signed_information_hash,
        transaction_code,
        buyer_signature_public_key,
        seller_signature_public_key,
    ):
        node_id = previous_block.node_id + 1 if previous_block else 0
        previous_hash = previous_block.hash_code if previous_block else "GENESIS"

        hash_code = sha256(json.dumps({
            "previous_hash": previous_hash,
            "epoch": epoch,
            "information": information_hash,
            "buyer_signed_information_hash": buyer_signed_information_hash,
            "seller_signed_information_hash": seller_signed_information_hash,
            "buyer_signature_public_key": buyer_signature_public_key,
            "seller_signature_public_key": seller_signature_public_key,
            "transaction_code": transaction_code
        }, sort_keys=True, separators=(',', ':')))

        object.__setattr__(self, "node_id", node_id)
        object.__setattr__(self, "previous_block", previous_block)
        object.__setattr__(self, "epoch", epoch)
        object.__setattr__(self, "information_hash", information_hash)
        object.__setattr__(self, "buyer_signed_information_hash", buyer_signed_information_hash)
        object.__setattr__(self, "seller_signed_information_hash", seller_signed_information_hash)
        object.__setattr__(self, "transaction_code", transaction_code)
        object.__setattr__(self, "buyer_signature_public_key", buyer_signature_public_key)
        object.__setattr__(self, "seller_signature_public_key", seller_signature_public_key)
        object.__setattr__(self, "hash_code", hash_code)

@dataclass(frozen=True)
class MarketBlock:
    def __init__(self, previous_block, epoch, title, price_wei, stock,
                 region, expire_at, tags, body, state,
                 seller_signature_public_key):

        node_id = previous_block.node_id + 1 if previous_block else 0
        previous_hash = previous_block.hash_code if previous_block else "GENESIS"

        info = {
            "title": title,
            "price": price_wei,
            "stock": stock,
            "region": region,
            "expire_at": expire_at,
            "tags": sorted(tags)
        }

        hash_code = sha256(json.dumps({
            "previous_hash": previous_hash,
            "epoch": epoch,
            "state": state,
            "seller_signature_public_key": seller_signature_public_key,
            "information_for_search_engine": info,
            "body": body
        }, sort_keys=True, separators=(',', ':')))

        object.__setattr__(self, "node_id", node_id)
        object.__setattr__(self, "previous_block", previous_block)
        object.__setattr__(self, "epoch", epoch)
        object.__setattr__(self, "information_for_search_engine", info)
        object.__setattr__(self, "body", body)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "seller_signature_public_key", seller_signature_public_key)
        object.__setattr__(self, "hash_code", hash_code)

class DHTboard:
    def __init__(self,transaction_block:TransactionBlock, market_block:MarketBlock):
        self.transaction_block = transaction_block
        self.market_block = market_block

        #{
        #   "user":{
        #       "bought":[node_ids],"sold":[node_ids]
        #   }
        #}
        self.transaction_board = {}


        #{
        #   "seller":[
        #       "item_id":{"node_id": k,
        #           "header":[],
        #           "body": any
        #       }
        #   ]
        #}
        self.market_board = {}

    def build_transaction_table(self):
        self.transaction_board = {} #clear_board
        current_node = self.transaction_block
        while current_node:

            buyer = current_node.buyer_signature_public_key
            seller = current_node.seller_signature_public_key
            if buyer not in self.transaction_board:
                self.transaction_board[buyer] = {"bought":[current_node.node_id],"sold":[]}
            else:
                self.transaction_board[buyer]["bought"].append(current_node.node_id)
            if seller not in self.transaction_board:
                self.transaction_board[seller] = {"bought":[],"sold":[current_node.node_id]}
            else:
                self.transaction_board[seller]["sold"].append(current_node.node_id)
            current_node = current_node.previous_block
        return self.transaction_board
    
    def build_market_table(self):
        self.market_board = {}#clear
        current_node = self.market_block
        while current_node:
            seller_signature_public_key = current_node.seller_signature_public_key
            header = current_node.information_for_search_engine
            body = current_node.body
            node_id = current_node.node_id
            item = {"information_for_search_engine":header, "body": body,"node_id":node_id}

            if current_node.state == SELL:
                if seller_signature_public_key not in self.market_board:
                    #Create one
                    self.market_board[seller_signature_public_key] = []
                self.market_board[seller_signature_public_key].append(item)
                

            if current_node.state == STOP:
                self.market_board[seller_signature_public_key].remove(item)

            if current_node.state==ADJUST:
                pass#chà tôi bí rồi xD
            current_node = current_node.previous_block    

        return self.market_board

    def update_transaction_table(self,transaction_block: TransactionBlock):
        current_node = transaction_block
        while current_node.node_id > self.transaction_block.node_id:
            buyer =  current_node.buyer_signature_public_key
            seller = current_node.seller_signature_public_key
            if buyer not in self.transaction_board:
                self.transaction_board[buyer] = {"bought":[current_node.node_id],"sold":[]}
            else:
                self.transaction_board[buyer]["bought"].append(current_node.node_id)
            if seller not in self.transaction_board:
                self.transaction_board[seller] = {"bought":[],"sold":[current_node.node_id]}
            else:
                self.transaction_board[seller]["sold"].append(current_node.node_id)
            current_node = current_node.previous_block
        self.transaction_block = transaction_block
    
    def update_market_table(self,market_block:MarketBlock):
        current_node = market_block
        while current_node.node_id > self.market_block.node_id:
            seller_signature_public_key = current_node.seller_signature_public_key
            if seller_signature_public_key not in self.market_board:
                #Create one
                self.market_board[seller_signature_public_key] = []
            header = current_node.information_for_search_engine
            body = current_node.body
            node_id = current_node.node_id
            item = {"information_for_search_engine":header, "body": body,"node_id":node_id}
            self.market_board[seller_signature_public_key].append(item)
            current_node = current_node.previous_block
        self.market_block = market_block


