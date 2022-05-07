from myhelpers import generate_list, get_unchanged, login, get_grades, dir_path
import argparse

parser = argparse.ArgumentParser(
    description="Why your NDHU E-Learning password should be different from your usual password.")
parser.add_argument('--list', type=dir_path,
                    help="Path to list of students (if you happen to know those who haven't changed their passwords).")
parser.add_argument('--generate-list', action='store_true',
                    help="Too lazy to give a list? Use this option. (W.I.P.)")
parser.add_argument('--skip-try', action='store_true',
                    help='When you just know that your input is right or that no one changes their passwords.')
parser.add_argument('--get-grades', action='store_true',
                    help="If you also need to know grades for some reason, proceed with caution.")
parser.add_argument('--browser', type=str, default='chrome',
                    help="Your favorite browser, as long as it's either chrome or firefox.")
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

if args.get_grades:
    for user in unchanged:
        driver = login(user, user, args.browser)
        print(f"Getting user {user} grades now.")
        get_grades(driver, user, user)
