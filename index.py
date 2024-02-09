import os
from os.path import join, dirname

import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DataFrameLoader

from data_preprocessor import DataPreprocessor

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')


class IndexBuilder:
    def __init__(self):
        self.preprocess_data = DataPreprocessor()
        self.data = self.preprocess_data.preprocess_data()
        self.loader = DataFrameLoader(self.data, page_content_column="sentence")
        self.documents = self.loader.load()

    def split_texts(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=430,
            chunk_overlap=20,
            length_function=len,
        )

        return text_splitter.split_documents(self.documents)

    def create_embeddings(self):
        documents = []
        metadatas = []
        ids = []
        chroma_client = chromadb.PersistentClient(path='chroma')
        openai_embeddings = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_KEY,
            model_name="text-embedding-ada-002"
        )

        chroma_collection = chroma_client.get_or_create_collection(metadata={"hnsw:space": "cosine"},
                                                                   name="financial_reports",
                                                                   embedding_function=openai_embeddings)

        if not os.path.exists('chroma'):
            for index, doc in enumerate(self.split_texts()):
                documents.append(doc.page_content)

                metadata = doc.metadata.copy()
                metadata['filingDate'] = metadata['filingDate'].strftime('%Y-%m-%d')
                metadatas.append(metadata)

                unique_id = f"{metadata['docID']}_idx{index}"

                ids.append(unique_id)
                chroma_collection.add(documents=documents, metadatas=metadatas, ids=ids)
        return chroma_client