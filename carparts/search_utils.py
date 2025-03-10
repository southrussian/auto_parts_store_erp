import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_embedding(text):
    if not text:
        return None
    return model.encode(text, convert_to_numpy=True).tolist()


def find_similar_products(search_text, products, threshold=0.3, top_n=5):
    search_embedding = generate_embedding(search_text)
    if search_embedding is None:
        return []

    similarities = []
    for product in products:
        if product.embedding:
            sim = np.dot(search_embedding, product.embedding) / (
                    np.linalg.norm(search_embedding) * np.linalg.norm(product.embedding)
            )
            similarities.append((product, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in similarities if item[1] > threshold][:top_n]
