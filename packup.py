#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import paths
import argparse, logging
import sys, os, os.path, subprocess
import datetime, time



time_format = "%Y-%m-%d %H:%M:%S"



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
    lastDateTime = getLastDateTime('daily')
    hours = (now - lastDateTime).seconds / 3600
    logger.debug('%i hours ago' % hours)
    
    # logic here
    if hours >= 12 and now.day != lastDateTime.day:
        return True
    return False

def isWeeklyBackupTime():
    lastDateTime = getLastDateTime('weekly')
    days = (now - lastDateTime).days
    logger.debug('%i days ago' % days)
    
    # logic here
    if days >= 7:
        return True
    return False

def isMonthlyBackupTime():
    lastDateTime = getLastDateTime('monthly')
    days = (now - lastDateTime).days
    logger.debug('%i days ago' % days)
    
    # logic here
    if days >= 30:
        return True
    return False


def getLastDateTime(scope):
    try:
        lastDateString = readFromFile(settingsDir + '/last_' + scope + '_datetime').strip()
    except IOError:
        lastDateString = "2000-01-01 00:00:00"
    logger.debug('Current time: ' + str(now))
    logger.info('Last %s backup: %s' % (scope, str(lastDateString)))
    lastDateTime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(lastDateString, time_format)))
    return lastDateTime


# interaction
def askForPermission(ownText):
    return True

def notifyByEMail():
    return True



# backup functions
def callRsnapshot(timecode):
    # TODO save date to file
    #   orig: date > "~/backup_date.txt"
    executeCommand(['time', 'sudo', 'rsnapshot', timecode])
    # TODO remove date file
    return True

def doSystemUpgrade():
    logger.info('System upgrade...')
    executeCommand(['sudo', 'apt-get', 'update'], obeyDry = True)
    executeCommand(['sudo', 'apt-get', 'dist-upgrade', '-y'], obeyDry = True)
    return True

def backupPackageSelection(targetPath = '~/packages.txt'):
    logger.info('Backing up package selection...')
    if not dry:
        res = getCommandOutput('dpkg --get-selections', obeyDry = True)
        targetPath = targetPath.replace('~', homeDir)
        writeToFile(targetPath, res)
        ownFile(targetPath)
    return True    

def downloadSingleFile(url, localFilename):
    localFilename = localFilename.replace('~', homeDir)
    # delete, download, own
    try:
        os.remove(localFilename)
    except OSError:
        pass    
    executeCommand(['wget', '-nc', '-O', localFilename, '-c', paths.GOOGLE_CALENDER_URL], obeyDry = True)
    ownFile(localFilename)
    return True

def backupGoogleCalender(url, localFilename):
    logger.info('Downloading Google calender...')
    return downloadSingleFile(url, localFilename)

def syncDirectories(source, target, name=''):
    logger.info('Syncing directories%s' % ('...' if name == '' else ' (' + name + ')...'))
    executeCommand(['su', username, '-c', 'rsync -avzrEL --delete ' + source + ' ' + target], obeyDry = True)
    return True

def isRespondingToPing(host):
    try:
        subprocess.check_call(['ping', '-qn', '-c', '1', host])
    except subprocess.CalledProcessError:
        logger.info('Host "%s" is not responding to ping attempt' % host)
        return False
    return True


# python/linux binding
def getCommandOutput(command, obeyDry = False):
    if obeyDry and dry:
        logger.debug('Executing: ' + str(command))
        return True
    return subprocess.getoutput(command)

def executeCommand(command, obeyDry = False, shell = False, silent = False):
    if obeyDry and dry:
        logger.debug('Executing: ' + str(command))
        return True
    # TODO obey silent parameter (set stdout to None?)
    return subprocess.call(command, shell=shell)

def ownFile(filename):
    getCommandOutput('chown %s:%s %s' % (username, username, filename), obeyDry = True)
def ownDir(path):
    getCommandOutput('chown -R %s:%s %s' % (username, username, path), obeyDry = True)

def writeToFile(filename, content):
    try:
        os.remove(filename)
    except OSError:
        pass 
    f = open(filename, 'w')
    f.write(content)
    f.close()

def readFromFile(filename):
    return open(filename, 'r').read()





# create logger
logger = logging.getLogger('packup-logger')
formatter = logging.Formatter('%(levelname)s: %(message)s')
sysohdlr = logging.StreamHandler(sys.stdout)
sysohdlr.setFormatter(formatter)
logger.addHandler(sysohdlr)

logger.setLevel(logging.DEBUG)
dry = False
now = datetime.datetime.now()


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
try:
    os.remove(settingsDir + '/runlog.log')
except OSError:
    pass
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
for path in paths.SYNC_PATHS:
    try:
        if 'pingList' in path:
            # make sure all the servers do respond to a ping
            for host in path['pingList']:
               if not isRespondingToPing(host):
                  raise StopIteration
               
    except StopIteration:
       continue
    # actually sync
    syncDirectories(path['source'], path['destination'], path['name'] if 'name' in path else '')


# daily stuff
if isDailyBackupTime():
    # updates
    doSystemUpgrade()
    # save packages installed on the system
    backupPackageSelection()
    # save calender
    backupGoogleCalender(paths.GOOGLE_CALENDER_URL, paths.GOOGLE_LOCAL_TARGET)
    pass

# rsnapshot part
if isMonthlyBackupTime():
    logger.info('Monthly backup...')
    callRsnapshot('monthly')
    writeToFile(settingsDir + '/last_monthly_datetime', now.strftime(time_format))

if isWeeklyBackupTime():
    logger.info('Weekly backup...')
    callRsnapshot('weekly')
    writeToFile(settingsDir + '/last_weekly_datetime', now.strftime(time_format))

if isDailyBackupTime():
    logger.info('Daily backup...')
    callRsnapshot('daily')
    writeToFile(settingsDir + '/last_daily_datetime', now.strftime(time_format))


# notifications
# send log file via mail



# cleanup
# reown settings directory
ownDir(settingsDir)

