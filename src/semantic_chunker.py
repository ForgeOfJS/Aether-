from typing import List
from src.chunking_utils import get_best_separator


class SemanticChunker:
    """
    A utility class used to split text into overlapping chunks based on semantic 
    boundaries (paragraphs, sentences, words). It acts similarly to a recursive 
    character text splitter, ensuring chunks are small enough for an LLM but 
    retain necessary context.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, separators: List[str] = None) -> None:
        """
        Initialize the SemanticChunker instance.

        Args:
            chunk_size (int): The maximum character length of each chunk.
            chunk_overlap (int): The number of characters to overlap between adjacent chunks.
            separators (List[str], optional): The list of separators to use for splitting. 
                                              Defaults to ["\n\n", "\n", " ", ""].
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators if separators is not None else ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        """
        Split the input text into a list of overlapping text chunks.

        Args:
            text (str): The text to be chunked.

        Returns:
            List[str]: A list of text chunks constrained by `chunk_size`.
        """
        return self._split_recursively(text, self.separators)

    def _split_recursively(self, text: str, separators: List[str]) -> List[str]:
        """
        Recursively split the text using the provided sequence of separators.

        Args:
            text (str): The text block to split.
            separators (List[str]): List of separators to sequence through.

        Returns:
            List[str]: A list of chunks.
        """
        if len(text) <= self.chunk_size:
            return [text]

        separator, new_separators = get_best_separator(text, separators)

        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)

        splits = [s for s in splits if s != ""]

        return self._merge_splits(splits, separator, new_separators)

    def _merge_splits(self, splits: List[str], separator: str, new_separators: List[str]) -> List[str]:
        """
        Merge smaller text splits into chunks of size up to `chunk_size`, 
        with `chunk_overlap`.

        Args:
            splits (List[str]): Smaller chunks of text separated by the separator.
            separator (str): The string used to join the splits back.
            new_separators (List[str]): Separators for further recursive splits if needed.

        Returns:
            List[str]: The final merged overlapping chunks.
        """
        docs = []
        current_doc = []
        total_length = 0

        for split in splits:
            split_len = len(split)

            if split_len > self.chunk_size:
                if current_doc:
                    doc = separator.join(current_doc)
                    if doc:
                        docs.append(doc)
                    current_doc = []
                    total_length = 0

                if new_separators:
                    docs.extend(self._split_recursively(split, new_separators))
                else:
                    docs.append(split)
                continue

            separator_len = len(separator) if len(current_doc) > 0 else 0

            if total_length + split_len + separator_len > self.chunk_size:
                if current_doc:
                    doc = separator.join(current_doc)
                    if doc:
                        docs.append(doc)

                    while total_length > self.chunk_overlap or (
                        total_length + split_len + separator_len > self.chunk_size and total_length > 0
                    ):
                        removed_len = len(current_doc[0]) + (len(separator) if len(current_doc) > 1 else 0)
                        total_length -= removed_len
                        current_doc.pop(0)
                        separator_len = len(separator) if len(current_doc) > 0 else 0

            current_doc.append(split)
            total_length += split_len + (len(separator) if len(current_doc) > 1 else 0)

        if current_doc:
            doc = separator.join(current_doc)
            if doc:
                docs.append(doc)

        return docs
