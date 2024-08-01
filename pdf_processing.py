import requests
from bs4 import BeautifulSoup
from collections import deque
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import fitz  # PyMuPDF
import json
from pinecone import Pinecone, PineconeException
import numpy as np
import logging
from typing import List
import time
from urllib3.exceptions import ProtocolError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize Pinecone
try:
    pc = Pinecone(api_key="e66c7e18-693a-44e1-998f-d617557eea9f")
    logger.info("Pinecone client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Pinecone client: {e}")
    raise

# Create Pinecone index if it doesn't exist
index_name = "sample"
try:
    if index_name not in pc.list_indexes():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
        )
        logger.info(f"Pinecone index '{index_name}' created successfully")
    else:
        logger.info(f"Pinecone index '{index_name}' already exists")
except PineconeException as e:
    logger.error(f"Error creating Pinecone index: {e}")
    raise

# Connect to the Pinecone index
try:
    index = pc.Index(index_name)
    logger.info(f"Connected to Pinecone index '{index_name}'")
except PineconeException as e:
    logger.error(f"Failed to connect to Pinecone index '{index_name}': {e}")
    raise


class ProcessRequest(BaseModel):
    blog_url: str
    pdf_path: str
    json_paths: List[str]


@app.post("/process-data/")
async def process_data(request: ProcessRequest):
    try:
        # Scrape blog content
        scraped_chunks = scrape_blog(request.blog_url)
        logger.info(f"Scraped {len(scraped_chunks)} chunks from blog")

        # Read PDF content
        pdf_chunks = read_pdf_content(request.pdf_path)
        logger.info(f"Read {len(pdf_chunks)} chunks from PDF")

        # Read JSON content
        json_content = read_json_content(request.json_paths)
        logger.info("Read JSON content")

        # Combine all content into chunks
        all_chunks = scraped_chunks + pdf_chunks + [json.dumps(json_content)]
        logger.info(f"Total chunks to process: {len(all_chunks)}")

        # Save chunks to Pinecone
        save_chunks_to_pinecone(all_chunks)

        return {"result": "Data processed and saved to Pinecone"}

    except Exception as e:
        logger.error(f"An error occurred during data processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def scrape_blog(blog_url: str, chunk_size: int = 300) -> List[str]:
    queue = deque([blog_url])
    visited = set()
    scraped_chunks = []

    try:
        while queue:
            current_url = queue.popleft()
            if current_url not in visited:
                logger.info(f"Crawling: {current_url}")
                response = requests.get(current_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")

                # Only process URLs that are part of the blog content
                if "post-body" in current_url or current_url == blog_url:
                    content_divs = soup.find_all(
                        "div", class_="post-body entry-content"
                    )
                    for div in content_divs:
                        text = div.get_text().strip()
                        chunks = [
                            text[i : i + chunk_size]
                            for i in range(0, len(text), chunk_size)
                        ]
                        scraped_chunks.extend(chunks)

                for link in soup.find_all("a"):
                    href = link.get("href")
                    if href and href.startswith("/") and not "post-edit" in href:
                        full_url = blog_url + href
                        queue.append(full_url)
                visited.add(current_url)
    except requests.RequestException as e:
        logger.error(f"Error scraping blog: {e}")
        raise

    return scraped_chunks


def read_pdf_content(pdf_path: str, chunk_size: int = 300) -> List[str]:
    chunks = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            page_chunks = [
                text[i : i + chunk_size] for i in range(0, len(text), chunk_size)
            ]
            chunks.extend(page_chunks)
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        raise
    return chunks


def read_json_content(json_paths: List[str]) -> dict:
    combined_json_content = {}
    for json_path in json_paths:
        try:
            with open(json_path, "r") as file:
                data = json.load(file)
                for key, value in data.items():
                    combined_json_content[key] = str(value)[
                        :100
                    ]  # Limit each JSON value to 100 characters
        except Exception as e:
            logger.error(f"Error reading JSON file {json_path}: {e}")
            raise
    return combined_json_content


def save_chunks_to_pinecone(chunks: List[str]):
    max_retries = 5

    for i, chunk in enumerate(chunks):
        chunk_id = f"chunk-{i}"
        chunk_vector = generate_document_vector(chunk)

        for attempt in range(max_retries):
            try:
                index.upsert(vectors=[(chunk_id, chunk_vector, {"content": chunk})])
                logger.info(f"Chunk saved to Pinecone: {chunk_id}")
                break
            except ProtocolError as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries} failed for chunk {chunk_id}: {e}"
                )
                if attempt < max_retries - 1:
                    sleep_time = 2**attempt  # Exponential backoff
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error(
                        f"Failed to save chunk {chunk_id} after {max_retries} attempts: {e}"
                    )
                    raise
            except PineconeException as e:
                logger.error(f"Error saving chunk {chunk_id} to Pinecone: {e}")
                raise
            except Exception as e:
                logger.error(
                    f"Unexpected error saving chunk {chunk_id} to Pinecone: {e}"
                )
                raise


def generate_document_vector(document: str) -> List[float]:
    # Placeholder function - replace with your actual embedding model to generate vector representation
    return np.random.rand(1536).tolist()  # Generate a random vector for demonstration


# Run FastAPI server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
