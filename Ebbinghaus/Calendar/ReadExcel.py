# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-11'

import xlrd
import datetime

class Reader(object):
    def __init__(self, path):
        self.__path = path
        self.__timetable = {}
        self.readFromExcel()

    def readFromExcel(self):
        data = xlrd.open_workbook(self.__path)
        sheet = data.sheet_by_index(0)
        # get the nums of row
        nrows = sheet.nrows

        # from the index:1 to start
        for i in range(1, nrows):
            daily_one = sheet.cell_value(i, 0)
            daily_one_description = sheet.cell_value(i, 1)
            start_time = sheet.cell_value(i, 2)
            time_length = sheet.cell_value(i, 3).split(':')
            pre_trigger = sheet.cell_value(i, 4)
            # get the start time
            fmt_start_time = datetime.datetime.strptime(start_time + ':00', '%Y-%m-%d %H:%M:%S')
            # get the hour and minute need to add
            hour = int(time_length[0])
            minute = int(time_length[1])
            # count the length
            fmt_time_length = datetime.timedelta(hours=hour, minutes=minute)

            # add them into dict, add time length
            self.__timetable[daily_one] = (fmt_start_time, fmt_time_length, daily_one_description, pre_trigger)

            # # count the end time
            # fmt_end_time = fmt_start_time + fmt_time_length
            # # add them into dict
            # self.__timetable[daily_one] = (fmt_start_time, fmt_end_time)

    def getAllDailyList(self):
        return self.__timetable


def debug():
    reader = Reader('TimeTable.xlsx')
    print reader.getAllDailyList()

if __name__ == '__main__':
    debug()

