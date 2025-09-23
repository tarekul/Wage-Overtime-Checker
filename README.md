Wage Overtime Checker

A simple Flask app to check if your pay matches expected wages including overtime. Includes automated tests with pytest.

Setup

1. Clone the repository

```
git clone <your-repo-url>
cd wage_overtime_checker
```

2. Create and activate a virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

Run the server

```
python app.py
```

Run Tests

```
pytest
```

This will run the automated tests in test_app.py.

Usage
Send a POST request to /check-pay with JSON:

```
{
  "hoursWorked": 50,
  "hourlyRate": 15,
  "totalPayReceived": 750
}
```
