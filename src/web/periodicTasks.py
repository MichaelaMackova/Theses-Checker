#----------------------------------------------------------------------------
# File          : periodicTask.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Created Date  : 11.12.2024
# Last Updated  : 11.12.2024
# License       : AGPL-3.0 license
#
# Description:
#     Executes periodic tasks.
# ---------------------------------------------------------------------------

try:

    import schedule
    import time
    import os
    import subprocess

    from web.settings import BASE_DIR, OPERATING_SYSTEM


    DELETE_FILES_TIMES = ["20:00", "08:00"] # times when the files are deleted in format HH:MM
    WINDOWS_FILE_PATH = '\"' + os.path.join(BASE_DIR, 'periodicDeleteFiles.ps1') + '\"' # path with spaces
    LINUX_FILE_PATH = os.path.join(BASE_DIR, 'periodicDeleteFiles.sh')


    def periodicDeleteFilesWindows():
        """
        Periodic task for deleting files on Windows.
        """
        subprocess.check_call(['powershell', '& ' + WINDOWS_FILE_PATH])

    def periodicDeleteFilesLinux():
        """
        Periodic task for deleting files on Linux.
        """
        subprocess.check_call(['bash', LINUX_FILE_PATH])



    if OPERATING_SYSTEM == 'Windows':
        periodic_delete_files_task = periodicDeleteFilesWindows
    elif OPERATING_SYSTEM == 'Linux':
        periodic_delete_files_task = periodicDeleteFilesLinux
    else:
        raise ValueError("Invalid operating system")

    # Schedule tasks
    for sched_time in DELETE_FILES_TIMES:
        # Run job every day at specific HH:MM
        schedule.every().day.at(sched_time).do(periodic_delete_files_task)

    # Or run job every 12 hours
    # schedule.every(12).hours.do(periodic_delete_files_task)

    while 1:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        schedule.run_pending()


except KeyboardInterrupt:
    pass
finally:
    schedule.clear()
