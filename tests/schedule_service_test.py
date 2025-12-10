import unittest
import datetime
from unittest.mock import Mock
from service.schedule_service import ScheduleService
from data.models.user import User
from data.models.schedule import Schedule, Shift


class TestScheduleService(unittest.TestCase):
    def setUp(self):
        self.user_repo = Mock()
        self.schedule_repo = Mock()
        self.service = ScheduleService(self.user_repo, self.schedule_repo)

    def test_get_schedules_returns_all_users(self):
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 7)

        user1 = User("Ahmad", datetime.date(2025, 1, 1), id=1)
        user2 = User("Widi", datetime.date(2025, 1, 1), id=2)

        self.user_repo.get_all.return_value = [user1, user2]
        self.schedule_repo.get_by_user.return_value = [
            Schedule(1, Shift.S, 0, id=1),
            Schedule(1, Shift.M, 2, id=2),
        ]

        result = self.service.get_schedules(start_date, end_date)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "001")
        self.assertEqual(result[0]["name"], "Ahmad")
        self.assertEqual(result[1]["id"], "002")
        self.assertEqual(result[1]["name"], "Widi")

    def test_get_schedules_by_user_returns_single_user(self):
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 7)
        user_id = 1

        user = User("Ahmad", datetime.date(2025, 1, 1), id=1)
        schedules = [Schedule(1, Shift.S, 0, id=1), Schedule(1, Shift.M, 2, id=2)]

        self.user_repo.get.return_value = user
        self.schedule_repo.get_by_user.return_value = schedules

        result = self.service.get_schedules_by_user(start_date, end_date, user_id)

        self.assertEqual(result["id"], "001")
        self.assertEqual(result["name"], "Ahmad")
        self.assertIn("schedules", result)

    def test_get_schedules_by_user_returns_empty_for_nonexistent_user(self):
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 7)
        user_id = 999

        self.user_repo.get.return_value = None

        result = self.service.get_schedules_by_user(start_date, end_date, user_id)

        self.assertEqual(result, {})

    def test_yohan_shift_for_17_03_2028(self):
        date = datetime.date(2028, 3, 17)
        user_id = 4

        user = User("Yohan", datetime.date(2024, 12, 26), id=4)
        schedules = [
            Schedule(4, Shift.L, 0),
            Schedule(4, Shift.P, 1),
            Schedule(4, Shift.P, 2),
            Schedule(4, Shift.P, 3),
            Schedule(4, Shift.S, 4),
            Schedule(4, Shift.S, 5),
            Schedule(4, Shift.P, 6),
            Schedule(4, Shift.L, 7),
            Schedule(4, Shift.S, 8),
            Schedule(4, Shift.S, 9),
            Schedule(4, Shift.P, 10),
            Schedule(4, Shift.S, 11),
            Schedule(4, Shift.S, 12),
            Schedule(4, Shift.P, 13)
        ]

        self.user_repo.get.return_value = user
        self.schedule_repo.get_by_user.return_value = schedules

        result = self.service.get_user_schedule(user_id, date)

        self.assertEqual(result["id"], "004")
        self.assertEqual(result["name"], "Yohan")
        self.assertEqual(result["date"], "2028-03-17")
        self.assertEqual(result["shift"], "S")

    def test_map_schedule_weekly_pattern(self):
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 7)
        cycle_start = datetime.date(2025, 1, 1)

        schedules = [
            Schedule(1, Shift.S, 0, id=1),
            Schedule(1, Shift.S, 1, id=2),
            Schedule(1, Shift.M, 2, id=3),
            Schedule(1, Shift.M, 3, id=4),
            Schedule(1, Shift.L, 4, id=5),
            Schedule(1, Shift.P, 5, id=6),
            Schedule(1, Shift.P, 6, id=7),
        ]

        result = self.service.map_schedule(schedules, start_date, end_date, cycle_start)

        self.assertEqual(len(result), 7)
        self.assertEqual(result["2025-01-01"], "M")
        self.assertEqual(result["2025-01-02"], "M")
        self.assertEqual(result["2025-01-03"], "L")

    def test_map_schedule_biweekly_pattern(self):
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 14)
        cycle_start = datetime.date(2025, 1, 1)

        schedules = []
        shifts = [
            Shift.S,
            Shift.P,
            Shift.S,
            Shift.S,
            Shift.P,
            Shift.L,
            Shift.P,
            Shift.P,
            Shift.P,
            Shift.S,
            Shift.S,
            Shift.P,
            Shift.L,
            Shift.S,
        ]

        for day, shift in enumerate(shifts):
            schedules.append(Schedule(1, shift, day, id=day + 1))

        result = self.service.map_schedule(schedules, start_date, end_date, cycle_start)

        self.assertEqual(len(result), 14)
        self.assertEqual(result["2025-01-01"], "S")
        self.assertEqual(result["2025-01-08"], "S")

    def test_map_schedule_empty_schedules(self):
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 7)
        cycle_start = datetime.date(2025, 1, 1)
        schedules = []

        result = self.service.map_schedule(schedules, start_date, end_date, cycle_start)

        self.assertEqual(result, {})

    def test_export_schedules_to_csv_generates_csv(self):
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 3)

        user = User("Ahmad", datetime.date(2025, 1, 1), id=1)
        schedules = [
            Schedule(1, Shift.S, 0, id=1),
            Schedule(1, Shift.S, 1, id=2),
            Schedule(1, Shift.M, 2, id=3),
        ]

        self.user_repo.get_all.return_value = [user]
        self.schedule_repo.get_by_user.return_value = schedules

        csv_gen = self.service.export_schedules_to_csv(start_date, end_date)
        csv_lines = list(csv_gen)

        self.assertGreater(len(csv_lines), 0)
        self.assertIn("ID,Nama", csv_lines[0])
        self.assertIn("2025/01/01", csv_lines[0])
        self.assertIn("001,Ahmad", csv_lines[1])


if __name__ == "__main__":
    unittest.main()
