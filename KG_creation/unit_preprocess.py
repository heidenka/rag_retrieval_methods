import json
import os
import ast
from py2neo import Graph, Node, Relationship

import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

categories = [
    'algorithms', 'programming', 'Python', 'computational problem solving', 'computer systems',
    'agile methodology', 'software development', 'professional responsibility',
    'social impacts', 'multidisciplinary team', 'execution model', 'software vulnerabilities',
    'input validation', 'secure programming practices', 'NLP', 'language models', 'vector representations',
    'performance evaluation', 'machine learning', 'data analysis', 'deep learning', 'data integration',
    'data visualization', 'stakeholder communication', 'computer vision',
    'MATLAB', 'image processing', 'internet technologies', 'web applications', 'scripting languages',
    'database implementation', 'SQL', 'imperative programming', 'operating systems', 'penetration testing',
    'numerical data visualization', 'spreadsheet applications', 'computational models',
    'cybersecurity', 'Java', 'object-oriented principles', 'logic programming', 'wireless networks',
    'cloud platforms', 'AI and adaptive systems', 'Internet of Things (IoT)', 'ubiquitous computing',
    'computational modelling', 'engineering synthesis and design processes', 'networking',
    'research investigation', 'machine readable format', 'wireless and mobile networks', 'software quality assurance',
    'formal project correctness', 'data science', 'high-performance computing', 'data warehousing',
    'software engineering', 'IoT applications', 'mathematical foundations', 'graphics programming',
    'data structures and algorithms', 'academic writing', 'multithreading', 'research methodologies',
    'data-driven decision making', 'security concepts'
]


def generate_unit_outcomes(json_data):
    unit_data_list = []

    for i, j in enumerate(json_data):
        unit_data = json_data[str(i)]
        unit_code = unit_data["Unit Code"]
        title = unit_data["Title"]
        print(title)
        school = unit_data["School"]
        content = unit_data["Content"]
        unit_learning_outcomes = unit_data["Unit Learning Outcomes"]

        unit_info = f"{content} {unit_learning_outcomes}"
        instruction = f"""
Your role is to find matching categories. A user will give you a description. 
The list of CATEGORIES is: {categories}. 

Provide only a Python list.
Do not output any codeblocks or ```python
The list should include all matching CATEGORIES.
Don't make up any new categories, use only the ones provided in the CATEGORIES.

"""

        prompt = f"Unit content and outcomes: {unit_info}"

        completions = openai.chat.completions.create(
            #model="gpt-3.5-turbo",
            model="gpt-4-0125-preview",
            temperature=0.0,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt},
            ]
        )

        answer = completions.choices[0].message.content
        try:
            parsed_list = ast.literal_eval(answer)
        except:
            print(f"UNIT FAILED {title} {unit_code}")
            continue

        valid_outcomes = []
        invalid_outcomes = []
        for generated_outcome in parsed_list:
            if generated_outcome in categories:
                valid_outcomes.append(generated_outcome)
            else:
                invalid_outcomes.append(generated_outcome)

        unit_data["outcomes"] = parsed_list
        unit_data["invalid_outcomes"] = invalid_outcomes
        unit_data["valid_outcomes"] = valid_outcomes


        int_unit_code = int(unit_code[4])

        degree = "MA"
        if int_unit_code < 4:
            degree = "BA"

        unit_data["degree"] = degree


        unit_data_list.append(unit_data)

    print(unit_data_list)



    with open("../data/units_with_outcome.json", 'w') as file:
        json.dump(unit_data_list, file, indent=4)

path = "../data/units.json"

with open(path, 'r') as file:
    json_data = json.load(file)
generate_unit_outcomes(json_data)
