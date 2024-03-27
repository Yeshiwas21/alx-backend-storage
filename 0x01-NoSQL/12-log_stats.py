#!/usr/bin/env python3
""" 12. Log stats
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: 0 for method in methods}

    if total_logs > 0:
        for method in methods:
            method_counts[method] = nginx_collection.count_documents({"method": method})

    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")

    status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
