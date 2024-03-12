""" Wrapper classes for various Synchronous Monnify API endpoints,
providing simplified access to functionality in Monnify
"""

from monnifyease.apis import Transactions
from monnifyease.base import MonnifyRequestClient


class Monnify(MonnifyRequestClient):
    """Monnify acts as a wrapper around various client APIs to
    interact with the Monnify API
    """

    def __init__(self, api_key=None, secret_key=None):
        super().__init__(api_key, secret_key)
        self.transactions = Transactions(api_key, secret_key)
