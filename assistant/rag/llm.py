import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from api import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def query_gemini(question, persist_dir="vector_store", top_k=3):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )

    docs = vectordb.similarity_search(question, k=top_k)
    print(docs,"docs")
    context = "\n\n".join([doc.page_content for doc in docs])
    for doc in docs:
        print(doc.metadata,"doc.metadeta")
    sources = [doc.metadata for doc in docs]

    prompt = f"Answer the question using only the context below:\n\n{context}\n\nQ: {question}\nA:"

    response = model.generate_content(prompt)

    return {
        "answer": response.text.strip(),
        "sources": sources
    }
