''' This is used to delete old security footage when the drive reaches a set capacity.
    With tweaking, it can also be used to automatically remove old logs, downloads, etc.
    
    I install cron job to check every 20 minutes:
    */20 * * * * privatei /usr/bin/python3 /home/slog/purge_files.py > /home/slog/purged.log 2>&1
'''

from os import statvfs
from pathlib import Path
from datetime import datetime


def get_oldest_path(path_name):
    oldest_time = 0
    current_time = 0
    list_path = Path(path_name)
    oldest_path = ''
    for child in list_path.glob('*'):
        if current_time == 0:
            current_time = child.stat().st_mtime
            oldest_time = current_time
            oldest_path = child
        else: 
            current_time = child.stat().st_mtime
            if current_time < oldest_time:
                oldest_time = current_time
                oldest_path = child
    return oldest_path


# Get the full path we want to be purging files from and return its str
# My security camera stores year/month/day e.g. 2020/03/12/security_cam_file.mp4
# This code has to be modified to work with the specific dir structure
def get_files_path(purge_path):
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    return_path = purge_path + '//' + year # usually our path should be from this year, but...
    oldest_path = get_oldest_path(purge_path)
    if str(oldest_path) != return_path:
        return_path = str(get_oldest_path(str(oldest_path)))  # return oldest subdir of oldest_path
    else:
        # year is the same, but check the month
        oldest_path = get_oldest_path(return_path)
        return_path = return_path + '//' + month
        if str(oldest_path) != return_path:
            return_path = str(oldest_path)
    
    return return_path


# threshold is an integer representing a percentage 
# e.g. 75 returns True if > 75% is being used
def above_threshold(threshold):
    
    percent_used = threshold / 100
    hdd_stats = statvfs('/')
    GB_left = (hdd_stats.f_bavail * hdd_stats.f_frsize) / (1024 * 1000000)  # gigabytes
    total_GB = (hdd_stats.f_blocks * hdd_stats.f_frsize) / (1024 * 1000000) # gigabytes

    if (total_GB - GB_left) / total_GB > percent_used:
        return True
    else:
        return False


def purge_files(path_name):
    purge_path = Path(path_name)
    for child in purge_path.glob('*'):
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            purge_files(child)
        else:
            # Why would this happen? What is not a dir or file?
            pass
    purge_path.rmdir()    


def main():
    percent_used = 75  # TODO: pass this via command line
    purge_paths = (
        '//home//slog//camera1', 
        '//home//slog//camera2', 
        '//home//slog//camera3'
    )
    
    if above_threshold(percent_used):
        
        for path in purge_paths:
            files_path = get_files_path(path)
            purged_path = get_oldest_path(files_path)
            print(f'{datetime.now()}: Purging files in {purged_path}.')
            purge_files(purged_path)
    else:
        print(f'{datetime.now()}: Threshold is acceptable. No files purged.')


if __name__ == "__main__":
    main()
