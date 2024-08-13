import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Initialize Pinecone client
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")

pc = Pinecone(api_key=pinecone_api_key)

# Define the index name
index_name = "sample"

# Create the index if it does not exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Dimension of your embeddings
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-west-2"),
    )

# Create or connect to the Pinecone index
index = pc.Index(index_name)


# Initialize OpenAI embeddings
def get_embeddings(text):
    embeddings = OpenAIEmbeddings()
    return embeddings.embed_query(text)


# Function to index documents with context
def index_document_with_context(index, document_id, text):
    index.upsert(
        vectors=[
            {
                "id": document_id,
                "vector": get_embeddings(text),
                "metadata": {"text": text},
            }
        ]
    )


# Function to extract a snippet around the search query
def extract_context(text, query, context_length=20):
    query_index = text.lower().find(query.lower())
    if query_index == -1:
        return text  # Query not found, return full text

    start = max(0, query_index - context_length)
    end = min(len(text), query_index + len(query) + context_length)

    return text[start:end]


# Function to search Pinecone and get context
def search_pinecone_with_text(query, top_k=5):
    query_vector = get_embeddings(query)
    response = index.query(vector=query_vector, top_k=top_k)

    print("Search Results:")
    for match in response["matches"]:
        document_id = match["id"]
        score = match["score"]
        metadata = match.get("metadata", {})

        text = metadata.get("text", "No text available")
        context_snippet = extract_context(text, query)

        print(f"ID: {document_id}")
        print(f"Score: {score}")
        print(f"Context Snippet: {context_snippet}")
        print("\n")


# Example usage: Index a sample document
index_document_with_context(
    index,
    document_id="doc1",
    text="This is a sample text about Carnatic music, which includes various aspects of the traditional music system.",
)

# Example search query
query_text = "saveri"
search_pinecone_with_text(query_text)
