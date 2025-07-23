from abc import abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from rest_api.services.elastic import ElasticSearchService

PydanticType = TypeVar("PydanticType", bound=BaseModel)


class CommonModelRepo[PydanticType]:
    pydantic_model: PydanticType
    es_instance: ElasticSearchService

    def __init__(
        self,
        es_instance: ElasticSearchService,
    ) -> None:
        self.es_instance = es_instance

    @abstractmethod
    def get(self, model_id: int) -> PydanticType:
        pass

    @abstractmethod
    def create(self, data: PydanticType) -> PydanticType:
        pass

    @abstractmethod
    def update(self, model_id: int, data: PydanticType) -> PydanticType:
        pass

    @abstractmethod
    def delete(self, model_id: int) -> None:
        pass
