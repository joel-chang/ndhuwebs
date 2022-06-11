from tabnanny import check
from selenium.webdriver.common.by import By
from student_def import Student
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from main_help import get_latest_in_dir
import time
import os
import json


dirs = json.load(open('dirs.json'))


def expand_all_semesters(driver, semester_name):
    base_xpath = '//*[@id="objTreeMenu_1_node_1_'
    semester_elements = []
    ind = 1
    print('All found semesters:')
    while(len(driver.find_elements_by_xpath(f'{base_xpath}{ind}"]')) != 0):
        semester_elements.append(driver.find_element_by_xpath(f'{base_xpath}{ind}"]'))
        print(driver.find_element_by_xpath(f'{base_xpath}{ind}"]').text)
        ind += 1
    
    for element in semester_elements:
        if semester_name in element.find_element_by_xpath('.//a').text:
            print("Found target semester.")
            print(element.find_element_by_xpath('.//a').text)
            print("Clicking target semester")
            element.find_elements_by_xpath('.//img')[0].click()
    return semester_elements


def go_to_course(driver, course_title, semester):
    """With driver at homepage, go to a given course within a given semester.

    Args:
        driver (selenium.webdriver): Selenium WebDriver instance at NDHU's e-learning homepage.
        course_title (str): Must match the course name in elearning dropdown.
        semester (str): Must match the semester in elearning dropdown.
    """
    print("Going to course.")
    expand_all_semesters(driver, semester)
    wait = WebDriverWait(driver, 600)
    # # find link for semester
    # print("Waiting for semester link to be clickable.")
    # semester_link = wait.until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, f"//a[@title='{semester}']")))
    # print("Going to semester link parent.")
    # semester_elem = semester_link.find_element_by_xpath("..")
    # print("Going to semester link sibling (the box).")
    # find link for course
    time.sleep(3)
    print("Waiting for course link.")
    course_link = driver.find_element_by_partial_link_text(course_title)
    print("Clicking on course.")
    course_link.click()


# "Midterm Exam File Upload"
def from_grades_page_click_file(driver, username, assignment_link, hints):
    """With driver at a given user's grades in some class, navigate to to a given assignment link and then try to click on a file containing exactly one of the given hints.

    Args:
        driver (selenium.webdriver): Selenium WebDriver instance at a given user's class grades page.
        username (str): Student ID of targeted user.
        assignment_link (str): Must match the assignment's link in elearning.
        hints (str): Usually .pdf, .doc, or .odt. You are free to try other hints, especially if the assignment asks for a specific filename format.
    """
    driver.find_element_by_partial_link_text(assignment_link).click()
    time.sleep(2)
    found_one = False
    for hint in hints:
        try:
            driver.find_element_by_partial_link_text(hint).click()
            print(f"File with hint '{hint}' was clicked.")
            time.sleep(2)
            while (get_latest_in_dir(dirs["download"]).startswith("Unconfirmed")):
                time.sleep(2)
            downloaded_file = get_latest_in_dir(dirs["download"])
            grade = driver.find_element_by_class_name('grade').text
            grade = grade.replace(' ', '_').replace('/','outOf').replace('.', '')
            new_filename = get_latest_in_dir(
                dirs["download"]).replace(hint, f"_{username}_{grade}{hint}")
            os.rename(downloaded_file, f'{new_filename}')
            found_one = True
            break
        except NoSuchElementException as e:
            print(f"Error: no link containing {hint} found. ")
            if True:
                print(e)

    if found_one is False:
        print(f'No files found for user {username}.')

def get_grades(driver, username, password, semester="all", course="all", assignment="all"):
    """
    Given a driver at the NDHU elearning dashboard, this function will 
    start to get the grades that have been entered by teachers. 
    Strictly getting grades from the grades link in each course.

    Args:
        driver (selenium.webdriver): driver at NDHU's elearning dashboard
        username (str): username (typically a student id)
        password (str): password (same as username by default)
    """
    if driver is not None:
        print(f'Account {username} accessed with {password}')
        new_student = Student(username, password)
        new_info = []
        # //*[@id="objTreeMenu_1_node_1_1_2"]/nobr/a
        time.sleep(4)
        if semester == 'all' and course == 'all' and assignment == 'all':
            tree_menu_elements = driver.find_elements(
                by=By.CLASS_NAME, value="treeMenuDefault")
            tree_menus_ids = []
            time.sleep(3)
            for element in tree_menu_elements:
                tree_menus_ids.append(str(element.get_attribute("id")).replace(
                    "objTreeMenu_1_node_1_", '').split('_'))
            print(tree_menus_ids)
            for i in tree_menus_ids:
                if len(i) == 1:
                    # semester index
                    time.sleep(2)
                    semester = driver.find_element_by_xpath(
                        f'//*[@id="objTreeMenu_1_node_1_{i[0]}"]/nobr/a/span')
                    semester_text = semester.text
                elif len(i) == 2:
                    # course index
                    time.sleep(2)
                    course = driver.find_element_by_xpath(
                        f'//*[@id="objTreeMenu_1_node_1_{i[0]}_{i[1]}"]/nobr/a')
                    course_text = course.text
                    course_link = course.get_attribute("href")
                    driver.get(course_link)
                    grades_link = driver.find_element(
                        by=By.LINK_TEXT, value='Grades')
                    grades_link.click()
                    # from here, get the last row in each column
                    time.sleep(2)
                    num_r0 = driver.find_elements(by=By.CLASS_NAME, value='r0')
                    num_r1 = driver.find_elements(by=By.CLASS_NAME, value='r1')
                    last_is_1 = False
                    if len(num_r0) == len(num_r1):
                        last_is_1 = True
                    # check if even and odds are the same
                    total_rows = len(num_r0) + len(num_r1)
                    last_row = total_rows + 1  # one empty tr + number of r0 + number of r1
                    time.sleep(2)
                    total_score = driver.find_element_by_xpath(
                        f'//*[@id="user-grade"]/tbody/tr[{last_row}]/td[4]/span').text
                    print(f'    Total score: {total_score}')
                    new = [semester_text, course_text, total_score]
                    new_info.append(new)
                    driver.get("http://www.elearn.ndhu.edu.tw/moodle/")
            new_student.set_grades(new_info)
            for piece in new_student.grades:
                print(piece)
        elif semester != 'all' and course != 'all' and assignment != 'all':
            go_to_course(driver, semester=semester, course_title=course)
            grades_link = driver.find_element(
                by=By.LINK_TEXT, value='Grades')
            grades_link.click()
            time.sleep(2)
            hints = ['.doc', '.pdf', '.odt', '.ppt', '.pptx', '.docx']
            from_grades_page_click_file(
                driver, username, assignment, hints)
            time.sleep(2)
        driver.quit()
