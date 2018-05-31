# -*- coding: utf-8 -*-
# !/usr/bin/python

__author__ = 'kwongtai'
__time__ = '2018-5-15'

import pickle
from os.path import exists

def str2dict():
    apiUser = raw_input("Please input your apiUser:")
    apiKey = raw_input("Please input your apiKey:")
    email = raw_input("Please input your email:")
    dic =  {"apiUser":apiUser,
            "apiKey":apiKey,
            "to":email
            }
    return dic

def saveKey(dic, path):
    with open(path, "wb") as f:
        pickle.dump(dic, f)

def loadKey(path):
    with open(path, "rb") as f:
        ret = pickle.load(f)
    return ret

def main():
    path = r'D:\key.pkl'
    if exists(path):
        print loadKey(path)
    else:
        dic = str2dict()
        saveKey(dic, path)


if __name__ == '__main__':
    main()