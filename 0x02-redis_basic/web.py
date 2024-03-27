#!/usr/bin/env python3

"""
web.py: Module for implementing an expiring web cache and tracker using Redis.
"""

import requests
import redis
import time
from functools import wraps
from typing import Callable

# Connect to Redis
r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    # Check if the URL content is cached
    cached_content = r.get(url)
    if cached_content:
        # Increment access count
        r.incr(f"count:{url}")
        return cached_content.decode('utf-8')

    # If not cached, fetch the content
    response = requests.get(url)
    content = response.text

    # Cache the content with expiration time of 10 seconds
    r.setex(url, 10, content)

    # Track access count
    r.incr(f"count:{url}")

    return content


def cache_and_track(func: Callable) -> Callable:
    """
    Decorator function to cache and track access count of a URL.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Wrapper function to cache and track access count of a URL.

        Args:
            url (str): The URL to fetch HTML content from.

        Returns:
            str: The HTML content of the URL.
        """
        cached_content = r.get(url)
        if cached_content:
            # Increment access count
            r.incr(f"count:{url}")
            return cached_content.decode('utf-8')

        content = func(url)

        # Cache the content with expiration time of 10 seconds
        r.setex(url, 10, content)

        # Track access count
        r.incr(f"count:{url}")

        return content
    return wrapper


# Example usage with function
print(get_page("http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"))


# Example usage with decorator
@cache_and_track
def get_page_decorated(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches it.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    return requests.get(url).text

print(get_page_decorated("http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"))
