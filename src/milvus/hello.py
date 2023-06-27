#!/usr/bin/env python

import os
import time
import json
from httpx import Client, Response, get
from urllib.parse import urljoin, urlparse


def log_request(request):
    print(f"> {request.method} {request.url}")


def log_response(response):
    request = response.request
    print(f"< {request.method} {request.url} - {response.status_code}")
    if response.status_code >= 299:
        response.read()
        print(f"\n{response.text}")


def main():
    # HTTPs setup
    #endpoint = urlparse(os.environ["ENDPOINT"])
    #endpoint = urlparse("http://localhost:9091/api/v1/health")
    #controller_endpoint = endpoint._replace(
    #    netloc=f"controller.{endpoint.netloc}"
    #).geturl()

    r = get("http://localhost:9091/api/v1/health")
    print(r.text)
    


if __name__ == "__main__":
    main()
