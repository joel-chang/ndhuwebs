from myhelpers import generate_list, get_unchanged, login, get_grades, dir_path
import argparse
import json


helpdoc = json.load(open("helpdoc.json",))
parser = argparse.ArgumentParser(description=helpdoc["desc"])
parser.add_argument('--list', type=dir_path, help=helpdoc["list"])
parser.add_argument('--generate-list', action='store_true', help=helpdoc["genlist"])
parser.add_argument('--skip-try', action='store_true', help=helpdoc["skiptry"])
parser.add_argument('--get-grades', action='store_true', help=helpdoc["getgrades"])
parser.add_argument('--browser', type=str, default='chrome', help=helpdoc["browser"])
parser.add_argument('--lang', type=str, default='en',help=helpdoc["lang"])
args = parser.parse_args()

print(args)

if args.lang:
    open("helpdoc.json", "w").write(open(f"helpdoc_{args.lang}.json").read())
    helpdoc = json.load(open("helpdoc.json",))
    print(helpdoc['lang_ok'])
    exit()

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
    if args.get_grades:
        print('Will try to login with default passwords.')
        unchanged = get_unchanged(candidates, args.browser)
        for user in unchanged:
            driver = login(user, user, args.browser)
            print(f"Getting user {user} grades now.")
            get_grades(driver, user, user)
