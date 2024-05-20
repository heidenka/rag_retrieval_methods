from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain.globals import set_debug

url = "bolt://localhost:7689"
username = "neo4j"
password = "new_jobs"
database = "neo4j"
graph = Neo4jGraph(
    url=url,
    username=username,
    password=password
)
set_debug(False)

graph.refresh_schema()

cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(temperature=0.0, model_name='gpt-4-0125-preview'),
    qa_llm=ChatOpenAI(temperature=0, model_name='gpt-4-0125-preview'),
    graph=graph, verbose=True,
)

answer = cypher_chain.invoke({"query": "How many jobs require knowledge in networking?"})
print(answer)

