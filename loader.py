from pypdf import PdfReader


def load_pdf(pdf_path: str):
    """
    Extract text from a PDF.

    Returns:
        List of dictionaries containing:
        - text
        - source
        - page
    """

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if text and text.strip():

            documents.append(
                {
                    "text": text.strip(),
                    "source": str(pdf_path),
                    "page": page_number + 1
                }
            )

    return documents