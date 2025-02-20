# Email Summarizer API

This project is a FastAPI-based backend service that provides email summarization using an LLM (Large Language Model). The API extracts key points and action items from email content and returns a structured JSON output.

## Features
- Accepts an email body as input.
- Summarizes email content with key actionable tasks.
- Uses OpenAI's GPT model to generate structured output.
- Implements CORS to allow frontend integrations.

## Setup Instructions

### 1. Create and Activate Virtual Environment
Run the following commands to set up a Python virtual environment:

```sh
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate virtual environment (Linux/macOS)
venv\Scripts\activate  # Activate virtual environment (Windows)
```

### 2. Install Dependencies
Run the following command to install the required dependencies:

```sh
pip install -r requirements.txt
```

> **Note:** Ensure you have Python 3.8+ installed.

### 3. Set Up OpenAI API Key
The application requires an OpenAI API key to function. Set it up using:

```sh
export OPENAI_API_KEY='your_openai_api_key'  # Linux/macOS
set OPENAI_API_KEY='your_openai_api_key'  # Windows
```

Alternatively, you can modify the `_set_env` function in the script to input the key when prompted.

### 4. Run the FastAPI Server
Start the FastAPI application by running:

```sh
uvicorn main:app --reload
```

### 5. API Endpoints

#### Root Endpoint
- **URL:** `/`
- **Method:** `GET`
- **Response:** `{ "messages": "Welcome to the Email Summarizer Backend!" }`

#### Summarize Email
- **URL:** `/summarize`
- **Method:** `POST`
- **Request Body:** `{ "email": "Your email content here" }`
- **Response:**
  ```json
  {
    "summary": "Summarized email content",
    "actionItems": ["Action 1", "Action 2"]
  }
  ```

## Technology Stack
- **Backend:** FastAPI (Python)
- **LLM:** OpenAI GPT model
- **Workflow Management:** LangGraph

## License
This project is licensed under the MIT License.
