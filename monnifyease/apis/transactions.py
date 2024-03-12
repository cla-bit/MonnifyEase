""" Wrapper for Monnify Transactions API
The Transactions API allows you to create and manage payments on your integration.
"""

from datetime import date
from typing import Optional
from monnifyease.base import MonnifyRequestClient


class Transactions(MonnifyRequestClient):
    """Monnify Transaction API """
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
        Reference: https://developers.monnify.com/api/#get-all-transactions
        :param per_page:
        :param page_size:
        :param payment_reference:
        :param transaction_reference:
        :param from_amount:
        :param to_amount:
        :param amount:
        :param customer_name:
        :param customer_email:
        :param payment_status:
        :param from_date:
        :param to_date:

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
        return self._get("/transactions/search", params=params)
