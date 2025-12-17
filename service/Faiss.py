import faiss
from sentence_transformers import SentenceTransformer
from app_types.annoucement import GovtItem

class FaissService:
    def __init__(self, announcements: list[GovtItem]):
        self.announcements = announcements
        self.encoder = SentenceTransformer("paraphrase-mpnet-base-v2")

    def _dedup_text(self, item: GovtItem) -> str | None:
        if item.get("title"):
            return item["title"].strip()

        content = item.get("content", "").strip()
        if content:
            # Use only first 300 chars to avoid boilerplate
            return content[:300]

        return None

    def get_unique(self, threshold: float = 0.95):
        texts = []
        items = []

        for item in self.announcements:
            text = self._dedup_text(item)
            if text:
                texts.append(text)
                items.append(item)

        if len(texts) <= 1:
            return items

        vectors = self.encoder.encode(texts, normalize_embeddings=True)
        d = vectors.shape[1]

        index = faiss.IndexFlatIP(d)
        index.add(vectors)

        distances, indices = index.search(vectors, k=2)

        to_remove = set()
        for i in range(len(indices)):
            sim = distances[i][1]
            j = indices[i][1]

            if sim >= threshold and j > i:
                to_remove.add(j)

        return [
            items[i]
            for i in range(len(items))
            if i not in to_remove
        ]
