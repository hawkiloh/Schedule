# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-30'

from apiKey import *
from requests import post
from os.path import exists
from json import loads

'''
params = {                                                                      
    "apiUser": API_USER, # 使用api_user和api_key进行验证                       
    "apiKey" : API_KEY,                                             
    "to" : "test@ifaxin.com", # 收件人地址, 用正确邮件地址替代, 多个地址用';'分隔  
    "from" : "sendcloud@sendcloud.org", # 发信人, 用正确邮件地址替代     
    "fromName" : "SendCloud",                                                    
    "subject" : "SendCloud python common",                              
    "html": "欢迎使用SendCloud"
} 
'''

class SendEmail(object):
    def __init__(self, api_file=r'/usr/key.pkl'):
        self.__api_path = api_file
        self.__send_file = ''
        self.__email_addr = ''
        self.__url = "http://api.sendcloud.net/apiv2/mail/send"
        self.__params = {}

        self.__loadApiKey()

    def __loadApiKey(self):
        key = loadKey(self.__api_path)
        self.__params['apiUser'] = key['apiUser']
        self.__params['apiKey'] = key['apiKey']
        print 'Load the api key Done!'

    def sendFile(self, send_file=None, email_addr=None):
        '''
        attach file and send it to email
        :return:
        '''
        # judge the file exist or not
        if not exists(send_file):
            print "ICS file not found!"
            raise IOError

        # set up config of files
        display_name = 'date.ics'
        fd = open(send_file, 'rb')
        files = [   ("attachments", \
                    (display_name, fd, \
                    'application/octet-stream')) ]

        # set up config of params
        info = 'Calendar'
        self.__params["from"] = "sendcloud@sendcloud.org"
        self.__params['to'] = email_addr
        self.__params["fromName"] = info
        self.__params["subject"] = info
        self.__params["html"] = 'This is your timetable.\n' + \
                                'Just add it into your calendar and enjoy it!\n'
        res = post(self.__url, files=files, data=self.__params)
        # get the res status and change it into json
        res_dict = loads(res._content)
        if res_dict['statusCode'] != 200:
            raise Exception("Unsuccessfully send the email!")
        print 'Successfully sent!'

def debug():
    send_file = r'calendar.ics'
    api_file = r'D:\key.pkl'
    se = SendEmail(api_file)
    email_addr = raw_input("Please input your email addr:")
    se.sendFile(send_file, email_addr)

if __name__ == '__main__':
    debug()
