""" Wrapper classes for various Synchronous Monnify API endpoints,
providing simplified access to functionality in Monnify
"""

from monnifyease.apis import Transactions
from monnifyease._base import MonnifyRequestClient


class Monnify(MonnifyRequestClient):
    """Monnify acts as a wrapper around various client APIs to
    interact with the Monnify API
    """

    def __init__(self, environment="test"):
        super().__init__(environment)
        self.transactions = Transactions(environment)
