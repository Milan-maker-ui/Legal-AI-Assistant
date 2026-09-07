from sentence_transformers import SentenceTransformer


# Load embedding model once
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings(texts):
    """
    Convert a list of texts into embeddings.
    """

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings


def create_query_embedding(query: str):
    """
    Convert user question into an embedding.
    """

    embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    return embedding