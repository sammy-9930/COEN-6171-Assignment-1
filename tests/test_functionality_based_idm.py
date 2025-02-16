import pytest
import csv
from src.course_schedule.course_schedule_II import CourseScheduleII

def load_test_cases():
    test_cases = []
    with open("tests/test_cases.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row

        for row in reader:
            num_courses = int(row[0].strip())  # Ensure clean integer parsing

            # Handle empty prerequisites
            prerequisites = []
            if row[1].strip():
                prerequisites = [tuple(map(int, pair.split(","))) for pair in row[1].split(";")]

            # Handle empty expected order
            expected_order = []
            if row[2].strip():
                expected_order = list(map(int, row[2].split(",")))

            test_cases.append((num_courses, prerequisites, expected_order))

    return test_cases

@pytest.mark.parametrize("num_courses, prerequisites, expected_order", load_test_cases())
def test_find_order(num_courses, prerequisites, expected_order):
    """Test course scheduling with different scenarios."""
    scheduler = CourseScheduleII()
    scheduler.set_number_of_courses(num_courses)

    for course, prerequisite in prerequisites:
        scheduler.add_prerequisite(course, prerequisite)

    order = scheduler.findOrder(scheduler.numCourses, list(scheduler.prerequisites))

    assert set(order) == set(expected_order), f"Expected {expected_order}, but got {order}"
