import datetime
import sys
from pathlib import Path

from utils.api_response import ApiResponse

sys.path.insert(0, str(Path(__file__).parent.absolute()))

from typing import Optional
from fastapi import FastAPI
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
):
    return schedule_controller.get_all_schedules(start_date, end_date, user_id)
