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

possible_skills = [
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


def process_skills(skill_clusters):
    categories = []
    skills = []

    if skill_clusters is not None:
        current_skills = skill_clusters.split(';')

        for skill in current_skills:
            if not skill or skill == "Specialised Skills":
                continue

            cleaned_skill = skill.replace("Specialised Skills", "").replace("|", "").replace("Common Skills", "")

            if not cleaned_skill:
                continue

            index = cleaned_skill.find(":")
            skill_category = cleaned_skill[:index]
            skill_value = cleaned_skill[index+2:]

            if skill_category not in categories:
                categories.append(skill_category)

            if skill_value not in skills:
                skills.append(skill_value)

    return categories, skills


def generate_job_data():
    job_data_list = []

    with open('../data/jobs.json', 'r') as file:
        json_data = json.load(file)

    jobs = json_data["Jobs"]["Job"]

    for job in jobs:
        title = job["CleanJobTitle"]


        print(f"Working on: {title}")

        city = job["CanonCity"]
        job_text = job["JobText"].strip()
        certification = job["CanonCertification"]
        skill_clusters = job["CanonSkillClusters"]
        degree = job["CanonRequiredDegrees"]
        min_experience = job["MinExperience"]
        max_salary = job["MaxAnnualSalary"]

        categories, skills = process_skills(skill_clusters)
        job["categories"] = categories
        job["skills"] = skills

        prompt = f"""
TASK:
Your job is to find the required skills from a job the user provides, while adhering to our guidelines.

GUIDELINES:
- Only use POSSIBLE SKILLS mentioned from our predefined POSSIBLE SKILLS list.
- The list should include all matching POSSIBLE SKILLS.
- Output a python list, without any explanation or apologies.
- Do not output any codeblocks or ```python

POSSIBLE SKILLS:
{possible_skills}
"""

        try:
            completions = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                # model="gpt-3.5-turbo-0125",
                # temperature=0.0,
                max_tokens=1500,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"My Job is: {job_text}"},
                ]
            )
        except:
            print(f"Error at {len(job_data_list)}")
            with open("data/jobs_with_outcome.json", 'w') as file:
                json.dump(job_data_list, file, indent=4)
            return

        answer = completions.choices[0].message.content
        try:
            parsed_list = ast.literal_eval(answer)
        except:
            print(f"JOB FAILED {title}")
            print(answer)
            continue

        valid_outcomes = []
        invalid_outcomes = []
        for generated_outcome in parsed_list:
            if generated_outcome in possible_skills:
                valid_outcomes.append(generated_outcome)
            else:
                invalid_outcomes.append(generated_outcome)

        job["outcomes"] = parsed_list
        job["invalid_outcomes"] = invalid_outcomes
        job["valid_outcomes"] = valid_outcomes

        job_data_list.append(job)

    print("Saving Jobs with Outcomes")

    with open("../data/jobs_with_outcome.json", 'w') as file:
        json.dump(job_data_list, file, indent=4)


generate_job_data()
