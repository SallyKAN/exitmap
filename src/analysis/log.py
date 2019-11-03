# Author: Sally Kang <snapekang@gmail.com>
# Created: 19-11-2
import csv
import re
import sys
import logging as log
from datetime import datetime
from itertools import izip


def time_diff(start, end):
    start_dt = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    diff = (end_dt - start_dt)
    secssDiff = diff.seconds
    minutesDiff = secssDiff / 60
    return minutesDiff


def read_log(log_file, name):
    fractions = []
    diffs = []
    with open(log_file) as fin:
        for line in fin.readlines():
            if 'Running module' in line:
                start = line.split(',')[0]
            if 'Probed' in line:
                values = line.split(",")
                fraction_info = values[-1]
                fraction = re.findall("\d+\.\d+", fraction_info)[0]
                fractions.append(fraction)
                time = time_diff(start, values[0])
                diffs.append(time)
                print(fraction + "," + str(time))
    with open(name + ".csv", 'w') as file:
        header = ['time', 'fraction']
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(izip(diffs, fractions))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        log.critical("Usage: %s LOG_FILE" % sys.argv[0])
        sys.exit(1)
    log_files = sys.argv[1:]
    for log_file in log_files:
        name = log_file.split("_")[-1].split(".")[0]
        read_log(log_file, name)
    sys.exit(0)
