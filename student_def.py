class Student:
    """Class for student in NDHU.

    Args:
        sid (str): Student ID
        spw (str): Student password
        grades (list): list containing tuples (semester, course_name, grade)
    """

    def __init__(self, sid, spw):
        # Each student has S semester, C courses per S semester, and a G grade per C course in each S semester
        self.sid = sid
        self.spw = spw
        self.grades = []

    def set_grades(self, grades):
        self.grades = grades
