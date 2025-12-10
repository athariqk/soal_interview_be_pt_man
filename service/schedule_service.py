import datetime
from typing import List, Optional
from data.repositories.user_repository import UserRepository
from data.repositories.schedule_repository import ScheduleRepository
from data.models.user import User
from data.models.schedule import Schedule, Shift


class ScheduleService:
    def __init__(self, user_repo: UserRepository, schedule_repo: ScheduleRepository):
        self.user_repo = user_repo
        self.schedule_repo = schedule_repo

    def get_schedules(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> List[dict]:
        results: List[dict] = []
        users = self.user_repo.get_all()

        for user in users:
            if not user.id:
                continue

            schedules = self.schedule_repo.get_by_user(user.id)
            schedules.sort(key=lambda x: x.day)

            mapped = self.map_schedule(schedules, start_date, end_date, user.start_date)
            results.append({"id": str(user.id).zfill(3), "name": user.name, "schedules": mapped})

        return results

    def get_schedules_by_user(
        self, start_date: datetime.date, end_date: datetime.date, user_id: int
    ) -> dict:
        user = self.user_repo.get(user_id)
        if not user:
            return {}

        schedules = self.schedule_repo.get_by_user(user_id)
        schedules.sort(key=lambda x: x.day)

        mapped = self.map_schedule(schedules, start_date, end_date, user.start_date)
        return {"id": str(user.id).zfill(3), "name": user.name, "schedules": mapped}

    def map_schedule(
        self,
        schedules: List[Schedule],
        start_date: datetime.date,
        end_date: datetime.date,
        cycle_start_date: datetime.date,
    ) -> dict:
        mapped = {}
        if not schedules:
            return mapped

        cycle_length = (
            max(s.day for s in schedules) + 1
        )  # total panjang siklus (contoh: yohan ada 14 hari)

        schedule_by_day = {s.day: s for s in schedules}

        # NOTE: komentar dibuat oleh Ahmad Ghalib Athariq, bukan chatgpt atau gemini

        # perlu kita offset untuk matching urutan dari hari dalam seminggu
        start_day_offset = cycle_start_date.weekday()

        days_between = (end_date - start_date).days
        for offset in range(days_between + 1):
            # tanggal di antara start_date dan end_date
            actual_date = start_date + datetime.timedelta(days=offset)

            days_since_anchor = (actual_date - cycle_start_date).days
            pattern_index = (days_since_anchor + start_day_offset) % cycle_length
            print(f"{actual_date.weekday()} : {pattern_index}")

            schedule = schedule_by_day.get(pattern_index)
            if schedule:
                mapped[actual_date.isoformat()] = schedule.shift.name

        return mapped
