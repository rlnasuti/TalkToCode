from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import GitLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from urllib.parse import urlparse

import os
import subprocess

load_dotenv()

EMBEDDINGS_CHUNK_SIZE=10
GPT_MODEL="gpt-3.5-turbo"

def get_default_branch(repo_url):
    # Fetch the branches
    branches = subprocess.getoutput(f"git ls-remote --heads {repo_url}")

    # Check if 'master' exists, if not, then use 'main'
    if "refs/heads/master" in branches:
        return "master"
    elif "refs/heads/main" in branches:
        return "main"
    else:
        return None

user_input = input("What is the url for the repository you'd like to speak with? ")
parsed_url = urlparse(user_input)
repo_name = parsed_url.path.split('/')[-1].replace('.git', '')
embeddings = OpenAIEmbeddings(chunk_size=EMBEDDINGS_CHUNK_SIZE, allowed_special={'<|endoftext|>'})

if not os.path.exists(f"./dbs/{repo_name}/faiss_index"):
    loader = GitLoader(
        clone_url=user_input,
        repo_path=f"./repos/{repo_name}",
        branch=get_default_branch(user_input),
    )

    source_code = loader.load_and_split()

    db = FAISS.from_documents(documents=source_code, embedding=embeddings)
    db.save_local(f"./dbs/{repo_name}/faiss_index")

    print("Source code loaded! You can now start talking with the code.")
else:
    db = FAISS.load_local(f"./dbs/{repo_name}/faiss_index", embeddings=embeddings)
    print("Existing source code loaded! New changes may not be indexed.")

llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm,retriever=db.as_retriever())

while(True):
    user_input=input("Me: ")
    answer = qa_chain({"query": user_input})
    print(answer['result'])