from monnifyease import Monnify

monnify_client = Monnify()
print(f"Loist Transactions: {monnify_client.transactions.list_transaction()}")
