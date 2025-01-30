import pytest
import re

from src.course_schedule.course_schedule_II import CourseScheduleII

class TestCourseScheduleII:
    @pytest.fixture
    def scheduler(self):
        return CourseScheduleII()

    def test_valid_course_number(self, scheduler):
        assert scheduler.set_number_of_courses(4) is True

    def test_invalid_course_number(self, scheduler):
        with pytest.raises(ValueError) as exc_info:
            scheduler.set_number_of_courses('a')

        expected_message = f"Number of courses must be an integer."
        assert str(exc_info.value) == expected_message

    def test_course_number_bounds(self, scheduler):
        assert scheduler.set_number_of_courses(1) is True
        assert scheduler.set_number_of_courses(2000) is True
        
        with pytest.raises(ValueError):
            scheduler.set_number_of_courses(2001)

    def test_valid_prerequisites(self, scheduler):
        scheduler.set_number_of_courses(4)
        assert scheduler.add_prerequisite(1, 0) is True
        assert [1, 0] in scheduler.prerequisites

    def test_invalid_prerequisite_self_dependency(self, scheduler):
        scheduler.set_number_of_courses(4)
        with pytest.raises(ValueError, match="Course 1 cannot be a prerequisite for itself"):
            scheduler.add_prerequisite(1, 1)

    def test_invalid_prerequisite(self, scheduler):
        scheduler.set_number_of_courses(2)
        with pytest.raises(ValueError, match =re.escape("Prerequisite 6 is not in valid range [0, 1]")):
            scheduler.add_prerequisite(1, 6)

    def test_valid_number_of_prerequisites(self, scheduler):
        """Test that the number of prerequisites is within the allowed limit."""
        scheduler.set_number_of_courses(3) 
        scheduler.prerequisites = [[0, 1], [0, 2], [1, 2]] 
        assert scheduler.validate_prerequisite_length() == True
    
    def test_single_course(self, scheduler):
        """Test with only one course (edge case)."""
        scheduler.set_number_of_courses(1)  # max_prerequisites = 1 * 0 = 0
        scheduler.prerequisites = []  # 0 prerequisites
        assert scheduler.validate_prerequisite_length() == True

    def test_exceed_max_prerequisites(self, scheduler):
        """Test that the number of prerequisites exceeds the allowed limit."""
        scheduler.set_number_of_courses(3)  # max_prerequisites = 3 * 2 = 6
        scheduler.prerequisites = [[0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [0, 1]]  # 7 prerequisites
        with pytest.raises(ValueError, match="Number of prerequisites cannot exceed 6"):
            scheduler.validate_prerequisite_length()

    def test_duplicate_prerequisites(self, scheduler):
        scheduler.set_number_of_courses(4)
        scheduler.add_prerequisite(1, 0)
        with pytest.raises(ValueError, match=re.escape("Prerequisite pair [1, 0] already exists")):
            scheduler.add_prerequisite(1, 0)  # This should trigger the ValueError

    def test_find_order_simple(self, scheduler):
        scheduler.set_number_of_courses(2)
        scheduler.add_prerequisite(1, 0)
        assert scheduler.findOrder(scheduler.numCourses, scheduler.prerequisites) == [0, 1]

    def test_find_order_complex(self, scheduler):
        scheduler.set_number_of_courses(4)
        scheduler.add_prerequisite(1, 0)
        scheduler.add_prerequisite(2, 0)
        scheduler.add_prerequisite(3, 1)
        scheduler.add_prerequisite(3, 2)
        order = scheduler.findOrder(scheduler.numCourses, scheduler.prerequisites)
        
        # Check that prerequisites come before their dependent courses
        assert order.index(0) < order.index(1)
        assert order.index(0) < order.index(2)
        assert order.index(1) < order.index(3)
        assert order.index(2) < order.index(3)

    def test_find_order_cycle(self, scheduler):
        scheduler.set_number_of_courses(2)
        scheduler.add_prerequisite(1, 0)
        scheduler.add_prerequisite(0, 1)
        assert scheduler.findOrder(scheduler.numCourses, scheduler.prerequisites) == []  # Empty list indicates impossible ordering