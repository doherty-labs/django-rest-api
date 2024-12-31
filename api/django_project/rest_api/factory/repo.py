from injector import Injector

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

InstanceInjector = Injector(
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
    ],
)


TestInjector = Injector(
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
    ],
)
