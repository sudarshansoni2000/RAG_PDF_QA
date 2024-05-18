"""
This module is not part of the  pipeline and it is only for showing how we can perform RAG using openai and vectordb in the terminal.

"""

import openai
import yaml
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from typing import List , Tuple 
from utils.load_config import LoadConfig
from openai import OpenAI
# For loading openai credentials
APPCFG = LoadConfig()
client = OpenAI()

with open("configs/app_config.yml") as cfg:
    app_config = yaml.load(cfg , Loader=yaml.FullLoader)


# Load the embedding functions 

embedding = OpenAIEmbeddings()


# Load the vector database
vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                  embedding_function=embedding)

print("Number of vectors in vector db: ", vectordb._collection.count())


while True : 
    question = input("\n\n Enter your question or press 'q' to exit")

    if question.lower() == "q":
        break

    question = "# User New Question:\n" + question
    docs = vectordb.similarity_search(question , k=APPCFG.k)

    retrieved_docs_page_content: List[Tuple] =[str(x.page_content)+"\n\n" for x in docs ]
    retrieved_docs_str = "# Retrieved content :\n\n" + str(retrieved_docs_page_content)
    prompt = retrieved_docs_str + "\n\n" + question

    response = client.chat.completions.create(
        # engine=APPCFG.llm_engine,
        messages= [
            {"role":"system" , "content":APPCFG.llm_system_role},
            {"role":"user", "content":prompt}
        ],
        model="gpt-3.5-turbo"
    )

    print(response.choices[0].message.content)

    
