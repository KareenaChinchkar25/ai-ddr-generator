from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


def build_vectorstore(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(chunks, embeddings)

    return vectorstore
