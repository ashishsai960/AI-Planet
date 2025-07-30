# main.py
from fastapi import FastAPI,UploadFile,File
import pymupdf
import chromadb
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import openai
from pydantic import BaseModel
from typing import List, Dict,Any


client = chromadb.PersistentClient(path="chroma_db")
collection= client.get_or_create_collection(name="documents")
load_dotenv()
client = openai.OpenAI()

class QueryRequest(BaseModel):
    question: str

app = FastAPI()

@app.post("/upload-document/")
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    full_text =""
    for page in doc:
        full_text+=page.get_text()
    
    doc_id = file.filename
    collection.add(
        documents=[full_text],
        metadatas=[{"filename":file.filename}],
        ids=[doc_id]
    )
    return{
        "filename":file.filename,
        "message":"Document processed and stored successfully"
    }

@app.post("/query/")
async def handle_query(request: QueryRequest):
    results = collection.query(
        query_texts=[request.question],
        n_results=1
    )
    context=""
    if results["documents"]:
        context=results["documents"][0][0]
    else:
        context ="No context found in the knowledge base"
    
    prompt=f""" Based on the following context, please answer the user's question.
    If the context does not contain the answer, say "I do not have enough information to answer that."
    context:
    {context}
    user question:
    {request.question}"""

    try:
        respones = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"You are a helpful assistant"},
                {"role":"user","content":prompt}
            ]

        )
        final_respones = respones.choices[0].message.content
    except Exception as e:
        final_respones=f"An error occurred with AI Model:{e}"
    

    return {"reponse":final_respones}
    # final_respones= f""" Based on the provideed document, here is the answer:
    # Context found: "{context}"and
    # Question found: "{request.question} (This is a simluated from the LLM) """

    # return {"respones": final_respones}

# FIX: Define NodeData first
class NodeData(BaseModel):
    label: str
    query: str | None = None
    fileName: str | None = None
    model: str | None = None
    prompt: str | None = None
    temperature: float | None = None
    webSearch: bool | None = None
    
class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: NodeData



class Edge(BaseModel):
    id: str
    source: str
    target: str

class WorkflowPayload(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    query: str

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/execute/")
def execute_workflow(payload: WorkflowPayload):
    nodes = payload.nodes
    edges = payload.edges
    user_query = payload.query

    final_answer = "Could not determine the workflow."
    
    try:
        user_query_node = next((n for n in nodes if n.type == 'userQuery'), None)
        
        if user_query_node:
            outgoing_edge = next((e for e in edges if e.source == user_query_node.id), None)
            
            if outgoing_edge:
                next_node_id = outgoing_edge.target
                next_node = next((n for n in nodes if n.id == next_node_id), None)

                if next_node and next_node.type == 'llm':
                    llm_prompt = next_node.data.prompt
                    final_answer = f"Simulated LLM response for query '{user_query}' using prompt '{llm_prompt}'"

                elif next_node and next_node.type == 'output':
                     final_answer = f"Workflow routed directly to output with query: {user_query}"
    except Exception as e:
        final_answer = f"An error occurred: {e}"


    return {"answer": final_answer}
