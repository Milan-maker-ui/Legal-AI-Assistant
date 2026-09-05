def split_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150
):
    """
    Split text into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(documents):
    """
    Create chunks while preserving metadata.
    """

    all_chunks = []

    for document in documents:

        text_chunks = split_text(
            document["text"]
        )

        for chunk_id, chunk in enumerate(text_chunks):

            all_chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "page": document["page"],
                    "chunk_id": chunk_id
                }
            )

    return all_chunks