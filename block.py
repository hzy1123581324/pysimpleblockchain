# coding:utf-8
from errors import NonceNotFoundError, TransactionVerifyError
from pow import ProofOfWork
from block_header import BlockHeader
from transactions import Transaction

class Block(object):
    """A Block
    Attributes:
        _magic_no (int): Magic number
        _block_header (Block): Header of the previous Block.
        _transactions (Transaction): transactions of the current Block.
    """
    MAGIC_NO = 0xBCBCBCBC
    def __init__(self, block_header, transactions):
        self._magic_no = self.MAGIC_NO
        self._block_header = block_header
        self._transactions = transactions

    def mine(self, bc):
        pow = ProofOfWork(self)
        for tx in self._transactions:
            if not bc.verify_transaction(tx):
                raise TransactionVerifyError('transaction verify error')
        try:
            nonce, _ = pow.run()
        except NonceNotFoundError as e:
            print(e)
        self._block_header.nonce = nonce
    
    @classmethod
    def new_genesis_block(cls, coin_base_tx):
        block_header = BlockHeader.new_genesis_block_header()
        return cls(block_header, coin_base_tx)

    @property
    def block_header(self):
        return self._block_header
    
    @property
    def transactions(self):
        return self._transactions
        
    def set_header_hash(self):
        self._block_header.set_hash()
    
    def get_header_hash(self):
        return self._block_header.hash

    def serialize(self):
        return {
            "magic_no": self._magic_no,
            "block_header": self._block_header.serialize(),
            "transactions": [tx.serialize() for tx in self._transactions]
        }
    
    @classmethod
    def deserialize(cls, data):
        block_header_dict = data['block_header']
        block_header = BlockHeader.deserialize(block_header_dict)
        transactions = data["transactions"]
        txs = []
        for transaction in transactions:
            txs.append(Transaction.deserialize(transaction))
        return cls(block_header, txs)

    def __repr__(self):
        return 'Block(_block_header=%s)' % self._block_header