import os
import logging
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from src.crawl import crawl_and_save_data
from src.seed_data import seed_qdrant

logging.basicConfig(level=logging.INFO)


# Load variable enviroment
load_dotenv()
qdrant_host = os.getenv("QDRANT_HOST")
qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_collection_name = os.getenv('QDRANT_COLLECTION_NAME')
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_model = os.getenv("EMBEDDING_MODEL")
url_web_crawl_history = os.getenv("URL_WEB_CRAWL_HISTORY")
url_web_crawl_culture = os.getenv("URL_WEB_CRAWL_CULTURE")
doc_name_history = os.getenv("DOC_NAME_HISTORY")
doc_name_culture = os.getenv("DOC_NAME_CULTURE")
directory_data = os.getenv("DIRECTORY_DATA")


if __name__=='__main__':
    chunk_size = 3000
    chunk_overlap = 500
    
    # Step 1: Crawl and save data 
    logging.info('Start crawl data')
    crawl_and_save_data(url_web_crawl=url_web_crawl_history, chunk_size=chunk_size, chunk_overlap=chunk_overlap, doc_name=doc_name_history, directory_data=directory_data)
    logging.info('Crawl Vietnamese history data successfully!')

    crawl_and_save_data(url_web_crawl=url_web_crawl_history, chunk_size=chunk_size, chunk_overlap=chunk_overlap, doc_name=doc_name_culture, directory_data=directory_data)
    logging.info('Crawl Vietnamese culture data successfully!')

    embeddings = OpenAIEmbeddings(
        model=embedding_model,
        openai_api_key=openai_api_key,
    )
    
    # Step 2: send data to Qdrant database
    logging.info('Start send data')
    seed_qdrant(qdrant_host=qdrant_host, qdrant_api_key=qdrant_api_key, collection_name=qdrant_collection_name, embedding_model=embeddings, filename=doc_name_history, directory=directory_data)
    logging.info('Send send Vietnamese history data successfully!')

    seed_qdrant(qdrant_host=qdrant_host, qdrant_api_key=qdrant_api_key, collection_name=qdrant_collection_name, embedding_model=embeddings, filename=doc_name_culture, directory=directory_data)
    logging.info('Send send Vietnamese culture data successfully!')

    logging.info('Send all data successfully!')