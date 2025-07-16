import fitz
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf_fitz(file_path):
    doc = fitz.open(file_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages.append((i + 1, text.strip()))
    doc.close()
    return pages

def chunk_pages(file_path, pages, chunk_size=800, chunk_overlap=100):
    docs = [
        Document(
            page_content=text,
            metadata={
                "page": page_num,
                "source": f"{file_path} - Page {page_num}"
            }
        )
        for page_num, text in pages
    ]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    return chunks

def load_and_chunk(file_path):
    pages = load_pdf_fitz(file_path)
    chunks = chunk_pages(file_path, pages)
    return chunks
