from typing import List 

class CourseScheduleII:
    MIN_COURSES = 1
    MAX_COURSES = 2000

    def __init__(self):
        self.numCourses = 0
        self.prerequisites: List[List[int]] = []

    def get_numCourses(self):
        return self.numCourses 
    
    def set_numCourses(self, num_courses):
        self.numCourses = num_courses

    def validate_number_of_courses(self, num_of_courses):
        """ 1 <= numCourses <= 2000 """
        try:
            if not isinstance(num_of_courses, int):
                raise ValueError("Number of courses must be an integer.")
            if not (self.MIN_COURSES <= num_courses <= self.MAX_COURSES):
                raise ValueError("Number of courses must be between {self.MIN_COURSES} and {self.MAX_COURSES}")
            self.numCourses = num_of_courses
        except ValueError as e:
            print(f"Invalid input: {e}")
            exit(1) 

    
    def validate_prerequisites(self):
        while True:
            line = input("Enter prerequisite pair or 'done': ").strip()
            if line.lower() == "done":
                break
            
            # Validate and parse the input
            try:
                crs, pre = map(int, line.split(","))
                # Check if courses are within valid range
                if crs < 0 or crs >= num_courses or pre < 0 or pre >= num_courses:
                    print(f"Error: Courses must be between 0 and {num_courses - 1}. Try again.")
                    continue
                prerequisites.append([crs, pre])
            except ValueError:
                print("Invalid input! Please enter pairs in the format 'course,prerequisite'.")
    
        return self.prerequisites

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
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

course = CourseScheduleII()
num_courses = int(input("Enter the number of courses (1-2000):"))
print(f"Enter the prerequisites as pairs (e.g., 1,0 means course 1 depends on course 0).")
print(f"Note: Course numbers should be between 0 and {course.get_numCourses() - 1}. Enter 'done' when you are finished.")




        