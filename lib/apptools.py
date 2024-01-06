#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def get_zodiac_sign(dt, sign_dates):
    # calculate
    for index, sign in enumerate(sign_dates):
        if (dt.month == sign[0][1] and dt.day >= sign[0][0]) or (dt.month == sign[1][1] and dt.day <= sign[1][0]):
            return index
    return -1
