from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver_help import go_to_course
import json


url_file = open('common_urls.json', 'r')
url_of = json.loads(url_file.read())


def get_students_from_course(driver, semester, course_title):
    """Get list of STUDENTS in a given course within a given semester.

    Args:
        driver (selenium.webdriver): Selenium WebDriver instance at homepage.
        semester (str): Semester name, must at least be a substring of the semester shown in dropdown.
        course_title (str): Course name, must at least be a substring of the course shown in dropdown.

    Returns:
        list[str]: List containing the student ids of participant students in course.
    """
    wait = WebDriverWait(driver, 600)
    # first check if driver is at ndhu home page
    assert driver.current_url == url_of["homepage"], "Browser not at homepage."
    go_to_course(driver, course_title=course_title, semester=semester)

    # find participants link
    participants_link = wait.until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Participants"))
    )
    participants_link.click()

    show_all = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="showall"]/a')))
    number_of_participants = int(show_all.text.split()[-1])
    show_all.click()

    all_parts = []
    student_ids = []
    for i in range(2, number_of_participants+2):
        participant = driver.find_element_by_xpath(
            f'//*[@id="participants"]/tbody/tr[{i}]/td[2]/strong/a')
        all_parts.append(participant.text)
        if participant.text.split()[-2] == '同學':
            student_ids.append(participant.text.split()[-1])

    return student_ids
