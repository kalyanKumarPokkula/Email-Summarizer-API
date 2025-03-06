from llm import email_summarizer, email_reply
from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import re

app = FastAPI()

origins = [
    "https://mail.google.com",  # Allow requests from Gmail
    "http://localhost:3000",    # Allow requests from local frontend (optional)
    "http://localhost:8000"     # Allow self-origin requests
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"messages" : "Welcome to the Email Summarizer Backend!"}

@app.post("/summarize")
def summarize(body: dict):
    email = body["email"]
    privacy_mode = body["privacy_mode"]
    if not email:
        raise HTTPException(status_code=400, detail="Email field is required")
    cleaned_json_data = email_summarizer(email, privacy_mode)

    # Use regex to extract valid JSON content
    match = re.search(r'```json\n(.*)```', cleaned_json_data, re.DOTALL)
    
    if match:
        cleaned_json_data = match.group(1)  # Extract JSON part

    # Convert JSON string to dictionary
    try:
        data = json.loads(cleaned_json_data)
        return data
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None

@app.post("/reply")
def reply(body : dict):
    email = body["email"]
    privacy_mode = body["privacy_mode"]

    response = email_reply(email, privacy_mode)
    print(response)
    return response



# json_Data = "```json\n{\n  \"summary\": \"Chaitanya Gadhe has a Backend Developer contract role opportunity and is seeking Kalyan Kumar's interest and availability for a discussion.\",\n  \"action_items\": [\n    \"Send Chaitanya Gadhe your CV\",\n    \"Respond with a good time for a quick chat\"\n  ]\n}\n```"
# cleaned_json_data = json_Data.strip('```json\n').strip('```')
# print(type(cleaned_json_data))
# data = json.loads(cleaned_json_data)
# print(type(data))
# print(data)