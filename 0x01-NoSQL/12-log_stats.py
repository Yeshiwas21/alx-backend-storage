#!/usr/bin/python3
"""
Log parsing script
"""

import sys

def print_stats(total_size, status_codes):
    """Print statistics"""
    print("File size: {}".format(total_size))
    for code, count in sorted(status_codes.items()):
        if count:
            print("{}: {}".format(code, count))

if __name__ == "__main__":
    total_size = 0
    status_codes = {"200": 0, "301": 0, "400": 0, "401": 0, "403": 0, "404": 0, "405": 0, "500": 0}
    lines_processed = 0

    try:
        for line in sys.stdin:
            parts = line.split()
            if len(parts) >= 9:
                status_code = parts[-2]
                file_size = parts[-1]
                if status_code in status_codes:
                    total_size += int(file_size)
                    status_codes[status_code] += 1
                    lines_processed += 1
            if lines_processed % 10 == 0:
                print_stats(total_size, status_codes)
    except KeyboardInterrupt:
        pass

    if lines_processed == 0:
        print("0 logs")
        print("Methods:")
        for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            print("method {}: 0".format(method))
        print("0 status check")
    else:
        print_stats(total_size, status_codes)
