provider "aws" {
  region = "ap-south-1"
}

# 🔐 Security Group
resource "aws_security_group" "app_sg" {
  name        = "app-sg"
  description = "Allow SSH and Streamlit access"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Streamlit"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 🖥️ EC2 Instance
resource "aws_instance" "app_server" {
  ami           = "ami-0f5ee92e2d63afc18"  # Ubuntu (ap-south-1)
  instance_type = "t3.micro"
  key_name      = "new-key"

  vpc_security_group_ids = [aws_security_group.app_sg.id]

  tags = {
    Name = "Agentic-AI-Server"
    Project = "Agentic-AI"
    Env = "Dev"
  }
}
output "public_ip"{
    value=aws_instance.app_server.public_ip
}