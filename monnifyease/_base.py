"""
Base client API for Monnify API with methods for handling HTTP requests, authentication using a secret key,
constructing HTTP headers, joining URLs with the API base URL, and logging response information.
"""
import base64
import json
import logging

# from datetime import time, date
# from typing import Union

from urllib.parse import urljoin
from decouple import config

import requests


logger = logging.getLogger(__name__)

MONNIFY_TEST_SECRET_KEY = config("MONNIFY_TEST_SECRET_KEY")
MONNIFY_TEST_API_KEY = config("MONNIFY_TEST_API_KEY")

MONNIFY_LIVE_SECRET_KEY = config("MONNIFY_LIVE_SECRET_KEY")
MONNIFY_LIVE_API_KEY = config("MONNIFY_LIVE_API_KEY")


class MonnifyBaseClient:
    """Base Client API for Monnify API"""

    _MONNIFY_SAND_BOX_URL = "https://sandbox.monnify.com/api/"
    _MONNIFY_LIVE_BOX_URL = "https://api.monnify.com/api/"
    _VALID_HTTP_METHODS = {"GET", "POST", "PUT", "DELETE"}

    def __init__(self, environment: str = "test") -> str:
        """
        Initialize the Monnify Base Client with the chosen environment

        :param: environment: the environment platform you want to connect

        :return
        """
        self._environment = environment

        if self._environment not in ("test", "live"):
            logger.error(
                "Kindly ensure you have either 'test' or 'live' environment variables"
            )
            raise ValueError(
                "Kindly ensure you have either 'test' or 'live' environment variables"
            )

        # load base url specific configuration
        self._base_url = {
            "test": self._MONNIFY_SAND_BOX_URL,
            "live": self._MONNIFY_LIVE_BOX_URL,
        }[self._environment]

        # Load environment specific configurations
        self._api_key = {
            "test": MONNIFY_TEST_API_KEY,
            "live": MONNIFY_LIVE_API_KEY,
        }[self._environment]

        self._secret_key = {
            "test": MONNIFY_TEST_SECRET_KEY,
            "live": MONNIFY_LIVE_SECRET_KEY,
        }[self._environment]

        # Raise an error if MONNIFY_API_KEY and MONNIFY_SECRET_KEY are not set in the instance or environment variables
        if not self._api_key and self._secret_key:
            logger.error(
                "Kindly ensure you have API_KEY and SECRET_KEY variables intact"
            )
            raise ValueError(
                "Kindly ensure you have API_KEY and SECRET_KEY variables intact"
            )

        self._session = requests.Session()

    def _get_authorization_header(self):
        """
        :return:
        """
        authentication = f"Basic {base64.b64encode(f'{self._api_key}:{self._secret_key}'.encode()).decode('utf-8')}"
        return authentication

    def _generate_access_token(self):
        """
        :return:
        """

        try:
            auth_header = self._get_authorization_header()
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "User-Agent": "monnifyease/0.1.0",
            }
            token_request_body = {"grant_type": "authorization_code"}
            access_response = self._session.post(
                url=self._join_url("v1/auth/login"),
                headers=headers,
                json=token_request_body
            )
            access_response = access_response.json()
            return access_response["responseBody"]["accessToken"]
        except requests.RequestException as error:
            logger.error("Error %s:", error)
            raise

    def _join_url(self, path: str):
        """
        Join URL with Paystack API URL
        :param path:
        :return:
        """
        if path.startswith("/"):
            path = path[1:]

        if self._environment == "test":
            return urljoin(self._base_url, path)

        return urljoin(self._base_url, path)

    def _auth_request_header(self):
        """
        :return:
        """
        self._access_token = self._generate_access_token()
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "User-Agent": "monnifyease/0.1.0",
        }

    def _request_url(
        self, method: str, url: str, data: dict = None, params: dict = None, **kwargs
    ):
        """
        :param method:
        :param url:
        :param data:
        :param params:
        :param kwargs:
        :return:
        """
        if method.upper() not in self._VALID_HTTP_METHODS:
            logger.error(
                f"Invalid HTTP method. Supported methods are GET, POST, PUT, DELETE. : %s",
                {method},
            )
            raise ValueError(
                f"Invalid HTTP method. Supported methods are GET, POST, PUT, DELETE. : {method}"
            )
        url = self._join_url(url)
        # Filtering params and data, then converting data to JSON
        params = (
            {key: value for key, value in params.items() if value is not None}
            if params
            else None
        )
        data = json.dumps(data) if data else None
        try:
            with self._session.request(
                method,
                headers=self._auth_request_header(),
                url=url,
                data=data,
                params=params,
                **kwargs,
                timeout=10,
            ) as response:
                logger.info("Response Status Code: %s", response.status_code)
                logger.info("Response JSON: %s", response.json())

                print(response.request.headers)
                print(response.headers)
                return response.json()
        except requests.RequestException as error:
            logger.error("Error %s:", error)
            raise


class MonnifyRequestClient(MonnifyBaseClient):
    """Monnify Request"""

    def _request_url_method(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        **kwargs
    ):
        """
        :param method:
        :param endpoint:
        :param data:
        :param params:
        :param kwargs:
        :return:
        """
        return self._request_url(method, url=endpoint, data=data, params=params, **kwargs)

    def _get(self, endpoint: str, params: dict = None, **kwargs):
        """
        :param endpoint:
        :param params:
        :param kwargs:
        :return:
        """
        return self._request_url_method("GET", endpoint, params, **kwargs)

    def _post(self, endpoint: str, data: dict = None, **kwargs):
        """
        :param endpoint:
        :param data:
        :param kwargs:
        :return:
        """
        return self._request_url_method("POST", endpoint=endpoint, data=data, **kwargs)

    def _put(self, endpoint: str, data: dict = None, **kwargs):
        """
        :param endpoint:
        :param data:
        :param kwargs:
        :return:
        """
        return self._request_url_method("PUT", endpoint=endpoint, data=data, **kwargs)

    def _delete(self, endpoint: str, **kwargs):
        """
        :param endpoint:
        :param kwargs:
        :return:
        """
        return self._request_url_method("DELETE", endpoint=endpoint, **kwargs)
