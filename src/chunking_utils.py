"""
Utility functions to support text chunking and splitting operations.
"""
from typing import List, Tuple


def get_best_separator(text: str, separators: List[str]) -> Tuple[str, List[str]]:
    """
    Find the most appropriate separator from the given list to split the text.
    
    The function tries standard priority separators (e.g., paragraph, sentence, 
    word) and returns the first one that appears in the text, along with all 
    subsequent separators for deeper level splitting.

    Args:
        text (str): The body of text to check for separators.
        separators (List[str]): The available separators in descending order of priority.

    Returns:
        Tuple[str, List[str]]: A tuple containing the chosen separator and the 
                               updated list of remaining separators.
    """
    selected_separator = separators[-1]
    remaining_separators = []

    for idx, sep in enumerate(separators):
        if sep == "":
            selected_separator = sep
            break
        if sep in text:
            selected_separator = sep
            remaining_separators = separators[idx + 1:]
            break

    return selected_separator, remaining_separators


def get_custom_separators() -> List[str]:
    """
    Returns the custom sequence of text separators in priority order.
    
    The algorithm typically attempts to split by paragraphs first, 
    then sentences, then words, and finally characters.

    Returns:
        List[str]: A list of separator strings.
    """
    return [
        "\n\n",   # Double newline (Paragraphs)
        "\n",     # Single newline (Line breaks)
        ". ",     # Periods (Sentences)
        "! ",     # Exclamation marks
        "? ",     # Question marks
        " ",      # Spaces (Words)
        ""        # Empty string (Characters as absolute last resort)
    ]
