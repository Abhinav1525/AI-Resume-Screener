# from dotenv import load_dotenv
# import os
# from pinecone import Pinecone, ServerlessSpec
# from sentence_transformers import SentenceTransformer

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Pinecone client
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # Create or connect to an index
# index_name = "resume-ranking"
# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=1536,  # Change as per your data
#         metric="euclidean",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1"),
#     )
# print(pc.list_indexes())

# # Connect to the index
# index = pc.Index(name=index_name)

# # Load the embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def get_resume_embedding(text):
#     return model.encode(text).tolist()

# def store_resume(resume_text, candidate_id):
#     vector = get_resume_embedding(resume_text)
#     index.upsert([(candidate_id, vector)])

# def search_resumes(query_text, top_k=5):
#     query_vector = get_resume_embedding(query_text)
#     results = index.query(query_vector, top_k=top_k, include_metadata=True)
#     return results



from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FAISS index
dimension = 384  # Dimension of embeddings from the model
index = faiss.IndexFlatL2(dimension)
metadata = {}

def get_resume_embedding(text):
    return model.encode(text).astype(np.float32)

def store_resume(resume_text, candidate_id):
    vector = get_resume_embedding(resume_text)
    index.add(np.array([vector]))
    metadata[len(metadata)] = {"candidate_id": candidate_id, "resume_text": resume_text}

def search_resumes(query_text, top_k=5):
    if index.ntotal == 0:
        return []

    query_vector = get_resume_embedding(query_text).reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for j, i in enumerate(indices[0]):
        if i == -1:  # No match found
            continue
        candidate = metadata.get(i, {})
        results.append({
            "candidate_id": candidate.get("candidate_id", "Unknown"),
            "distance": distances[0][j],
            "rank": j + 1  # Add ranking
        })
    
    return sorted(results, key=lambda x: x["distance"])

