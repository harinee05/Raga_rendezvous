# Raga Rendezvous

**Raga Rendezvous** is an innovative application designed to enhance the learning experience of Carnatic music enthusiasts through AI-driven personalized practice routines. Merging advanced AI techniques with a deep appreciation for traditional music, this project offers a dynamic platform for exploring and mastering Carnatic music.

## Features

- **Personalized Learning**: Tailor-made practice routines based on user proficiency levels.
- **Interactive Chatbot**: Engage with an AI-powered chatbot for real-time guidance on Carnatic music.
- **Contact Form**: Reach out for inquiries or feedback, with optional file uploads.
- **Quiz Application**: Test your knowledge of Carnatic music with interactive quizzes.
- **Content Retrieval**: Advanced Retrieval-Augmented Generation (RAG) for precise and contextually relevant responses.
- **Vector Search**: Efficient data retrieval using Pinecone for handling Carnatic music content.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: MongoDB (for contact form submissions), Pinecone (for vector storage)
- **AI/ML**: OpenAI (for generating responses), Pinecone (for RAG)
- **PDF Processing**: PyMuPDF (Fitz) for handling PDF documents
- **Web Scraping**: BeautifulSoup for extracting content from web pages

## Project Structure

- `raga_rendezvous.py`: Main Streamlit application for UI and navigation.
- `ragarend.py`: Contains AI logic, including Pinecone integration and RAG implementation.
- `contact.py`: Manages the contact form functionality and document uploads.
- `pdf_processing.py`: Handles PDF extraction and chunking for data ingestion.
- `RequestProcess.py`: Manages the processing of contact form submissions and file uploads.
- `requirements.txt`: Lists required Python libraries.
- `.env`: Stores environment variables such as MongoDB URI and Pinecone API key.

## File Descriptions

### `pdf_processing.py`

This file is responsible for extracting text from PDF documents and preparing it for indexing. Key functionalities include:

- **PDF Extraction**: Utilizes PyMuPDF (Fitz) to extract text from PDF files.
- **Chunking**: Splits the extracted text into smaller chunks to make it manageable for indexing and retrieval.
- **Text Preparation**: Prepares text chunks for ingestion into the vector store by ensuring that they are clean and properly formatted.

### `RequestProcess.py`

This file handles the processing of contact form submissions and file uploads. Key functionalities include:

- **Form Data Handling**: Processes and stores data submitted through the contact form.
- **File Upload Management**: Manages the upload and storage of files associated with contact submissions.
- **Data Validation**: Ensures that the submitted data and files meet the required formats and constraints before storage.

## RAG Implementation

### Data Preparation

1. **PDF Processing**: Extract and chunk text from PDFs using `pdf_processing.py`.
2. **Web Content Scraping**: Extract and structure text from blog pages using BeautifulSoup.
3. **JSON Data Handling**: Read and structure JSON data about ragas and swaras.

### Data Ingestion into Pinecone

1. **Vector Generation**: Convert text chunks into vectors using embedding models.
2. **Pinecone Indexing**: Store and retrieve vectors efficiently with Pinecone.
3. **Error Handling**: Robust error handling for API interactions and data processing.

## How to Run

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud instance)
- Pinecone account (for API key)
- Required Python libraries (listed in `requirements.txt`)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/harineepurushothaman/raga-rendezvous.git
   cd raga-rendezvous
2. **Install Dependencies**:
   ``bash
   pip install -r requirements.txt
3. **Set Up Environment Variables**: Create a .env file in the project root with the following content:
   ``bash
   MONGO_URI=your_mongo_uri
   PINECONE_API_KEY=your_pinecone_api_key
4. **Run the FastAPI server**:
   ``bash
   uvicorn pdf_processing:app --reload
5. **Run through the docs to move into pinecone**:
   ``bash
   python RequestProcess.py
6. **Run the streamlit-app**:
   ``streamlit run raga_rendezvous.py

