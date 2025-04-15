from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_employees_different_year():
    response = client.get("/employees_per_quarter?year=2020")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
