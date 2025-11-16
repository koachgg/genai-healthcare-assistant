# API Reference

Complete API reference for the Healthcare Document Assistant.

**Base URL**: `http://localhost:8000/api/v1`

**Authentication**: Currently open (implement in production)

**Interactive Documentation**: 
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## Health Check

### GET /health

Check API health status.

**Response**:
```json
{
  "status": "healthy",
  "message": "Healthcare Document Assistant API is running successfully",
  "version": "1.0.0"
}
```

---

## Document Management

### POST /get-presigned-url

Get a presigned S3 URL for document upload.

**Request Body**:
```json
{
  "userId": "string",
  "documentName": "string"
}
```

**Response**:
```json
{
  "presignedUrl": "https://s3.amazonaws.com/...",
  "documentId": "encoded_string",
  "expiresIn": 3600
}
```

### POST /trigger-document-processing

Trigger background processing for an uploaded document.

**Request Body**:
```json
{
  "userId": "string",
  "uuid": "document_id"
}
```

**Response**:
```json
{
  "status": "ok"
}
```

### GET /get-processed-documents

List all processed documents for a user.

**Query Parameters**:
- `userId` (string, required)

**Response**:
```json
{
  "documents": [
    {
      "documentId": "string",
      "filename": "string",
      "status": "completed",
      "uploadedAt": "2025-11-16T12:00:00Z"
    }
  ]
}
```

---

## Document Content

### GET /get-summary

Get document summary.

**Query Parameters**:
- `userId` (string, required)
- `documentId` (string, required)

**Response**:
```json
{
  "summary": "Document summary text...",
  "documentId": "string",
  "generatedAt": "2025-11-16T12:00:00Z"
}
```

### GET /get-images

Get images extracted from document.

**Query Parameters**:
- `userId` (string, required)
- `documentId` (string, required)

**Response**:
```json
{
  "images": [
    {
      "imageId": "string",
      "pageNumber": 1,
      "url": "https://..."
    }
  ]
}
```

### GET /get-tables

Get tables extracted from document.

**Query Parameters**:
- `userId` (string, required)
- `documentId` (string, required)

**Response**:
```json
{
  "tables": [
    {
      "tableId": "string",
      "pageNumber": 2,
      "data": [[...], [...]],
      "imageUrl": "https://..."
    }
  ]
}
```

### GET /get-preview

Get document preview images.

**Query Parameters**:
- `userId` (string, required)
- `documentId` (string, required)
- `pageNumber` (integer, optional)

**Response**:
```json
{
  "previews": [
    {
      "pageNumber": 1,
      "imageUrl": "https://..."
    }
  ]
}
```

---

## Content Generation

### POST /generate-content

Generate content based on documents (Q&A, Reports).

**Request Body**:
```json
{
  "contentFormat": "qa|report",
  "objective": "string",
  "audience": "string",
  "tone": "professional|casual|technical",
  "text": "User question or instructions",
  "imagePaths": ["path1", "path2"]
}
```

**Response**:
```json
{
  "content": "Generated content...",
  "citations": [
    {
      "documentId": "string",
      "documentName": "string",
      "chunkId": "string",
      "relevance": 0.95,
      "link": "https://drive.google.com/..."
    }
  ],
  "images": ["url1", "url2"]
}
```

### POST /content-flow

Get next question in content generation flow.

**Request Body**:
```json
{
  "currentState": {
    "key": "value"
  },
  "stepIndex": 0
}
```

**Response**:
```json
{
  "question": "What sections do you want in the report?",
  "options": ["Introduction", "Findings", "Summary"],
  "nextStep": 1,
  "completed": false
}
```

### POST /content-findings

Analyze content from documents.

**Request Body**:
```json
{
  "userId": "string",
  "documentIds": ["id1", "id2"],
  "analysisType": "clinical_findings|key_points"
}
```

**Response**:
```json
{
  "findings": [
    {
      "type": "clinical_finding",
      "content": "...",
      "source": "document_id",
      "confidence": 0.92
    }
  ]
}
```

---

## Google Drive Integration

### POST /google-drive/setup

Set up and test Google Drive API connection.

