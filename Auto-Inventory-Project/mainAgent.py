from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, Agent
import os
from dotenv import load_dotenv
import time
import httpx
from contextlib import asynccontextmanager
from langmem_adapter import LangMemOpenAIAgentToolAdapter
from langmem import create_search_memory_tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig
import chromadb
import requests
import chainlit as cl
import asyncio
from google import genai                          # Google GenAI SDK for Gemini
from google.genai.types import EmbedContentConfig
from langchain_community.document_loaders import PyPDFLoader
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

SERPER_API = os.getenv("SERPER_API")

clientchroma = chromadb.Client()
clientgemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def getPdfPath(file_path:str):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages

user_input = input("Enter File Path: ")
pdfpages = getPdfPath(user_input)

pages_content = [page.page_content for page in pdfpages]
pdf_docs_id = [f"pdf_pages_{i}" for i in range(len(pdfpages))]

try:
    embed_content = clientgemini.models.embed_content(
    model = "gemini-embedding-exp-03-07",
    contents=pages_content,
    config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )   
    print("[DEBUG] Embedding Succesfully Completed")
except Exception as e:
    print(f"[DEBUG] Could not complete embeddings: {e}")

pdf_doc_embeddings = [emb.values for emb in embed_content.embeddings]

collection = clientchroma.create_collection("Inventory")

try: 
    collection.add(
        embeddings=pdf_doc_embeddings,
        documents=pages_content,
        ids=pdf_docs_id
    )

    print(f"[DEBUG] Added {len(pdfpages)} PDF pages to the knowledge base.")
except Exception as e:
    print(f"[DEBUG] Could not add PDF documents to collection, potentially they already exist: {e}")


DB_URL = 'postgresql://neondb_owner:npg_Biwen29oLjXl@ep-damp-pond-adu35pp2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

@asynccontextmanager
async def get_store():
    async with AsyncPostgresStore.from_conn_string(
        DB_URL,
        index={
            "dims":768,
            "embed": GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GEMINI_API_KEY"), model="models/text-embedding-004")
        },
        pool_config=PoolConfig(
            max_size=50,
            min_size=5
        )
    ) as store:
        yield store

namespace = ("assistant", "collection")

search = LangMemOpenAIAgentToolAdapter(
    lambda store, namespace = None: create_search_memory_tool(store=store, namespace=namespace),
    namespace_template=namespace,
    store_provider=get_store
)

searchingTool = search.as_tool()

@function_tool
def GetGoogleIdeas(query:str):
    try:
        embed_content_query = clientgemini.models.embed_content(
            model = "gemini-embedding-exp-03-07",
            contents=query,
            config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        print("[DEBUG] Query Embed Succesfully")
    except Exception as e:
        print(f"[DEBUG] Failed To Query Embed: {e}")
    
    queryEmbed = [queryemb.values for queryemb in embed_content_query.embeddings]

    try:
        data = collection.query(
            query_embeddings=queryEmbed,
            n_results=1,
            include=["documents"]
        )
        print("[DEBUG] Query Fetched Succesfully")
        top_doc = data["documents"][0][0]
        return top_doc
    except Exception as e:
        print(f"[DEBUG] Failed To Fetch Query: {e}")

@function_tool
def SearchTool(query:str):
    headers = {"X-API-KEY": SERPER_API}
    payload = {
        "q": query,
        "gl": "pk",
        "hl": "en"
    }
    res = requests.post("https://google.serper.dev/search", json=payload, headers=headers)
    return res.json().get("organic", [])

@function_tool
def AddProduct(
    name: str,
    description: str,
    price: float,
    price_without_discount: float,
    discount_percent: int,
    in_stock: bool,
    quantity: int,
    category: str,
    image_url: str
    ):

    data = {"name": name, "description": description, "price": price, "price_without_discount": price_without_discount,
            "discount_percent": discount_percent, "in_stock": in_stock, "quantity": quantity, "categpry":category, "image_url": image_url}

    postData = requests.post("http://127.0.0.1:8000/product", json=data)
    if postData.status_code != 200:
        return "Failed To Post Data"
    return "Data posted Succesfully"

MainAgent = Agent(
    name="MainAgent",
instructions = """
You're an AI Inventory Manager & Market Research Assistant for an e-commerce owner.

Your role is to:
1. Understand the user's product or research-related queries.
2. If the user mentions a product (e.g., "Smart Watches"), use the GetGoogleIdeas tool to:
   - Search stored PDF content for product-related info like keywords, sites, and goals.
   - Match based on the closest product in PDF.
3. Use the SearchTool (e.g., Serper) with keywords/sites/goals from PDF to find:
   - Market insights: price range, features, customer ratings, demand trends, etc.
4. Present insights in a clean, bullet-point format so the user can decide.
5. If user approves the product for their store:
   - Use AddProduct tool.
   - Autofill name, description, from search results.
   - Confirm the price with the user before adding.
6. If user asks about trending or in-demand products:
   - Use LangMem memory search tool (searchingTool) to retrieve trends from past conversations or stored memory.
7. Always work in a **step-by-step** flow:
   - First: clarify user intent.
   - Second: search PDF (if needed).
   - Third: fetch Google insights.
   - Fourth: present results.
   - Fifth: confirm before final action.

Important Rules:
- Never hallucinate or assume facts.
- Only use PDF data that matches product name closely.
- Always confirm product approval and price before calling AddProduct.
- Be smart, precise, and business-focused at every step.
""",
    model=model,
    tools=[GetGoogleIdeas, AddProduct, SearchTool, searchingTool]
)

@cl.on_chat_start
async def ChatStart():
    await cl.Message(content="Welcome Admin👀").send()
    cl.user_session.set('history', [])

@cl.on_message
async def Messaging(message:cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(MainAgent, history)
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set('history', history)
    await cl.Message(content=result.final_output).send()