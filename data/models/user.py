import datetime
from typing import Optional, Dict, Any, override
from data.base_classes.model import Model


class User(Model):
    def __init__(self, name: str, start_date: datetime.date, id: Optional[int] = None) -> None:
        self.id = id
        self.name = name
        self.start_date = start_date
    
    @override
    def get_id(self) -> Optional[int]:
        return self.id
    
    @override
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date
        }
