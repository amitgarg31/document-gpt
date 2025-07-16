from loader import load_and_chunk
from embedding import embed_and_store

def ingest_pdf(file_path):
    chunks = load_and_chunk(file_path)
    embed_and_store(chunks)
    print("Ingestion complete.")

# # Example:
# ingest_pdf("offer.pdf")
