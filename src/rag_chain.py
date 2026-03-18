from groq import Groq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Loading FAISS index...")
vectorstore = FAISS.load_local(
    "data/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
print("✓ RAG chain ready!\n")

def build_prompt(question, context_chunks):
    context = "\n\n".join([
        f"[Source: {c.metadata.get('source_file','?')}, "
        f"Page {c.metadata.get('page','?')}]\n{c.page_content}"
        for c in context_chunks
    ])
    return f"""You are a helpful assistant for vehicle and laptop manuals.
Answer ONLY using the context below. If the answer is not in the context, say "I could not find this in the manuals."
At the end of your answer, always cite sources as (filename, page number).

Context:
{context}

Question: {question}

Answer:"""

def ask(question):
    chunks = retriever.get_relevant_documents(question)
    prompt = build_prompt(question, chunks)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    sources = list(set([
        f"{c.metadata.get('source_file','?')} — page {c.metadata.get('page','?')}"
        for c in chunks
    ]))
    return answer, sources

if __name__ == "__main__":
    print("=== Sprint 3: Testing RAG Chain ===\n")
    questions = [
        "What is the oil change interval for Fortuner?",
        "How do I connect to WiFi on Lenovo ThinkPad?",
        "What type of coolant should I use for Innova Crysta?",
        "How do I replace the battery on Dell Inspiron?",
        "What is the warranty period for HP laptop?"
    ]
    for q in questions:
        print(f"Q: {q}")
        answer, sources = ask(q)
        print(f"A: {answer}")
        print(f"Sources: {sources}")
        print("─" * 60)