#! /bin/bash

#----------------------------------------------------------------------------
# File          : getStorageAvailableSpace.sh

# Description:
#    Prints current disk available space in bytes.
#----------------------------------------------------------------------------

df -B 1 --sync --total ./ | tail -1 | awk '{print $3}'