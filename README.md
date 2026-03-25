# ForgeOfJS-RAG

This project implements a basic Retrieval-Augmented Generation (RAG) system using Google Vertex AI for embeddings and MongoDB for vector storage.

## Features

- **PDF Text Extraction**: Extracts text from PDF documents.
- **Semantic Chunking**: Splits text into overlapping chunks using semantic boundaries.
- **Vertex AI Embeddings**: Generates vector embeddings for text chunks.
- **MongoDB Storage**: Stores chunks and embeddings in a MongoDB database.
- **Duplicate Prevention**: Checks if a document has already been processed before embedding.

## Prerequisites

- Python 3.8+
- MongoDB instance
- Google Cloud Project with Vertex AI enabled

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd ForgeOfJS-RAG
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
PROJECT_ID=your-gcp-project-id
LOCATION=your-gcp-location
MONGO_URI=your-mongodb-connection-string
```

## Usage

Run the main script to process a PDF:

```bash
python main.py
```

The script will:

1. Extract text from `data/<pdf_file>`
2. Split the text into chunks
3. Generate embeddings using Vertex AI
4. Store the chunks and embeddings in MongoDB

## Project Structure

```
ForgeOfJS-RAG/
├── data/
│   └── JosueSUpdatedResume.pdf
├── src/
│   ├── pdf_extractor.py
│   ├── semantic_chunker.py
│   ├── mongo_utils.py
│   ├── schemas.py
│   └── chunking_utils.py
├── .env
├── main.py
└── requirements.txt
```

## License

This project is licensed under the MIT License.
