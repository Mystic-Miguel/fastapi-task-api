"""Smoke tests for the Task API."""

import pytest
from fastapi.testclient import TestClient
from app import app, DB


@pytest.fixture(autouse=True)
def clear_db():
    """Clear the database before each test."""
    DB.clear()
    yield
    DB.clear()


client = TestClient(app)


class TestHealth:
    def test_health_check(self):
        """Test that the health endpoint returns ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestCreateTask:
    def test_create_task_happy_path(self):
        """Test creating a valid task."""
        response = client.post("/tasks", json={"title": "Buy milk", "done": False})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy milk"
        assert data["done"] is False
        assert "id" in data

    def test_create_task_default_done_false(self):
        """Test that done defaults to False."""
        response = client.post("/tasks", json={"title": "Buy milk"})
        assert response.status_code == 201
        assert response.json()["done"] is False

    def test_create_task_empty_title_fails(self):
        """Test that empty title is rejected."""
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_create_task_missing_title_fails(self):
        """Test that missing title is rejected."""
        response = client.post("/tasks", json={"done": False})
        assert response.status_code == 422


class TestListTasks:
    def test_list_tasks_empty(self):
        """Test listing tasks when database is empty."""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == {}

    def test_list_tasks_after_create(self):
        """Test listing tasks after creating one."""
        client.post("/tasks", json={"title": "Buy milk"})
        response = client.get("/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestGetTask:
    def test_get_task_happy_path(self):
        """Test getting an existing task."""
        created = client.post("/tasks", json={"title": "Buy milk"}).json()
        response = client.get(f"/tasks/{created['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == "Buy milk"

    def test_get_task_not_found(self):
        """Test getting a nonexistent task returns 404."""
        response = client.get("/tasks/nonexistent-id")
        assert response.status_code == 404


class TestUpdateTask:
    def test_update_task_happy_path(self):
        """Test updating an existing task."""
        created = client.post("/tasks", json={"title": "Buy milk"}).json()
        response = client.put(f"/tasks/{created['id']}", json={"title": "Buy eggs", "done": True})
        assert response.status_code == 200
        assert response.json()["title"] == "Buy eggs"
        assert response.json()["done"] is True

    def test_update_task_not_found(self):
        """Test updating a nonexistent task returns 404."""
        response = client.put("/tasks/nonexistent-id", json={"title": "Buy eggs", "done": False})
        assert response.status_code == 404


class TestDeleteTask:
    def test_delete_task_happy_path(self):
        """Test deleting an existing task."""
        created = client.post("/tasks", json={"title": "Buy milk"}).json()
        response = client.delete(f"/tasks/{created['id']}")
        assert response.status_code == 204

    def test_delete_task_not_found(self):
        """Test deleting a nonexistent task returns 404."""
        response = client.delete("/tasks/nonexistent-id")
        assert response.status_code == 404

    def test_delete_removes_task(self):
        """Test that deleted task is no longer accessible."""
        created = client.post("/tasks", json={"title": "Buy milk"}).json()
        client.delete(f"/tasks/{created['id']}")
        response = client.get(f"/tasks/{created['id']}")
        assert response.status_code == 404
