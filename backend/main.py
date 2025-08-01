import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv
import pymupdf  
import chromadb
import openai

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="documents")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI()

db_stacks = {}

class NodeData(BaseModel):
    label: str | None = None
    query: str | None = None
    fileName: str | None = None
    model: str | None = None
    prompt: str | None = None
    temperature: float | None = None
    webSearch: bool | None = None
    updateNodeData: Dict[Any, Any] | None = None 

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

class Workflow(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]

class Stack(BaseModel):
    name: str
    description: str
    workflow: Workflow
@app.post("/upload-document/")
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    full_text = "".join(page.get_text() for page in doc)
    
    response = openai_client.embeddings.create(input=full_text, model="text-embedding-ada-002")
    embedding = response.data[0].embedding
    
    collection.add(
        ids=[file.filename],
        embeddings=[embedding],
        documents=[full_text],
        metadatas=[{"filename": file.filename}]
    )
    return {"filename": file.filename, "message": "Document processed and stored."}

@app.post("/stacks/")
def save_stack(stack: Stack):
    stack_id = f"stack_{len(db_stacks) + 1}"
    db_stacks[stack_id] = stack
    print(f"Stack saved: {stack.name}")
    return {"message": "Stack saved successfully", "stack_id": stack_id}

@app.get("/stacks/")
def get_stacks():
    return db_stacks

@app.post("/execute/")
def execute_workflow(payload: WorkflowPayload):
    nodes = {node.id: node for node in payload.nodes}
    edges = payload.edges
    user_query = ""
    for node in payload.nodes:
        if node.type == 'userQuery':
            user_query = node.data.query or payload.query
            break

    if not user_query:
        return {"answer": "Error: Could not find user query."}

    start_node = next((n for n in payload.nodes if n.type == 'userQuery'), None)
    if not start_node:
        return {"answer": "Error: User Query node not found."}

    current_node_id = start_node.id
    data_payload = user_query  
    context = ""

    while True:
        outgoing_edge = next((e for e in edges if e.source == current_node_id), None)
        if not outgoing_edge:
            break

        target_node = nodes.get(outgoing_edge.target)
        if not target_node:
            break

        if target_node.type == 'knowledgeBase':
            query_embedding = openai_client.embeddings.create(input=data_payload, model="text-embedding-ada-002").data[0].embedding
            results = collection.query(query_embeddings=[query_embedding], n_results=1)
            context = results['documents'][0][0] if results['documents'] else ""
            data_payload = context 

        elif target_node.type == 'llm':
            prompt = target_node.data.prompt or "Answer based on the following: {context}"
            final_prompt = prompt.replace("{context}", context).replace("{query}", user_query)
            
            completion = openai_client.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": final_prompt}
                ]
            )
            data_payload = completion.choices[0].message.content

        current_node_id = target_node.id
    
    return {"answer": data_payload}
