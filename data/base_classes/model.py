from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Model(ABC):
    @abstractmethod
    def get_id(self) -> Optional[int]:
        raise NotImplementedError
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError
