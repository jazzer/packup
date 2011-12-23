#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess
import os.path
import datetime


# define preconditions
def isDirectoryMounted(path):
    print('Checking if path "%s" is mounted' % path)
    if os.path.exists(path):
        print('It is mounted.')
        return True
    else:
        print('It is not mounted.')
        return False


def isWirelessAvailible(SSID):
    print('Checking if wireless network named "%s" is availible' % SSID)
    output = getCommandOutput('sudo iwlist scan')
    #print(output)
    if output.find('ESSID:"%s"' % SSID) > -1:
        print('It is availible.')
        return True
    else:
        print('It is not availible.')
        return False

def isWirelessConnected(SSID):
    print('Checking if we are connected to a wireless network named "%s"' % SSID)
    output = getCommandOutput('iwconfig')
    #print(output)
    if output.find('ESSID:"%s"' % SSID) > -1:
        print('We are connected.')
        return True
    else:
        print('We are not connected.')
        return False

# time of day related
def afterHourOfDay(hour):
    print('Checking if it is later than %s o\'clock' % hour)
    if datetime.datetime.now().hour >= hour:
        print('Time is okay.')
        return True
    else:
        print('Too early.')
        return False

# backup frequency related
def notBackuppedToday():
    return False

def isWeeklyBackupTime(weeklyBackupDay):
    return True
def isMonthlyBackupTime(monthlyBackupDay):
    return True

# interaction
def askForPermission(ownText):
    return True

def notifyByEMail():
    return True


# backup functions
def callRsnapshot(timecode):
    return True


# python/linux binding
def getCommandOutput(command):
    return subprocess.getoutput(command)
