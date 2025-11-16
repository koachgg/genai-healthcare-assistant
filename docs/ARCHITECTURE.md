# Healthcare Document Assistant - Technical Documentation

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Frontend Layer                             │
│                      (User Interface / Chat)                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                              │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                     API Endpoints (v1)                         │  │
│  │  • Document Upload & Processing                               │  │
│  │  • Q&A Chat Interface                                         │  │
│  │  • Report Generation                                          │  │
│  │  • Google Drive Integration                                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────┬─────────────────┬──────────────────┬─────────────────┘
               │                 │                  │
               ▼                 ▼                  ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   AWS S3         │  │   MongoDB        │  │   Qdrant         │
│   (Documents)    │  │   (Metadata)     │  │   (Vectors)      │
└──────────────────┘  └──────────────────┘  └──────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   LLM Services       │
                    │  • OpenAI (GPT-4o)   │
                    │  • Ollama (Local)    │
                    └──────────────────────┘
```

## Core Components

### 1. Document Processing Pipeline

**Purpose**: Ingests and processes medical documents for analysis

**Flow**:
1. User uploads document → S3 storage
2. Document metadata saved to MongoDB
3. PDF extracted and chunked
4. Text chunks embedded using LLM
5. Vectors stored in Qdrant for retrieval

**Key Files**:
- `utils/document_handling/process_document.py` - Main processing orchestration
- `utils/document_handling/extraction_engine.py` - Text extraction
- `utils/document_handling/chunker.py` - Document chunking
- `services/document_encoder.py` - ID generation and S3 path management

### 2. Retrieval-Augmented Generation (RAG) System

**Purpose**: Enables Q&A with citation support

**Flow**:
1. User submits question
2. Question embedded using LLM
3. Semantic search in Qdrant for relevant chunks
4. Retrieved chunks + question sent to LLM
5. Response generated with source citations
6. Citations include document links (especially for Google Drive)

**Key Files**:
- `services/qdrant_host.py` - Vector database connection
- `lib/brain.py` - LLM inference abstraction
- `services/ollama_host.py` - Ollama-specific operations

### 3. Report Generation System

**Purpose**: Creates structured medical reports from documents

**Flow**:
1. User requests report with specific sections
2. System uses LLM function calling to:
   - Extract exact content from documents
   - Pull tables and figures
   - Generate summaries where requested
3. Content assembled into report structure
4. Export as downloadable PDF

**Key Files**:
- `utils/document_handling/content_generation.py` - Report generation
- `utils/document_handling/prompt_builder.py` - Prompt construction
- `api/v1/endpoints/generate_content.py` - API endpoint

### 4. Google Drive Integration

**Purpose**: Enables processing of documents from shared Google Drive folders

**Flow**:
1. Service account authenticates with Google Drive API
2. Lists and downloads documents from configured folder
3. Documents processed through standard pipeline
4. Responses include clickable Drive links to source files

**Key Files**:
- `services/google_drive_service.py` - Google Drive operations
- `api/v1/endpoints/google_drive.py` - API endpoints
- `credentials/service_account.json` - Authentication credentials

## Data Models

### Document Model
- Stores document metadata, processing status, and S3 references
- Location: `models/doc.py`

### Workspace Model
- Manages user workspaces and associated documents
- Location: `models/workspace.py`

### Other Models
- `models/images.py` - Document images
- `models/tables.py` - Extracted tables
- `models/preview.py` - Document previews
- `models/summary.py` - Document summaries

## API Structure

All endpoints are versioned under `/api/v1`:

### Document Management
- `POST /api/v1/get-presigned-url` - Get S3 upload URL
- `POST /api/v1/trigger-process-document` - Start document processing
- `GET /api/v1/get-processed-documents` - List processed documents

### Content Retrieval
- `GET /api/v1/get-summary` - Get document summary
- `GET /api/v1/get-images` - Retrieve document images
- `GET /api/v1/get-tables` - Get extracted tables
- `GET /api/v1/get-preview` - Get document preview

### Q&A and Generation
- `POST /api/v1/generate-content` - Generate structured content
- `POST /api/v1/content-findings` - Analyze content
- `GET /api/v1/get-prompt-library` - Access prompt templates

### Google Drive
- `POST /api/v1/google-drive/setup` - Configure Drive integration
- `GET /api/v1/google-drive/documents` - List Drive documents
- `POST /api/v1/google-drive/sync` - Sync Drive documents

### Health Check
- `GET /api/v1/health` - API health status

## Configuration

All configuration is managed through environment variables in `.env`:

### Required Variables
```env
# Database
DOCUMENT_DB_CONNECTION_STRING=mongodb://...
QDRANT_HOST_URL=http://localhost:6333

# AWS S3
access_key=your_access_key
secret_key=your_secret_key

# LLM Services
OLLAMA_ENDPOINT_URL=http://localhost:11434
OPENAI_API_KEY=sk-...

# Google Drive (Optional)
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=credentials/service_account.json
```

See `configs/config.py` for all available settings.

## Development Workflow

### Setup
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` file
6. Start services (MongoDB, Qdrant, Ollama if using)
7. Run: `uvicorn app.main:app --reload`

### Testing
Tests are located in `tests/` directory.

Run tests with:
```bash
pytest tests/
```

## Deployment

The application is containerizable with Docker. Key considerations:

1. **Environment Variables**: Ensure all required variables are set
2. **Volume Mounts**: Mount credentials directory for Google Drive
3. **Network**: Ensure connectivity to MongoDB, Qdrant, and LLM services
4. **Ports**: Expose port 8000 for the FastAPI application

## Security Considerations

1. **API Keys**: Never commit `.env` or credential files
2. **CORS**: Configure `ALLOWED_ORIGINS` for production
3. **Authentication**: Implement proper user authentication (TODO)
4. **S3 Access**: Use IAM roles and policies to restrict access
5. **Google Service Account**: Limit permissions to read-only

## Performance Optimization

1. **Async Operations**: FastAPI endpoints use async/await
2. **Connection Pooling**: Database connections are pooled
3. **Caching**: Consider implementing caching for frequently accessed documents
4. **Batch Processing**: Process multiple documents concurrently

## Future Enhancements

1. Implement user authentication and authorization
2. Add support for more document formats (Word, Excel)
3. Enhance report templates and customization
4. Implement real-time collaboration features
5. Add advanced search and filtering capabilities
6. Optimize vector search performance
7. Add monitoring and observability
