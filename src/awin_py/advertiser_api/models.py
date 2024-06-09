from typing import Optional, List
from uuid import UUID
from datetime import datetime


class AdvertiserCost:
    amount: Optional[float]
    currency: Optional[str]

    def __init__(self, amount: Optional[float], currency: Optional[str]) -> None:
        self.amount = amount
        self.currency = currency


class ClickRefs:
    click_ref: UUID

    def __init__(self, click_ref: UUID) -> None:
        self.click_ref = click_ref


class CustomParameter:
    key: int
    value: str

    def __init__(self, key: int, value: str) -> None:
        self.key = key
        self.value = value


class TrackedPart:
    amount: float
    code: str
    currency: str

    def __init__(self, amount: float, code: str, currency: str) -> None:
        self.amount = amount
        self.code = code
        self.currency = currency


class TransactionPart:
    advertiser_cost: None
    amount: float
    commission_amount: float
    commission_group_code: str
    commission_group_id: int
    commission_group_name: str
    tracked_parts: List[TrackedPart]

    def __init__(self, advertiser_cost: None, amount: float, commission_amount: float, commission_group_code: str, commission_group_id: int, commission_group_name: str, tracked_parts: List[TrackedPart]) -> None:
        self.advertiser_cost = advertiser_cost
        self.amount = amount
        self.commission_amount = commission_amount
        self.commission_group_code = commission_group_code
        self.commission_group_id = commission_group_id
        self.commission_group_name = commission_group_name
        self.tracked_parts = tracked_parts


class Transaction:
    advertiser_cost: AdvertiserCost
    advertiser_country: str
    advertiser_id: int
    amend_reason: None
    amended: bool
    basket_products: None
    campaign: None
    click_date: datetime
    click_device: str
    click_refs: ClickRefs
    commission_amount: AdvertiserCost
    commission_sharing_publisher_id: None
    commission_sharing_selected_rate_publisher_id: None
    commission_status: str
    custom_parameters: List[CustomParameter]
    customer_acquisition: None
    customer_country: str
    decline_reason: None
    id: int
    ip_hash: str
    lapse_time: int
    network_fee: AdvertiserCost
    old_commission_amount: None
    old_sale_amount: None
    order_ref: str
    original_sale_amount: None
    paid_to_publisher: bool
    payment_id: int
    publisher_id: int
    publisher_url: None
    sale_amount: AdvertiserCost
    site_name: str
    tracked_currency_amount: None
    transaction_date: datetime
    transaction_device: str
    transaction_parts: List[TransactionPart]
    transaction_query_id: int
    type: str
    url: str
    validation_date: None
    voucher_code: str
    voucher_code_used: bool

    def __init__(self, **kwargs):
        # Convert keys from camel case to snake case
        converted_kwargs = {self._to_snake_case(key): value for key, value in kwargs.items()}
        # Initialize attributes
        for key, value in converted_kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def _to_snake_case(string):
        return ''.join(['_' + c.lower() if c.isupper() else c for c in string]).lstrip('_')

    # def __init__(self, advertiser_cost: AdvertiserCost, advertiser_country: str, advertiser_id: int, amend_reason: None, amended: bool, basket_products: None, campaign: None, click_date: datetime, click_device: str, click_refs: ClickRefs, commission_amount: AdvertiserCost, commission_sharing_publisher_id: None, commission_sharing_selected_rate_publisher_id: None, commission_status: str, custom_parameters: List[CustomParameter], customer_acquisition: None, customer_country: str, decline_reason: None, id: int, ip_hash: str, lapse_time: int, network_fee: AdvertiserCost, old_commission_amount: None, old_sale_amount: None, order_ref: str, original_sale_amount: None, paid_to_publisher: bool, payment_id: int, publisher_id: int, publisher_url: None, sale_amount: AdvertiserCost, site_name: str, tracked_currency_amount: None, transaction_date: datetime, transaction_device: str, transaction_parts: List[TransactionPart], transaction_query_id: int, type: str, url: str, validation_date: None, voucher_code: str, voucher_code_used: bool) -> None:
    #     self.advertiser_cost = advertiser_cost
    #     self.advertiser_country = advertiser_country
    #     self.advertiser_id = advertiser_id
    #     self.amend_reason = amend_reason
    #     self.amended = amended
    #     self.basket_products = basket_products
    #     self.campaign = campaign
    #     self.click_date = click_date
    #     self.click_device = click_device
    #     self.click_refs = click_refs
    #     self.commission_amount = commission_amount
    #     self.commission_sharing_publisher_id = commission_sharing_publisher_id
    #     self.commission_sharing_selected_rate_publisher_id = commission_sharing_selected_rate_publisher_id
    #     self.commission_status = commission_status
    #     self.custom_parameters = custom_parameters
    #     self.customer_acquisition = customer_acquisition
    #     self.customer_country = customer_country
    #     self.decline_reason = decline_reason
    #     self.id = id
    #     self.ip_hash = ip_hash
    #     self.lapse_time = lapse_time
    #     self.network_fee = network_fee
    #     self.old_commission_amount = old_commission_amount
    #     self.old_sale_amount = old_sale_amount
    #     self.order_ref = order_ref
    #     self.original_sale_amount = original_sale_amount
    #     self.paid_to_publisher = paid_to_publisher
    #     self.payment_id = payment_id
    #     self.publisher_id = publisher_id
    #     self.publisher_url = publisher_url
    #     self.sale_amount = sale_amount
    #     self.site_name = site_name
    #     self.tracked_currency_amount = tracked_currency_amount
    #     self.transaction_date = transaction_date
    #     self.transaction_device = transaction_device
    #     self.transaction_parts = transaction_parts
    #     self.transaction_query_id = transaction_query_id
    #     self.type = type
    #     self.url = url
    #     self.validation_date = validation_date
    #     self.voucher_code = voucher_code
    #     self.voucher_code_used = voucher_code_used