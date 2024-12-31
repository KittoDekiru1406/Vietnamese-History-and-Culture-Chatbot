import os
import re
import json
from langchain_community.document_loaders import RecursiveUrlLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging

LOGGER = logging.getLogger(__name__)

load_dotenv()
def bs4_extractor(html: str) -> str:
    """
    Extract and clean content from HTML
    Args:
        html: HTML string to process
    Returns:
        str: Cleaned text, removing HTML tags and extra whitespace
    """
    soup = BeautifulSoup(html, "html.parser")  # Parse HTML
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()  # Remove extra whitespace and empty lines

def crawl_web(url_data: str, chunk_size: int, chunk_overlap: int) -> list:
    """
    Crawl data from a URL recursively
    Args:
        url_data (str): Root URL to start crawling
    Returns:
        list: List of Document objects, each object containing split content
              and corresponding metadata
    """
    # Create a loader with a maximum depth of 4 levels
    loader = RecursiveUrlLoader(url=url_data, extractor=bs4_extractor, max_depth=4)
    docs = loader.load()  # Load content
    print('length: ', len(docs))  # Print the number of loaded documents

    # Split text into chunks of 10000 characters, with 500 character overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(docs)
    print('length_all_splits: ', len(all_splits))  # Print the number of text chunks after splitting
    return all_splits

def web_base_loader(url_data: str, chunk_size: int, chunk_overlap: int) -> list:
    """
    Load data from a single URL (non-recursive)
    Args:
        url_data (str): URL to load data from
    Returns:
        list: List of split Document objects
    """
    loader = WebBaseLoader(url_data)  # Create a basic loader
    docs = loader.load()  # Load content
    print('length: ', len(docs))  # Print the number of documents

    # Split text similarly to above
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(docs)
    return all_splits

def save_data_locally(documents, filename, directory):
    """
    Save a list of documents to a JSON file
    Args:
        documents (list): List of Document objects to save
        filename (str): JSON filename (e.g., 'data.json')
        directory (str): Directory path to save the file
    Returns:
        None: This function does not return a value, it only saves the file and prints a message
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)  # Create the full file path

    # Convert documents to a serializable format
    data_to_save = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in documents]
    # Save to JSON file
    with open(file_path, 'w') as file:
        json.dump(data_to_save, file, indent=4)
    print(f'Data saved to {file_path}')  # Print a success message

def crawl_and_save_data(url_web_crawl: str, chunk_size: int, chunk_overlap: int, doc_name: str, directory_data: str) -> None:
    """
    Crawls data from a specified website, saves it locally, and prints the crawled data.

    This function orchestrates the process of:
    1. Crawling content from the given URL.
    2. Saving the extracted data into a JSON file within the specified directory.
    3. Printing the crawled data to the console for verification purposes.

    Args:
        url_web_crawl (str): The URL of the website to crawl.
        chunk_size (int): The size of text chunks to split the crawled content into. This is likely used for further processing, such as vectorization.
        chunk_overlap (int): The number of overlapping characters between consecutive text chunks. This helps maintain context between chunks.
        doc_name (str): The desired name for the saved JSON file (without the extension).
        directory_data (str): The directory where the crawled data will be saved as a JSON file.

    Returns:
        None: This function does not explicitly return any value. Its primary effect is saving data to a file and printing to the console.
    """

    data = crawl_web(url_web_crawl, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    LOGGER.info("Crawl successfully!")

    save_data_locally(data, doc_name , directory_data)
    LOGGER.info("Save data in local successfully!")