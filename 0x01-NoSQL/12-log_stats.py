#!/usr/bin/env python3
"""
MongoDB stats script
"""

import pymongo

def count_documents(collection, query={}):
    """Count documents in a collection"""
    return collection.count_documents(query)

def count_method_documents(collection, method):
    """Count documents with a specific method"""
    return collection.count_documents({"method": method})

def count_status_check(collection):
    """Count documents with method GET and path /status"""
    return collection.count_documents({"method": "GET", "path": "/status"})

if __name__ == "__main__":
    client = pymongo.MongoClient()
    db = client.logs
    nginx_collection = db.nginx

    total_logs = count_documents(nginx_collection)
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = count_method_documents(nginx_collection, method)
        print(f"    method {method}: {count}")

    status_check_count = count_status_check(nginx_collection)
    print(f"{status_check_count} status check")
