#!/usr/bin/env python3

import requests, threading, time
from datetime import datetime

def log(event):
    print(str(datetime.now().strftime('%H:%M:%S')) + ' ::: ' + str(event))

def login(session, username, password):
    log('Logging in to SIS')
    payload = {
        'username': username,
        'password': password,
        'loginAction': '',
        'institution': 'CASE1'
    }
    response = session.post('https://sismobile.case.edu/app/profile/logintoapp', data=payload)
    if 'The username or password you entered is incorrect' in response.text:
        log('ERROR: Incorrect username or password')
        return False
    else:
        log('OK: Logged into to SIS')
        return True

def enroll(session, course_list):
    payload = {
        'instituion':'CASE1',
        'acad_career':'UGRD',
        'strm':'2168',
        'confirm_enrollment':'N',
        'CSRFToken': get_csrf_token(session),
        'enroll':'',
        'selected[]': course_list
    }
    log('Pew!')
    response = session.post('https://sismobile.case.edu/app/student/enrollmentcart/enroll/CASE1/UGRD/2168',data=payload)

def get_csrf_token(session):
    return requests.utils.dict_from_cookiejar(session.cookies)['CSRFCookie']

def main():
    session = requests.session()
    courses = [1235, 11309, 11444] # Copy course numbers from your SIS shopping cart
    username = 'USERNAME'
    password = 'PASSWORD'
    sleep = 1
    if login(session, username, password):
        log('Try increasing the sleep time if this breaks')
        input('Hit any key to start firing requests... ')
        while True:
            thread = threading.Thread(target=enroll, args=(session, courses))
            thread.start()
            time.sleep(sleep)

if __name__ == '__main__':
    main()