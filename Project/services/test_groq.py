import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm=ChatGroq(
    model=os.environ.get("GROQ_MODEL"),
    temperature=0.7,
    max_tokens=1000,
    max_retries=3,
)
response=llm.invoke("Write a short poem about the beauty of nature.")
import json
print(
    json.dumps(
        response.model_dump(mode="json"),
        indent=4,
        ensure_ascii=False
    )
)