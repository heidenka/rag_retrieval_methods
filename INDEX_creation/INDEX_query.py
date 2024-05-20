from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from INDEX_creation import load_index
from langchain.globals import set_debug

set_debug(False)

vectorstore = load_index()
llm = ChatOpenAI(model_name="gpt-4-0125-preview")

vector_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

answer = vector_qa.invoke(
    {"query": "How many jobs require knowledge in networking?"}
)
print(answer["result"])

