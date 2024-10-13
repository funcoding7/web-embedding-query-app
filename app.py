from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb
import uvicorn
from transformers import T5ForConditionalGeneration, T5Tokenizer
import logging

# Initialize the FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the SentenceTransformer model for embeddings
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    logging.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load embedding model: {e}")
    raise HTTPException(status_code=500, detail="Failed to load embedding model.")

# Load the T5 model and tokenizer for text generation (configurable for optimization)
MODEL_NAME = "t5-small"  # Can switch to "t5-base" for better quality but slower response
try:
    t5_model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    t5_tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
    logging.info(f"T5 model '{MODEL_NAME}' loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load T5 model '{MODEL_NAME}': {e}")
    raise HTTPException(status_code=500, detail="Failed to load T5 model.")

# Initialize the ChromaDB client and collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("web_embeddings")

# Define Pydantic models for incoming requests
class URLRequest(BaseModel):
    url: HttpUrl  # Validates that the provided URL is in the correct format

class QueryRequest(BaseModel):
    query: str

# Function to extract text from a URL
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful (e.g., HTTP 200)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        if not text:
            logging.error(f"No text extracted from URL: {url}")
            raise HTTPException(status_code=400, detail="No text extracted from the webpage.")

        # Extract text from links (depth of 1)
        links = [a['href'] for a in soup.find_all('a', href=True)]
        for link in links:
            if link.startswith('http'):
                try:
                    link_response = requests.get(link, timeout=5)
                    link_soup = BeautifulSoup(link_response.text, 'html.parser')
                    link_text = link_soup.get_text(separator=' ', strip=True)
                    text += ' ' + link_text
                except requests.RequestException as e:
                    logging.warning(f"Failed to extract text from link {link}: {e}")
                    continue

        return text
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve URL {url}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve URL")

# Function to chunk text into manageable pieces
def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Endpoint to parse a URL and store embeddings
import uuid

@app.post("/url-parser")
def parse_url(request: URLRequest):
    logging.info(f"Received URL: {request.url}")
    
    text = extract_text_from_url(request.url)
    if not text:
        raise HTTPException(status_code=400, detail="No text could be extracted from the given URL.")
    
    chunks = chunk_text(text)
    embeddings = embedding_model.encode(chunks)
    
    for i, embedding in enumerate(embeddings):
        # Generate a unique ID for each chunk
        chunk_id = str(uuid.uuid4())
        collection.add(documents=[chunks[i]], embeddings=[embedding], ids=[chunk_id])

    logging.info("Embeddings stored successfully.")
    return {"message": "Text parsed and embeddings stored successfully."}

# Function to generate an answer based on context using T5
def generate_answer(context, question):
    # Format the input for the T5 model
    input_text = f"question: {question} context: {context}"
    
    # Tokenize and generate the answer
    input_ids = t5_tokenizer.encode(input_text, return_tensors="pt")
    output_ids = t5_model.generate(input_ids, num_beams=5, max_new_tokens=5000, length_penalty=5.0)
    
    # Decode the answer
    answer = t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return answer

# Endpoint to query embeddings and retrieve relevant text chunks
@app.post("/query")
def query_embeddings(request: QueryRequest):
    if not request.query.strip():
        logging.error("Empty query received.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    query_embedding = embedding_model.encode([request.query])
    
    # Search for relevant embeddings in ChromaDB
    try:
        results = collection.query(query_embeddings=query_embedding, n_results=1)
    except Exception as e:
        logging.error(f"Failed to query embeddings: {e}")
        raise HTTPException(status_code=500, detail="Failed to query embeddings.")
    
    if not results['documents']:
        logging.warning("No relevant documents found for the query.")
        raise HTTPException(status_code=404, detail="No relevant documents found")
    
    # Extract the most relevant text chunk
    relevant_chunk = results['documents'][0]
    logging.info(f"Found relevant chunk: {relevant_chunk}")

    # Use T5 model to generate a detailed answer based on the context
    answer = generate_answer(relevant_chunk, request.query)
    
    return {"context": relevant_chunk, "result": answer}

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
