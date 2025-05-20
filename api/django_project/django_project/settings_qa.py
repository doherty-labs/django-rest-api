import structlog

from django_project.settings import *  # noqa: F403
from django_project.settings import add_open_telemetry_spans, initialize_opentelemetry

CSRF_TRUSTED_ORIGINS = ["https://xxxxx.com"]

DEBUG = False
IS_PRODUCTION = False
IS_QA = True


SECRET_KEY = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/django_secret_key",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": onepassword_service.get_item(
            DEV_ONEPASSWORD_REFERENCE
            + "digitalocean/postgres_connection_pool_database",
        ),
        "USER": onepassword_service.get_item(
            DEV_ONEPASSWORD_REFERENCE
            + "digitalocean/postgres_connection_pool_username",
        ),
        "PASSWORD": onepassword_service.get_item(
            DEV_ONEPASSWORD_REFERENCE
            + "digitalocean/postgres_connection_pool_password",
        ),
        "HOST": onepassword_service.get_item(
            DEV_ONEPASSWORD_REFERENCE + "digitalocean/postgres_connection_pool_host",
        ),
        "PORT": onepassword_service.get_item(
            DEV_ONEPASSWORD_REFERENCE + "digitalocean/postgres_connection_pool_port",
        ),
        "OPTIONS": {"sslmode": "require"} if not DEBUG else {},
    },
}


BUCKET_NAME = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/bucket_name"
)
BUCKET_KEY = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/bucket_access_key"
)
BUCKET_SECRET = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/bucket_secret_key"
)

do_bucket_endpoint = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/bucket_endpoint"
)
BUCKET_ENDPOINT = "https://" + do_bucket_endpoint if do_bucket_endpoint else None
BUCKET_REGION = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/bucket_region"
)


CDN_BUCKET_NAME = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/cdn_bucket_name"
)
CDN_BUCKET_KEY = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/cdn_bucket_access_key"
)
CDN_BUCKET_SECRET = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/cdn_bucket_secret_key"
)
do_cdn_bucket_endpoint = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/cdn_bucket_endpoint"
)
CDN_BUCKET_ENDPOINT = (
    "https://" + do_cdn_bucket_endpoint if do_cdn_bucket_endpoint else None
)
CDN_BUCKET_REGION = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/cdn_bucket_region"
)

AUTH0_DOMAIN = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "auth0/rest_api_domain"
)
AUTH0_IDENTIFIER = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "auth0/rest_api_identifier"
)

AUTH0_DATABASE_CONNECTION_ID = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "auth0/db_connection_id"
)

AUTH0_GOOGLE_CONNECTION_ID = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "auth0/google_connection_id"
)

AUTH0_REST_API_CLIENT_ID = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "auth0/rest_api_client_id"
)
AUTH0_REST_API_CLIENT_SECRET = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "auth0/rest_api_client_secret"
)

AUTH0_MERCHANT_ROLE_ID = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "auth0/roles_merchant"
)


ELASTIC_SEARCH = {
    "host": onepassword_service.get_item(
        DEV_ONEPASSWORD_REFERENCE + "elastic/url",
    ),
    "port": 9200,
    "user": onepassword_service.get_item(
        DEV_ONEPASSWORD_REFERENCE + "elastic/username",
    ),
    "password": onepassword_service.get_item(
        DEV_ONEPASSWORD_REFERENCE + "elastic/password",
    ),
}

CELERY_BROKER_URL = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "kubernetes/rabbitmq_url",
)
CELERY_RESULT_BACKEND = onepassword_service.get_item(
    DEV_ONEPASSWORD_REFERENCE + "digitalocean/redis_url",
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(CELERY_RESULT_BACKEND)],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": CELERY_RESULT_BACKEND,
    },
}

LOGIN_URL = "/admin/login/"

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

JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "django_project.auth_utils.jwt_get_username_from_payload_handler",
    "JWT_DECODE_HANDLER": "django_project.auth_utils.jwt_decode_token",
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": AUTH0_IDENTIFIER,
    "JWT_ISSUER": "https://" + AUTH0_DOMAIN + "/" if AUTH0_DOMAIN else None,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
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
