''' This is used to delete old security footage when the drive reaches a set capacity.
    It can also be used to automatically remove old logs, downloads, etc.
'''

from os import statvfs
from pathlib import Path
from datetime import datetime


# threshold is an integer representing a percentage. e.g. 20 indicates 20%
def above_threshold(threshold):
    
    threshold = threshold / 100
    hdd_stats = statvfs('/')
    GB_left = (hdd_stats.f_bavail * hdd_stats.f_frsize) / (1024 * 1000000)  # gigabytes
    total_GB = (hdd_stats.f_blocks * hdd_stats.f_frsize) / (1024 * 1000000) # gigabytes

    if (GB_left / total_GB) > threshold:
        return True
    else:
        return False


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


def purge_files(path_name):
    purge_path = Path(path_name)
    for child in purge_path.glob('*'):
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            purge_files(child)
        else:
            # Why would this happen? What is not a dir or file? I don't know.
            pass
    purge_path.rmdir()


# Get current year and month, and return it for dir stucture: /year/month/
def get_year_month():
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')

    return '/' + year + '/' + month + '/'


# Go back a month
def rewind_month():
    pass


def main():
    # This has to be customized to the dir structure
    pass
    # My security camera stores year/month/day e.g. 2020/03/12/security_cam_file.mp4


if __name__ == "__main__":
    main()