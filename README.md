# Healthcare Document Assistant 🏥📄

> An AI-powered assistant for healthcare organizations to manage, analyze, and generate insights from medical documents.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

This project implements a comprehensive AI-powered document assistant that enables healthcare organizations to:
- **Upload and Process** medical documents (PDFs, images, tables)
- **Ask Questions** with grounded, citation-backed answers
- **Generate Reports** with exact content extraction and structured formatting
- **Integrate Google Drive** for seamless document access

## ✨ Key Features

### 📤 Document Management
- Multi-format support (PDF, Word, Excel, images)
- Automatic document processing and vectorization
- AWS S3 storage with organized file structure
- Preview generation for quick document access

### 💬 Q&A with Citations
- Conversational AI interface with memory across turns
- Answers grounded exclusively in provided documents
- Automatic citation generation with source references
- Clickable links to Google Drive documents
- Explicit "information not available" responses (no hallucinations)

### 📊 Report Generation
- Structured medical report creation with customizable sections
- Exact content extraction (no paraphrasing unless requested)
- Table and figure extraction from PDFs
- LLM function calling for intelligent content assembly
- PDF export for generated reports

### ☁️ Google Drive Integration
- Direct access to shared Google Drive folders
- Service account authentication
- Document synchronization
- Source linking in responses

## 🏗️ Architecture

```
┌─────────────┐
│  Frontend   │  ← User Interface
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────┐
│         FastAPI Backend (Python)             │
│  ┌────────────────────────────────────────┐ │
│  │  API Endpoints (v1)                    │ │
│  │  • Documents  • Q&A  • Reports        │ │
│  │  • Google Drive  • Workspace          │ │
│  └────────────────────────────────────────┘ │
└──┬────────┬──────────┬──────────────────────┘
   │        │          │
   ▼        ▼          ▼
┌─────┐ ┌────────┐ ┌────────┐
│ S3  │ │MongoDB │ │Qdrant  │  ← Storage Layer
└─────┘ └────────┘ └────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  LLM Services   │  ← AI Layer
              │ OpenAI | Ollama │
              └─────────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## 🛠️ Tech Stack

### Backend & API
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Databases
- **MongoDB** - Document metadata storage
- **Qdrant** - Vector database for semantic search

### AI & ML (100% Open Source)
- **LangChain** - LLM orchestration framework
- **Groq API** - Free, fast inference with Llama 3.1 (Primary)
- **Ollama** - Local LLM alternative
- **OpenAI GPT-4o** - Optional paid alternative
- **Sentence Transformers** - Document embeddings

### Document Processing
- **PyMuPDF (fitz)** - PDF manipulation
- **PDFPlumber** - Table extraction
- **PyPDF2** - PDF utilities
- **YOLOv8** - Image detection

### Cloud & Storage
- **AWS S3** - Document storage
- **boto3** - AWS SDK
- **Google Drive API** - Drive integration

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- MongoDB instance
- Qdrant instance
- AWS S3 bucket
- Groq API key (Free at https://console.groq.com)
- (Optional) OpenAI API key or Ollama for alternative LLMs

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/koachgg/genai-healthcare-assistant.git
   cd genai-healthcare-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp app/.env.example app/.env
   # Edit app/.env with your configuration
   ```

5. **Start the application**
   ```bash
   cd app
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

## 📝 Configuration

### Required Environment Variables

```env
# Database
DOCUMENT_DB_CONNECTION_STRING=mongodb://localhost:27017/healthcare_docs
QDRANT_HOST_URL=http://localhost:6333

# AWS S3
access_key=YOUR_AWS_ACCESS_KEY
secret_key=YOUR_AWS_SECRET_KEY

# LLM
OPENAI_API_KEY=sk-your-key-here
OLLAMA_ENDPOINT_URL=http://localhost:11434

# Google Drive (Optional)
GOOGLE_DRIVE_FOLDER_ID=your-folder-id
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=credentials/service_account.json
```

See `app/.env.example` for complete configuration options.

## 📚 API Documentation

### Core Endpoints

#### Document Management
- `POST /api/v1/get-presigned-url` - Get S3 upload URL
- `POST /api/v1/trigger-process-document` - Process uploaded document
- `GET /api/v1/get-processed-documents` - List all processed documents

#### Q&A and Analysis
- `POST /api/v1/generate-content` - Generate content/answers
- `GET /api/v1/get-summary` - Get document summary
- `GET /api/v1/content-findings` - Analyze document content

#### Google Drive
- `POST /api/v1/google-drive/setup` - Configure Drive integration
- `GET /api/v1/google-drive/documents` - List Drive documents
- `POST /api/v1/google-drive/sync` - Sync Drive documents

#### Health Check
- `GET /api/v1/health` - Service health status

Full API documentation available at `/api/v1/docs` when running the application.

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

## 📂 Project Structure

```
healthcare-document-assistant/
├── app/                          # Main application directory
│   ├── api/                      # API endpoints
│   │   └── v1/                   # API version 1
│   │       ├── routes.py         # Route aggregation
│   │       └── endpoints/        # Individual endpoints
│   ├── configs/                  # Configuration management
│   │   └── config.py             # Settings classes
│   ├── lib/                      # Core utilities
│   │   ├── brain.py              # LLM interface
│   │   ├── logger.py             # Logging utility
│   │   └── hasher.py             # Hashing functions
│   ├── models/                   # Data models
│   ├── schemas/                  # Pydantic schemas
│   ├── services/                 # Business logic services
│   │   ├── document_encoder.py  # ID and path generation
│   │   ├── qdrant_host.py        # Vector DB connection
│   │   ├── s3host.py             # S3 operations
│   │   └── google_drive_service.py
│   ├── utils/                    # Utility functions
│   │   └── document_handling/    # Document processing
│   ├── tests/                    # Test files
│   ├── main.py                   # Application entry point
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment template
├── docs/                         # Documentation
│   └── ARCHITECTURE.md           # Architecture details
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

## 🔒 Security Notes

- Never commit `.env` files or credentials
- Use environment-specific configurations
- Implement proper authentication in production
- Configure CORS for specific domains
- Use IAM roles for AWS access
- Restrict Google Service Account permissions

## 🚢 Deployment

The application is ready for containerization with Docker. Key considerations:

1. Set all required environment variables
2. Mount credentials directory for Google Drive
3. Ensure connectivity to MongoDB, Qdrant, and LLM services
4. Expose port 8000
5. Configure reverse proxy (e.g., nginx) for production

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Developed as part of a GenAI Engineer hiring assignment.

## 🙏 Acknowledgments

- FastAPI framework
- LangChain community
- OpenAI and Ollama teams
- Healthcare professionals providing requirements

---

**Note**: This project is designed for educational and demonstration purposes. For production healthcare use, ensure compliance with relevant regulations (HIPAA, GDPR, etc.).
