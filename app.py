from myhelpers import generate_list, get_unchanged, login, get_grades, dir_path
import argparse
import json
from course import get_students_from_course


helpdoc = json.load(open("helpdoc.json",))
parser = argparse.ArgumentParser(description=helpdoc["desc"])
parser.add_argument('--list', type=dir_path, help=helpdoc["list"])
parser.add_argument('--check-change', action='store_true')
parser.add_argument('--generate-list', action='store_true', help=helpdoc["genlist"])
parser.add_argument('--skip-try', action='store_true', help=helpdoc["skiptry"])
parser.add_argument('--get-grades', action='store_true', help=helpdoc["getgrades"])
parser.add_argument('--browser', type=str, default='chrome', help=helpdoc["browser"])
parser.add_argument('--lang', type=str, help=helpdoc["lang"])
parser.add_argument('--get-students', action='store_true')
parser.add_argument('--from-semester', type=str)
parser.add_argument('--from-course', type=str)
parser.add_argument('--user', type=str)
parser.add_argument('--pw', type=str)

args = parser.parse_args()

print(args)

if args.lang is not None:
    open("helpdoc.json", "w") .write(open(f"helpdoc_{args.lang}.json").read())
    helpdoc = json.load(open("helpdoc.json",))
    print(helpdoc['lang_ok'])
    exit()

candidates = []

if args.get_students == True:
    semester = args.from_semester if args.from_semester else input('Please enter desired semester: ')
    course =  args.from_course if args.from_course else input('Please enter desired course: ')
    user = args.user if args.user else input('Please enter your username: ')
    password = args.pw if args.pw else input(f'Please enter your password ({user}): ')
    if password == '':
        password = user

    driver = login(user, password, args.browser)

    student_ids = get_students_from_course(driver, args.from_semester, args.from_course)
    with open(f"students_{semester.replace(' ', '_')}_{course}.txt", "w") as output_file:
        for line in student_ids:
            output_file.write("".join(line) + "\n")

if args.list:
    print(f"Importing list from: '{args.list}'")
    with open(args.list, 'r') as input_file:
        entries = input_file
        for entry in entries:
            candidates.append(entry.strip())
        print('IDs found in list: ')
        print(candidates)
    if args.check_change:
        get_unchanged(candidates, args.browser)
elif args.generate_list:
    candidates = generate_list()
    print('IDs generated: ')
    print(candidates)

unchanged = []
if args.skip_try:
    print('--skip-try argument given. Will skip trying to log in.')
    unchanged = candidates
else:
    unchanged = get_unchanged(candidates, args.browser)

if args.get_grades:
    print('Will now assume default passwords.')
    for user in unchanged:
        driver = login(user, user, args.browser)
        print(f"Getting user {user} grades now.")
        get_grades(driver, user, user, args.from_semester, args.from_course)
            
# --list --skip-try --get-grades --from-semester --from-course