**Response**:
```json
{
  "success": true,
  "message": "Google Drive setup successful. Found 15 accessible documents.",
  "folderId": "google_drive_folder_id"
}
```

### GET /google-drive/documents

List all medical documents from Google Drive.

**Response**:
```json
{
  "success": true,
  "documents": [
    {
      "documentId": "string",
      "name": "Medical Report.pdf",
      "mimeType": "application/pdf",
      "modifiedTime": "2025-11-16T12:00:00Z",
      "webViewLink": "https://drive.google.com/...",
      "size": 1024000,
      "sourceType": "google_drive"
    }
  ],
  "totalCount": 15
}
```

### POST /google-drive/sync

Sync Google Drive documents to local system.

**Request Body**:
```json
{
  "userId": "string",
  "forceResync": false
}
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully synced 15 Google Drive documents",
  "syncedDocumentIds": ["id1", "id2", ...],
  "totalSynced": 15
}
```

### POST /google-drive/document/content

Get content of specific Google Drive document.

**Request Body**:
```json
{
  "userId": "string",
  "fileId": "google_drive_file_id"
}
```

**Response**:
```json
{
  "success": true,
  "fileId": "string",
  "filename": "Medical Report.pdf",
  "contentSize": 1024000,
  "downloadUrl": "https://..."
}
```

---

## Workspace Management

### POST /create-workspace

Create a new workspace for organizing documents.

**Request Body**:
```json
{
  "userId": "string",
  "workspaceName": "string",
  "description": "string"
}
```

**Response**:
```json
{
  "workspaceId": "string",
  "name": "string",
  "createdAt": "2025-11-16T12:00:00Z"
}
```

---

## Prompt Library

### GET /get-prompt-library

Get available prompt templates.

**Response**:
```json
{
  "prompts": [
    {
      "id": "clinical_summary",
      "name": "Clinical Summary",
      "template": "...",
      "category": "medical"
    }
  ]
}
```

---

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "detail": "Both userId and uuid are required fields"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to access this document"
}
```

### 404 Not Found
```json
{
  "detail": "Document not found in S3 storage"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing document: [error details]"
}
```

---

## Rate Limiting

Currently not implemented. Recommended for production:
- 100 requests per minute per user
- 1000 requests per hour per user

---

## Best Practices

1. **Error Handling**: Always check response status codes
2. **Async Operations**: Document processing is async; poll for status
3. **File Size**: Limit documents to 50MB for optimal performance
4. **Citations**: Always include citations when displaying generated content
5. **Security**: Implement authentication before production use

---

## Code Examples

### Python
```python
import requests

# Upload document
response = requests.post(
    "http://localhost:8000/api/v1/get-presigned-url",
    json={"userId": "user123", "documentName": "report.pdf"}
)
presigned_url = response.json()["presignedUrl"]

# Upload file to S3
with open("report.pdf", "rb") as f:
    requests.put(presigned_url, data=f)

# Trigger processing
requests.post(
    "http://localhost:8000/api/v1/trigger-document-processing",
    json={"userId": "user123", "uuid": document_id}
)
```

### JavaScript
```javascript
// Upload document
const response = await fetch('http://localhost:8000/api/v1/get-presigned-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    userId: 'user123',
    documentName: 'report.pdf'
  })
});

const { presignedUrl, documentId } = await response.json();

// Upload file to S3
await fetch(presignedUrl, {
  method: 'PUT',
  body: file
});

// Trigger processing
await fetch('http://localhost:8000/api/v1/trigger-document-processing', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    userId: 'user123',
    uuid: documentId
  })
});
```

### cURL
```bash
# Upload document
curl -X POST "http://localhost:8000/api/v1/get-presigned-url" \
  -H "Content-Type: application/json" \
  -d '{"userId": "user123", "documentName": "report.pdf"}'

# Trigger processing
curl -X POST "http://localhost:8000/api/v1/trigger-document-processing" \
  -H "Content-Type: application/json" \
  -d '{"userId": "user123", "uuid": "document_id"}'
```

---

## Support

For more information:
- Interactive Docs: http://localhost:8000/api/v1/docs
- Architecture: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- Setup Guide: [docs/SETUP.md](SETUP.md)
