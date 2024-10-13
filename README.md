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

5. Using the Endpoints
You can interact with the FastAPI application through tools like Postman or using cURL commands in the terminal.

1. Using Postman
   
Postman is a popular API client for testing and interacting with APIs.

By default, app will run on http://127.0.0.1:8000.
Testing the /url-parser Endpoint:
Create a New Request:

In Postman, click on New → Request.
Set the request type to POST.
URL: http://127.0.0.1:8000/url-parser.
Set Headers:

Go to the Headers tab and set the following header:  

Key: Content-Type
Value: application/json
Set Body:

Go to the Body tab and select raw.
Choose JSON format and enter the following body:  

{
  "url": "https://example.com"
}
Send the Request:

Click Send.
You should get a response like:  

{
  "message": "Text parsed and embeddings stored successfully."
}
Testing the /query Endpoint:
Create Another Request:

In Postman, create a new request with POST as the request type.
URL: http://127.0.0.1:8000/query.
Set Headers:

Go to the Headers tab and set:  

Key: Content-Type
Value: application/json
Set Body:

Go to the Body tab, select raw, and choose JSON format.
Enter a query, for example:  

{
  "query": "What is a collective noun?"
}
Send the Request:

Click Send.
You should get a response similar to this:  

{
  "context": "The relevant text chunk",
  "result": "Generated answer based on the context"
}  

2. Using cURL
You can also interact with the API directly from your terminal using cURL.

Testing the /url-parser Endpoint:
Run the following cURL command in your terminal:  

curl -X POST http://127.0.0.1:8000/url-parser \
-H "Content-Type: application/json" \
-d "{\"url\": \"https://example.com\"}"  

You should receive a response like:  

{
  "message": "Text parsed and embeddings stored successfully."
}
Testing the /query Endpoint:
Run the following cURL command in your terminal:  

curl -X POST http://127.0.0.1:8000/query \
-H "Content-Type: application/json" \
-d "{\"query\": \"What is a collective noun?\"}"  

You should receive a response like:  

{
  "context": "The relevant text chunk",
  "result": "Generated answer based on the context"
}
