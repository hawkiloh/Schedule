# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-11'

from datetime import timedelta, datetime

class Ebbinghaus(object):
    def __init__(self, start_time, time_length):
        '''
        init func
        :param start_time: a time stamp
        :param time_length: time length
        '''
        self.__start_time = start_time
        self.__first_time_length = time_length
        self.__other_time_length = timedelta(minutes=30)
        self.__time_list = []
        self.calculateTime()


    def calculateTime(self):
        '''
        to calculate time according to Ebbinghaus
        the 1th: start time
        the 2th: after 12 hours
        the 3th: after 1 day
        the 4th: after 3 day
        the 5th: after 6 day
        the 6th: after 14 day
        the 1th length is according to user provide
        the 2th to 6th is set 30 minutes
        :return:
        '''
        self.__time_list.append((self.__start_time,\
                                 self.__start_time + self.__first_time_length))
        self.__time_list.append((self.__start_time + timedelta(hours=12), \
                                 self.__start_time + timedelta(hours=12) + self.__other_time_length))
        self.__time_list.append((self.__start_time + timedelta(days=1), \
                                 self.__start_time + timedelta(days=1) +self.__other_time_length))
        self.__time_list.append((self.__start_time + timedelta(days=3), \
                                 self.__start_time + timedelta(days=3) +self.__other_time_length))
        self.__time_list.append((self.__start_time + timedelta(days=6), \
                                 self.__start_time + timedelta(days=6) +self.__other_time_length))
        self.__time_list.append((self.__start_time + timedelta(days=14), \
                                 self.__start_time + timedelta(days=14) +self.__other_time_length))

    def getAllList(self):
        '''
        get the result list:
        an element is tuple
        a tuple include start time and end time
        :return:
        '''
        return self.__time_list

def debug():
    from datetime import datetime
    e = Ebbinghaus(datetime.now(), timedelta(hours=2))
    print e.getAllList()

if __name__ == '__main__':
    debug()

