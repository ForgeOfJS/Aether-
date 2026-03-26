import PyPDF2

class PDFExtractor:
    """
    A utility class used to extract text from PDF documents using the PyPDF2 library.
    """

    def __init__(self) -> None:
        """
        Initialize the PDFExtractor instance.
        """
        pass

    def extract_text(self, file_path: str) -> str:
        """
        Extract text content from the given PDF file.

        Args:
            file_path (str): The absolute or relative path to the PDF file.

        Returns:
            str: The fully extracted text from all pages of the PDF.

        Raises:
            FileNotFoundError: If the specified PDF file cannot be found.
            Exception: If an error occurs during PDF processing or reading.
        """
        extracted_text = []

        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)

        return "\n".join(extracted_text)
