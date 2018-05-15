# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-15'

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
    def __init__(self, api_file, send_file, email_addr):
        self.__api_path = api_file
        self.__send_file = send_file
        self.__email_addr = email_addr
        self.__url = "http://api.sendcloud.net/apiv2/mail/send"
        self.__params = {}

        self.loadApiKey()
        self.sendFile()

    def loadApiKey(self):
        key = loadKey(self.__api_path)
        self.__params['apiUser'] = key['apiUser']
        self.__params['apiKey'] = key['apiKey']
        # self.__params['to'] = key['to']
        self.__params['to'] = self.__email_addr
        print 'Load the api key done!'

    def sendFile(self):
        '''
        attach file and send it to email
        :return:
        '''
        # judge the file exist or not
        if not exists(self.__send_file):
            print "ICS file not found!"
            raise IOError

        # set up config of files
        display_name = 'date.ics'
        fd = open(self.__send_file, 'rb')
        files = [   ("attachments", \
                    (display_name, fd, \
                    'application/octet-stream')) ]

        # set up config of params
        info = 'Calendar'
        self.__params["from"] = "sendcloud@sendcloud.org"
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
    se = SendEmail(api_file, send_file)

if __name__ == '__main__':
    debug()
