from django_project.settings import *  # noqa
from rest_api.services.hcp import HcpVaultSecrets

DEBUG = False

SECRETS = HcpVaultSecrets().get_secret()

SECRET_KEY = SECRETS.get(
    "django_secret_key",
    "",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": SECRETS.get("pg_dbname", ""),
        "USER": SECRETS.get("pg_username", ""),
        "PASSWORD": SECRETS.get("pg_password", ""),
        "HOST": SECRETS.get("pg_host", ""),
        "PORT": SECRETS.get("pg_port", ""),
        "OPTIONS": {"sslmode": "require"} if not DEBUG else {},
    }
}

ELASTIC_SEARCH = {
    "host": SECRETS.get("elastic_search_url", ""),
    "port": 9200,
    "user": SECRETS.get("elastic_search_username", ""),
    "password": SECRETS.get("elastic_search_password", ""),
}

CELERY_BROKER_URL = SECRETS.get("celery_broker_url", "")
CELERY_RESULT_BACKEND = SECRETS.get("redis_url", "")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(SECRETS.get("redis_url", ""))],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": SECRETS.get("redis_url", ""),
    }
}

GMAPS_API_KEY = SECRETS.get("gmaps_api_key", "")

BUCKET_NAME = SECRETS.get("bucket_name", "")
BUCKET_KEY = SECRETS.get("bucket_access_key", "")
BUCKET_SECRET = SECRETS.get("bucket_secret_key", "")
BUCKET_ENDPOINT = "https://" + SECRETS.get("bucket_endpoint", "")
BUCKET_REGION = SECRETS.get("bucket_region", "")


CDN_BUCKET_NAME = SECRETS.get("cdn_bucket_name", "")
CDN_BUCKET_KEY = SECRETS.get("cdn_bucket_access_key", "")
CDN_BUCKET_SECRET = SECRETS.get("cdn_bucket_secret_key", "")
CDN_BUCKET_ENDPOINT = "https://" + SECRETS.get("cdn_bucket_endpoint", "")
CDN_BUCKET_REGION = SECRETS.get("cdn_bucket_region", "")


LOGIN_URL = "/admin/login/"
AUTH0_DOMAIN = SECRETS.get("auth_domain", "")
AUTH0_IDENTIFIER = SECRETS.get("auth_identifier", "")

AUTH0_DATABASE_CONNECTION_ID = SECRETS.get("auth_database_connection_id", "")
AUTH0_GOOGLE_CONNECTION_ID = SECRETS.get("auth_google_connection_id", "")
AUTH0_REST_API_CLIENT_ID = SECRETS.get("auth_rest_api_client_id", "")
AUTH0_REST_API_CLIENT_SECRET = SECRETS.get("auth_rest_api_client_secret", "")

SENDGRID_API_KEY = SECRETS.get("sendgrid_api_key", "")

TWILIO_ACCOUNT_SID = SECRETS.get("twilio_account_sid", "")
TWILIO_AUTH_TOKEN = SECRETS.get("twilio_auth_token", "")

STRIPE_API_KEY = SECRETS.get("stripe_api_key", "")
STRIPE_WEBHOOK_SECRET = SECRETS.get("stripe_webhook_secret", "")

MIXPANEL_TOKEN = SECRETS.get("mixpanel_token", "")
