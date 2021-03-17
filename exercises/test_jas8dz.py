import pytest
import System
import random
import string
from RestoreData import * # so I can reset every time


### 1. login - System.py ( 1 FAIL )
# Tests if the program can handle a wrong username
def test_login(grading_system):
    username = 'jas8dz'
    password = 'bestTA'
    grading_system.login(username, password)


# # This function checks that the password is correct. # Enter several different formats of passwords to verify that
# the password returns correctly if the passwords are the same.

### 2. check_password - System.py (2 FAIL)
def test_check_password(grading_system):
    users = grading_system.users

    for user in users.keys():
        password = [users[user]['password']]
        for i in range(9):
            password.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

        for pwd in password:
            assert pwd == users[user]['password']
            # assert grading_system.login('user', pwd)


# This function will change the grade of a student and updates the database. ( 3 FAIL)
# Verify that the correct grade is changed on the correct user in the database.
# 3. change_grade - Staff.py

def test_grade(grading_system):
    assignment = 'assignment1'
    new_grade = random.randint(0, 100)

    # log in as TA and change grade
    grading_system.login('cmhbf5', 'bestTA')
    grading_system.usr.change_grade('yted91', 'software_engineering', assignment, new_grade)

    # log in as Student and check grade
    # grading_system.login('yted91', 'imoutofpasswordnames')
    # grades = grading_system.usr.check_grades('software_engineering')
    student_grade = grading_system.users['yted91']['courses']['software_engineering'][assignment]["grade"]

    # right_grade = False
    # for grade in grades:
    #     if grade[0] == assignment:
    #         right_grade = True if (grade[1] == new_grade) else False

    assert student_grade == new_grade


# This function allows the staff to create a new assignment. ( 1 PASS)
# Verify that an assignment is created with the correct due date in the correct course in the database.
# 4. create_assignment Staff.py
def test_assignment(grading_system):
    course = 'cloud_computing'
    assignment = 'assignment5'
    due_date = '04/01/20'

    grading_system.login('calyam', '#yeet')

    grading_system.usr.create_assignment(assignment, due_date, course)

    # get_data from system
    course_assignment = grading_system.courses[course]['assignments'][assignment]
    # print(course_assignment)

    assert course_assignment['due_date'] == due_date

    # grading_system.login('yted91', 'imoutofpasswordnames')
    # courses_list = courses()
    # assignments = courses_list[course]
    #
    # is_everything = False
    # for i in range(len(assignment_list)):
    #     if assignment_list[i] in assignments['assignments']:
    #         is_everything = True
    #     else:
    #         is_everything = False
    #         break
    # assert is_everything


# This function allows the professor to add a student to a course. ( 4 FAIL)
# Verify that a student will be added to the correct course in the database.
# 5. add_student - Professor.py
def test_student_add(grading_system):  # something is wrong here
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.add_student('yted91', 'databases')
    # grading_system.reload_data()

    student_courses = grading_system.users['yted91']['courses']

    assert 'databases' in student_courses


# This function allows the professor to drop a student in a course. (2 PASS)
# Verify that the student is added and dropped from the correct course in the database.
# 6. drop_student Professor.py
def test_drop_student(grading_system):
    # grading_system.reload_data()
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.drop_student('hdjsr7', 'databases')

    # grading_system.reload_data()

    student_courses = grading_system.users['hdjsr7']['courses']
    # if 'databases' in student_courses:
    #     assert False
    # else:
    #     assert True
    assert not 'databases' in student_courses


# This function allows a student to submit an assignment. ( 3 PASS)
# Verify that the database is updated with the correct assignment, submission, submission dateand in the correct course.
# 7. submit_assignment - Student.py
def test_submit_assignment(grading_system):
    # create assignment
    grading_system.login('calyam', '#yeet')
    grading_system.usr.create_assignment('assignment_test', '04/04/20', 'cloud_computing')

    grading_system.login('hdjsr7', 'pass1234')
    dummy = {
        "grade": "N/A",
        "submission_date": "02/04/20",
        "submission": "Blah Blah Blah",
        "ontime": True
    }

    grading_system.usr.submit_assignment("cloud_computing", "assignment_test", dummy["submission"],
                                         dummy["submission_date"])
    assginment = grading_system.users['hdjsr7']['courses']['cloud_computing']['assignment_test']

    assert dummy == assginment


