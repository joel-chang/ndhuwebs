from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from student_def import Student
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,  WebDriverException
import time


def login(_username, _password, browser):
    """Login helper function for NDHU's elearning portal. Returns driver if user/pass combination exists, returns None if it doesn't.

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


def get_grades(driver, username, password):
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
        tree_menu_elements = driver.find_elements(
            by=By.CLASS_NAME, value="treeMenuDefault")
        tree_menus_ids = []
        time.sleep(3)
        for element in tree_menu_elements:
            time.sleep(2)
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
        driver.quit()

