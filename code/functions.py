#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


# define preconditions
def isDirectoryMounted(path):
    return True

def isWirelessAvailible(SSID):
    return True

def isWirelessConnected(SSID):
    return True

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
def callRsnapshot(timeframe):
    return True
