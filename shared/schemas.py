"""
Data schemas for standardized MongoDB documents.
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class EmbeddingDocument:
    """
    Standard schema for a document chunk embedding stored in MongoDB.
    
    Attributes:
        chunk_index (int): The sequential index of the text chunk.
        text (str): The raw text content of the chunk.
        embedding (List[float]): The vector embedding generated for the chunk.
        metadata (Optional[Dict[str, Any]]): Optional metadata fields (e.g., source file).
    """
    chunk_index: int
    text: str
    embedding: List[float]
    metadata: Optional[Dict[str, Any]] = None
