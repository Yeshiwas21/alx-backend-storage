#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import requests
import redis
import functools
from typing import Callable

_redis = redis.Redis()


def count_request(method: Callable) -> Callable:
    """Decorator to count number of requests sent to a URL"""

    @functools.wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function for decorator"""
        _redis.incr(f"count:{url}")
        cache = _redis.get(f"cache:{url}")

        if cache:
            return cache.decode('utf-8')
        else:
            html = method(url)
            _redis.setex(f"cache:{url}", 10, html)
            return html

    return wrapper


@count_request
def get_page(url: str) -> str:
    """Function to obtain HTML content through URL"""
    res = requests.get(url)
    return res.text


if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.example.com"
    print(get_page(url))  # First request, should fetch from server
    print(get_page(url))  # Second request, should fetch from cache
    print(get_page(url))  # Third request, should fetch from cache

    # Output the count of requests for the URL
    print(_redis.get(f"count:{url}").decode('utf-8'))
