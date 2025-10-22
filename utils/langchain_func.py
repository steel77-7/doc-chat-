from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_chroma import Chroma
# from langchain_openai import OpenAIEmbeddings
from db.db import chroma_client
from langchain_community.document_loaders import PyPDFLoader

# from db.db import chroma_client
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
)


def split_text(doc: str):
    loader = PyPDFLoader("pdf_files/" + doc)
    docs = loader.load()
    texts = text_splitter.split_documents(docs)
    return texts


def make_embeddings(file_name: str):
    docs = split_text(file_name)
    collection = chroma_client.get_or_create_collection(name=file_name)

    texts = [doc.page_content for doc in docs]

    metadatas = [doc.metadata for doc in docs]

    batch_size = 512

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_metadatas = metadatas[i : i + batch_size]
        batch_ids = [f"doc_{i + j}" for j in range(len(batch_texts))]

        # response = chroma_client.embeddings.create(
        #     model="text-embedding-3-large", input=batch_texts
        # )

        # embeddings = [d.embedding for d in response.data]

        # Store in Chroma
        collection.add(
            ids=batch_ids,
            # embeddings=embeddings,
            documents=batch_texts,
            metadatas=batch_metadatas,
        )


def query(query_text, file_name):
    collection = chroma_client.get_or_create_collection(name=file_name)
    result = collection.query(query_texts=[query_text])
    print(result["documents"])
