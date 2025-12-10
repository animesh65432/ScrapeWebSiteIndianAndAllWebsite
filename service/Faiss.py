import faiss
from sentence_transformers import SentenceTransformer

class FaissService:
    def __init__(self, Announcements: list[dict]):
        self.Announcements = Announcements
        self.encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
        self.index = None  
        self.vectors = None
        self.texts = None

    def text_to_vectors(self, texts: list[str]):
        return self.encoder.encode(texts, normalize_embeddings)

    def build_index(self):
        # Choose text or content automatically
        self.texts = []
        for item in self.Announcements:
            if "text" in item and item["text"]:
                self.texts.append(item["text"].strip())
            elif "content" in item and item["content"]:
                self.texts.append(item["content"].strip())
            else:
                self.texts.append("")  # fallback to empty string

        # Encode embeddings
        self.vectors = self.text_to_vectors(self.texts)

        d = self.vectors.shape[1]
        self.index = faiss.IndexFlatIP(d)
        self.index.add(self.vectors)

    def search_duplicates(self, threshold: float = 0.90):

        if self.index is None:
            self.build_index()

        distances, ann = self.index.search(self.vectors, k=2)

        to_remove = set()
        for i in range(len(self.vectors)):
            if distances[i][1] > threshold:
                dup_index = ann[i][1]
                to_remove.add(max(i, dup_index))

        return to_remove

    def get_unique(self, threshold: float = 0.90):

        if self.index is None:
            self.build_index()

        duplicates = self.search_duplicates(threshold)

        unique_items = [
            self.Announcements[i]
            for i in range(len(self.Announcements))
            if i not in duplicates
        ]
        return unique_items
