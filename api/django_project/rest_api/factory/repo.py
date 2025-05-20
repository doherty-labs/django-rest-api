import sys

from injector import Injector

from rest_api.modules.auth0 import Auth0ServiceModule, TestAuth0ServiceModule
from rest_api.modules.cdn_storage import (
    CdnObjectStorageModule,
    TestCdnObjectStorageModule,
)
from rest_api.modules.es_module import EsModule, TestEsModule
from rest_api.modules.geo import GeoModule, TestGeoModule
from rest_api.modules.mixpanel import MixpanelModule, TestMixpanelModule
from rest_api.modules.object_storage import ObjectStorageModule, TestObjectStorageModule
from rest_api.modules.redis_module import RedisModule, TestRedisModule
from rest_api.modules.sendgrid import EmailModule, TestEmailModule
from rest_api.modules.stripe import StripeModule, TestStripeModule
from rest_api.modules.twilio import SMSModule, TestSMSModule

real_injector = Injector(
    [
        RedisModule,
        EsModule,
        GeoModule,
        ObjectStorageModule,
        CdnObjectStorageModule,
        EmailModule,
        StripeModule,
        SMSModule,
        MixpanelModule,
        Auth0ServiceModule,
    ],
)


test_injector = Injector(
    [
        TestRedisModule,
        TestEsModule,
        TestGeoModule,
        TestObjectStorageModule,
        TestCdnObjectStorageModule,
        TestEmailModule,
        TestStripeModule,
        TestSMSModule,
        TestMixpanelModule,
        TestAuth0ServiceModule,
    ],
)

InstanceInjector = test_injector if "pytest" in sys.modules else real_injector
