import os
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime, timedelta


from advertiser_api.errors import AwinError, PersonioApiError
"""
Implementation of the Awin API functions

Docs: https://wiki.awin.com/index.php/Advertiser_API
"""

class Awin:

    BASE_URL = "https://api.awin.com/"
    """base URL of the Personio HTTP API"""

    def __init__(self, base_url=None, client_id=None, client_secret=None):
        self.base_url = base_url or self.BASE_URL
        
        load_dotenv()
        self.client_id = client_id or os.getenv('CLIENT_ID')
        self.client_secret = client_secret or os.getenv('CLIENT_SECRET')
        
        self.headers = {
            "Authorization": f"Bearer {self.client_secret}"
        }

    def request(self, path, params=None, method='GET'):
            """
            Make a request against the AWIN API.
            Returns the HTTP response, which might be successful or not.

            :param path: the URL path for this request (relative to the Personio API base URL)
            :param method: the HTTP request method (default: GET)
            :param params: dictionary of URL parameters (optional)
            :param headers: contains the api secret
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
                raise PersonioApiError.from_response(response)
    
    def get_accounts(self):
        """
        GET accounts
        provides a list of accounts you have access to

        :return: list of ``account`` instances

        https://wiki.awin.com/index.php/API_get_accounts
        """
        accounts = self.request('accounts')
        return accounts
        
    def get_publishers(self):
        """
        GET publishers
        provides a list of publishers you have an active relationship with

        :return: list of ``publisher`` instances

        https://wiki.awin.com/index.php/API_get_publishers
        """
        publishers = self.request(f'advertisers/{self.client_id}/publishers')
        return publishers

    def get_transactions(self, start_date, end_date, date_type='transaction', timezone='UTC', status=None, publisher_id=None, show_basket_products=None):
        """
        GET transactions (list)
        provides a list of your individual transactions

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

        # paginage in steps of 31 days
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
            transactions = self.request(f'advertisers/{self.client_id}/transactions/', params)
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