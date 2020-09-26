''' Monitor a directory and remove the oldest files to stay at a specified usage threshold

    I install cron job to check every 15 minutes:
    */15 * * * * /usr/bin/python3 /path/to/purge_files.py 75 /home/user/watcher >> /home/privatei/user/purge_files/purged.log 2>&1
'''

from os import statvfs
from pathlib import Path
from datetime import datetime
from sys import argv

EXEMPT_DIRS = 'purge_files'


def recursive_filegrab(path_string, exempt_dirs):
    file_list = []
    monitored_path = Path(path_string)
    for sub_path in monitored_path.glob('**/*'):
        if exempt_dirs not in sub_path.parts:
            if sub_path.is_file():
                file_list.append(sub_path)
            elif sub_path.is_dir():
                if sub_path.as_posix() not in exempt_dirs:
                    recursive_filegrab(sub_path.as_posix(), exempt_dirs)
            else:
                print(sub_path)  # For safety. Is there a non-directory, non-file?
    return file_list


def remove_oldest(pathlib_filelist):
    oldest_file = pathlib_filelist[0]
    for file in pathlib_filelist:
        create_time = oldest_file.stat().st_mtime
        if file.stat().st_mtime == create_time:
            pass
        else:
            if create_time < file.stat().st_mtime:
                oldest_file = file
    try:
        print(f'{datetime.today().strftime("%m/%d/%Y %I:%M:%S %p")}: Removed {oldest_file.as_posix()} from {datetime.fromtimestamp(create_time).strftime("%m/%d/%Y %I:%M:%S %p")}')
        oldest_file.unlink()
    except Exception:
        print(f'Failed to remove {oldest_file}')


# threshold is an integer representing a percentage of disk usage
# e.g. 75 returns True if > 75% is being used
def above_threshold(threshold):

    percent_used = threshold / 100
    hdd_stats = statvfs('/')
    GB_left = (hdd_stats.f_bavail * hdd_stats.f_frsize) / (1024 * 1000000)  # gigabytes
    total_GB = (hdd_stats.f_blocks * hdd_stats.f_frsize) / (1024 * 1000000)  # gigabytes

    if (total_GB - GB_left) / total_GB > percent_used:
        return True
    else:
        return False


def main(threshold, monitored_path):
    try:
        while above_threshold(threshold):
            pathlib_filelist = recursive_filegrab(monitored_path, EXEMPT_DIRS)
            remove_oldest(pathlib_filelist)
        print(f'{datetime.today().strftime("%m/%d/%Y %I:%M:%S %p")}: Threshold is acceptable. Purge delayed.')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(argv) != 3:
        print('usage: purge_files <threshold> <monitored path>')
    else:
        main(int(argv[1]), argv[2])
