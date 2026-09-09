from app.ingestion.embeddings import (
    create_query_embedding
)


class Retriever:

    def __init__(
        self,
        vector_store,
        chunks
    ):

        self.vector_store = vector_store
        self.chunks = chunks

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):

        query_embedding = create_query_embedding(
            query
        )

        distances, indices = (
            self.vector_store.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for index, distance in zip(
            indices[0],
            distances[0]
        ):

            if index != -1:

                chunk = self.chunks[index]

                results.append(
                    {
                        "text": chunk["text"],
                        "source": chunk["source"],
                        "page": chunk["page"],
                        "chunk_id": chunk["chunk_id"],
                        "distance": float(distance)
                    }
                )

        return results