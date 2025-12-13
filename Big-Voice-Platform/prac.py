# from agents import AsyncOpenAI, Agent, OpenAIChatCompletionsModel, RunContextWrapper, Runner,handoff, function_tool, set_tracing_disabled
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from fastapi import FastAPI, WebSocket
# from gtts import gTTS
# import io
# import os
# import stripe
# import httpx
# from contextlib import asynccontextmanager
# from langmem_adapter import LangMemOpenAIAgentToolAdapter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langmem import create_manage_memory_tool, create_search_memory_tool
# from langgraph.store.postgres import AsyncPostgresStore
# from langgraph.store.postgres.base import PoolConfig
# import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# load_dotenv()

# @asynccontextmanager
# async def get_store():
#     async with AsyncPostgresStore.from_conn_string(
#         os.getenv("NEONDBURL"),
#         index={
#             "dims": 768,
#             "embed": GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GEMINI_API_KEY"), model="models/text-embedding-004")
#         },
#         pool_config=PoolConfig(min_size=5, max_size=20)
#     ) as store:
#         yield store


# async def fetchPastOrders():
#     async with get_store() as store:
#         try:
#             result = await store.asearch(("assistant", "04472414212", "collection"))
#             print(result[0].value["content"])
#         except Exception as e:
#             print(f"Error in Fetching {e}")

# import asyncio 
# asyncio.run(fetchPastOrders())
from agents import AsyncOpenAI, Agent, OpenAIChatCompletionsModel, RunContextWrapper, Runner,handoff, function_tool, set_tracing_disabled
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from gtts import gTTS
import io
import os
import stripe
import httpx
from contextlib import asynccontextmanager
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig
from email.message import EmailMessage
import smtplib
import chromadb
from google.genai import Client
from langchain.document_loaders import PyPDFLoader
from google.genai.types import EmbedContentConfig

load_dotenv()

googleClient = Client(api_key=os.getenv("GEMINI_API_KEY"))
chromaClient = chromadb.Client()

pdf_path = "Policy.pdf"

loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

allPages = [page.page_content for page in pages]
pageIDs = [f"ID {page}" for page in range(len(pages))]

embedContent = googleClient.models.embed_content(
    model="gemini-embedding-exp-03-07",
    contents=allPages,
    config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
)

data = [embed.values for embed in embedContent.embeddings]

collection = chromaClient.create_collection("Policies")

try:
    collection.add(
        documents=allPages,
        embeddings=data,
        ids=pageIDs
    )
    print("[DEBUG] Data Added Succesfully in ChromaDB")

except Exception as e:
    print(f"Failed TO Add Data in ChromaDB: {e}")

def getPolicies():
    try:
        embedQuery = googleClient.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents="Whats your return policy",
        config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )

        queryEmbed = embedQuery.embeddings[0].values

        searching = collection.query(
        n_results=1,
        query_embeddings=queryEmbed,
        include=["documents"]
        )

        data = searching["documents"][0][0]
        return data
    except Exception as e:
        print(f"Error in Quering: {e}")

policies = getPolicies()
print(policies)