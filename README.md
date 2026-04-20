# Resume-ats
Agentic Resume Improvement AI
An automated, locally-hosted (or EC2-hosted) AI agent that analyzes resumes and provides expert improvement suggestions. This project leverages Qwen 2 0.5B via Ollama, orchestrated with LangChain, and served through a FastAPI backend and Streamlit frontend.

🚀 Features
Automatic PDF Processing: Upload a resume, and it is parsed immediately.

Agentic Analysis: Uses a "Professional Career Coach" persona to provide actionable feedback.

Local LLM: Powered by Qwen 2 0.5B via Ollama for privacy and speed.

Production Architecture: Separated Frontend (Streamlit) and Backend (FastAPI).

Infrastructure as Code: Fully deployable to AWS EC2 using Terraform.

🛠️ Tech Stack
LLM: Qwen 2 0.5B (via Ollama)

Orchestration: LangChain

Backend: FastAPI (Python 3.10+)

Frontend: Streamlit

Deployment: Terraform & AWS EC2

💻 Local Setup
1. Install Ollama & Pull Model
Download Ollama from ollama.com and run:

Bash

ollama pull qwen2:0.5b
2. Environment Setup
Bash

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
3. Run the Application
Open two terminals:

Terminal 1 (Backend):

Bash

uvicorn backend:app --reload --port 8000
Terminal 2 (Frontend):

Bash

streamlit run frontend.py
☁️ AWS Deployment (Terraform)
This project includes Terraform configurations to provision an EC2 T3.Medium (minimum recommended for local LLM inference) on AWS.

1. Configuration
Ensure your main.tf is configured with your AWS credentials or IAM role.

2. Deployment Commands
Bash

cd terraform/
terraform init
terraform plan
terraform apply -auto-approve
3. Post-Deployment
The Terraform script automatically:

Installs Docker and Ollama on the EC2 instance.

Pulls the qwen2:0.5b model.

Starts the FastAPI and Streamlit services as background processes.

📂 Project Structure
Plaintext

├── backend.py            # FastAPI server with LangChain logic
├── frontend.py           # Streamlit UI
├── requirements.txt      # Python dependencies
├── terraform/
│   ├── main.tf           # EC2 & Security Group definitions
│   ├── variables.tf      # AWS Region/Instance variables
│   └── outputs.tf        # Public IP output
└── README.md

ci cd don
