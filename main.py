#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
print ("[%.4f]\tLoading modules..." % (time.process_time()))

# Prevent user stopping script by CTRL + Z
import signal
signal.signal(signal.SIGTSTP,signal.SIG_IGN)

import os
import json
import random

from datetime import datetime
from zoneinfo import ZoneInfo

from calendar import Calendar

import numpy as np
from PIL import Image,ImageDraw,ImageFont
from gpiozero import Button

from astral import LocationInfo, moon
from astral.sun import sun

import lib.epd2in7_V2 as epd2in7_V2
import lib.appconfig as appconfig
import lib.apptools as apptools


def handle_btnpress(btn):
    # python hack for a switch statement. The number represents the pin number and
    # the value is the message it will print
    switcher = {
        5: "K1",
        6: "K2",
        13: "K3",
        19: "K4"
    }

    # get the string based on the passed button and send it
    epd_key = switcher.get(btn.pin.number,"K0")
    take_action(epd_key)


def take_action(ident):
    global namedays,holidays_s,holidays_un,keep_runing

    if ident != "K0":
        keep_runing = True
        draw.rectangle((0,0,epd.width,epd.height),fill = 1)

    if ident == "K4":
        keep_runing = False

    if ident == "K3":
        h = 0
        day_status = ""

        moon_phrase = moon.phase(current_date)
        moon_status = ""
        if moon_phrase >= 0 and moon_phrase <=  1:
            moon_status = "Nów"

        if moon_phrase >=  14 and moon_phrase <=  15:
            moon_status = "Pełnia"

        day_status += moon_status

        _,_,_,bbox_h = draw.textbbox((0,0),day_status,font = font12)
        draw.text((2,0),day_status,font = font12,fill = 0)

        h +=  bbox_h
        _,_,bbox_w,bbox_h = draw.textbbox((0,0),str(current_date.day),font = font48)
        draw.text(((epd.width/2)-(bbox_w/2),h),str(current_date.day),font = font48,fill = 0)

        holyday = holidays_s[0] if holidays_s else ""
        holyday +=  "\n"
        holyday +=  random.choice(holidays_un)

        h +=  bbox_h
        _,_,bbox_w,bbox_h = draw.textbbox((0,0),holyday,font = font12)
        draw.text(((epd.width/2)-(bbox_w/2),h),holyday,font = font12,fill = 0)

        sun_ref = sun(city.observer, date = current_date)

        sun_status = sun_ref["sunrise"].strftime('%H:%M')
        sun_status +=  "\n"
        sun_status +=  sun_ref["dusk"].strftime('%H:%M')

        h +=  bbox_h
        h +=  12
        draw.text((2,h),sun_status,font = font22,fill = 0)

        sign_index = apptools.get_zodiac_sign(current_date,appconfig.sign_dates)
        sign_name = appconfig.pl_sign_dict[sign_index][1]

        draw.text((65,h),str(sign_name),font = font22,fill = 0)

        s = ""
        for holyday in next_holidays:
            s +=  "%s %s\n"%(holyday[0].ljust(8),holyday[1])

        h +=  bbox_h
        h +=  36
        draw.text((2,h),s,font = font12,fill = 0)

    if ident == "K2":
        h = 0
        bbox_h = 0
        for name in holidays_s:
            _,_,_,bbox_h = draw.textbbox((0,0),name,font = font12)
            h +=  bbox_h
            draw.text((2,h),name,font = font12,fill = 0)

        h +=  bbox_h
        for name in holidays_un:
            _,_,_,bbox_h = draw.textbbox((0,0),name,font = font12)
            h +=  bbox_h
            draw.text((2,h),name,font = font12,fill = 0)

    if ident == "K1":
        namedays_str = "\n".join(namedays[:16])
        draw.text((2,0),namedays_str,font = font12,fill = 0)

    epd.display(epd.getbuffer(Limage))


if __name__ == "__main__":
    print ("[%.4f]\tProcessing..."%(time.process_time()))
    # DateTime
    current_date = datetime.now(tz=ZoneInfo("Europe/Warsaw"))
    month_name = appconfig.months[current_date.month-1]

    rootdir = "/home/pi"

    # Load database for current month
    with open (rootdir+"/calendarium.json","rt") as f:
        calendarium = json.load(f)

    # Get data for today
    day_index = "%s%02d"%(month_name[0],current_date.day)
    try:
        calendarcard = calendarium[day_index]
    except:
        exit(-1)

    # Global boolean state
    keep_runing = True

    # Keys are assigned to the corresponding pin
    key1 = Button(5)
    key2 = Button(6)
    key3 = Button(13)
    key4 = Button(19)

    # Tell the button what to do when pressed
    key1.when_pressed = handle_btnpress
    key2.when_pressed = handle_btnpress
    key3.when_pressed = handle_btnpress
    key4.when_pressed = handle_btnpress

    # Fonts
    font12 = ImageFont.truetype(os.path.join(rootdir,'fonts','Font02.ttc'),12)
    font22 = ImageFont.truetype(os.path.join(rootdir,'fonts','Font02.ttc'),22)
    font48 = ImageFont.truetype(os.path.join(rootdir,'fonts','Font02.ttc'),48)

    city = LocationInfo("Częstochowa", "Poland", "Europe/Warsaw", 50.7964, 19.1239)

    # e-Papier
    epd = epd2in7_V2.EPD()
    epd.init()
    epd.Clear()

    # initialize canvas
    Limage = Image.new('1',(epd.width,epd.height),255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)

    holidays_s = []
    for item in calendarcard['holidays_standard']:
        holidays_s.append(item[0])

    holidays_un = []
    for item in calendarcard['holidays_unofficial']:
        holidays_un.append(item[0])

    namedays = []
    for item in calendarcard['namedays']:
        namedays.append(item[0])

    # Get upcoming holyday.
    # This iterator will return all days for the month and all days before
    # the start of the month or after the end of the month that are required
    # to get a complete week.
    next_holidays = []
    for next_date in Calendar().itermonthdates(current_date.year,current_date.month):
        if next_date.month == current_date.month:
            if next_date.day > current_date.day:
                try:
                    day_index = "%s%02d"%(month_name[0],next_date.day)

                    cc = calendarium[day_index]
                    if cc:
                        if len(cc['holidays_standard']):
                            next_holidays.append([next_date.strftime('%d/%m'),cc['holidays_standard'][0][0]])
                except Exception as ex:
                    pass

    next_holidays = next_holidays[:3]

    take_action("K3")
    try:
        while keep_runing:
            pass
    except KeyboardInterrupt:
        keep_runing = False


    print ("[%.4f]\tDone."%(time.process_time()))
    quit()
