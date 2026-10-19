import unittest

from app import create_app
from app.services import task_service
from app.utils.validator import validate_task


class ValidatorTests(unittest.TestCase):
    def test_title_kosong_ditolak(self):
        valid, _ = validate_task({"title": "   "})
        self.assertFalse(valid)

    def test_status_tidak_valid_ditolak(self):
        valid, _ = validate_task({"title": "Belajar", "status": "selesai"})
        self.assertFalse(valid)

    def test_data_valid_diterima(self):
        valid, errors = validate_task({"title": "Belajar DevSecOps", "status": "todo"})
        self.assertTrue(valid)
        self.assertEqual(errors, [])


class ServiceTests(unittest.TestCase):
    def setUp(self):
        task_service.reset()

    def test_create_status_default_todo(self):
        task = task_service.create("Task 1")
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["status"], "todo")

    def test_filter_berdasarkan_status(self):
        task_service.create("A", "todo")
        task_service.create("B", "done")
        self.assertEqual(len(task_service.get_all("done")), 1)

    def test_update_dan_remove(self):
        task = task_service.create("A")
        updated = task_service.update(task["id"], status="done")
        self.assertEqual(updated["status"], "done")
        self.assertTrue(task_service.remove(task["id"]))
        self.assertFalse(task_service.remove(999))


class ApiTests(unittest.TestCase):
    def setUp(self):
        task_service.reset()
        self.client = create_app().test_client()

    def test_health(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "ok")

    def test_buat_dan_ambil_task(self):
        res = self.client.post("/api/tasks", json={"title": "Belajar CI"})
        self.assertEqual(res.status_code, 201)
        res = self.client.get("/api/tasks/1")
        self.assertEqual(res.get_json()["title"], "Belajar CI")

    def test_post_tanpa_title_gagal(self):
        res = self.client.post("/api/tasks", json={})
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()