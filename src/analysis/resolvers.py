# Author: Sally Kang <snapekang@gmail.com>
# Created: 19-11-1

import csv
import sys

import cymruwhois
import logging as log


def exit_resolvers(csv_file):
    with open(csv_file, 'r') as records, open('./resolvers/exit_resolvers.csv', 'w') as output:
        reader = csv.reader(records, delimiter=',')
        writer = csv.writer(output, delimiter=',')
        # header = ['fingerprint', 'exit_relay', 'resolver_ip', 'company', 'location']
        # writer.writerow(header)
        for row in reader:
            if row[1] == row[2]:
                resolver = 'local'
            else:
                client = cymruwhois.Client()
                r = client.lookup(row[2])
                resolver = r.owner
            resolver.replace("\"", "")
            resolver_info = resolver.split(",")
            company = resolver_info[0].strip()
            location = resolver_info[-1].strip()
            row = [row[0], row[1], row[2], company, location]
            # print(row)
            writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        log.critical("Usage: %s CSV_FILE" % sys.argv[0])
        sys.exit(1)
    csv_file = sys.argv[1]
    exit_resolvers(csv_file)
    sys.exit(0)
