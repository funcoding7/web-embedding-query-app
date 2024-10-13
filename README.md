# web-embedding-query-app
This project is a FastAPI-based application that extracts text from webpages, generates embeddings for text chunks using the SentenceTransformer model, and allows users to query those embeddings to retrieve relevant text or generate detailed answers using the T5 model.

Features
URL Text Parsing:

Extracts text from a webpage (including linked pages up to depth 1) using BeautifulSoup.
Splits the text into manageable chunks.
Encodes each chunk into embeddings using the SentenceTransformer model.
Stores the embeddings in ChromaDB, a vector database, for efficient querying.
Text Query and Answer Generation:

Users can input a query, which is encoded into an embedding.
The system searches for the most relevant text chunk in ChromaDB based on the query embedding.
It generates detailed answers from the retrieved text chunk using the T5 model.
Error Handling:

Proper validation and error handling for invalid URLs, empty queries, failed embedding searches, and other edge cases.
Technologies Used
FastAPI: For creating the RESTful API endpoints.
Sentence-Transformers: To generate embeddings from the text chunks.
ChromaDB: For storing and querying embeddings.
Transformers (T5): To generate detailed answers based on retrieved text chunks.
BeautifulSoup: For web scraping and extracting text from URLs.
Uvicorn: ASGI server to run the FastAPI app.
Endpoints
1. /url-parser (POST)
Description: Parse a webpage, extract its text, create embeddings for text chunks, and store them in ChromaDB.
Request:
Body:
json
Copy code
{
  "url": "https://example.com"
}
url: The URL of the webpage to parse.
Response:

{
  "message": "Text parsed and embeddings stored successfully."
}  

2. /query (POST)
Description: Query the stored embeddings with a question, retrieve the most relevant text chunk, and generate an answer using T5.
Request:
Body:

{
  "query": "What is a collective noun?"
}
query: The question or text to search for.
Response:
json
{
  "context": "The relevant text chunk",
  "result": "Generated answer based on the context"
}
# Setup and Installation
1. Clone the repository
   
git clone https://github.com/funcoding7/web-embedding-query-app.git

cd web-embedding-query-app  

2. Set up a Python environment
   
python -m venv venv  

source venv/bin/activate   # On Windows: venv\Scripts\activate  

3. Install the dependencies
   
pip install -r requirements.txt  

4. Run the FastAPI app
   
uvicorn app:app --reload
