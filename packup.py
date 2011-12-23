#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import code.functions 
import argparse
import sys

# parse parameters
parser = argparse.ArgumentParser(description='Backup script based on rsnapshot, Unix magic, and python.')
# TODO implement (verbose, dry-run, ...)

debug = True

# check if preconditions are met
if not code.functions.isDirectoryMounted('/home'):
    sys.exit(1)
if not code.functions.isWirelessConnected('MiNetz'):
    sys.exit(1)
if not code.functions.isWirelessAvailible('MiNetz'):
    sys.exit(1)
if not code.functions.afterHourOfDay(10):
    sys.exit(1)

# Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)
