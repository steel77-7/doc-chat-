from langchain_text_splitters import RecursiveCharacterTextSplitter
from db.db import chroma_client
from langchain_community.document_loaders import PyPDFLoader

# from db.db import chroma_client
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
)
collection_name = None


def split_text(doc: str):
    loader = PyPDFLoader(doc)
    docs = loader.load()
    texts = text_splitter.split_documents(docs)
    return texts


def make_embeddings(file_name: str):
    docs = split_text(file_name)
    collection_name = file_name.replace("/", "")
    collection = chroma_client.get_or_create_collection(name=collection_name)

    texts = [doc.page_content for doc in docs]

    metadatas = [doc.metadata for doc in docs]

    batch_size = 512

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_metadatas = metadatas[i : i + batch_size]
        batch_ids = [f"doc_{i + j}" for j in range(len(batch_texts))]
        collection.add(
            ids=batch_ids,
            # embeddings=embeddings,
            documents=batch_texts,
            metadatas=batch_metadatas,
        )


def query_func(query_text, file_name):
    collection_name = file_name.replace("/", "")
    collection = chroma_client.get_or_create_collection(name=collection_name)
    result = collection.query(query_texts=[query_text])
    # print(result)
    return result["documents"]


def load_document(file_name):
    split_text(file_name)
    make_embeddings(file_name)
