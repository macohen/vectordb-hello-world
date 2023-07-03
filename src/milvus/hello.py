#!/usr/bin/env python

import os
import time
import json
from httpx import Client, Response
import pprint
from urllib.parse import urljoin


def log_request(request):
    print(f"> {request.method} {request.url}")

def log_response(response):
    request = response.request
    print(f"< {request.method} {request.url} - {response.status_code}")
    if response.status_code >= 299:
        response.read()
        print(f"\n{response.text}")

entities = {
    "collection_name": "book",
    "fields_data": [
        {
            "field_name": "book_id",
            "type": 5,
            "field": [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
                78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100
            ]
        },
        {
            "field_name": "word_count",
            "type": 5,
            "field": [
                1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000,
                16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000,
                30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000,
                44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000,
                58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000,
                72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000,
                86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000,
                100000
            ]
        },
        {
            "field_name": "book_intro",
            "type": 101,
            "field": [
                [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1],
                [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [20, 1], [21, 1], [22, 1], [23, 1],
                [24, 1], [25, 1], [26, 1], [27, 1], [28, 1], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 1],
                [35, 1], [36, 1], [37, 1], [38, 1], [39, 1], [40, 1], [41, 1], [42, 1], [43, 1], [44, 1], [45, 1],
                [46, 1], [47, 1], [48, 1], [49, 1], [50, 1], [51, 1], [52, 1], [53, 1], [54, 1], [55, 1], [56, 1],
                [57, 1], [58, 1], [59, 1], [60, 1], [61, 1], [62, 1], [63, 1], [64, 1], [65, 1], [66, 1], [67, 1],
                [68, 1], [69, 1], [70, 1], [71, 1], [72, 1], [73, 1], [74, 1], [75, 1], [76, 1], [77, 1], [78, 1],
                [79, 1], [80, 1], [81, 1], [82, 1], [83, 1], [84, 1], [85, 1], [86, 1], [87, 1], [88, 1], [89, 1],
                [90, 1], [91, 1], [92, 1], [93, 1], [94, 1], [95, 1], [96, 1], [97, 1], [98, 1], [99, 1], [100, 1]
            ]
        }
    ],
    "num_rows": 100
}

def main():
    endpoint = os.environ["ENDPOINT"] + "/api/v1/"
    client = Client(
        verify=False,
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        },
    )
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
    }

    create_collection = {
        "collection_name": "book",
        "schema": {
            "autoID": False,
            "description": "Test book search",
            "fields": [
                {
                    "name": "book_id",
                    "description": "book id",
                    "is_primary_key": True,
                    "autoID": False,
                    "data_type": 5
                },
                {
                    "name": "word_count",
                    "description": "count of words",
                    "is_primary_key": False,
                    "data_type": 5
                },
                {
                    "name": "book_intro",
                    "description": "embedded vector of book introduction",
                    "data_type": 101,
                    "is_primary_key": False,
                    "type_params": [
                        {
                            "key": "dim",
                            "value": "2"
                        }
                    ]
                }
            ],
            "name": "book"
        }
    }

    create_collection_resp = client.request('POST', urljoin(endpoint, "collection"), content=json.dumps(create_collection),
                                     headers=headers)
    pprint.pprint(create_collection_resp.text)

    entities_insert_resp = client.request('POST', urljoin(endpoint, "entities"), content=json.dumps(entities), headers=headers)

    index_cmd = {
        "collection_name": "book",
        "field_name": "book_intro",
        "extra_params":[
            {"key": "metric_type", "value": "L2"},
            {"key": "index_type", "value": "IVF_FLAT"},
            {"key": "params", "value": "{\"nlist\":1024}"}
        ]
    }

    vector_index_resp = client.request("POST", urljoin(endpoint, "index"), content=json.dumps(index_cmd), headers=headers)

    content = {"collection_name": "book" }
    res = client.request("POST", urljoin(endpoint, "collection/load"), content=json.dumps(content), headers=headers)
    time.sleep(10)

    query = {
        "collection_name": "book",
        "output_fields": ["book_id"],
        "search_params": [
            {"key": "anns_field", "value": "book_intro"},
            {"key": "topk", "value": "2"},
            {"key": "params", "value": "{\"nprobe\": 10}"},
            {"key": "metric_type", "value": "L2"},
            {"key": "round_decimal", "value": "-1"}
        ],
        "vectors": [ [0.1,0.2] ],
        "dsl_type": 1
    }
    query_res = client.request("POST", urljoin(endpoint, "search"), content=json.dumps(query), headers=headers)

    pprint.pprint(f"{query}")
    pprint.pprint(f"{json.loads(query_res.text)}")

    release_resp = client.request("DELETE", urljoin(endpoint, "collection/load"), content='{"collection_name": "book"}', headers=headers)

    delete = {
        "collection_name": "book",
        "field_name": "book_intro"
    }
    delete_index_res = client.request("DELETE", urljoin(endpoint, "index"), content=json.dumps(delete), headers=headers)


    drop_collection_resp = client.request('DELETE', urljoin(endpoint, "collection"),
                                                            content='{"collection_name": "book"}', headers=headers)




if __name__ == "__main__":
    main()
"""
Milvus can be setup using docker compose which was easy.
Digging through the documentation, Milvus certainly pushes you to use one of their four SDKs: python, Java, what else
Took me a few to figure out that prior to Milvus 2.2.x you needed to manage metadata outside of the vector db through either MySQL or SQLite
The REST API makes you dig through data type names to get to the values; had to dig around in the source for https://github.com/milvus-io/milvus/blob/b68fa2049bc068564b13faa31cee491580395fd7/internal/core/src/common/type_c.h#L55
to learn that varchar is fi
then https://milvus.io/blog/2022-08-08-How-to-use-string-data-to-empower-your-similarity-search-applications.md

"""