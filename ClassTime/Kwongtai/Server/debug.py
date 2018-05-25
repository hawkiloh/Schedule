# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-24'

from json import loads

def loadJson(path):
    with open(path, "rb") as f:
        return loads(f.read())

if __name__ == '__main__':
    print loadJson("data.json")