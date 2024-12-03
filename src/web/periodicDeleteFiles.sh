#! /bin/bash

#----------------------------------------------------------------------------
# File          : dailyDeleteFiles.sh
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 19.10.2024
# Last Updated  : 03.12.2024
# License       : AGPL-3.0 license
#
# Description: 
#    Deletes PDF files in "files/" or "static/" folder
#    that are older than 24 hours.
# ---------------------------------------------------------------------------


TWO_HOURS_IN_SEC=7200
TWELVE_HOURS_IN_SEC=43200
DAY_IN_SEC=86400
THREE_DAYS_IN_SEC=259200
WEEK_IN_SEC=604800


Period=$TWELVE_HOURS_IN_SEC # SET PERIOD HERE


Today=$(date +'%s') # today as seconds since Epoch
Yesterday=$((Today-Period))

for i in files/*.pdf static/*.pdf files/json/*.json ; do 
    if [ -f "$i" ] ; then
        # all files (-f) in directory "files/" or "static/" that end in ".pdf" and files in directory "files/json/" that end in ".json"

        File_date=$(stat -c "%Y" "$i") # time of last modification of a file as seconds since Epoch

        if [ "$File_date" -le "$Yesterday" ]; then
            # remove file
            rm -f "$i"
        fi
    fi
done
