from __future__ import annotations

import json
import logging
import uuid
from collections.abc import Callable
from functools import wraps
from typing import Any, Self, TypeVar

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search
from injector import Inject
from pydantic import BaseModel

FuncT = TypeVar("FuncT", bound=Callable[..., Any])
ElasticPydanticModel = TypeVar("ElasticPydanticModel", bound=BaseModel)
logger = logging.getLogger(__name__)


class ElasticSearchService[ElasticPydanticModel]:
    es_index_name: str
    pydantic_model: ElasticPydanticModel
    es_index_mapping: dict

    def __init__(
        self,
        es: Inject[Elasticsearch],
    ) -> None:
        self.es = es

    @staticmethod
    def index_check_decorator(func: FuncT) -> FuncT:
        @wraps(func)
        def wrapper(self: Self, *args: tuple, **kwargs: dict) -> FuncT:
            if not self.check_index_exists():
                self.create_index()
            return func(self, *args, **kwargs)

        return wrapper

    @property
    def read_name(self) -> str:
        return self.es_index_name

    @property
    def write_name(self) -> str:
        return self.es_index_name + ".write"

    @property
    def search_dsl(self) -> str:
        return Search(using=self.es, index=self.es_index_name)

    def get_new_index_name(self) -> str:
        guid = str(uuid.uuid4())
        return f"{self.es_index_name}_{guid}"

    def get_index_names_with_alias(self, alias: str) -> list[str]:
        return list(self.es.indices.get_alias(name=alias).keys())

    def safe_create_index(self) -> None:
        if not self.check_index_exists():
            self.create_index()

    def create_index(self) -> ObjectApiResponse:
        index_name = self.get_new_index_name()
        result = self.es.indices.create(
            index=index_name,
            mappings=self.es_index_mapping,
        )
        self.es.indices.update_aliases(
            actions=[
                {
                    "remove": {
                        "index": "*",
                        "alias": self.read_name,
                    },
                },
                {
                    "remove": {
                        "index": "*",
                        "alias": self.write_name,
                    },
                },
                {
                    "add": {
                        "index": index_name,
                        "alias": self.read_name,
                    },
                },
                {
                    "add": {
                        "index": index_name,
                        "alias": self.write_name,
                        "is_write_index": True,
                    },
                },
            ],
        )
        return result

    def create_migration_index(self) -> ObjectApiResponse:
        new_index_name = self.get_new_index_name()
        result = self.es.indices.create(
            index=new_index_name,
            mappings=self.es_index_mapping,
        )

        actions = [
            {
                "remove": {
                    "index": "*",
                    "alias": self.write_name,
                },
            },
            {
                "add": {
                    "index": new_index_name,
                    "alias": self.write_name,
                    "is_write_index": True,
                },
            },
        ]

        read_index_names = self.get_index_names_with_alias(self.read_name)

        if len(read_index_names) == 0:
            actions.append(
                {
                    "add": {
                        "index": new_index_name,
                        "alias": self.read_name,
                    },
                },
            )

        self.es.indices.update_aliases(
            actions=actions,
        )

        return result

    def complete_migration(self) -> ObjectApiResponse:
        old_index_names = self.get_index_names_with_alias(self.read_name)
        new_index_name = self.get_index_names_with_alias(self.write_name)[0]
        for old_index_name in old_index_names:
            if old_index_name == new_index_name:
                continue

            self.es.indices.delete(index=old_index_name, ignore_unavailable=True)

        return self.es.indices.update_aliases(
            actions=[
                {
                    "remove": {
                        "index": "*",
                        "alias": self.read_name,
                    },
                },
                {
                    "add": {
                        "index": new_index_name,
                        "alias": self.read_name,
                    },
                },
            ],
        )

    def update_index_mapping(self) -> ObjectApiResponse:
        return self.es.indices.put_mapping(
            index=self.write_name,
            body=self.es_index_mapping,
        )

    def delete_index(self) -> ObjectApiResponse:
        self.es.indices.delete_alias(
            index="*",
            name=self.read_name,
        )
        self.es.indices.delete_alias(
            index="*",
            name=self.write_name,
        )
        return self.es.indices.delete(index=self.write_name, ignore_unavailable=True)

    def check_index_exists(self) -> ObjectApiResponse:
        return self.es.indices.exists(index=self.write_name) and self.es.indices.exists(
            index=self.read_name,
        )

    def refresh_index(self) -> ObjectApiResponse:
        return self.es.indices.refresh(index=self.write_name)

    def get_count(self) -> ObjectApiResponse:
        return self.es.count(index=self.read_name)["count"]

    @index_check_decorator
    def add(
        self,
        model_id: str,
        doc_data: ElasticPydanticModel,
    ) -> ObjectApiResponse | None:
        return self.es.index(
            index=self.write_name,
            id=model_id,
            document=doc_data.model_dump(),
            refresh=True,
        )

    @index_check_decorator
    def remove(self, model_id: str) -> ObjectApiResponse | None:
        self.es.delete(index=self.write_name, id=model_id, refresh=True)

    @index_check_decorator
    def get(self, model_id: str) -> ElasticPydanticModel | None:
        res = self.es.get(index=self.read_name, id=model_id)["_source"]
        if res:
            return self.pydantic_model.model_validate(**res)
        return None

    @index_check_decorator
    def update(
        self,
        model_id: str,
        doc_data: ElasticPydanticModel,
    ) -> ObjectApiResponse:
        return self.es.update(
            index=self.write_name,
            id=model_id,
            doc=doc_data.model_dump(),
            refresh=True,
            doc_as_upsert=True,
        )

    @index_check_decorator
    def search(
        self,
        query: dict | None = None,
        size: int | None = None,
        suggest: dict | None = None,
        aggs: dict | None = None,
        sort: list[dict] | None = None,
    ) -> ObjectApiResponse:
        return self.es.search(
            index=self.read_name,
            query=query,
            suggest=suggest,
            size=size,
            aggs=aggs,
            sort=sort,
        )

    def bulk_add_docs(self, documents: list[ElasticPydanticModel]) -> int:
        actions = [
            {
                "_index": self.write_name,
                "_op_type": "index",
                "_id": doc.model_dump().get("id"),
                "_source": doc.model_dump(),
            }
            for doc in documents
        ]
        success_count, fails = helpers.bulk(self.es, actions)
        if isinstance(fails, list) and len(fails) > 0:
            msg = f"Failed to bulk add docs: {json.dumps(fails)}"
            raise RuntimeError(msg)
        return success_count
