- [VectorDB Hello World](#vectordb-hello-world)
  - [Pinecone](#pinecone)
  - [OpenSearch](#opensearch)
  - [Vespa](#vespa)
- [Developing](#developing)
- [License](#license)
- [Copyright](#copyright)

## VectorDB Hello World

Samples of querying vector DBs without using vendor-specific clients.

### Pinecone

Sign up for [Pinecone](https://pinecone.io), get an `API_TOKEN` and a `PROJECT_ID`.

Run a working sample as follows.

```
API_KEY=... PROJECT_ID=... ENDPOINT=https://us-west4-gcp-free.pinecone.io poetry run src/pinecone/hello.py

> GET https://controller.us-west4-gcp-free.pinecone.io/databases
< GET https://controller.us-west4-gcp-free.pinecone.io/databases - 200
> POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/vectors/upsert
< POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/vectors/upsert - 200
> POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/query
< POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/query - 200
{'results': [], 'matches': [{'id': 'vec1', 'score': 0.999999881, 'values': [], 'metadata': {'genre': 'drama'}}], 'namespace': 'namespace'}
```

### OpenSearch

You can use a managed service (e.g. [Amazon OpenSearch](https://aws.amazon.com/opensearch-service/)), or download and run open-source OpenSearch with Docker.

```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

Run a working sample as follows.

```
USERNAME=admin PASSWORD=admin ENDPOINT=https://localhost:9200 poetry run src/open_search/hello.py

> GET https://localhost:9200/_cat/indices
< GET https://localhost:9200/_cat/indices - 200
> PUT https://localhost:9200/my-index
< PUT https://localhost:9200/my-index - 200
> POST https://localhost:9200/_bulk
< POST https://localhost:9200/_bulk - 200
> POST https://localhost:9200/my-index/_search
< POST https://localhost:9200/my-index/_search - 200
{'total': {'value': 1, 'relation': 'eq'}, 'max_score': 0.97087383, 'hits': [{'_index': 'my-index', '_id': 'vec1', '_score': 0.97087383, '_source': {'index': {'_index': 'my-index', '_id': 'vec2'}, 'vector': [0.2, 0.3, 0.4], 'metadata': {'genre': 'action'}}}]}
> DELETE https://localhost:9200/my-index
< DELETE https://localhost:9200/my-index - 200
```

### Vespa

You can use the [vespa.ai cloud service](https://cloud.vespa.ai/), or download and run [Vespa](https://vespa.ai/) with Docker.

Make sure you [configure Docker with at least 4GB RAM](https://docs.docker.com/desktop/settings/mac/#resources).

```sh
docker info | grep "Total Memory" # make sure it's at least 4Gb
docker pull vespaengine/vespa
```

Start Vespa.

```
docker run --detach --name vespa --hostname vespa-container \
  --publish 8080:8080 --publish 19071:19071 \
  vespaengine/vespa
```

Deploy the sample application and schema.

```sh
(cd src/vespa/vector-app && zip -r - .) | \
  curl --header Content-Type:application/zip --data-binary @- \
  localhost:19071/application/v2/tenant/default/prepareandactivate

curl --header Content-Type:application/zip -XPOST localhost:19071/application/v2/tenant/default/session
```

Finally, run the Vespa sample ingestion and search. You might have to wait for a few seconds for the endpoint to be ready after the last command.

```sh
ENDPOINT=http://localhost:8080 CONFIG_ENDPOINT=http://localhost:19071 poetry run src/vespa/hello.py

> POST http://localhost:8080/document/v1/vector/vector/docid/vec1
< POST http://localhost:8080/document/v1/vector/vector/docid/vec1 - 200
> POST http://localhost:8080/document/v1/vector/vector/docid/vec2
< POST http://localhost:8080/document/v1/vector/vector/docid/vec2 - 200
> GET http://localhost:8080/search/?yql=select%20%2A%20from%20sources%20%2A%20where%20%7BtargetHits%3A%201%7D%20nearestNeighbor%28values%2Cvector_query_embedding%29&ranking.profile=vector_similarity&hits=1&input.query%28vector_query_embedding%29=%5B0.1%2C0.2%2C0.3%5D
< GET http://localhost:8080/search/?yql=select%20%2A%20from%20sources%20%2A%20where%20%7BtargetHits%3A%201%7D%20nearestNeighbor%28values%2Cvector_query_embedding%29&ranking.profile=vector_similarity&hits=1&input.query%28vector_query_embedding%29=%5B0.1%2C0.2%2C0.3%5D - 200
{'sddocname': 'vector', 'documentid': 'id:vector:vector::vec1', 'id': 'vec1', 'values': {'type': 'tensor<float>(x[3])', 'values': [0.10000000149011612, 0.20000000298023224, 0.30000001192092896]}, 'metadata': {'genre': 'drama'}}
> DELETE http://localhost:19071/application/v2/tenant/default/application/default
< DELETE http://localhost:19071/application/v2/tenant/default/application/default - 200
```

### Milvus

You can use [Zilliz Cloud](https://cloud.zilliz.com/), or download and run [Milvus](https://milvus.io/docs/install_standalone-docker.md) with Docker Compose.

Follow these docs to set up an initial example application: https://milvus.io/docs/manage_connection.md.

Finally, run the Milvus sample ingestion and search included here. 

```sh
% ENDPOINT=http://localhost:9091 poetry run src/milvus/hello.py 
> POST http://localhost:9091/api/v1/collection
< POST http://localhost:9091/api/v1/collection - 200
'{}'
> POST http://localhost:9091/api/v1/entities
< POST http://localhost:9091/api/v1/entities - 200
> POST http://localhost:9091/api/v1/index
< POST http://localhost:9091/api/v1/index - 200
> POST http://localhost:9091/api/v1/collection/load
< POST http://localhost:9091/api/v1/collection/load - 200
> POST http://localhost:9091/api/v1/search
< POST http://localhost:9091/api/v1/search - 200
("{'collection_name': 'book', 'output_fields': ['book_id'], 'search_params': "
 "[{'key': 'anns_field', 'value': 'book_intro'}, {'key': 'topk', 'value': "
 '\'2\'}, {\'key\': \'params\', \'value\': \'{"nprobe": 10}\'}, {\'key\': '
 "'metric_type', 'value': 'L2'}, {'key': 'round_decimal', 'value': '-1'}], "
 "'vectors': [[0.1, 0.2]], 'dsl_type': 1}")
("{'status': {}, 'results': {'num_queries': 1, 'top_k': 2, 'fields_data': "
 "[{'type': 5, 'field_name': 'book_id', 'Field': {'Scalars': {'Data': "
 "{'LongData': {'data': [1, 2]}}}}, 'field_id': 100}], 'scores': [1.45, 4.25], "
 "'ids': {'IdField': {'IntId': {'data': [1, 2]}}}, 'topks': [2], "
 "'output_fields': ['book_id']}, 'collection_name': 'book'}")
> DELETE http://localhost:9091/api/v1/collection/load
< DELETE http://localhost:9091/api/v1/collection/load - 200
> DELETE http://localhost:9091/api/v1/index
< DELETE http://localhost:9091/api/v1/index - 200
> DELETE http://localhost:9091/api/v1/collection
< DELETE http://localhost:9091/api/v1/collection - 200

```

## Developing

See [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md).

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright Daniel Doubrovkine, and contributors.
