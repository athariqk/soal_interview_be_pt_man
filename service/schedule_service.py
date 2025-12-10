import datetime
import csv
from typing import List, Optional
from data.repositories.user_repository import UserRepository
from data.repositories.schedule_repository import ScheduleRepository
from data.models.schedule import Schedule


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
            results.append(
                {"id": str(user.id).zfill(3), "name": user.name, "schedules": mapped}
            )

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

    def get_user_schedule(self, user_id: int, date: datetime.date) -> dict:
        user = self.user_repo.get(user_id)
        if not user:
            return {}

        schedules = self.schedule_repo.get_by_user(user_id)
        schedules.sort(key=lambda x: x.day)

        mapped = self.map_schedule(schedules, date, date, user.start_date)
        return {
            "id": str(user.id).zfill(3),
            "name": user.name,
            "date": date.isoformat(),
            "shift": mapped.get(date.isoformat()),
        }

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

        # NOTE: komentar dibuat oleh Ahmad Ghalib Athariq, bukan LLM

        # perlu kita offset untuk matching urutan dari hari dalam seminggu
        start_day_offset = cycle_start_date.weekday()

        days_between = (end_date - start_date).days
        for offset in range(days_between + 1):
            # tanggal di antara start_date dan end_date
            actual_date = start_date + datetime.timedelta(days=offset)

            days_since_anchor = (actual_date - cycle_start_date).days
            pattern_index = (days_since_anchor + start_day_offset) % cycle_length

            schedule = schedule_by_day.get(pattern_index)
            if schedule:
                mapped[actual_date.isoformat()] = schedule.shift.name

        return mapped

    def export_schedules_to_csv(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        user_id: Optional[int] = None,
    ):
        if user_id:
            schedules = [self.get_schedules_by_user(start_date, end_date, user_id)]
        else:
            schedules = self.get_schedules(start_date, end_date)

        return self._generate_csv(schedules, start_date, end_date)

    def _generate_csv(
        self, schedules: List[dict], start_date: datetime.date, end_date: datetime.date
    ):
        date_headers = []
        current_date = start_date
        while current_date <= end_date:
            date_headers.append(current_date.strftime("%Y/%m/%d"))
            current_date += datetime.timedelta(days=1)

        header = ["ID", "Nama"] + date_headers
        yield ",".join(header) + "\n"

        for user_schedule in schedules:
            row = [user_schedule["id"], user_schedule["name"]]

            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.isoformat()
                shift = user_schedule["schedules"].get(date_str, "")
                row.append(shift)
                current_date += datetime.timedelta(days=1)

            yield ",".join(row) + "\n"
