# awin-py

**awin-py** is a python wrapper around the [AWIN API](https://wiki.awin.com/index.php/API).
The goals is to provide an easy to use interface for all AWIN API endpoints.
It handles pagination, rate limiting, errors. Most information needed is available via docstrings, for further details please refer to the [AWIN API docs](https://wiki.awin.com/index.php/API).

```python
>>> from advertiser_api.client import Awin
>>> Awin = Awin(client_id='***', client_secret='***')
>>> start_date = datetime.now() - timedelta(days=361)
>>> end_date = datetime.now()
>>> transactions = Awin.get_transactions(start_date=start_date, end_date=end_date)
>>> len(transactions)
1302
>>> transactions[0]
{"advertiserCost": {"amount": null, "currency": null},
 "advertiserCountry": "DE",
 "advertiserId": 11111,
 "amendReason": null,
 "amended": false,
 "basketProducts": null,
 "campaign": null,
 "clickDate": "2024-05-04T20:54:00",
 "clickDevice": "Android Mobile",
 "clickRefs": {"clickRef": "9184c7g4-9gbb-48g7-9e43-44717t5bed70"},
 "commissionAmount": {"amount": 4.26, "currency": "EUR"},
 "commissionSharingPublisherId": null,
 "commissionSharingSelectedRatePublisherId": null,
 "commissionStatus": "pending",
 "customParameters": [],
 "customerAcquisition": null,
 "customerCountry": "IE",
 "declineReason": null,
 "id": 1591984035,
 "ipHash": "-917875755098098",
 "lapseTime": 286,
 "networkFee": {"amount": 1.19, "currency": "EUR"},
 "oldCommissionAmount": null,
 "oldSaleAmount": null,
 "orderRef": "99439999999",
 "originalSaleAmount": null,
 "paidToPublisher": false,
 "paymentId": 0,
 "publisherId": 426667,
 "publisherUrl": null,
 "saleAmount": {"amount": 42.56, "currency": "EUR"},
 "siteName": "http://www.payback.de",
 "trackedCurrencyAmount": null,
 "transactionDate": "2024-05-14T20:59:00",
 "transactionDevice": "Linux",
 "transactionParts": [{"advertiserCost": null,
                       "amount": 42.56,
                       "commissionAmount": 4.26,
                       "commissionGroupCode": "DEFAULT",
                       "commissionGroupId": 167797,
                       "commissionGroupName": "Default",
                       "trackedParts": [{"amount": 42.56,
                                         "code": "DEFAULT",
                                         "currency": "EUR"}]}],
 "transactionQueryId": 0,
 "type": "Commission group transaction",
 "url": "http://www.payback.de",
 "validationDate": null,
 "voucherCode": "TESTTEST100",
 "voucherCodeUsed": true}
```

If something appears to be broken, please have a look at the [open issues](https://github.com/FriedrichtenHagen/awin-py/issues) and vote for an existing issue or create a new one, if you can't find an issue that describes your problem.

## Features

* Aims to cover all functions of the Awin API (work in progress)
* Python function wrappers for all API endpoints as part of the Awin class
* Support for type hints

## API Functions

awin-py currently only implements a subset of all available API features. This section gives an overview over which API endpoints are accessible through awin-py.

### Available

- Advertiser API
    - GET accounts
    - GET publishers
    - GET transactions (list)
    - GET transactions (ID)
    - GET reports aggregated by publisher
    - GET reports aggregated by creative
    - GET reports aggregated by campaign

### Not yet implemented

- Publisher API
- Transaction Validation API

## License
Copyright 2024 Friedrich ten Hagen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


