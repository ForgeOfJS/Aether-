"""
Utility module for interacting with MongoDB.
"""
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List, Dict, Any, Optional
from dataclasses import asdict
from shared.schemas import EmbeddingDocument


class MongoVectorDB:
    """
    A utility class to handle connecting to MongoDB and storing 
    chunks of text along with their associated vector embeddings.
    """

    def __init__(self, connection_string: str, db_name: str = "rag_db", collection_name: str = "document_embeddings") -> None:
        """
        Initialize the MongoDB client.

        Args:
            connection_string (str): The MongoDB connection string URI.
            db_name (str): The name of the database.
            collection_name (str): The name of the collection to store embeddings.
        """
        self.client: MongoClient = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def is_document_processed(self, source_name: str) -> bool:
        """
        Check if a document has already been processed and its embeddings stored.

        Args:
            source_name (str): The name or identifier of the source document.

        Returns:
            bool: True if the document exists in the database, False otherwise.
        """
        count = self.collection.count_documents({"metadata.source": source_name})
        return count > 0

    def store_embeddings(self, chunks: List[str], embeddings: List[List[float]], metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Store the text chunks and their corresponding embeddings into MongoDB.

        Args:
            chunks (List[str]): The list of extracted text chunks.
            embeddings (List[List[float]]): The corresponding vector embeddings.
            metadata (Optional[Dict[str, Any]]): Any extra metadata to associate with these chunks (e.g. filename).
        """
        if len(chunks) != len(embeddings):
            raise ValueError("The number of chunks must match the number of embeddings.")

        documents = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Instantiate using the standardized schema
            schema_doc = EmbeddingDocument(
                chunk_index=i,
                text=chunk,
                embedding=embedding,
                metadata=metadata
            )
            
            # Convert standard dataclass to dictionary for PyMongo
            doc_dict = asdict(schema_doc)
            
            # Clean up empty metadata to perfectly preserve original functionality
            if not metadata:
                doc_dict.pop("metadata", None)
                
            documents.append(doc_dict)

        if documents:
            self.collection.insert_many(documents)
