import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from .prompts import DDR_PROMPT

load_dotenv()


def generate_ddr(text):

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    # Free local embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Build vector store
    vectorstore = FAISS.from_texts(chunks, embeddings)

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 6}
    )

    # Retrieve relevant context
    docs = retriever.invoke(text)

    context = "\n\n".join([doc.page_content for doc in docs])

    # OpenRouter LLM
    llm = ChatOpenAI(
        model="openai/gpt-oss-20b",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2
    )

    prompt = DDR_PROMPT.format(context=context)

    response = llm.invoke(prompt)

    return response.content