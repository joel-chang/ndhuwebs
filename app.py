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
input()
candidates = []
if args.list:
    with open(args.list, 'r') as input_file:
        entries = input_file
        for entry in entries:
            candidates.append(entry.strip())
else:
    candidates = generate_list()

print(candidates)
input()

unchanged = candidates if args.skip_try else get_unchanged(candidates, args.browser)

if not args.skip_grades:
    for user in unchanged:
        driver = login(user, user, args.browser)
        print(f"Getting user {user} grades now.")
        get_grades(driver, user, user)
