import os
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
import time
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union, Literal
import logging 


from .errors import AwinError, AwinApiError
"""
Implementation of the Awin API functions

Docs: https://wiki.awin.com/index.php/Advertiser_API
"""

class Awin:
    BASE_URL = "https://api.awin.com/"
    """base URL of the Awin HTTP API"""

    def __init__(self, 
                 base_url:str = None, 
                 client_id:str = None, 
                 client_secret:str = None) -> None:
        self.base_url = base_url or self.BASE_URL
        
        load_dotenv()
        self.client_id = client_id or os.getenv('CLIENT_ID')
        self.client_secret = client_secret or os.getenv('CLIENT_SECRET')
        
        self.headers = {
            "Authorization": f"Bearer {self.client_secret}"
        }

    def _request(self, 
                 path:str, 
                 params:str = None, 
                 method='GET') -> List[Dict[str, Any]]:
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
    
    def _paginate_date_range(self, 
                             path:str, 
                             start_date:date, 
                             end_date:date, 
                             is_report:bool, 
                             params=None) -> List[Dict[str, Any]]:
        """
        Paginate over a provided date range.
        Returns a list of results

        :param path: the URL path (relative to the Awin API base URL)
        :param start_date: date object that specifies the beginning of the selected date range
        :param end_date: date object that specifies the end of the selected date range
        :param is_report: boolean to indicate if report endpoint or other. Necessary for date formats
        :param params: dictionary of URL parameters
        :return: list of transactions

        """
        # the maximum date range between startDate and endDate currently supported is 31 days
        # calculate number of requests:
        number_of_days = (end_date - start_date).days
        number_of_requests = number_of_days // 31
        if number_of_requests % 31 != 0 or number_of_days < 31:
            number_of_requests += 1
        logging.info(f'number of requests: {number_of_requests}')
        # paginate in steps of 31 days
        total_transaction_list = []
        for i in range(number_of_requests):
            logging.info(f'current request is number {i}')
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

            if is_report:
                # date in ISO8601 e.g 2017-01-01
                dt_start_str = pag_start_date.date().isoformat()
                dt_end_str = pag_end_date.date().isoformat()
            else:
                # accounts, publishers and transaction endpoints expect timestamps
                # add 1s to end date. This prevents the end date and the start date of the next request from overlapping
                if i > 0:
                    pag_start_date += timedelta(seconds=1)
                # Convert datetime to awin date string format
                dt_start_str = pag_start_date.strftime("%Y-%m-%dT%H:%M:%S")
                dt_end_str = pag_end_date.strftime("%Y-%m-%dT%H:%M:%S")

            logging.info(f'Start date: {dt_start_str}. End date: {dt_end_str}')
            # add start and end date to params
            params['startDate'] = dt_start_str
            params['endDate'] = dt_end_str

            # make sure rate limit is not reached
            if i % 20 == 0 and i > 0:
                time.sleep(60)

            pag_transaction_list = self._request(f'advertisers/{self.client_id}/{path}', params)
            total_transaction_list.extend(pag_transaction_list)
        return total_transaction_list
    
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

    def get_transactions(self, 
                         start_date:date, 
                         end_date:date, 
                         date_type:Optional[Literal['transaction', 'validation']] = 'transaction', 
                         timezone: Optional[Literal[
                         'Europe/Berlin',
                         'Europe/Paris',
                         'Europe/London',
                         'Europe/Dublin',
                         'Canada/Eastern',
                         'Canada/Central',
                         'Canada/Mountain',
                         'Canada/Pacific',
                         'US/Eastern',
                         'US/Central',
                         'US/Mountain',
                         'US/Pacific',
                         'UTC'
                         ]] = 'UTC', 
                         status:Optional[Literal['pending', 'approved', 'declined', 'deleted']] = None, 
                         publisher_id:str = None, 
                         show_basket_products:bool = None)  -> List[Dict[str, Any]]:
        """
        GET transactions (list)
        provides a list of your individual transactions

        :param start_date: date object that specifies the beginning of the selected date range
        :param end_date: date object that specifies the end of the selected date range
        :param date_type: The type of date by which the transactions are selected. Can be 'transaction' or 'validation'. (optional)
        :param timezone: chosen timezone. Defaults to 'UTC'
        :param status: Filter by transaction status. Can be one of the following: pending, approved, declined, deleted
        :param publisherId: Allows filtering by publisher id. Example: 12345 or 12345,67890 for multiple ones
        :param show_basket_products: If &showBasketProducts=true then products sent via Product Level Tracking matched to the transaction can be viewed
        :return: list of ``transaction`` instances

        https://wiki.awin.com/index.php/API_get_transactions_list
        """
        params = {
            'timezone': timezone,
            'dateType': date_type,
            'status': status,
            'publisherId': publisher_id,
            'showBasketProducts': show_basket_products	
        }
        pag_transaction_list = self._paginate_date_range(path='transactions/', start_date= start_date, end_date= end_date, is_report= False, params= params)

        # model_testing_list = []
        # for transaction in total_transaction_list:
        #     model_testing_list.append(Transaction(**transaction))

        return pag_transaction_list

    def get_transactions_by_id(self, 
                               ids: List[str], 
                                     timezone: Optional[Literal[
                                        'Europe/Berlin',
                                        'Europe/Paris',
                                        'Europe/London',
                                        'Europe/Dublin',
                                        'Canada/Eastern',
                                        'Canada/Central',
                                        'Canada/Mountain',
                                        'Canada/Pacific',
                                        'US/Eastern',
                                        'US/Central',
                                        'US/Mountain',
                                        'US/Pacific',
                                        'UTC'
                                     ]] = 'UTC', 
                               show_basket_products: bool = None) -> List[Dict[str, Any]]:
        """
        GET transactions (list)
        provides a list of transactions by id

        :param ids:	List of ids.
        :param timezone: chosen timezone. Defaults to 'UTC'
        :param show_basket_products: If &showBasketProducts=true then products sent via Product Level Tracking matched to the transaction can be viewed
        :return: list of ``transaction`` instances

        https://wiki.awin.com/index.php/API_get_transactions_ids
        """

        # extract ids from comma separated string
        comma_separated_ids = ", ".join(ids)
        logging.info(f'comma separated ids: {comma_separated_ids}')

        params = {
            'ids': comma_separated_ids,
            'timezone': timezone,
            'showBasketProducts': show_basket_products	
        }

        transactions = self._request(f'advertisers/{self.client_id}/transactions/', params)

        # model_testing_list = []
        # for transaction in transactions:
        #     model_testing_list.append(Transaction(**transaction))
        return transactions

    def get_reports_agg_by_publisher(self, 
                                     start_date:date, 
                                     end_date:date, 
                                     date_type:Optional[Literal['transaction', 'validation']] = 'transaction', 
                                     timezone: Optional[Literal[
                                        'Europe/Berlin',
                                        'Europe/Paris',
                                        'Europe/London',
                                        'Europe/Dublin',
                                        'Canada/Eastern',
                                        'Canada/Central',
                                        'Canada/Mountain',
                                        'Canada/Pacific',
                                        'US/Eastern',
                                        'US/Central',
                                        'US/Mountain',
                                        'US/Pacific',
                                        'UTC'
                                     ]] = 'UTC',) -> List[Dict[str, Any]]:
        """
        GET reports aggregated by publisher
        provides aggregated reports for the publishers you work with

        :param start_date: date object that specifies the beginning of the selected date range
        :param end_date: date object that specifies the end of the selected date range
        :param date_type: The type of date by which the transactions are selected. Can be 'transaction' or 'validation'. (optional)
        :param timezone: chosen timezone. Defaults to 'UTC'
        :return: list of ``report`` instances

        https://wiki.awin.com/index.php/API_get_reports_aggrcampaign_adv
        """
        params = {
            'date_type': date_type,
            'timezone': timezone,
        }
        pag_transaction_list = self._paginate_date_range(path='reports/publisher', start_date= start_date, end_date= end_date, is_report= True, params= params)
        return pag_transaction_list
    
    def get_reports_agg_by_creative(self, 
                                     start_date:date, 
                                     end_date:date, 
                                     date_type:Optional[Literal['transaction', 'validation']] = 'transaction', 
                                     region:Optional[Literal['AT', 'AU', 'BE', 'BR', 'BU', 'CA', 'CH', 'DE',
                                        'DK', 'ES', 'FI', 'FR', 'GB', 'IE', 'IT', 'NL', 'NO', 'PL', 'SE',
                                        'US',]] = 'DE',
                                     timezone: Optional[Literal[
                                        'Europe/Berlin',
                                        'Europe/Paris',
                                        'Europe/London',
                                        'Europe/Dublin',
                                        'Canada/Eastern',
                                        'Canada/Central',
                                        'Canada/Mountain',
                                        'Canada/Pacific',
                                        'US/Eastern',
                                        'US/Central',
                                        'US/Mountain',
                                        'US/Pacific',
                                        'UTC'
                                     ]] = 'UTC',) -> List[Dict[str, Any]]:
        """
        GET reports aggregated by creative
        provides aggregated reports for the creatives you used

        :param start_date: date object that specifies the beginning of the selected date range
        :param end_date: date object that specifies the end of the selected date range
        :param date_type: The type of date by which the transactions are selected. Can be 'transaction' or 'validation'. (optional)
        :param region: AT, AU, BE, BR (Brazil programs in BRL), BU (Brazil programs in USD), CA, CH, DE, DK, ES, FI, FR, GB, IE, IT, NL, NO, PL, SE, US,
        :param timezone: chosen timezone. Defaults to 'UTC'
        :return: list of ``report`` instances

        https://wiki.awin.com/index.php/API_get_reports_aggrbycreative_adv
        """
        params = {
            'date_type': date_type,
            'region': region,
            'timezone': timezone,
        }
        pag_transaction_list = self._paginate_date_range(path='reports/creative', start_date= start_date, end_date= end_date, is_report= True, params= params)
        return pag_transaction_list
    
    def get_reports_agg_by_campaign(self, 
                                     start_date:date, 
                                     end_date:date, 
                                     campaign:str = None,
                                     timezone: Optional[Literal[
                                        'Europe/Berlin',
                                        'Europe/Paris',
                                        'Europe/London',
                                        'Europe/Dublin',
                                        'Canada/Eastern',
                                        'Canada/Central',
                                        'Canada/Mountain',
                                        'Canada/Pacific',
                                        'US/Eastern',
                                        'US/Central',
                                        'US/Mountain',
                                        'US/Pacific',
                                        'UTC'
                                     ]] = 'UTC',
                                     publisher_ids:List[int] = None,
                                     include_numbers_without_campaign:bool = False,
                                     interval:Optional[Literal['day', 'month', 'year']] = None) -> List[Dict[str, Any]]:
        """
        GET reports aggregated by campaign
        provides aggregated reports for the campaigns that the publisher promotes

        :param start_date: date object that specifies the beginning of the selected date range
        :param end_date: date object that specifies the end of the selected date range
        :param campaign: The value which was used in &campaign=.
        :param timezone: chosen timezone. Defaults to 'UTC'
        :param publisher_ids: One or more publisher ID.
        :param include_numbers_without_campaign: By default the API just delivers numbers in case of a campaign was associated with the click or the transations.
            If set to "true" the result will also incl. numbers from clicks and transaction without campaign parameter.
            The parameter will BE ignored (default "false") once the parameter "campaign=" contains a valid value.
        :param interval: If set, numbers will be reported in sums per interval (day, month, year).
        :return: list of ``report`` instances

        https://wiki.awin.com/index.php/API_get_reports_aggrbycampaign_adv
        """
        params = {
            'campaign': campaign,
            'timezone': timezone,
            'publisher_ids': publisher_ids,
            'include_numbers_without_campaign': include_numbers_without_campaign,
            'interval': interval
        }
        pag_transaction_list = self._paginate_date_range(path='reports/campaign', start_date= start_date, end_date= end_date, is_report= True, params= params)
        return pag_transaction_list