#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

COMPUTER_NAME = 'Laptop'

MOUNTED_DIR = '/home/username'
WIRELESS_NETWORK_SSID = 'MyWireless'

GOOGLE_CALENDER_URL = 'http://www.google.com/calendar/ical/youraccount%40googlemail.com/private-9150150cf978b7ab7710591dd87er896e/basic.ics'
GOOGLE_LOCAL_TARGET = '~/Documents/calender.ics'

SYNC_PATHS = [
    {'name': 'backup to server',
     'source': '"/home/user/some_dir"', 
     'destination': '"user@yourdomain.com:/home/user/some_dir/"',
     'pingList': ['yourdomain.com-invalidated']}
]

SMTP_DOMAIN = 'example.com'
SMTP_USER = 'user@example.com'
SMTP_PASS = 'mypass'
SMTP_FROM = 'packup <packup@example.com>'
SMTP_TO = 'notification@example.com'
