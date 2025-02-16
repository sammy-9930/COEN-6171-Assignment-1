import pytest
import re 

from src.course_schedule.course_schedule_II import CourseScheduleII

class TestInterfaceBasedIDM:
    @pytest.fixture
    def scheduler(self):
        return CourseScheduleII()
    
    def test_valid_course_number(self, scheduler):
        """Valid number of courses"""
        assert scheduler.set_number_of_courses(2) is True

    def test_single_course(self, scheduler):
        """Test with only one course (edge case)."""
        scheduler.set_number_of_courses(1)  # max_prerequisites = 1 * 0 = 0
        scheduler.prerequisites = []  # 0 prerequisites
        assert scheduler.validate_prerequisite_length() == True

    def test_invalid_course_number(self, scheduler):
        """Invalid number of courses"""
        with pytest.raises(ValueError) as exc_info:
            scheduler.set_number_of_courses(-1)
        expected_message = f"Number of courses must be between 1 and 2000"
        assert str(exc_info.value) == expected_message

    def test_valid_prerequisites(self, scheduler):
        """Valid list of prerequisite pairs."""
        scheduler.set_number_of_courses(2)
        assert scheduler.add_prerequisite(1, 0) is True
        assert [1, 0] in scheduler.prerequisites

    def test_invalid_prerequisites(self, scheduler):
        """Invalid prerequisite where course index is out of bounds."""
        scheduler.set_number_of_courses(2)
        with pytest.raises(ValueError, match=re.escape("Prerequisite 5 is not in valid range [0, 1]")):
            scheduler.add_prerequisite(1, 5)

    def test_invalid_prerequisite_out_of_bounds(self, scheduler):
        """Test for an invalid prerequisite where course index is out of bounds."""
        scheduler.set_number_of_courses(3)
        scheduler.add_prerequisite(1, 0) 
        with pytest.raises(ValueError, match=re.escape("Prerequisite 5 is not in valid range [0, 2]")):
            scheduler.add_prerequisite(2, 5)

    def test_empty_prerequisites_valid(self, scheduler):
        """Empty prerequisites but valid numCourses."""
        scheduler.set_number_of_courses(3)
        assert scheduler.validate_prerequisite_length() is True

    def test_empty_prerequisites_invalid(self, scheduler):
        """Invalid empty prerequisites when numCourses is 0."""
        with pytest.raises(ValueError, match="Number of courses must be between 1 and 2000"):
            scheduler.set_number_of_courses(0)

    def test_single_valid_dependency(self, scheduler):
        """Valid dependency with a 2-course system"""
        scheduler.set_number_of_courses(2)
        assert scheduler.add_prerequisite(1, 0) is True

    def test_invalid_single_valid_dependency(self, scheduler):
        """Testing dependency with 1 course system"""
        scheduler.set_number_of_courses(1)
        with pytest.raises(ValueError, match=re.escape("Course 1 is not in valid range [0, 0]")):
            scheduler.add_prerequisite(1, 0)
    
    def test_cycle_detection(self, scheduler):
        """Cycle in prerequisites"""
        scheduler.set_number_of_courses(2)
        scheduler.add_prerequisite(1, 0)
        scheduler.add_prerequisite(0, 1)  # Cycle exists
        assert scheduler.findOrder(scheduler.numCourses, list(scheduler.prerequisites)) == []

    def test_empty_prerequisite(self, scheduler):
        """Test empty prerequisites, valid number of courses"""
        scheduler.set_number_of_courses(2)
        scheduler.prerequisites = []
        assert scheduler.findOrder(scheduler.numCourses, scheduler.prerequisites) == [0, 1]

    def test_invalid_prerequisite_self_dependency(self, scheduler):
        scheduler.set_number_of_courses(4)
        with pytest.raises(ValueError, match="Course 1 cannot be a prerequisite for itself"):
            scheduler.add_prerequisite(1, 1)

    def test_duplicate_prerequisites(self, scheduler):
        scheduler.set_number_of_courses(4)
        scheduler.add_prerequisite(1, 0)
        with pytest.raises(ValueError, match=re.escape("Prerequisite pair [1, 0] already exists")):
            scheduler.add_prerequisite(1, 0) 

    def test_valid_prerequisites_multiple(self, scheduler):
        """Test multiple valid dependencies with 3 courses and 2 valid prerequisites."""
        scheduler.set_number_of_courses(3)
        scheduler.add_prerequisite(1, 0)  # Course 1 depends on 0
        scheduler.add_prerequisite(2, 0)  # Course 2 also depends on 0
        order = scheduler.findOrder(scheduler.numCourses, list(scheduler.prerequisites))
        # Ensure all courses are included
        assert set(order) == {0, 1, 2}
        # Ensure 0 comes before 1 and 2
        assert order.index(0) < order.index(1)
        assert order.index(0) < order.index(2)

    def test_exceed_max_prerequisites(self, scheduler):
        """Test that the number of prerequisites exceeds the allowed limit."""
        scheduler.set_number_of_courses(3)  # max_prerequisites = 3 * 2 = 6
        scheduler.prerequisites = [[0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [0, 1]]  # 7 prerequisites
        with pytest.raises(ValueError, match="Number of prerequisites cannot exceed 6"):
            scheduler.validate_prerequisite_length()

    def test_valid_number_of_prerequisites(self, scheduler):
        """Test that the number of prerequisites is within the allowed limit."""
        scheduler.set_number_of_courses(3) 
        scheduler.prerequisites = [[0, 1], [0, 2], [1, 2]] 
        assert scheduler.validate_prerequisite_length() == True

    def test_number_of_courses_is_int(self, scheduler):
        with pytest.raises(ValueError, match="Number of courses must be an integer."):
            scheduler.set_number_of_courses('a')

    def test_invalid_prerequisite_value(self, scheduler):
        scheduler.set_number_of_courses(2)
        with pytest.raises(ValueError, match="Course numbers must be integers."):
            scheduler.add_prerequisite('a','b')