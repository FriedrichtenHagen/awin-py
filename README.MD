A python wrapper around the AWIN API.
Currently only supports the advertiser api.

Handles pagination, rate limiting, ...




## todo:
- data model:
    kwargs vs explicit naming
    How do I handle the returned models? Is this really that helpful?
- add typing: return types and parameter types

- Error handeling:
    Request failed with HTTP status code 429: request.limit.exceeded. Details: Requests limit '20' times per '1' minutes' is exceeded
    Awin has a throttling system in place that limits the number of API requests to 20 API calls per minute per user.