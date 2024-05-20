from py2neo import Graph, Node, Relationship
import json
import os

graph = Graph("bolt://localhost:7689", user="neo4j", password="new_jobs")


def create_or_get_node(label, **properties):
    node = graph.nodes.match(label, **properties).first()

    if node is None:
        node = Node(label, **properties)
        graph.create(node)

    return node


def createUnitNodes():
    with open("../data/units_with_outcome.json", 'r') as file:
        unit_data = json.load(file)

    for unit in unit_data:
        unit_code = unit["Unit Code"]
        title = unit["Title"]
        school = unit["School"]
        content = unit["Content"]
        unit_learning_outcomes = unit["Unit Learning Outcomes"]
        generated_outcomes = unit["outcomes"]
        degree = unit["degree"]

        unit_node = create_or_get_node("Unit", name=title, code=unit_code, description=content,
                                       learning_outcomes=unit_learning_outcomes, degree=degree)
        school_node = create_or_get_node("School", name=school)

        graph.merge(Relationship(unit_node, "AT_SCHOOL", school_node))

        for skill in generated_outcomes:
            skill_node = create_or_get_node("Skill", name=skill)
            graph.merge(Relationship(unit_node, "TEACHES", skill_node))


def createJobNodes():
    with open("../data/jobs_with_outcome.json", 'r') as file:
        job_data = json.load(file)

    for job in job_data:
        title = job["CleanJobTitle"]
        city = job["CanonCity"]
        description = job["JobText"]
        certification = job["CanonCertification"]
        skill_clusters = job["CanonSkillClusters"]
        degree = job["CanonRequiredDegrees"]
        categories = job["categories"]
        skills = job["skills"]
        parsed_list = job["outcomes"]
        invalid_outcomes = job["invalid_outcomes"]
        valid_outcomes = job["valid_outcomes"]

        min_experience = job["MinExperience"]
        if min_experience is not None:
            min_experience = int(float(min_experience))

        max_salary = job["MaxAnnualSalary"]
        if max_salary is not None:
            max_salary = int(float(max_salary))

        degree_list = None
        if degree is not None:
            degree_list = degree.split("|")


        job_node = create_or_get_node("Job",
                                      name=title,
                                      description=description,
                                      max_salary=max_salary,
                                      min_experience=min_experience,
                                      degree=degree_list
                                      )

        city_node = create_or_get_node("City", name=city)
        graph.merge(Relationship(job_node, "LOCATED_IN", city_node))



        for skill in valid_outcomes:
            skill_node = create_or_get_node("Skill", name=skill)
            graph.merge(Relationship(job_node, "REQUIRES", skill_node))

        for category in categories:
            category_node = create_or_get_node("Category", name=category)
            graph.merge(Relationship(job_node, "HAS_CATEGORY", category_node))


createUnitNodes()
createJobNodes()
