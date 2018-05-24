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
        self.__start_time = self.get_start_time()

        self.__base_time = {
            0: ["08:30:00", "10:05:00"],
            1: ["10:25:00", "12:00:00"],
            2: ["13:50:00", "16:15:00"],
            3: ["14:40:00", "16:15:00"],
            4: ["16:25:00", "18:00:00"],
            5: ["18:30:00", "20:55:00"]
        }

        self.__subjects = []
        self.__ics_info = None

        self.set_subjects()

        self.set_ics_info()

        self.saveICS()



    def set_ics_info(self):
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
                event_str += '\nBEGIN:VEVENT\nDTSTART:' + time[0].strftime('%Y%m%dT%H%M%SZ')
                event_str += '\nDTEND:' + time[1].strftime('%Y%m%dT%H%M%SZ')
                event_str += '\nDTSTAMP:' + self.createTime()
                event_str += '\nUID:' + self.createUID()
                event_str += '\nCREATED:' + self.createTime()
                event_str += '\nDESCRIPTION:' + sub["teacher"]
                event_str += '\nLAST-MODIFIED:' + self.createTime()
                event_str += '\nLOCATION:'
                event_str += '\nSEQUENCE:0'
                event_str += '\nSUMMARY:' + sub["course"] + " " + sub["address"]
                # for trigger
                event_str += '\nBEGIN:VALARM'
                event_str += '\nX-WR-ALARMUID:' + self.createUID()
                event_str += '\nUID:' + self.createUID()
                event_str += '\nTRIGGER:' + '-PT0M'
                event_str += '\nACTION:DISPLAY'
                event_str += '\nEND:VALARM'

                event_str += '\nEND:VEVENT\n'
        # for the tail
        self.__ics_info += event_str + '\nEND:VCALENDAR'
        print "Make isc info Done!"

    def get_start_time(self):
        time = datetime.strptime(self.__base_dict["date"], '%Y-%m-%d')
        index = time.weekday()
        if index != 0:
            raise Exception("The time is not the Monday! Please check and input again!")
        return time

    def set_subjects(self):
        '''
        make the times of course
        :return:
        '''
        subjects = self.__base_dict["subjects"]

        for sub in subjects:
            one_dic = {}
            week_index = sub["week"]
            time_index = sub["time"]
            start_week = sub["startWeek"]
            end_week = sub["endWeek"]

            start_h_m_s = map(lambda x: int(x), \
                              self.__base_time[time_index][0].split(":") )
            end_h_m_s = map(lambda x: int(x), \
                            self.__base_time[time_index][1].split(":") )

            times = []
            first_start_time = self.__start_time + timedelta(days=week_index)
            for i in range(start_week, end_week + 1):
                time = first_start_time + timedelta(days=((i - 1) * 7))
                start_time = time + timedelta(hours=start_h_m_s[0], \
                                              minutes=start_h_m_s[1], \
                                              seconds=start_h_m_s[2])
                end_time = time + timedelta(hours=end_h_m_s[0], \
                                              minutes=end_h_m_s[1], \
                                              seconds=end_h_m_s[2])
                times.append((start_time, end_time))
                one_dic["course"] = sub["course"]
                one_dic["teacher"] = sub["teacher"]
                one_dic["address"] = sub["address"]
                one_dic["times"] = times
            self.__subjects.append(one_dic)
            del times
            del one_dic
        print "Make time of course Done!"

    def createTime(self):
        return datetime.now().strftime('%Y%m%dT%H%M%SZ')

    def createUID(self):
        return ''.join(sample(ascii_letters, 20)) + '@kwongtai'

    def saveICS(self):
        with open('calendar.ics', 'w') as f:
            f.write(self.__ics_info.encode('utf-8'))
        print 'Save the ics file done!'

def main():
    json = None
    with open("data.json", "rb") as f:
        json = loads(f.read())
    m = MakeICS(json)

if __name__ == '__main__':
    main()