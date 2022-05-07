from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from myhelpers import generate_list, get_unchanged, login, get_grades, dir_path
from student_def import Student
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import argparse

parser = argparse.ArgumentParser(description='arg_description.txt')
parser.add_argument('--list', type=dir_path)
parser.add_argument('--generate-list', action='store_true')
parser.add_argument('--skip-try', action='store_true')
parser.add_argument('--skip-grades', action='store_true')
parser.add_argument('--browser', type=str, default='chrome')
args = parser.parse_args()

print(args)

candidates = []
if args.list:
    print(f"Importing list from: '{args.list}'")
    with open(args.list, 'r') as input_file:
        entries = input_file
        for entry in entries:
            candidates.append(entry.strip())
        print('IDs found in list: ')
        print(candidates)
else:
    candidates = generate_list()
    print('IDs generated: ')
    print(candidates)

unchanged = []
if args.skip_try:
    print('--skip-try argument given. Will skip trying to log in.')
    unchanged = candidates
else:
    print('Will try to login with default passwords.')
    unchanged = get_unchanged(candidates, args.browser)

if not args.skip_grades:
    for user in unchanged:
        driver = login(user, user, args.browser)
        print(f"Getting user {user} grades now.")
        get_grades(driver, user, user)
