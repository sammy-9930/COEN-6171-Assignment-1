from typing import List 

class CourseScheduleII:
    MIN_COURSES = 1
    MAX_COURSES = 2000

    def __init__(self):
        self.numCourses = 0
        self.prerequisites: List[List[int]] = []

    def set_number_of_courses(self, num_of_courses):
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
        """
        Add and validate a prerequisite pair.
        """
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
        
        try:
            self.validate_prerequisite_length()
        except ValueError as e:
            self.prerequisites.pop()  # Remove the invalid prerequisite
            raise e
        return True
        
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Find a valid course ordering that satisfies all prerequisites.
        Returns empty list if no valid ordering exists.
        """
        # build an adjacency list with the pre-requisites 
        prereq = { c:[] for c in range(numCourses)}
        for crs,pre in prerequisites:
            prereq[crs].append(pre)
        # A course has 3 possible states:
        # visited: crs has been added to output 
        # visiting: crs not added to output, but added to cycle
        # unvisited: crs not added to output or cycle 
        output = []
        visit, cycle = set(), set()
        def dfs(crs):
            if crs in cycle:
                return False 
            if crs in visit:
                return True 
            
            cycle.add(crs)
            for pre in prereq[crs]:
                if dfs(pre) == False:
                    return False 
            cycle.remove(crs)
            visit.add(crs)
            output.append(crs)
            return True 
        
        for c in range(numCourses):
            if dfs(c) == False:
                return []
        return output 




        