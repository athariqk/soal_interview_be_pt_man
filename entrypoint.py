import datetime
import sys
from pathlib import Path

from utils.api_response import ApiResponse

sys.path.insert(0, str(Path(__file__).parent.absolute()))

from typing import Optional
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager

from data.repositories.schedule_repository import ScheduleRepository
from data.repositories.user_repository import UserRepository
from init_sqlite_db import init_database
from service.schedule_service import ScheduleService
from controller.schedule_controller import ScheduleController


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(title="Soal Programmer", lifespan=lifespan)

user_repo = UserRepository()
schedule_repo = ScheduleRepository()
schedule_service = ScheduleService(user_repo=user_repo, schedule_repo=schedule_repo)
schedule_controller = ScheduleController(schedule_service)


@app.get("/")
def read_root():
    return ApiResponse(
        status="success",
        data={"message": "Soal Programmer", "author": "Ahmad Ghalib Athariq"},
        http_code=200,
    )


@app.get("/schedules", response_model=ApiResponse)
def get_all_schedules(
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    user_id: Optional[str] = None,
) -> ApiResponse:
    return schedule_controller.get_all_schedules(start_date, end_date, user_id)


@app.get("/check-schedule", response_model=ApiResponse)
def get_user_schedule(
    user_id: Optional[str] = None, date: Optional[datetime.date] = None
) -> ApiResponse:
    return schedule_controller.get_user_schedule(user_id, date)


@app.get("/export-schedules", response_class=StreamingResponse)
def export_schedules(
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    user_id: Optional[str] = None,
):
    csv_generator = schedule_controller.export_schedules(start_date, end_date, user_id)
    user_id_str = user_id.zfill(3) if user_id else "all"
    start_date_str = start_date.strftime("%Y-%m-%d") if start_date else "null"
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else "null"
    filename = f"jadwal_shift_{user_id_str}_{start_date_str}_to_{end_date_str}.csv"
    return StreamingResponse(
        csv_generator,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
