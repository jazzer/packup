#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import paths
import argparse
import sys, os
import logging
import subprocess
import os.path
import datetime











# define preconditions
def isDirectoryMounted(path):
    logger.debug('Checking if directory "%s" is mounted...' % path)
    if os.path.exists(path):
        logger.debug('It is mounted.')
        return True
    else:
        logger.debug('It is not mounted.')
        return False


def isWirelessAvailible(SSID):
    logger.debug('Checking if wireless network named "%s" is availible...' % SSID)
    output = getCommandOutput('sudo iwlist scan')
    if output.find('ESSID:"%s"' % SSID) > -1:
        logger.debug('It is availible.')
        return True
    else:
        logger.debug('It is not availible.')
        return False

def isWirelessConnected(SSID):
    logger.debug('Checking if we are connected to a wireless network named "%s"...' % SSID)
    output = getCommandOutput('iwconfig')
    if output.find('ESSID:"%s"' % SSID) > -1:
        logger.debug('We are connected.')
        return True
    else:
        logger.debug('We are not connected.')
        return False

# time of day related
def afterHourOfDay(hour):
    logger.debug('Checking if it is later than %s o\'clock...' % hour)
    if datetime.datetime.now().hour >= hour:
        logger.debug('Time is okay.')
        return True
    else:
        logger.debug('Too early.')
        return False



# backup frequency related
def isDailyBackupTime():
    return True
def isWeeklyBackupTime():
    return True
def isMonthlyBackupTime():
    return True



# interaction
def askForPermission(ownText):
    return True

def notifyByEMail():
    return True



# backup functions
def callRsnapshot(timecode):
    # TODO save date to file
    #   orig: date > "~/backup_date.txt"
    # TODO call rsnapshot
    # TODO remove date file
    return True

def doSystemUpgrade():
    logger.info('System upgrade...')
    #executeCommand(['sudo', 'apt-get', 'update'], obeyDry = True)
    #executeCommand(['sudo', 'apt-get', 'dist-upgrade', '-y'], obeyDry = True)
    return True

def backupPackageSelection(targetPath = '~/packages.txt'):
    logger.info('Backing up package selection...')
    if not dry:
        res = getCommandOutput('dpkg --get-selections', obeyDry = True)
        targetPath = targetPath.replace('~', homeDir)
        f = open(targetPath, 'w')
        f.write(res)
        f.close()
        ownFile(targetPath)
    return True    

def downloadSingleFile(url, localFilename):
    logger.info('Downloading Google calender...')
    localFilename = localFilename.replace('~', homeDir)
    # delete, download, own
    try:
        os.remove(localFilename)
    except OSError:
        pass    
    executeCommand(['wget', '-nc', '-O', localFilename, '-c', paths.GOOGLE_CALENDER_URL], obeyDry = True)
    ownfile(localFilename)
    return True

def backupGoogleCalender(url, localFilename):
    return downloadSingleFile(url, localFilename)

def syncDirectories(source, target):
    return True



# python/linux binding
def getCommandOutput(command, obeyDry = False):
    if obeyDry and dry:
        logger.debug(command)
        return True
    return subprocess.getoutput(command)

def executeCommand(command, obeyDry = False, shell = False):
    if obeyDry and dry:
        logger.debug(command)
        return True
    return subprocess.call(command, shell=shell)

def ownFile(filename):
    getCommandOutput('chown %s:%s %s' % (username, username, filename), obeyDry = True)
def ownDir(path):
    getCommandOutput('chown -R %s:%s %s' % (username, username, path), obeyDry = True)






# create logger
logger = logging.getLogger('packup-logger')
formatter = logging.Formatter('%(levelname)s: %(message)s')
sysohdlr = logging.StreamHandler(sys.stdout)
sysohdlr.setFormatter(formatter)
logger.addHandler(sysohdlr)

logger.setLevel(logging.DEBUG)
dry = False


# parse parameters
parser = argparse.ArgumentParser(description='Backup script based on rsnapshot, Unix magic, and python.')
# TODO implement (verbose, dry-run, ...)


# get username
# more ideas: http://stackoverflow.com/questions/4598001/how-do-you-find-the-original-user-through-multiple-sudo-and-su-commands
if not getCommandOutput('echo $SUDO_USER') == '':
    username = getCommandOutput('echo $SUDO_USER')
else:
    username = getCommandOutput('id -un') # same as whoami
# get home directory of that particular user
homeDir = getCommandOutput('cat /etc/passwd | grep %s:x' % username)
homeDir = homeDir.split(':')[-2]
# make hidden directory for settings and such
settingsDir = homeDir + '/.packup'
try:
    os.mkdir(settingsDir)
except OSError:
    pass
# reown settings dir
ownDir(settingsDir)

# now we can log to the apropriate file as well
hdlr = logging.FileHandler(settingsDir + '/runlog.log')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

logger.info('Running in %s\'s account.' % username)
logger.info('Home directory: %s' % homeDir)
logger.info('Settings directory: %s' % settingsDir)


# check if preconditions are met
if not isDirectoryMounted(paths.MOUNTED_DIR):
    sys.exit(1)
if not isWirelessConnected(paths.WIRELESS_NETWORK_SSID):
    sys.exit(1)
if not isWirelessAvailible(paths.WIRELESS_NETWORK_SSID):
    sys.exit(1)
if not afterHourOfDay(10):
    sys.exit(1)

# some rsyncing data around

# coordinate rsnapshot
if isDailyBackupTime():
    # updates
    doSystemUpgrade()
    # save packages installed on the system
    backupPackageSelection()
    # save calender
    backupGoogleCalender(paths.GOOGLE_CALENDER_URL, paths.GOOGLE_LOCAL_TARGET)

    logger.info('Daily backup...')
    pass

if isWeeklyBackupTime():
    logger.info('Weekly backup...')
    pass

if isMonthlyBackupTime():
    logger.info('Monthly backup...')
    pass

#Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)

# notifications
# send report via mail



# cleanup
# reown settings dir
ownDir(settingsDir)

