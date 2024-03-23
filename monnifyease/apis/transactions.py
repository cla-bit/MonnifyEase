""" Wrapper for Monnify Transactions API
The Transactions API allows you to create and manage payments on your integration.
"""

from datetime import date
from typing import Optional, List, Dict
from monnifyease._base import MonnifyRequestClient


class Transactions(MonnifyRequestClient):
    """Monnify Transaction API """

    def initialize_transaction(
            self,
            amount: float,
            customer_name: str,
            customer_email: str,
            payment_reference: str,
            payment_description: str,
            currency: str,
            merchant_contract_code: str,
            payment_methods: Optional[List[str]] = None,
            redirect_url: Optional[str] = None,
            income_split_account: Optional[bool] = None,
            metadata: Optional[Dict[str, str]] = None,
    ) -> dict:
        """
        Create a transaction
        Reference: https://developers.monnify.com/api/#initialize-transaction

        :param: amount
        :param: customer_name
        :param: customer_email
        :param: payment_reference: A unique string of characters that identifies each transaction
        :param: payment_description: Reason of payment
        :param: currency
        :param: merchant_contract_code: The merchant contract code
        :param: redirect_url: A url to redirect to after payment completion
        :param: payment_methods: The method of payment collection
        :param: income_split_account: A way to split payments among subAccounts.
        :param: metadata: pass extra information from customers.

        :return: The response form the API
        :rtype: dict
        """
        data = {
            "amount": amount,
            "customerName": customer_name,
            "customerEmail": customer_email,
            "paymentReference": payment_reference,
            "paymentDescription": payment_description,
            "currencyCode": currency,
            "contractCode": merchant_contract_code,
            "redirectUrl": redirect_url,
            "paymentMethods": payment_methods,
            "incomeSplitConfig": income_split_account,
            "metadata": metadata,
        }
        return self._post("/v1/merchant/transactions/init-transaction", data=data)

    def pay_with_bank_transfer(
            self,
            transaction_reference: str,
            bank_code: str
    ) -> dict:
        """
        Create a transaction
        Reference: https://developers.monnify.com/api/#initialize-transaction

        :param: transaction_reference: This is the transaction reference gotten from the initialize_transaction method
        :param: bank_code

        :return: The response form the API
        :rtype: dict
        """
        data = {
            "transactionReference": transaction_reference,
            "bankCode": bank_code
        }
        return self._post("/v1/merchant/bank-transfer/init-payment", data=data)

    def list_transaction(
            self,
            per_page: Optional[int] = None,
            page_size: Optional[int] = None,
            payment_reference: Optional[str] = None,
            transaction_reference: Optional[str] = None,
            from_amount: Optional[float] = None,
            to_amount: Optional[float] = None,
            amount: Optional[float] = None,
            customer_name: Optional[str] = None,
            customer_email: Optional[str] = None,
            payment_status: Optional[str] = None,
            from_date: Optional[date] = None,
            to_date: Optional[date] = None
    ) -> dict:
        """
        Get all Transactions List
        Reference: https://developers.monnify.com/api/#get-all-transactions

        :param: per_page
        :param: page_size
        :param: payment_reference
        :param: transaction_reference
        :param: from_amount
        :param: to_amount
        :param: amount
        :param: customer_name
        :param: customer_email
        :param: payment_status
        :param: from_date
        :param: to_date

        :return: The response form the API
        :rtype: dict
        """
        params = {
            'per_page': per_page,
            'page_size': page_size,
            'payment_reference': payment_reference,
            'transaction_reference': transaction_reference,
            'from_amount': from_amount,
            'to_amount': to_amount,
            'amount': amount,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'payment_status': payment_status,
            'from_date': from_date,
            'to_date': to_date
        }
        return self._get("/v1/transactions/search", params=params)
