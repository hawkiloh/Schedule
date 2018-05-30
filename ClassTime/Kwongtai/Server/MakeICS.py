# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-24'

from datetime import datetime, timedelta
from random import sample
from string import ascii_letters
from json import loads

class MakeICS(object):
    def __init__(self, dic):
        self.__base_dict = dic

        # get the format start time
        self.__start_time = self.__get_start_time()

        self.__subjects = []
        self.__ics_info = None

        # set the times of all subjects
        self.__set_subjects()
        # according to the times, make the ics information
        self.__set_ics_info()

    def __set_ics_info(self):
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
        self.__ics_info = 'BEGIN:VCALENDAR' + \
                          '\nPRODID:-//Google Inc//Google Calendar 70.9054//EN' + \
                          '\nVERSION:2.0' + \
                          '\nCALSCALE:GREGORIAN' + \
                          '\nMETHOD:PUBLISH' + \
                          '\nX-WR-CALNAME:' + datetime.now().date().strftime('%b-%d-%Y') + \
                          '\nX-WR-TIMEZONE:Asia/Shanghai'

        event_str = ''
        for sub in self.__subjects:
            for time in sub["times"]:
                event_str += '\nBEGIN:VEVENT\nDTSTART:' + time[0].strftime('%Y%m%dT%H%M%S')
                event_str += '\nDTEND:' + time[1].strftime('%Y%m%dT%H%M%S')
                event_str += '\nDTSTAMP:' + self.__createTime()
                event_str += '\nUID:' + self.__createUID()
                event_str += '\nCREATED:' + self.__createTime()
                event_str += '\nDESCRIPTION:' + sub["teacher"]
                event_str += '\nLAST-MODIFIED:' + self.__createTime()
                event_str += '\nLOCATION:'
                event_str += '\nSEQUENCE:0'
                event_str += '\nSUMMARY:' + sub["course"] + " " + sub["address"]
                # for trigger
                event_str += '\nBEGIN:VALARM'
                event_str += '\nX-WR-ALARMUID:' + self.__createUID()
                event_str += '\nUID:' + self.__createUID()
                event_str += '\nTRIGGER:' + '-PT0M'
                event_str += '\nACTION:DISPLAY'
                event_str += '\nEND:VALARM'

                event_str += '\nEND:VEVENT\n'
        # for the tail
        self.__ics_info += event_str + '\nEND:VCALENDAR'
        print "Make isc info Done!"

    def __get_start_time(self):
        '''
        To get the first day from json
        Exception: The first day should be the Monday.
        :return:
        '''
        time = datetime.strptime(self.__base_dict["date"], '%Y-%m-%d')
        index = time.weekday()
        if index != 0:
            raise Exception("The time is not the Monday! Please check and input again!")
        return time

    def __set_subjects(self):
        '''
        make the times of course
        :return:
        '''
        subjects = self.__base_dict["subjects"]

        for sub in subjects:
            one_dic = {}
            week_index = sub["week"]
            str_start_h_m = sub["startTime"]
            str_end_h_m = sub["endTime"]
            start_week = sub["startWeek"]
            end_week = sub["endWeek"]

            int_start_h_m = map(lambda x:int(x), str_start_h_m.split(":"))
            int_end_h_m = map(lambda x:int(x), str_end_h_m.split(":"))

            times = []
            first_start_time = self.__start_time + timedelta(days=week_index)
            for i in range(start_week, end_week + 1):
                time = first_start_time + timedelta(days=((i - 1) * 7))
                start_time = time + timedelta(hours=int_start_h_m[0], \
                                              minutes=int_start_h_m[1])
                end_time = time + timedelta(hours=int_end_h_m[0], \
                                              minutes=int_end_h_m[1])
                times.append((start_time, end_time))
                one_dic["course"] = sub["course"]
                one_dic["teacher"] = sub["teacher"]
                one_dic["address"] = sub["address"]
                one_dic["times"] = times
            self.__subjects.append(one_dic)
            del times
            del one_dic
        print "Make time of course Done!"

    def __createTime(self):
        '''
        Get the now time, return string like %Y%m%dT%H%M%SZ.
        :return:
        '''
        return datetime.now().strftime('%Y%m%dT%H%M%SZ')

    def __createUID(self):
        '''
        The ics need the UID, that func provide the UID with random.
        :return:
        '''
        return ''.join(sample(ascii_letters, 20)) + '@kwongtai'

    def get_ics(self):
        return self.__ics_info.encode('utf-8')

    def save_ics(self, path='calendar.ics'):
        '''
        Sava the ics according to the path that given.
        :return:
        '''
        with open(path, 'w') as f:
            f.write(self.__ics_info.encode('utf-8'))
        print 'Save the ics file Done!'

def main():
    json = None
    with open("data.json", "rb") as f:
        json = loads(f.read())
    m = MakeICS(json)
    print m.get_ics()

if __name__ == '__main__':
    main()