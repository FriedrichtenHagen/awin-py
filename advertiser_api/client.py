import os
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv

from advertiser_api.errors import AwinError
"""
Implementation of the Awin API functions

Docs: https://wiki.awin.com/index.php/Advertiser_API
"""

class Awin:

    BASE_URL = "https://api.awin.com/"
    """base URL of the Personio HTTP API"""

    ACCOUNTS_URL = 'accounts'
    PUBLISHERS_URL = ''
    TRANSACTIONS_URL = ''

    def __init__(self, base_url=None, client_id=None, client_secret=None):
        self.base_url = base_url or self.BASE_URL
        
        # Load environment variables from the .env file
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
                pass
                # raise AwinApiError.from_response(response)
    
    def get_accounts(self):
        """
        GET accounts
        provides a list of accounts you have access to

        :return: list of ``Employee`` instances
        """
        accounts = self.request('accounts')
        return accounts
    
    

        # GET accounts
        # provides a list of accounts you have access to
        
        # GET publishers
        # provides a list of publishers you have an active relationship with
        
        # GET transactions (list)
        # provides a list of your individual transactions
        
        # GET transactions (by ID)
        # provides individual transactions by ID
        
        # GET reports aggregated by publisher
        # provides aggregated reports for the publishers you work with
        
        # GET reports aggregated by creative
        # provides aggregated reports for the creatives you used
        
        # GET reports aggregated by campaign
        # provides aggregated reports for the campaigns that the publisher promotes