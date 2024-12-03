#! /bin/bash

#----------------------------------------------------------------------------
# File          : getStorageUsage.sh

# Description:
#    Prints the server storage used in bytes (for: pythonanywhere.com).
#----------------------------------------------------------------------------

du -s -B 1 --total /tmp ~/.[!.]* ~/* | tail -1 | awk '{print $1}'