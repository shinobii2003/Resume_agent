import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2

# LangChain Imports
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LangChain Ollama Object
# Ensure the model matches your 'ollama list'
llm = OllamaLLM(model="qwen2:0.5b", temperature=0.3)

state = {"resume_text": ""}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        pdf = PyPDF2.PdfReader(io.BytesIO(content))
        text = "\n".join([page.extract_text() for page in pdf.pages])
        state["resume_text"] = text.strip()
        return {"message": "Resume uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import time

@app.post("/suggestions")
async def suggestions():
    if not state["resume_text"]:
        raise HTTPException(status_code=400, detail="No resume data found.")

    # 1. Create a stricter Prompt Template
    # We add "Response:" at the end to nudge the model to start typing
    template = """Role: Professional Career Coach
Task: Analyze the resume text provided and give 3 specific improvement tips.

Resume Content: {resume}

Instructions:
- Use a numbered list (1, 2, 3).
- Do NOT use tables or complex formatting.
- Each tip should be one concise paragraph.

Response:"""
    
    prompt = PromptTemplate.from_template(template)

    # 2. Re-initialize the LLM with a specific timeout if needed
    # Note: LangChain's OllamaLLM talks to Ollama's server.
    # If it's slow, we use 'ainvoke' to keep the server responsive.
    chain = prompt | llm

    try:
        print("--- AI Agent started thinking... ---")
        start_time = time.time()
        
        # USE AINVOKE: This is the async version of invoke
        # It prevents the FastAPI server from "freezing" while waiting for the LLM
        response = await chain.ainvoke({"resume": state["resume_text"]})
        
        end_time = time.time()
        print(f"--- AI Agent finished in {round(end_time - start_time, 2)}s ---")
        
        return {"suggestions": response}
        
    except Exception as e:
        print(f"Error caught: {str(e)}")
        return {"error": f"Agent Timeout or Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)