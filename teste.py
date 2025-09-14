# pip install openai==1.40.0  # ou versão recente


from dotenv import load_dotenv
load_dotenv()
from openai import AzureOpenAI
import os

# Chat (gpt-4o-mini)
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

resp = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    messages=[{"role":"user","content":"Ping?"}],
    max_tokens=10,
)
print("Chat OK:", resp.choices[0].message.content)

# Embeddings (text-embedding-3-small)
emb_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_EMBEDDINGS_API_KEY", os.getenv("AZURE_OPENAI_API_KEY")),
    api_version=os.getenv("AZURE_OPENAI_EMBEDDINGS_API_VERSION", os.getenv("AZURE_OPENAI_API_VERSION")),
    azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDINGS_ENDPOINT", os.getenv("AZURE_OPENAI_ENDPOINT")),
)

e = emb_client.embeddings.create(
    model=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT"),
    input="hello world",
)
print("Embeddings OK: dim", len(e.data[0].embedding))