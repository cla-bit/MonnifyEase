from monnifyease import Monnify


monnify_client = Monnify()

print(f"List Transactions: {monnify_client.transactions.list_transaction()}")
