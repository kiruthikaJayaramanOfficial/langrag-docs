from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path

def load_all_pdfs(data_dir="data/raw"):
    docs = []
    for pdf_path in Path(data_dir).glob("*.pdf"):
        print(f"Loading: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        for page in pages:
            page.metadata["source_file"] = pdf_path.name
        docs.extend(pages)
        print(f"  → {len(pages)} pages loaded")
    print(f"\nTotal pages loaded: {len(docs)}")
    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"Total chunks created: {len(chunks)}")
    return chunks

def build_index(chunks):
    print("\nLoading embedding model (first time takes ~2 mins)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("data/faiss_index")
    print("✓ Index saved to data/faiss_index/")
    return vectorstore

if __name__ == "__main__":
    print("=== Sprint 2: PDF Ingestion ===\n")
    docs = load_all_pdfs()
    chunks = chunk_documents(docs)
    build_index(chunks)
    print("\n✓ All done! FAISS index is ready.")