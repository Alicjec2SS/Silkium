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
from lib.helper import sha256
import json

#quy định: user id chính là hash(signature_public_key)

class TransactionBlock:
    def __init__(
        self,
        previous_block: "TransactionBlock | None",
        epoch: int,
        information_hash: str,#hash(item, quantity, price, sum_price)
        buyer_signed_information_hash: str,
        seller_signed_information_hash: str,
        transaction_code: str,
        buyer_signature_public_key:str,
        seller_signature_public_key:str,
    ):
        self.node_id = previous_block.node_id + 1 if previous_block else 0
        self.previous_block = previous_block
        self.epoch = epoch
        self.information_hash = information_hash
        self.buyer_signed_information_hash = buyer_signed_information_hash
        self.seller_signed_information_hash = seller_signed_information_hash
        self.transaction_code = transaction_code
        self.buyer_signature_public_key = buyer_signature_public_key
        self.seller_signature_public_key = seller_signature_public_key

        previous_hash = previous_block.hash_code if previous_block else "GENESIS"

        self.hash_code = sha256(
            json.dumps(
                {
                    "previous_hash":str(previous_hash),
                    "epoch":str(epoch),
                    "information":str(information_hash),
                    "buyer_signed_information_hash":str(buyer_signed_information_hash),
                    "seller_signed_information_hash":str(seller_signed_information_hash),
                    "buyer_signature_public_key":str(buyer_signature_public_key),
                    "seller_signature_public_key":str(seller_signature_public_key),
                    "transaction_code":str(transaction_code)
                },sort_keys=True, separators=(',', ':')
            )
        )

class MarketBlock:#Block dùng để lưu trữ các món hàng
    def __init__(self, 
                 previous_block:"MarketBlock | None",
                 epoch:int,  
                 header: list, 
                 body: str,
                 seller_signature_public_key: str):
        self.previous_block = previous_block
        self.node_id = previous_block.node_id + 1 if previous_block else 0
        self.epoch = epoch
        self.header = header # lưu tags

        #header: [<Tên vật phẩm>, <giá tiền một món>, <vùng địa lí>, <các tags hàng khác>]

        #Cụ thể một xíu về cái vùng địa lý, nó sẽ có dạng RR-CCC
        #ví dụ: GLOBAL
        #VN
        #VN-HCM
        #VN-HN
        #VN-GL
        #SEA
        #EU
        #US-WEST,....

        self.body = body
        self.seller_signature_public_key = seller_signature_public_key

        previous_hash = previous_block.hash_code if previous_block else "GENESIS"

        self.hash_code = sha256(
            json.dumps(
                {
                    "previous_hash":previous_hash,
                    "epoch":epoch,
                    "seller_signature_public_key":seller_signature_public_key,
                    "header": header,
                    "body": body
                },sort_keys=True, separators=(',', ':')
            )
        )



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
            if seller_signature_public_key not in self.market_board:
                #Create one
                self.market_board[seller_signature_public_key] = []
            header = current_node.header
            body = current_node.body
            node_id = current_node.node_id
            item = {"header":header, "body": body,"node_id":node_id}
            self.market_board[seller_signature_public_key].append(item)
            current_node = current_node.previous_block


