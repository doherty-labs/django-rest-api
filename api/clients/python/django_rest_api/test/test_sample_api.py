# coding: utf-8

"""
    REST API

    API for all things …

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from django_rest_api.api.sample_api import SampleApi  # noqa: E501


class TestSampleApi(unittest.TestCase):
    """SampleApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SampleApi()

    def tearDown(self) -> None:
        pass

    def test_list_auth_view_tests(self) -> None:
        """Test case for list_auth_view_tests"""
        pass


if __name__ == "__main__":
    unittest.main()