from abc import ABC, abstractmethod
from typing import Optional, Sequence

from data.base_classes.model import Model

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, model: Model) -> Model:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: int) -> Optional[Model]:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> Sequence[Model]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, model: Model) -> Optional[Model]:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        raise NotImplementedError
