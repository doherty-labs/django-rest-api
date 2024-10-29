from unittest.mock import MagicMock
from urllib.parse import urlparse

from elasticsearch import Elasticsearch
from injector import Module, provider, singleton

from django_project import settings


class EsModule(Module):
    @singleton
    @provider
    def elastic_server(self) -> Elasticsearch:
        if (
            settings.ELASTIC_SEARCH.get("user") is not None
            and settings.ELASTIC_SEARCH.get("user") != ""
        ):
            parser_url = urlparse(str(settings.ELASTIC_SEARCH.get("host")))
            out_url = parser_url._replace(
                netloc=parser_url.netloc.replace(str(parser_url.port), "")
            ).geturl()

            es = Elasticsearch(
                [out_url],
                http_auth=(
                    settings.ELASTIC_SEARCH.get("user", ""),
                    settings.ELASTIC_SEARCH.get("password", ""),
                ),
                verify_certs=False,
                max_retries=10,
                retry_on_timeout=True,
            )
        else:
            host_url = (
                "http://"
                + str(settings.ELASTIC_SEARCH.get("host"))
                + ":"
                + str(settings.ELASTIC_SEARCH.get("port"))
            )
            es = Elasticsearch([host_url], verify_certs=False)

        return es


class TestEsModule(Module):
    @singleton
    @provider
    def elastic_server(self) -> Elasticsearch:
        return MagicMock()
