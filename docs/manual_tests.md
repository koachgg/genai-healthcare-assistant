# 🧪 Manual Test Commands for Google Drive Integration

Your server is running on: **http://192.168.10.50:5665/**

## Quick Individual Tests

Copy and paste these commands in your terminal to test specific features:

### 1. 🏥 **Basic Server Health Check**
```bash
curl -X GET "http://192.168.10.50:5665/api/v1/health_check"
```

### 2. 🔑 **Google Drive Setup Test**
```bash
curl -X POST "http://192.168.10.50:5665/api/v1/google-drive/setup"
```

### 3. 📁 **List Google Drive Documents**
```bash
curl -X GET "http://192.168.10.50:5665/api/v1/google-drive/documents"
```

### 4. 🔄 **Sync Google Drive Documents**
```bash
curl -X POST "http://192.168.10.50:5665/api/v1/google-drive/sync" \
  -H "Content-Type: application/json" \
  -d '{"userId": "test_user"}'
```

### 5. 🔍 **Preview Auto-Discovery**
```bash
curl -X POST "http://192.168.10.50:5665/api/v1/search/preview" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "medical information clinical trial",
    "userId": "test_user",
    "max_results": 10,
    "score_threshold": 0.5
  }'
```

### 6. 💬 **Smart Chat with Auto-Discovery** ⭐
```bash
curl -X POST "http://192.168.10.50:5665/api/v1/chat/smart" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What medical information is available?",
    "userId": "test_user",
    "max_documents": 5,
    "relevance_threshold": 0.6
  }'
```

### 7. 🏥 **Search System Health**
```bash
curl -X GET "http://192.168.10.50:5665/api/v1/search/health"
```

### 8. 🔗 **Get Google Drive Document Link**
```bash
# Replace FILE_ID with an actual file ID from step 3
curl -X GET "http://192.168.10.50:5665/api/v1/google-drive/document/FILE_ID/link"
```

---

## 🎯 **Expected Results**

### ✅ **Success Indicators:**
- **Health Check**: `{"statusCode": 200, "message": "Server is running successfully"}`
- **Google Drive Setup**: `{"success": true, "message": "Google Drive setup successful"}`
- **Document List**: Shows your uploaded medical documents with `"source_type": "google_drive"`
- **Smart Chat**: Streams response with mixed citations from uploaded + Drive docs

### ❌ **Common Issues:**
- **"Google Drive not configured"**: Check your `.env` file has the folder ID
- **"Authentication failed"**: Verify service account file exists and Drive folder is shared
- **"No documents found"**: Make sure you uploaded files to the shared Google Drive folder

---

## 🚀 **Test Your Assignment Requirements**

### **Part 1 Requirements Testing:**

#### **Grounded Responses (No Hallucinations)**
```bash
curl -X POST "http://192.168.10.50:5665/api/v1/chat/smart" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of Mars?",
    "userId": "test_user"
  }'
```
**Expected**: Should respond that information is not available in documents.

#### **Citations & References**
```bash
curl -X POST "http://192.168.10.50:5665/api/v1/chat/smart" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the clinical findings mentioned in the documents?",
    "userId": "test_user"
  }'
```
**Expected**: Response with specific document names and page numbers.

#### **Google Drive Integration with Clickable Links**
The responses should include both:
- `[📁 Drive: filename.pdf]` - Google Drive documents with clickable links
- `[Uploaded: filename.pdf, page X]` - Uploaded documents with page references

#### **Multi-turn Conversation**
```bash
# First message
curl -X POST "http://192.168.10.50:5665/api/v1/chat/smart" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What medical studies are mentioned?",
    "userId": "test_user",
    "context_id": "conversation_123"
  }'

# Follow-up message (same context_id)
curl -X POST "http://192.168.10.50:5665/api/v1/chat/smart" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What were the results of those studies?",
    "userId": "test_user",
    "context_id": "conversation_123"
  }'
```

---

## 🎉 **Your System Features**

✅ **Intelligent Auto-Discovery**: Finds relevant docs automatically
✅ **Mixed Source Citations**: Combines uploaded + Google Drive documents
✅ **Clickable Google Drive Links**: Direct access to original files
✅ **Advanced Source Highlighting**: PDF highlighting with screenshots
✅ **Multi-turn Memory**: Conversation context preservation

**This exceeds typical assignment requirements!** 🏆