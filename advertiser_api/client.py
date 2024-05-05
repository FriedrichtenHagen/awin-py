import os
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime, timedelta
import time
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

from advertiser_api.errors import AwinError, AwinApiError
"""
Implementation of the Awin API functions

Docs: https://wiki.awin.com/index.php/Advertiser_API
"""

class Awin:

    BASE_URL = "https://api.awin.com/"
    """base URL of the Awin HTTP API"""

    def __init__(self, base_url=None, client_id=None, client_secret=None):
        self.base_url = base_url or self.BASE_URL
        
        load_dotenv()
        self.client_id = client_id or os.getenv('CLIENT_ID')
        self.client_secret = client_secret or os.getenv('CLIENT_SECRET')
        
        self.headers = {
            "Authorization": f"Bearer {self.client_secret}"
        }

    def _request(self, path, params=None, method='GET') -> List[Dict[str, Any]]:
            """
            Make a request against the AWIN API.
            Returns the HTTP response, which might be successful or not.

            :param path: the URL path for this request (relative to the Awin API base URL)
            :param params: dictionary of URL parameters (optional)
            :param method: the HTTP request method (default: GET)
            :return: the parsed json response, when the request was successful, or a AwinApiError
            """
            # make the request
            url = urljoin(self.base_url, path)
            response = requests.request(method, url, headers=self.headers, params=params)
            if response.ok:
                try:
                    return response.json()
                except ValueError:
                    raise AwinError(f"Failed to parse response as json: {response.text}")
            else:
                raise AwinApiError.from_response(response)
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        """
        GET accounts
        provides a list of accounts you have access to

        :return: list of ``account`` instances

        https://wiki.awin.com/index.php/API_get_accounts
        """
        accounts = self._request('accounts')
        return accounts
        
    def get_publishers(self) -> List[Dict[str, Any]]:
        """
        GET publishers
        provides a list of publishers you have an active relationship with

        :return: list of ``publisher`` instances

        https://wiki.awin.com/index.php/API_get_publishers
        """
        publishers = self._request(f'advertisers/{self.client_id}/publishers')
        return publishers

    def get_transactions(self, start_date, end_date, date_type='transaction', timezone='UTC', status=None, publisher_id=None, show_basket_products=None)  -> List[Dict[str, Any]]:
        """
        GET transactions (list)
        provides a list of your individual transactions

        :param start_date: date object that specifies the beginning of the selected date range
        :param end_date: date object that specifies the end of the selected date range
        :param date_type: The type of date by which the transactions are selected. Can be 'transaction' or 'validation'. (optional)
        :param timezone: Can be one of the following:
            Europe/Berlin
            Europe/Paris
            Europe/London
            Europe/Dublin
            Canada/Eastern
            Canada/Central
            Canada/Mountain
            Canada/Pacific
            US/Eastern
            US/Central
            US/Mountain
            US/Pacific
            UTC
        :param status: Filter by transaction status. Can be one of the following: pending, approved, declined, deleted
        :param publisherId: Allows filtering by publisher id. Example: 12345 or 12345,67890 for multiple ones
        :param show_basket_products: If &showBasketProducts=true then products sent via Product Level Tracking matched to the transaction can be viewed
        :return: list of ``transaction`` instances

        https://wiki.awin.com/index.php/API_get_transactions_list
        """
        # the maximum date range between startDate and endDate currently supported is 31 days
        # calculate number of requests:
        number_of_days = (end_date - start_date).days
        number_of_requests = number_of_days // 31
        if number_of_requests % 31 != 0 or number_of_days < 31:
            number_of_requests += 1
        print(f'number of request: {number_of_requests}')

        # paginate in steps of 31 days
        result = []
        for i in range(number_of_requests):
            print(f'request number {i}')
            if number_of_requests == 1:
                # only one request
                pag_start_date = start_date
                pag_end_date = end_date
            elif i == number_of_requests - 1:
                # last request
                pag_start_date = start_date + timedelta(days=i * 31)
                pag_end_date = end_date
            else:
                # other requests
                pag_start_date = start_date + timedelta(days=i * 31)
                pag_end_date = pag_start_date + timedelta(days=31)

            # add 1s to end date. This prevents the end date and the start date of the next request from overlapping
            if i > 0:
                pag_start_date += timedelta(seconds=1)

            # Convert datetime to string
            dt_start_str = pag_start_date.strftime("%Y-%m-%dT%H:%M:%S")
            dt_end_str = pag_end_date.strftime("%Y-%m-%dT%H:%M:%S")
            print(f'Start timestamp: {dt_start_str}. End timestamp:{dt_end_str}')
            
            params = {
                'startDate': dt_start_str,
                'endDate': dt_end_str,
                'timezone': timezone,
                'dateType': date_type,
                'status': status,
                'publisherId': publisher_id,
                'showBasketProducts': show_basket_products	
            }

            # make sure rate limit is not reached
            if i % 20 == 0 and i > 0:
                time.sleep(60)

            transactions = self._request(f'advertisers/{self.client_id}/transactions/', params)
            result.append(transactions)
        return result
    

    # GET transactions (by ID)
    # provides individual transactions by ID
    
    # GET reports aggregated by publisher
    # provides aggregated reports for the publishers you work with
    
    # GET reports aggregated by creative
    # provides aggregated reports for the creatives you used
    
    # GET reports aggregated by campaign
    # provides aggregated reports for the campaigns that the publisher promotes