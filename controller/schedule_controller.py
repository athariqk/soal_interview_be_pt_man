import datetime
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel

from service.schedule_service import ScheduleService
from utils.api_response import ApiResponse


class UserScheduleResponse(BaseModel):
    id: str
    name: str
    schedules: dict


class ScheduleController:
    def __init__(self, schedule_service: ScheduleService):
        self.schedule_service = schedule_service

    def get_all_schedules(
        self,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
        user_id: Optional[str] = None,
    ) -> ApiResponse:
        if not start_date or not end_date:
            raise HTTPException(
                status_code=400, detail="start_date and end_date are required"
            )

        if user_id:
            if not user_id.isdigit():
                raise HTTPException(
                    status_code=400, detail="user_id must be a valid integer"
                )
            result = self.schedule_service.get_schedules_by_user(
                start_date, end_date, int(user_id)
            )
            return ApiResponse(
                status="success",
                data=UserScheduleResponse(**result),
                http_code=200
            )
        else:
            results = self.schedule_service.get_schedules(start_date, end_date)
            return ApiResponse(
                status="success",
                data=[UserScheduleResponse(**result) for result in results],
                http_code=200
            )
