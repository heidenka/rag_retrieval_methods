import json
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

index_store_path = "../INDEX_creation/index_store"
embeddings_model = OpenAIEmbeddings()

def create_index():
    list_of_documents = []

    with open("../data/units_with_outcome.json", 'r') as file:
        units = json.load(file)
        list_of_documents.extend([str(unit) for unit in units])

    with open("../data/jobs_with_outcome.json", 'r') as file:
        jobs = json.load(file)
        for job in jobs:
            title = job["CleanJobTitle"]
            city = job["CanonCity"]
            description = job["JobText"]
            degree = job["CanonRequiredDegrees"]
            categories = job["categories"]
            valid_outcomes = job["valid_outcomes"]


            data_for_index = f"""The job is {title}. It is located in {city}. 
The job description is as follows: {description}. The degree is {degree}.
The job categories are {categories}. The valid outcomes are {valid_outcomes}"""
            list_of_documents.append(data_for_index)

    _vectorstore = FAISS.from_texts(
        list_of_documents, embedding=embeddings_model
    )

    _vectorstore.save_local(index_store_path)

    return _vectorstore


def load_index():
    _vectorstore = FAISS.load_local(index_store_path, embeddings=embeddings_model)
    return _vectorstore





