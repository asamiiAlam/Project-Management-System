
from functools import lru_cache

from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_tokenizer():
    return AutoTokenizer.from_pretrained(MODEL_NAME)


def split_documents(documents):
    """Split a list of documents into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=get_tokenizer(),
        chunk_size=200,
        chunk_overlap=30,
    )

    chunks = splitter.split_documents(documents)

    return chunks
