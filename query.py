import os
from os.path import join, dirname

from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from index import IndexBuilder

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')


class QueryEngine:
    def __init__(self):
        self.index = IndexBuilder()
        self.chroma_client = self.index.create_embeddings()
        self.embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.chroma_db = Chroma(
            client=self.chroma_client,
            collection_name='financial_reports',
            embedding_function=self.embedding_function,
        )

    def prompt(self):
        template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Use three sentences maximum and keep the answer as concise as possible.
        Always say "thanks for asking!" at the end of the answer.

        {context}

        Question: {question}

        Helpful Answer:"""
        return PromptTemplate.from_template(template)

    def query_engine(self, query):
        llm = ChatOpenAI(model_name='gpt-4-0613')
        chain = RetrievalQA.from_chain_type(
            llm,
            retriever=self.chroma_db.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt()}
        )
        response = chain({'query': query})
        return response['result']
