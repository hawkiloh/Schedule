# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-15'

from SendEmail import SendEmail
from MakeICS import MakeICS
from os.path import exists

def main():
    email_addr = raw_input('Please input your email addr:')
    mkics = MakeICS()
    api_path = r'D:\key.pkl'
    send_file_path = r'calendar.ics'
    if not exists(send_file_path):
        raise IOError
    sm = SendEmail(api_path, send_file_path, email_addr)

if __name__ == '__main__':
    main()