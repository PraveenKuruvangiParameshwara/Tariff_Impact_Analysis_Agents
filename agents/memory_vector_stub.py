"""Vector memory stub. Replace with Pinecone, Vertex Matching, or similar.", """

class VectorMemory:
    def __init__(self, index_name):
        self.index_name = index_name
        self.store = {}

    def upsert(self, vector_id, metadata_or_vector):
        # For now, store raw metadata for debugging/demo
        print(f"[VectorMemory] Upsert id={vector_id} into index={self.index_name}")
        self.store[vector_id] = metadata_or_vector

    def query(self, query_vector=None, top_k=5):
        # Return top_k dummy matches
        keys = list(self.store.keys())[:top_k]
        return [{'id':k, 'metadata': self.store.get(k)} for k in keys]
