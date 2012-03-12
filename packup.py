#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import data
import argparse, logging
import sys, os, os.path, subprocess
import datetime, time


time_format = "%Y-%m-%d %H:%M:%S"

# create logger
logger = logging.getLogger('packup-logger')
formatter = logging.Formatter('%(levelname)s: %(message)s')
sysohdlr = logging.StreamHandler(sys.stdout)
sysohdlr.setFormatter(formatter)
logger.addHandler(sysohdlr)
logger.setLevel(logging.DEBUG)

dry = False
verbose = True
now = datetime.datetime.now()
notify = False











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
    output = getCommandOutput('iwlist scan')
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
def isOlder(days, title):
    lastDateTime = getLastDateTime(title)
    daysAgo = (now - lastDateTime).days
    logger.debug('%i days ago' % days)
    
    # logic here
    if daysAgo >= days:
        return True
    return False


def getLastDateTime(event):
    try:
        lastDateString = readFromFile(settingsDir + '/' + event + '_datetime').strip()
    except IOError:
        lastDateString = "2000-01-01 00:00:00"
    logger.debug('Current time: ' + str(now))
    logger.info('Last %s: %s' % (event, str(lastDateString)))
    lastDateTime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(lastDateString, time_format)))
    return lastDateTime


# interaction
def askForPermission(ownText):
    return True

def notifyByEMail():
    return True



# backup functions
def callRsnapshot(timecode):
    dateFilename = homeDir + '/backup_date.txt'
    # save date to file
    writeToFile(dateFilename, str(datetime.datetime.now()))
    executeCommand('time rsnapshot ' + timecode, obeyDry = True, shell=True)
    # remove date file
    removeFile(dateFilename)
    return True

def doSystemUpgrade():
    logger.info('System upgrade...')
    executeCommand('sudo apt-get update', obeyDry = True)
    executeCommand('sudo apt-get dist-upgrade -y', obeyDry = True)
    return True

def backupPackageSelection(targetPath = '~/packages.txt'):
    logger.info('Backing up package selection...')
    if not dry:
        res = getCommandOutput('dpkg --get-selections', obeyDry = True)
        targetPath = targetPath.replace('~', homeDir)
        writeToFile(targetPath, res)
        ownFile(targetPath, username)
    return True    

def downloadSingleFile(url, localFilename):
    localFilename = localFilename.replace('~', homeDir)
    # delete, download, own
    removeFile(localFilename)
    executeCommand('wget -nc -O "%s" -c "%s"' % (localFilename, data.GOOGLE_CALENDER_URL), obeyDry = True)
    ownFile(localFilename, username)
    return True

def backupGoogleCalender(url, localFilename):
    logger.info('Downloading Google calender...')
    return downloadSingleFile(url, localFilename)

def syncDirectories(source, target, name=''):
    logger.info('Syncing directories%s' % ('...' if name == '' else ' (' + name + ')...'))
    executeCommand("su -c 'rsync -avzrEL --delete %s %s' %s" % (source, target, username), obeyDry = True, shell=True)
    return True

def isRespondingToPing(host):
    good = ' 0% packet loss' in getCommandOutput('ping -qn -c 1 "%s"' % host, obeyDry = False)
    if not good:
        logger.info('Host "%s" is not responding to ping attempt' % host)
        return False
    logger.info('Host "%s" is reachable' % host)
    return True


# python/linux binding
def getCommandOutput(command, obeyDry = False):
    logger.debug('Executing: ' + str(command))
    if obeyDry and dry:
        return True
    return subprocess.getoutput(command)

def executeCommand(command, obeyDry = False, shell = True, silent = False):
    out = subprocess.STDOUT
    if silent:
        out = open('/dev/null', 'w')

    logger.debug('Original command %s' % str(command))
    if verbose:
        command = command + (' | tee -a "%s"' % logFilename)
    else:
        command = command + (' >> "%s"' % logFilename)
    logger.debug('Changed command %s' % str(command))

    if obeyDry and dry:
        logger.debug('Executing: ' + str(command))
        return True

    proc = subprocess.Popen(command, shell=shell)#, stdout=out)
    proc.wait()
    return proc

def ownFile(filename, username):
    getCommandOutput('chown %s:%s %s' % (username, username, filename), obeyDry = True)
def ownDir(path, username):
    getCommandOutput('chown -R %s:%s %s' % (username, username, path), obeyDry = True)

def removeFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

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









# parse arguments
parser = argparse.ArgumentParser(description='Backup script based on rsnapshot, Unix magic, and python.')
# TODO implement (verbose, dry-run, ...)


# get home directory
username = getCommandOutput('logname')
homeDir = os.path.expanduser('~')
# make hidden directory for settings and such
settingsDir = homeDir + '/.packup/'
try:
    os.mkdir(settingsDir)
except OSError:
    pass
# reown settings dir
ownDir(settingsDir, username)

# now we can log to the apropriate file as well
logFilename = settingsDir + 'runlog.log'
removeFile(logFilename)
hdlr = logging.FileHandler(logFilename)
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

logger.info('Running in %s\'s account.' % username)
logger.info('Home directory: %s' % homeDir)
logger.info('Settings directory: %s' % settingsDir)
ownFile(logFilename, username)


# check if preconditions are met
if not isWirelessConnected(data.WIRELESS_NETWORK_SSID):
    sys.exit(1)
#if not isWirelessAvailible(data.WIRELESS_NETWORK_SSID):
#    sys.exit(1)
#if not afterHourOfDay(10):
#    sys.exit(1)



# daily stuff
if isOlder(1, 'update'):
    # updates
    doSystemUpgrade()
    # save packages installed on the system
    backupPackageSelection()
    # save calender
    try:
        backupGoogleCalender(data.GOOGLE_CALENDER_URL, data.GOOGLE_LOCAL_TARGET)
    except AttributeError:
        pass # no calender backup...
    writeToFile(settingsDir + 'update_datetime', now.strftime(time_format))
    pass


# some rsyncing data around
for path in data.SYNC_PATHS:
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
notify = True    


# rsnapshot part
rsnapshot_names = ['monthly', 'weekly', 'daily']
rsnapshot_days = [30, 7, 1]

for i in range(0,3):
    name = rsnapshot_names[i]
    if isOlder(rsnapshot_days[i], name + '-rsnapshot'):
        logger.info('%s backup...' % name)
        if isDirectoryMounted(data.MOUNTED_DIR):
            callRsnapshot(name) # TODO check success!, otherwise don't execute next two lines
            writeToFile(settingsDir + '%s-rsnapshot_datetime' % name, now.strftime(time_format))
            notify = True    
        # print backup size for a short overview
        if rsnapshot_names[i] is 'daily':
            try:
                executeCommand('du -sh "%s"' % data.DAILY_BACKUP_PATH)
            except AttributeError:
                pass # not forcing anybody to do that check


# send log file via mail
# Import smtplib for the actual sending function
if notify:
    import smtplib
    from email.mime.text import MIMEText

    fileh = open(logFilename, 'r', encoding='utf8')
    message_text = fileh.read()
    fileh.close()
    msg = MIMEText(message_text, _charset='utf8')
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    msg['Subject'] = "Backup beendet (%s)" % data.COMPUTER_NAME
    msg['From'] = data.SMTP_FROM
    msg['To'] = data.SMTP_TO
    s = smtplib.SMTP(data.SMTP_DOMAIN)
    s.login(data.SMTP_USER, data.SMTP_PASS)
    s.sendmail(data.SMTP_USER, [data.SMTP_TO], msg.as_string())
    s.quit()


# cleanup
# reown settings directory
ownDir(settingsDir, username)


