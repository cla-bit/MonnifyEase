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

MONNIFY_SECRET_KEY = config("MONNIFY_SECRET_KEY")
MONNIFY_API_KEY = config("MONNIFY_API_KEY")


class MonnifyBaseClient:
    """Base Client API for Monnify API"""

    _MONNIFY_SAND_BOX_URL = "https://sandbox.monnify.com/api/v1/"
    _VALID_HTTP_METHODS = {"GET", "POST", "PUT", "DELETE"}

    def __init__(self, api_key: str = None, secret_key: str = None) -> None:
        """
        :param api_key:
        :param secret_key:

        :return
        """
        self._api_key = api_key
        self._secret_key = secret_key

        # Default to MONNIFY_API_KEY and MONNIFY_SECRET_KEY if not provided in the instance
        if not self._api_key:
            self._api_key = MONNIFY_API_KEY
        if not self._secret_key:
            self._secret_key = MONNIFY_SECRET_KEY

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
        # url = self._join_url("auth/login")
        try:
            auth_header = self._get_authorization_header()
            headers = {"Authorization": auth_header, "Content-Type": "application/json"}
            token_request_body = {"grant_type": "authorization_code"}
            response = self._session.post(url=self._join_url("auth/login"), headers=headers, json=token_request_body)
            response = response.json()
            return response["responseBody"]["accessToken"]
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
        return urljoin(self._MONNIFY_SAND_BOX_URL, path)

    def _auth_request_header(self):
        """
        :return:
        """
        self._access_token = self._generate_access_token()
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
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
