#!/usr/bin/env python3
""" 12. Log stats
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    if total_logs == 0:
        print("Methods:")
        for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            print(f"\tmethod {method}: 0")
        print("0 status check")
    else:
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        print("Methods:")
        for method in methods:
            count = nginx_collection.count_documents({"method": method})
            print(f"\tmethod {method}: {count}")

        status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
        print(f"{status_check_count} status check")
