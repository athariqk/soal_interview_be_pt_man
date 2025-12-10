import datetime
from typing import Optional
from fastapi import HTTPException

from resources.user_schedule_response import UserScheduleResponse
from resources.user_schedules_response import UserSchedulesResponse
from service.schedule_service import ScheduleService
from utils.api_response import ApiResponse


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
                status="success", data=UserSchedulesResponse(**result), http_code=200
            )
        else:
            results = self.schedule_service.get_schedules(start_date, end_date)
            return ApiResponse(
                status="success",
                data=[UserSchedulesResponse(**result) for result in results],
                http_code=200,
            )

    def get_user_schedule(
        self, user_id: Optional[str] = None, date: Optional[datetime.date] = None
    ) -> ApiResponse:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        if not date:
            raise HTTPException(status_code=400, detail="date is required")
        if not user_id.isdigit():
            raise HTTPException(
                status_code=400, detail="user_id must be a valid integer"
            )

        result = self.schedule_service.get_user_schedule(int(user_id), date)

        return ApiResponse(
            status="success",
            data=UserScheduleResponse(**result),
            http_code=200,
        )

    def export_schedules(
        self,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
        user_id: Optional[str] = None,
    ):
        if not start_date or not end_date:
            raise HTTPException(
                status_code=400, detail="start_date and end_date are required"
            )

        return self.schedule_service.export_schedules_to_csv(
            start_date, end_date, int(user_id) if user_id else None
        )
