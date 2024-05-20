import json

from langchain_community.graphs import Neo4jGraph
import os
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import requests


url = "bolt://localhost:7689"
username ="neo4j"
password = "password"

graph = Neo4jGraph(
    url=url,
    username=username,
    password=password
)

import_url = "https://gist.githubusercontent.com/tomasonjo/08dc8ba0e19d592c4c3cde40dd6abcc3/raw/e90b0c9386bf8be15b199e8ac8f83fc265a2ac57/microservices.json"
import_query = requests.get(import_url).json()['query']
graph.query(import_query) # method to execute queries is just .query

os.environ['OPENAI_API_KEY'] = "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"

#calculate the embedding values and create the vector index
vector_index = Neo4jVector.from_existing_graph(
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    index_name='everything',
    node_label="Team",
    text_node_properties=['name', 'description', 'status'],
    embedding_node_property='embedding',
)

response = vector_index.similarity_search(
    "How will RecommendationService be updated?"
)


vector_qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(), chain_type="stuff", retriever=vector_index.as_retriever())

# question1 = vector_qa.invoke(
#     {"query": "Who is part of team A?"}
# )
#
# print(question1)

question2 = vector_qa.invoke(
    {"query": "Who is RecommendationFeature assigned to?"}
)

print(question2)