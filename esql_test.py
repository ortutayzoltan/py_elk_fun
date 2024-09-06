#!/usr/bin/python3

from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
# Example search query

res = es.esql.query( query="FROM fitnotes | KEEP Date,Weight | LIMIT 10",  format="json")
print(res['values'])
