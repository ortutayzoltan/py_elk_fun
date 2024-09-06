#!/usr/bin/python3

from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
# Example search query

res = es.search(index="fitnotes", body={"query": {"match_all": {}}})
print(res['hits']['hits'])
