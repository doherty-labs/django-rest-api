import structlog

from django_project.settings import *  # noqa: F403
from django_project.settings import add_open_telemetry_spans, initialize_opentelemetry
from rest_api.services.hcp import HcpVaultSecrets

CSRF_TRUSTED_ORIGINS = ["https://api-qa.dohertylabs.com"]

DEBUG = False
IS_PRODUCTION = False
IS_QA = True

SECRETS_MANAGER = HcpVaultSecrets()

SECRET_KEY = SECRETS_MANAGER.get_secret(
    "django_secret_key",
    "",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": SECRETS_MANAGER.get_secret("pg_dbname", ""),
        "USER": SECRETS_MANAGER.get_secret("pg_username", ""),
        "PASSWORD": SECRETS_MANAGER.get_secret("pg_password", ""),
        "HOST": SECRETS_MANAGER.get_secret("pg_host", ""),
        "PORT": SECRETS_MANAGER.get_secret("pg_port", ""),
        "OPTIONS": {"sslmode": "require"} if not DEBUG else {},
    },
}

ELASTIC_SEARCH = {
    "host": SECRETS_MANAGER.get_secret("elastic_search_url", ""),
    "port": 9200,
    "user": SECRETS_MANAGER.get_secret("elastic_search_username", ""),
    "password": SECRETS_MANAGER.get_secret("elastic_search_password", ""),
}

CELERY_BROKER_URL = SECRETS_MANAGER.get_secret("celery_broker_url", "")
CELERY_RESULT_BACKEND = SECRETS_MANAGER.get_secret("redis_url", "")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(SECRETS_MANAGER.get_secret("redis_url", ""))],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": SECRETS_MANAGER.get_secret("redis_url", ""),
    },
}

GMAPS_API_KEY = SECRETS_MANAGER.get_secret("gmaps_api_key", "")

BUCKET_NAME = SECRETS_MANAGER.get_secret("bucket_name", "")
BUCKET_KEY = SECRETS_MANAGER.get_secret("bucket_key", "")
BUCKET_SECRET = SECRETS_MANAGER.get_secret("bucket_secret", "")
BUCKET_ENDPOINT = "https://" + SECRETS_MANAGER.get_secret("bucket_endpoint", "")
BUCKET_REGION = SECRETS_MANAGER.get_secret("bucket_region", "")


CDN_BUCKET_NAME = SECRETS_MANAGER.get_secret("cdn_bucket_name", "")
CDN_BUCKET_KEY = SECRETS_MANAGER.get_secret("cdn_bucket_key", "")
CDN_BUCKET_SECRET = SECRETS_MANAGER.get_secret("cdn_bucket_secret", "")
CDN_BUCKET_ENDPOINT = "https://" + SECRETS_MANAGER.get_secret("cdn_bucket_endpoint", "")
CDN_BUCKET_REGION = SECRETS_MANAGER.get_secret("cdn_bucket_region", "")


LOGIN_URL = "/admin/login/"
AUTH0_DOMAIN = SECRETS_MANAGER.get_secret("auth_domain", "")
AUTH0_IDENTIFIER = SECRETS_MANAGER.get_secret("auth_identifier", "")

AUTH0_DATABASE_CONNECTION_ID = SECRETS_MANAGER.get_secret(
    "auth_database_connection_id",
    "",
)
AUTH0_GOOGLE_CONNECTION_ID = SECRETS_MANAGER.get_secret("auth_google_connection_id", "")
AUTH0_REST_API_CLIENT_ID = SECRETS_MANAGER.get_secret("auth_rest_api_client_id", "")
AUTH0_REST_API_CLIENT_SECRET = SECRETS_MANAGER.get_secret(
    "auth_rest_api_client_secret",
    "",
)

SENDGRID_API_KEY = SECRETS_MANAGER.get_secret("sendgrid_api_key", "")

TWILIO_ACCOUNT_SID = SECRETS_MANAGER.get_secret("twilio_account_sid", "")
TWILIO_AUTH_TOKEN = SECRETS_MANAGER.get_secret("twilio_auth_token", "")

STRIPE_API_KEY = SECRETS_MANAGER.get_secret("stripe_api_key", "")
STRIPE_WEBHOOK_SECRET = SECRETS_MANAGER.get_secret("stripe_webhook_secret", "")

MIXPANEL_TOKEN = SECRETS_MANAGER.get_secret("mixpanel_token", "")


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": BUCKET_KEY,
            "secret_key": BUCKET_SECRET,
            "bucket_name": BUCKET_NAME,
            "endpoint_url": BUCKET_ENDPOINT,
            "region_name": BUCKET_REGION,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": CDN_BUCKET_KEY,
            "secret_key": CDN_BUCKET_SECRET,
            "bucket_name": CDN_BUCKET_NAME,
            "endpoint_url": CDN_BUCKET_ENDPOINT,
            "region_name": CDN_BUCKET_REGION,
        },
    },
}


STATIC_URL = f"{CDN_BUCKET_ENDPOINT}/"


initialize_opentelemetry()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                add_open_telemetry_spans,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.stdlib.ExtraAdder(),
                structlog.processors.UnicodeDecoder(),
            ],
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"],
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "json_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/logs/json.log",
            "formatter": "json_formatter",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "level": "WARNING",
        },
        "flat_line_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/logs/flat_line.log",
            "formatter": "key_value",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "level": "WARNING",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "flat_line_file", "json_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        add_open_telemetry_spans,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ExtraAdder(),
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
