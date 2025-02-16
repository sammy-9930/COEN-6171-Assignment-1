import pytest
import csv
from src.course_schedule.course_schedule_II import CourseScheduleII

def load_test_cases():
    test_cases = []
    with open("tests/large_input.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  

        for row in reader:
            num_courses = int(row[0].strip())  # Convert numCourses to int

            # Handle large prerequisite case
            if row[1] == "large_graph":
                prerequisites = [(i, i+1) for i in range(num_courses - 1)]
            else:
                prerequisites = [tuple(map(int, pair.split(","))) for pair in row[1].split(";")] if row[1].strip() else []

            # Handle large expected order case
            if row[2] == "large_graph":
                expected_order = list(range(num_courses))  # [0, 1, 2, ..., 1999]
            else:
                expected_order = list(map(int, row[2].split(","))) if row[2].strip() else []

            test_cases.append((num_courses, prerequisites, expected_order))

    return test_cases

@pytest.mark.parametrize("num_courses, prerequisites, expected_order", load_test_cases())
def test_find_order_large_input(num_courses, prerequisites, expected_order):
    """Test course scheduling with different scenarios."""
    scheduler = CourseScheduleII()
    scheduler.set_number_of_courses(num_courses)

    for course, prerequisite in prerequisites:
        scheduler.add_prerequisite(course, prerequisite)

    order = scheduler.findOrder(scheduler.numCourses, list(scheduler.prerequisites))

    assert order == expected_order or order == expected_order[::-1], (
    f"Expected {expected_order[:10]}... or {expected_order[::-1][:10]}..., but got {order[:10]}..."
)

