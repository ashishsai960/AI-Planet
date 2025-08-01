# GenAI Stack - Visual Workflow Builder

![GenAI Stack Screenshot](https-github-com-ashishsai960-AI-Planet-blob-main-Screenshot%202025-07-30%20at%201-33-20%E2%80%AFAM-jpg)

## Overview

[cite_start]GenAI Stack is a No-Code/Low-Code web application designed for visually creating and interacting with intelligent AI workflows. [cite: 122] [cite_start]The platform allows users to configure a flow of components that handle user input, extract information from documents, connect with large language models, and deliver answers through a chat interface. [cite: 123]

Once a workflow (called a "Stack") is built, users can test it in real-time by asking questions. [cite_start]The system processes the query through the user-defined components to generate a final, context-aware response. [cite: 124, 125]

## Key Features

* **Visual Drag-and-Drop Canvas:** Build complex workflows by dragging components onto the canvas and connecting them.
* **Stack Management:** A dashboard to view all saved workflows and a modal to create new ones from scratch.
* **Component-Based Architecture:** Construct workflows using modular components:
    * [cite_start]**User Query:** The entry point for user questions. [cite: 138, 140]
    * [cite_start]**Knowledge Base:** Upload PDFs to provide context for the AI. [cite: 142, 143]
    * [cite_start]**LLM (OpenAI):** Configure and interact with large language models like GPT. [cite: 150]
    * [cite_start]**Web Search:** A placeholder for a tool to search the web. [cite: 134]
    * [cite_start]**Output:** Displays the final generated response. [cite: 158]
* [cite_start]**Real-time Chat Interaction:** Test and run your workflows through an interactive chat modal. [cite: 167]
* [cite_start]**Dockerized Deployment:** The entire full-stack application is containerized with Docker for easy setup and consistent deployment. [cite: 193]

## Tech Stack

| Category              | Technology                                   |
| --------------------- | -------------------------------------------- |
| **Frontend** | [cite_start]React.js [cite: 127]                         |
| **Backend** | [cite_start]FastAPI (Python) [cite: 128]                  |
| **Database** | [cite_start]PostgreSQL [cite: 129]                       |
| **Drag & Drop** | [cite_start]React Flow [cite: 130]                       |
| **Vector Store** | [cite_start]ChromaDB [cite: 131]                         |
| **Text Extraction** | [cite_start]PyMuPDF [cite: 135]                          |
| **AI Models** | [cite_start]OpenAI GPT (LLM), OpenAI Embeddings [cite: 132, 133] |
| **Deployment** | Docker                                       |

---

## Getting Started

### Prerequisites
* [Docker](https://www.docker.com/products/docker-desktop/) installed and running.
* An OpenAI API key with available credits.

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/ashishsai960/AI-Planet.git](https://github.com/ashishsai960/AI-Planet.git)
    cd AI-Planet
    ```

2.  **Configure Environment Variables**
    Create a file named `.env` inside the `backend/` directory and add your OpenAI API key.
    ```env
    # backend/.env
    OPENAI_API_KEY="sk-YourSecretApiKeyGoesHere"
    ```

3.  **Build and Run with Docker**
    From the **root directory** of the project, run the following command. This will build the images for the frontend and backend and start the application.
    ```bash
    docker compose up --build
    ```

4.  **Access the Application**
    Once the containers are running, open your web browser and navigate to:
    * **Frontend:** `http://localhost:3000`

---

## How It Works

1.  **Dashboard:** The application starts on the "My Stacks" dashboard, where you can view existing workflows or create a new one.
2.  **Create Stack:** Clicking "+ New Stack" opens a modal to name and describe your workflow.
3.  **Builder:** You are then taken to the canvas where you can drag components from the sidebar, drop them onto the canvas, and connect them to define the data flow.
4.  **Configuration:** Each node on the canvas can be configured with specific settings (e.g., uploading a PDF to the Knowledge Base, setting the temperature for the LLM).
5.  **Save:** The "Save" button sends the current state of your workflow (nodes and edges) to the backend.
6.  **Chat with Stack:** Clicking this button opens a chat modal. When you send a message, the entire workflow and your query are sent to the backend for execution.
7.  **Execution:** The backend processes the workflow by following the connections, queries the knowledge base, calls the LLM with the appropriate context and prompt, and returns the final answer.
8.  **Response:** The AI's response is displayed in the chat window.

## API Endpoints

The FastAPI backend exposes the following endpoints:

* [cite_start]`POST /upload-document/`: Handles PDF file uploads for the Knowledge Base. [cite: 207]
* [cite_start]`POST /stacks/`: Saves a new workflow. [cite: 215]
* [cite_start]`GET /stacks/`: Retrieves all saved workflows. [cite: 215]
* [cite_start]`POST /execute/`: Executes a given workflow with a user query. [cite: 209]

## Future Improvements

* **Load Saved Stacks:** Implement the logic to load a saved stack back onto the canvas for editing.
* [cite_start]**User Authentication:** Add user accounts to keep stacks private and secure. [cite: 238]
* [cite_start]**Chat History:** Persist chat conversations for each stack. [cite: 235]
