# django_rest_api.SampleApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_auth_view_tests**](SampleApi.md#list_auth_view_tests) | **GET** /sample/get | 


# **list_auth_view_tests**
> List[object] list_auth_view_tests()





### Example

```python
import time
import os
import django_rest_api
from django_rest_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = django_rest_api.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with django_rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = django_rest_api.SampleApi(api_client)

    try:
        api_response = api_instance.list_auth_view_tests()
        print("The response of SampleApi->list_auth_view_tests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SampleApi->list_auth_view_tests: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

**List[object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
