import os
from dotenv import load_dotenv
import vertexai

from worker.ingestion.extractor import PDFExtractor
from worker.ingestion.chunker import SemanticChunker
from worker.vector_store.client import MongoVectorDB
from worker.ingestion.chunking_utils import get_custom_separators
from worker.embeddings.generator import getEmbeddingsPerChunck

load_dotenv()

def main() -> None:
    
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    pdf_extractor = PDFExtractor()
    text = pdf_extractor.extract_text("data/JosueSUpdatedResume.pdf")

    # Initialize the chunker with the separated custom separators
    custom_separators = get_custom_separators()

    # Initialize the chunker with your explicit separators
    chunker = SemanticChunker(
        chunk_size=1000, 
        chunk_overlap=200, 
        separators=custom_separators
    )
    
    source_document = "JosueSUpdatedResume.pdf"
    
    # Check MongoDB to avoid duplicate processing
    mongo_uri = os.environ.get("MONGO_URI")
    db_client = MongoVectorDB(connection_string=mongo_uri)
    
    if db_client.is_document_processed(source_document):
        print(f"Document '{source_document}' is already processed! Skipping embedding generation.")
        return

    # Split the text
    chunks = chunker.split_text(text)

    embeddings = getEmbeddingsPerChunck(chunks)
    
    print("Storing chunks and embeddings in MongoDB...")
    db_client.store_embeddings(
        chunks=chunks, 
        embeddings=embeddings, 
        metadata={"source": source_document}
    )
    print("Successfully stored chunks and embeddings!")


if __name__ == "__main__":
    main()
