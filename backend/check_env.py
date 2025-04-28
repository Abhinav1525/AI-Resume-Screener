# # # import os
# # # print(os.getenv("PINECONE_API_KEY"))



# # import os
# # from dotenv import load_dotenv

# # # Load environment variables from .env file
# # load_dotenv()

# # # Print the value of PINECONE_API_KEY to verify it's loaded
# # print(os.getenv("PINECONE_API_KEY"))


# import faiss
# print(faiss.__version__)



from utils.database import store_resume, search_resumes, index  # Import index from database.py

# Ensure a resume is stored before searching
store_resume("Python developer with experience in AI and data science.", "resume_1")

# Print FAISS index size
print("Total resumes stored in FAISS:", index.ntotal)

# Search for similar resumes
results = search_resumes("Looking for a Python AI expert", top_k=2)

# Print results
print("Search Results:", results)

