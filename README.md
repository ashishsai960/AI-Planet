GenAI Stack - Visual Workflow Builder
This project is a No-Code/Low-Code web application designed to enable users to visually create and interact with intelligent workflows. Users can build "stacks" by dragging, dropping, and connecting components on a canvas. Once a workflow is built, users can interact with it through a chat interface to get real-time, AI-powered answers.

Key Features
Visual Workflow Builder: Drag-and-drop interface powered by React Flow to create and connect workflow nodes.

Component-Based System: Build workflows using modular components like User Query, Knowledge Base, LLM (OpenAI), and Web Search.

Stack Management: A dashboard to view all saved workflows and a modal to create new ones.

Workflow Persistence: Save your created workflows to the backend.

Interactive Chat: Test and run your workflows through a real-time chat modal.

File Uploads: The Knowledge Base component supports PDF uploads for context-aware AI responses.

Dockerized Deployment: The entire application is containerized for easy setup and consistent deployment.

Tech Stack
Category	Technology
Frontend	React.js
Backend	FastAPI (Python)
Drag & Drop	React Flow
Vector Store	ChromaDB
Text Extraction	PyMuPDF
AI Models	OpenAI GPT (LLM), OpenAI Embeddings
Setup and Installation
Prerequisites
Docker must be installed and running.

An OpenAI API key.

1. Clone the Repository
Clone this project to your local machine:

Bash

git clone https://github.com/ashishsai960/AI-Planet.git
cd AI-Planet
2. Configure Environment Variables
In the backend/ folder, create a new file named .env. Add your OpenAI API key to this file:

Code snippet

# backend/.env
OPENAI_API_KEY="sk-YourSecretApiKeyGoesHere"
3. Build and Run with Docker
From the root directory of the project, run the following command. This will build the images for the frontend and backend and start the application.

Bash

docker compose up --build
4. Access the Application
Once the containers are running, you can access the application in your web browser:

Frontend Application: http://localhost:3000

Backend API Docs: http://localhost:8000/docs

Application Workflow
Dashboard: The application starts on the "My Stacks" dashboard, where you can view existing workflows or create a new one.

Create Stack: Clicking "+ New Stack" opens a modal to name and describe your workflow.

Builder: You are then taken to the canvas where you can drag components from the sidebar, drop them onto the canvas, and connect them to define the data flow.

Configuration: Each node on the canvas can be configured with specific settings (e.g., uploading a PDF to the Knowledge Base, setting the temperature for the LLM).

Save: The "Save" button sends the current state of your workflow (nodes and edges) to the backend.

Chat with Stack: Clicking this button opens a chat modal. When you send a message, the entire workflow and your query are sent to the backend for execution.

Execution: The backend processes the workflow, queries the knowledge base, calls the LLM, and returns the final answer.

Response: The AI's response is displayed in the chat window.

API Endpoints
The FastAPI backend exposes the following endpoints:

POST /upload-document/: Handles PDF file uploads for the Knowledge Base.

POST /stacks/: Saves a new workflow.

GET /stacks/: Retrieves all saved workflows.

POST /execute/: Executes a given workflow with a user query.
