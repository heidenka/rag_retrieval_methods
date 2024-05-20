import openai
import os
from py2neo import Graph


def generate_schema(graph):
    node_properties_query = """
    CALL apoc.meta.data()
    YIELD label, other, elementType, type, property
    WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
    WITH label AS nodeLabels, collect(property) AS properties
    RETURN {labels: nodeLabels, properties: properties}
    """

    rel_properties_query = """
    CALL apoc.meta.data()
    YIELD label, other, elementType, type, property
    WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
    WITH label AS nodeLabels, collect(property) AS properties
    RETURN {type: nodeLabels, properties: properties}
    """

    rel_query = """
    CALL apoc.meta.data()
    YIELD label, other, elementType, type, property
    WHERE type = "RELATIONSHIP" AND elementType = "node"
    RETURN {source: label, relationship: property, target: other}
    """

    node_props = graph.run(node_properties_query).data()
    rel_props = graph.run(rel_properties_query).data()
    rels = graph.run(rel_query).data()
    return f"""
        This is the schema representation of the Neo4j database.
        Node properties are the following:
        {node_props}
        Relationship properties are the following:
        {rel_props}
        Relationship point from source to target nodes
        {rels}
        Make sure to respect relationship types and directions.
    """


def promptMe(prompt):
    completions = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    anwser = completions.choices[0].message.content
    return anwser




graph = Graph("neo4j://localhost:7687", user="neo4j", password="acre-orange-fabrications")

schema = generate_schema(graph)

#print(schema)

print(promptMe("HI"))


