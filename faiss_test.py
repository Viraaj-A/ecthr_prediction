from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load the .pkl file
with open('documents/all_documents_text.pkl', 'rb') as f:
    results = pickle.load(f)

# Load the SentenceTransformer model
model = SentenceTransformer('embedding_model')

# Load the FAISS index
index = faiss.read_index('faiss_index/bert_sentence_transformer.faiss')

# Sentence transformer inference
def search(query_text, top_k=5):
    # Encode the query
    query_vector = model.encode([query_text])

    # Search the Faiss index
    distances, indices = index.search(query_vector, top_k)

    # Retrieve the original rows for the closest matches
    closest_rows = [results[i] for i in indices[0]]

    return closest_rows

# Querying the model
'''
Items 1-6 correspond to the following in order - url, entire_text, case_title, importance_number, judgment_date, facts, conclusion
'''

query = "An officer of the law physically assaulted me without any apparent or communicated reason?"
top_results = search(query, top_k=5)
print(type(top_results))