# This function checks if an assignment is submitted on time.
# Verify that it will return true if the assignment is on time, and false if the assignment is late.
# 8. check_ontime - Student.py
def test_check_ontime(grading_system):
    # early assignment
    grading_system.login('calyam', '#yeet')
    grading_system.usr.create_assignment('test_check_ontime_1', '04/04/20', 'cloud_computing')
    grading_system.usr.create_assignment('test_check_ontime_2', '04/04/20', 'cloud_computing')

    grading_system.login('hdjsr7', 'pass1234')

    grading_system.usr.submit_assignment("cloud_computing", "test_check_ontime_1", "BLAAHHHH",
                                         "02/04/20")

    # late assignment
    grading_system.usr.submit_assignment("cloud_computing", "test_check_ontime_2", "BLAAHHHH",
                                         "05/04/20")

    assert grading_system.users['hdjsr7']['courses']['cloud_computing']['test_check_ontime_1']['ontime']
    assert not grading_system.users['hdjsr7']['courses']['cloud_computing']['test_check_ontime_2']['ontime']


# This function returns the users grades for a specific course.
# Verify the correct grades are returned for the correct user.
# 9. check_grades - Student.py
def test_check_grades(grading_system):
    grading_system.login('yted91', 'imoutofpasswordnames')
    as1 = ['assignment1', 0]
    as2 = ['assignment2', 22]

    assignments = grading_system.usr.check_grades('software_engineering')

    assert as1[1] == assignments[0][1] and as2[1] == assignments[1][1]


# 10. view_assignments - Student.py
# This function returns assignments and their due dates for a specific course.
# Verify that the correct assignments for the correct course are returned.
def test_view_assignments(grading_system):
    grading_system.login('hdjsr7', 'pass1234')

    course = 'software_engineering'
    assignments = grading_system.usr.view_assignments(course)

    backend = grading_system.courses['software_engineering']['assignments']
    name = list(backend.keys())

    for assignment, key in zip(assignments, name):
        assert assignment[0] == key
        assert assignment[1] == backend[assignment[0]]['due_date']



## MY TESTS
# test if handle wrong submission course
# 11. submission_course 
def test_submission_course(grading_system):
    grading_system.login('hdjsr7', 'pass1234')
    assgn = 'assignment2'
    date = "02/02/20"
    submission = 'Blahhhhh'
    # course = 'cloud_computing'
    course = 'databases' #hdjsr7 not in db course

    grading_system.usr.submit_assignment(course, assgn, submission, date)


def test_check_grades_course(grading_system):
    #hdjsr7 not in comp_sci course
    grading_system.login('hdjsr7', 'pass1234')
    
    grading_system.usr.check_grades('comp_sci')

def test_change_grade_wrong_assgn(grading_system):
    # log in as TA and change grade
    grading_system.login('cmhbf5', 'bestTA')
    #there is no wrong_assignment
    grading_system.usr.change_grade('yted91', 'cloud_computing', "wrong_assignment", 90)

def test_change_grade_wrong_usr(grading_system):
    # log in as TA and change grade
    grading_system.login('cmhbf5', 'bestTA')
    #wrong username
    grading_system.usr.change_grade('akend3', 'cloud_computing', "assignment_test", 90)


def test_wrong_submission_date(grading_system):
    grading_system.login('cmhbf5', 'bestTA')
    grading_system.usr.create_assignment('wrong_date_assgn', '?/?/?', 'cloud_computing')

    #go to db, if assgn is there, tests fails (should not be able ot create the assignment)

    assert not 'wrong_date_assgn' in grading_system.courses['cloud_computing']['assignments']

# def test_wrong_grade(grading_system):
#     # create assignment
#     grading_system.login('calyam', '#yeet')
#     grading_system.usr.create_assignment('assignment_test_2', '04/04/20', 'cloud_computing')

#     grading_system.login('hdjsr7', 'pass1234')
#     dummy = {
#         "grade": "N/A",
#         "submission_date": "?/?/?",
#         "submission": "Blah Blah Blah",
#         "ontime": True
#     }

#     grading_system.usr.submit_assignment("cloud_computing", "assignment_test", dummy["submission"],
#                                          dummy["submission_date"])
#     # assginment = grading_system.users['hdjsr7']['courses']['cloud_computing']['assignment_test_2']

    # assert dummy == assginment

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem


def courses():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem.load_course_db()


# if __name__ == "__main__":
#     # gradingSystem = System.System()
#     # gradingSystem.load_data()

