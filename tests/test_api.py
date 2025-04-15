import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_get_employees_different_year():
    response = client.get("/employees/employees-per-quarter?year=2020")
    
    assert response.status_code == 200
    
 
    response_json = response.json()
    assert isinstance(response_json, list)
    
    for item in response_json:
        assert "department" in item
        assert "job" in item
        assert "Q1" in item
        assert "Q2" in item
        assert "Q3" in item
        assert "Q4" in item

def test_get_departments():
    response = client.get("/department/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    
    for dept in response.json():
        assert 'department' in dept
        assert 'id' in dept

def test_load_employees_from_csv():
    with open("files/hired_employees.csv", "rb") as f:
        response = client.post("/employees/load", files={"csv_file": f})
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert "inserted" in response.json()


