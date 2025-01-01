from __future__ import annotations

import json
import uuid
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generic, Self, TypeVar

from elasticsearch import Elasticsearch, helpers
from pydantic import BaseModel

if TYPE_CHECKING:
    from elastic_transport import ObjectApiResponse
    from injector import Inject
    from redis import Redis

FuncT = TypeVar("FuncT", bound=Callable[..., Any])
ElasticPydanticModel = TypeVar("ElasticPydanticModel", bound=BaseModel)


class ElasticSearchService(Generic[ElasticPydanticModel]):
    es_index_name: str
    pydantic_model: ElasticPydanticModel
    es_index_mapping: dict
    es_settings: dict

    def __init__(
        self,
        es: Inject[Elasticsearch],
        redis: Inject[Redis],
    ) -> None:
        self.es = es
        self.redis = redis
        self.lock = self.redis.lock(
            f"{self.es_index_name}_index_lock",
            timeout=60 * 60 * 2,
        )

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
            settings=self.es_settings,
        )
        self.es.indices.update_aliases(
            actions=[
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
                    },
                },
            ],
        )
        return result

    def begin_migration(self) -> None:
        self.lock.acquire(blocking=True)
        new_index_name = self.get_new_index_name()
        self.es.indices.create(
            index=new_index_name,
            mappings=self.es_index_mapping,
            settings=self.es_settings,
        )
        actions = [
            {
                "add": {
                    "index": new_index_name,
                    "alias": self.write_name,
                },
            },
        ]
        current_index_names = self.get_index_names_with_alias(self.write_name)
        actions.extend(
            {
                "remove": {
                    "index": index_name,
                    "alias": self.write_name,
                },
            }
            for index_name in current_index_names
        )
        self.es.indices.update_aliases(actions=actions)

    def end_migration(self) -> None:
        current_index_names = self.get_index_names_with_alias(self.read_name)
        migrated_index_names = self.get_index_names_with_alias(self.write_name)

        action = [
            {"remove": {"index": index_name, "alias": self.read_name}}
            for index_name in current_index_names
        ] + [
            {"add": {"index": index_name, "alias": self.read_name}}
            for index_name in migrated_index_names
        ]

        self.es.indices.update_aliases(actions=action)
        for index_name in current_index_names:
            self.es.indices.delete(index=index_name, ignore_unavailable=True)

        self.refresh_index()
        self.lock.release()

    def handle_migration_exception(self) -> None:
        action = []
        new_index_names = self.get_index_names_with_alias(self.write_name)
        current_index_names = self.get_index_names_with_alias(self.read_name)

        action = [
            {"remove": {"index": index_name, "alias": self.write_name}}
            for index_name in new_index_names
        ] + [
            {"add": {"index": index_name, "alias": self.write_name}}
            for index_name in current_index_names
        ]

        self.es.indices.update_aliases(actions=action)
        for index_name in new_index_names:
            self.es.indices.delete(index=index_name, ignore_unavailable=True)

        self.lock.release()

    def update_index_mapping(self) -> ObjectApiResponse:
        return self.es.indices.put_mapping(
            index=self.write_name,
            body=self.es_index_mapping,
        )

    def delete_index(self) -> ObjectApiResponse:
        return self.es.indices.delete(index=self.write_name, ignore_unavailable=True)

    def check_index_exists(self) -> ObjectApiResponse:
        return self.es.indices.exists(index=self.write_name)

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
        if not self.es.exists(index=self.write_name, id=id):
            return self.es.index(
                index=self.write_name,
                id=model_id,
                document=doc_data.dict(),
                refresh=True,
            )
        return None

    @index_check_decorator
    def remove(self, model_id: str) -> ObjectApiResponse | None:
        if self.es.exists(index=self.write_name, id=model_id):
            return self.es.delete(index=self.write_name, id=model_id, refresh=True)
        return None

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
                "_op_type": "create",
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
