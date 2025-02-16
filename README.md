This assignment implements a solution for the Course Schedule II problem, which involves finding a valid course ordering given prerequisites.

## Project Structure
- `src/course_schedule/`: Contains the main implementation
- `tests/`: Contains unit tests
- `requirements.txt`: Project dependencies
- `setup.py`: Project configuration

## Recommended : create a virtual env 
```
choco install make
python -m venv .venv
.\.venv\Scripts\Activate
```

## Running Tests and coverage 
```bash
pip install -r requirements.txt
python -m pytest tests/
pytest --cov=src/course_schedule --cov-report=term-missing
```
