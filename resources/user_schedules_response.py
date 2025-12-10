from pydantic import BaseModel


class UserSchedulesResponse(BaseModel):
    id: str
    name: str
    schedules: dict
