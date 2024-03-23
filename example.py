import webbrowser

from monnifyease import Monnify
# from monnifyease.helpers.tool_kit import PaymentMethods

monnify_client = Monnify()
# list_transactions = monnify_client.transactions.list_transaction()
# print(f"List Transactions: {list_transactions}")
create_transaction = monnify_client.transactions.initialize_transaction(
    amount=1000.00,
    customer_name='John Doe',
    customer_email='johndoe@email.com',
    payment_reference="jky234esqd",
    payment_description="Testing this transaction init",
    currency="NGN",
    merchant_contract_code="9498021956",
)

print(f"Transaction success: {create_transaction}")

get_trans_ref = create_transaction
print(get_trans_ref['responseBody']['transactionReference'])

pwt_bank = monnify_client.transactions.pay_with_bank_transfer(
    transaction_reference=get_trans_ref['responseBody']['transactionReference'],
    bank_code="945"
)

print(f"Pay with bank transfer success: {pwt_bank}")

# # Add this line to your main script after printing the transaction success
# checkout_url = create_transaction['responseBody']['checkoutUrl']
# print(f"Checkout URL: {checkout_url}")
#
# # Automatically open the checkout URL in a web browser
# webbrowser.open(checkout_url)
