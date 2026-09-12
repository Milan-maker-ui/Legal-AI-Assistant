import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.index = None

    def create_index(self, embeddings):
        embeddings = np.array(embeddings).astype("float32")
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query_embedding, top_k: int = 3):
        query_embedding = np.array(query_embedding).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        return distances, indices
