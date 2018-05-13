# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-11'

from Ebbinghaus import *
from ReadExcel import *
from datetime import datetime
from random import sample
from string import ascii_letters

class MakeICS(object):
    def __init__(self):
        self.__ics_info = None
        self.__daily_dict = None
        self.__daily_ebb_dict = {}

        self.readExcel()
        self.makeEbbTime()
        self.createTime()
        self.makeICS()
        self.saveICS()

    def readExcel(self):
        self.__daily_dict = Reader('TimeTable.xlsx').getAllDailyList()

    def makeEbbTime(self):
        for key, val in self.__daily_dict.items():
            temp_ebb_list = Ebbinghaus(val[0], val[1]).getAllList()
            self.__daily_ebb_dict[key] = (temp_ebb_list, val[2], val[3])
            del temp_ebb_list
        print self.__daily_ebb_dict

    def makeICS(self):
        '''
        example:
            BEGIN:VCALENDAR
            PRODID:-//Google Inc//Google Calendar 70.9054//EN
            VERSION:2.0
            CALSCALE:GREGORIAN
            METHOD:PUBLISH
            X-WR-CALNAME:Study_Schedule
            X-WR-TIMEZONE:Asia/Shanghai
            -------------------------------------------------
            BEGIN:VEVENT
            DTSTART:20180501T000000Z
            DTEND:20180501T010000Z
            DTSTAMP:20180513T071902Z
            UID:77e5b3gqh3cij0qs4mkt1lf1e1@google.com
            CREATED:20180428T145924Z
            DESCRIPTION:
            LAST-MODIFIED:20180428T145924Z
            LOCATION:
            SEQUENCE:0
            STATUS:CONFIRMED
            SUMMARY:leetcode88
            TRANSP:OPAQUE
            END:VEVENT
            -------------------------------------------------
            END:VCALENDAR
        :return:
        '''
        # for header
        self.__ics_info = 'BEGIN:VCALENDAR' +\
            '\nPRODID:-//Google Inc//Google Calendar 70.9054//EN' +\
            '\nVERSION:2.0' +\
            '\nCALSCALE:GREGORIAN' +\
            '\nMETHOD:PUBLISH' +\
            '\nX-WR-CALNAME:' + datetime.now().date().strftime('%b-%d-%Y') +\
            '\nX-WR-TIMEZONE:Asia/Shanghai'
        event_str = ''
        for key, val in self.__daily_ebb_dict.items():
            for _time in val[0]:
                event_str += '\nBEGIN:VEVENT\nDTSTART:' + _time[0].strftime('%Y%m%dT%H%M%SZ')
                event_str += '\nDTEND:' + _time[1].strftime('%Y%m%dT%H%M%SZ')
                event_str += '\nDTSTAMP:' + self.createTime()
                event_str += '\nUID:' + self.createUID()
                event_str += '\nCREATED:' + self.createTime()
                event_str += '\nDESCRIPTION:' + val[1]
                event_str += '\nLAST-MODIFIED:' + self.createTime()
                event_str += '\nLOCATION:'
                event_str += '\nSEQUENCE:0'
                event_str += '\nSUMMARY:' + key
                # for trigger
                event_str += '\nBEGIN:VALARM'
                event_str += '\nX-WR-ALARMUID:' + self.createUID()
                event_str += '\nUID:' + self.createUID()
                event_str += '\nTRIGGER:' + '-PT' + val[2]
                event_str += '\nACTION:DISPLAY'
                event_str += '\nEND:VALARM'

                event_str += '\nEND:VEVENT\n'
        # for the tail
        self.__ics_info += event_str + '\nEND:VCALENDAR'

    def createTime(self):
        return datetime.now().strftime('%Y%m%dT%H%M%SZ')

    def createUID(self):
        return ''.join(sample(ascii_letters, 20)) + '@kwongtai'

    def saveICS(self):
        with open('calender.ics', 'w') as f:
            f.write(self.__ics_info.encode('utf-8'))


def debug():
    m = MakeICS()

if __name__ == '__main__':
    debug()