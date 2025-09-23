import json
import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client
        
def test_valid_input(client):
    response = client.post("/check-pay", 
        json={"hoursWorked": 50, "hourlyRate": 15, "totalPayReceived": 750})
    data = response.get_json()
    assert response.status_code == 200
    assert data["expectedPay"] == 825
    assert data["underpayment"] == 75
    
def test_below_min_wage(client):
    response = client.post("/check-pay", 
        json={"hoursWorked": 50, "hourlyRate": 6.5, "totalPayReceived": 750})
    data = response.get_json()
    assert response.status_code == 200
    assert data["expectedPay"] == None
    assert data["underpayment"] == None
    assert data["message"] == "Your entered hourly rate ($6.50) is below the federal minimum wage of $7.25. This may be a violation of federal labor law."
    
def test_invalid_input(client): 
    response = client.post("/check-pay", 
        json={"hoursWorked": -5, "hourlyRate": 15, "totalPayReceived": 750})
    data = response.get_json()
    assert response.status_code == 200
    assert data["error"] == "Invalid input values"
    