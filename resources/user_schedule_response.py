from pydantic import BaseModel


class UserScheduleResponse(BaseModel):
    id: str
    name: str
    date: str
    shift: str
