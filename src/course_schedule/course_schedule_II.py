from typing import List
from collections import deque
import logging

class CourseScheduleII:
    MIN_COURSES = 1
    MAX_COURSES = 2000

    def __init__(self):
        self.numCourses = 0
        self.prerequisites: List[List[int]] = []
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG) 

    def set_number_of_courses(self, num_of_courses: int) -> bool:
        """ 1 <= numCourses <= 2000 """
        if not isinstance(num_of_courses, int):
            raise ValueError("Number of courses must be an integer.")
        if not (self.MIN_COURSES <= num_of_courses <= self.MAX_COURSES):
            raise ValueError(f"Number of courses must be between {self.MIN_COURSES} and {self.MAX_COURSES}")
        self.numCourses = num_of_courses
        return True

    def validate_prerequisite_length(self):
        """Validate that prerequisites length meets constraints"""
        max_prerequisites = self.numCourses * (self.numCourses - 1)
        if len(self.prerequisites) > max_prerequisites:
            raise ValueError(f"Number of prerequisites cannot exceed {max_prerequisites}")
        return True

    def add_prerequisite(self, course: int, prerequisite: int) -> bool:
        """Add and validate a prerequisite pair."""
        if not isinstance(course, int) or not isinstance(prerequisite, int):
            raise ValueError("Course numbers must be integers.")

        if not (0 <= course < self.numCourses):
            raise ValueError(f"Course {course} is not in valid range [0, {self.numCourses - 1}]")

        if not (0 <= prerequisite < self.numCourses):
            raise ValueError(f"Prerequisite {prerequisite} is not in valid range [0, {self.numCourses - 1}]")

        if course == prerequisite:
            raise ValueError(f"Course {course} cannot be a prerequisite for itself")

        if [course, prerequisite] in self.prerequisites:
            raise ValueError(f"Prerequisite pair [{course}, {prerequisite}] already exists")

        self.prerequisites.append([course, prerequisite])
        return True

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Returns a valid course ordering using Kahn’s Algorithm (BFS).
        If no valid order exists (cycle detected), returns an empty list.
        """
        # Step 1: Build adjacency list and in-degree array
        prereq = {i: [] for i in range(numCourses)}
        in_degree = [0] * numCourses  # Number of prerequisites for each course

        for course, pre in prerequisites:
            prereq[pre].append(course)  # Reverse dependency
            in_degree[course] += 1  # Increase in-degree of dependent course

        # Step 2: Initialize queue with courses having in-degree = 0 (no prerequisites)
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        order = []

        # Step 3: Process queue
        while queue:
            course = queue.popleft()
            order.append(course)  # Append normally

            for dependent in prereq[course]:
                in_degree[dependent] -= 1  # Remove dependency
                if in_degree[dependent] == 0:  # If no more prerequisites, add to queue
                    queue.append(dependent)

        # Step 4: Check if all courses are included in order (no cycle)
        return order if len(order) == numCourses else []
