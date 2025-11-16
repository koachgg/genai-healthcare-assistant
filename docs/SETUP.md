# Setup Guide

Complete setup instructions for the Healthcare Document Assistant.

## Prerequisites

Before you begin, ensure you have:
- Python 3.9 or higher
- Git
- Access to the following services (see below for setup)

---

## Required Services Setup

### 1. 🤖 Groq API Key (REQUIRED - FREE)

**Recommended - Fully Open Source with Free API**

**Steps**:
1. Go to https://console.groq.com/
2. Sign up (GitHub authentication available)
3. Navigate to **API Keys**
4. Click **Create API Key**
5. Copy the key (starts with `gsk_...`)
6. Add to `.env`:
   ```env
   GROQ_API_KEY=gsk-your-actual-key-here
   GROQ_API_MODEL=llama-3.1-70b-versatile
   ```

**Why Groq?**
- ✅ 100% FREE with generous limits
- ✅ Open-source models (Llama 3.1, Mixtral)
- ✅ Lightning-fast inference (fastest API)
- ✅ OpenAI-compatible API

---

### 1b. 🔑 OpenAI API Key (OPTIONAL - PAID)

**Alternative LLM Option**

**Steps**:
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create new secret key**
5. Copy the key (starts with `sk-...`)
6. Add to `.env`:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Note**: To use OpenAI, change `inference="groq"` to `inference="openai"` in endpoints.

---

### 2. ☁️ AWS S3 (REQUIRED)

**Steps**:
1. Go to https://aws.amazon.com/
2. Create account or log in
3. Navigate to **IAM** > **Users** > **Create User**
4. Enable **Programmatic access**
5. Attach policy: `AmazonS3FullAccess`
6. Save **Access Key ID** and **Secret Access Key**
7. Create S3 bucket
8. Add to `.env`:
   ```env
   access_key=YOUR_AWS_ACCESS_KEY_ID
   secret_key=YOUR_AWS_SECRET_ACCESS_KEY
   ```

---

### 3. 🗄️ MongoDB (REQUIRED)

**Option A: MongoDB Atlas (Recommended)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free tier available)
3. Create cluster
4. Click **Connect** > Get connection string
5. Add to `.env`:
   ```env
   DOCUMENT_DB_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/healthcare_docs
   ```

**Option B: Local MongoDB**
```bash
docker run -p 27017:27017 mongo:7.0
```
Then use:
```env
DOCUMENT_DB_CONNECTION_STRING=mongodb://localhost:27017/healthcare_docs
```

---

### 4. 🔍 Qdrant Vector Database (REQUIRED)

**Option A: Local (Easiest)**
```bash
docker run -p 6333:6333 qdrant/qdrant
```
Then use:
```env
QDRANT_HOST_URL=http://localhost:6333
```

**Option B: Qdrant Cloud**
1. Go to https://cloud.qdrant.io/
2. Create cluster
3. Use provided URL

---

### 5. 📁 Google Drive API (OPTIONAL)

**Only needed if you want Google Drive integration**

**Steps**:

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Click **Create Project**

2. **Enable Google Drive API**
   - Go to **APIs & Services** > **Library**
   - Search "Google Drive API"
   - Click **Enable**

3. **Create Service Account**
   - Go to **APIs & Services** > **Credentials**
   - Click **Create Credentials** > **Service Account**
   - Name it and click **Create**
   - Grant **Editor** role

4. **Download Service Account Key**
   - Click on service account
   - Go to **Keys** tab
   - Click **Add Key** > **Create New Key** > **JSON**
   - Save downloaded file as `app/credentials/service_account.json`

5. **Share Google Drive Folder**
   - Create folder in Google Drive
   - Share with service account email (from JSON file)
   - Copy folder ID from URL

6. **Update .env**:
   ```env
   GOOGLE_DRIVE_FOLDER_ID=your-folder-id
   GOOGLE_SERVICE_ACCOUNT_KEY_PATH=credentials/service_account.json
   GOOGLE_DRIVE_ENABLED=true
   ```

**⚠️ NEVER commit `credentials/` folder or `.env` file!**

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/koachgg/genai-healthcare-assistant.git
cd genai-healthcare-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd app
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
# Windows: notepad .env
# Linux/Mac: nano .env
```

### 5. Create Credentials Folder

```bash
mkdir -p credentials
# Place service_account.json here if using Google Drive
```

### 6. Start Services

**Using Docker Compose (Recommended)**:
```bash
cd ..
docker-compose up -d
```

**Or start services manually**:
- MongoDB: `docker run -p 27017:27017 mongo:7.0`
- Qdrant: `docker run -p 6333:6333 qdrant/qdrant`

### 7. Run Application

```bash
cd app
uvicorn main:app --reload
```

### 8. Verify

- API Docs: http://localhost:8000/api/v1/docs
- Health: http://localhost:8000/api/v1/health

---

## Minimal .env Configuration

```env
# OpenAI (Required)
OPENAI_API_KEY=sk-your-key

# AWS S3 (Required)
access_key=your-aws-key
secret_key=your-aws-secret

# MongoDB (Required)
DOCUMENT_DB_CONNECTION_STRING=mongodb://localhost:27017/healthcare_docs

# Qdrant (Required)
QDRANT_HOST_URL=http://localhost:6333

# Google Drive (Optional - remove if not using)
# GOOGLE_DRIVE_FOLDER_ID=
# GOOGLE_SERVICE_ACCOUNT_KEY_PATH=credentials/service_account.json
# GOOGLE_DRIVE_ENABLED=false
```

---

## Security Checklist

- [ ] `.env` file created and NOT in Git
- [ ] `credentials/` folder NOT in Git
- [ ] `.gitignore` is configured (already done)
- [ ] All API keys are secret
- [ ] Service account JSON NOT committed

---

## What You Need to Set Up

### MUST HAVE:
1. ✅ **OpenAI API Key** - for Q&A and generation
2. ✅ **AWS S3 Credentials** - for document storage
3. ✅ **MongoDB** - for metadata (use Atlas free tier or Docker)
4. ✅ **Qdrant** - for vector search (use Docker locally)

### OPTIONAL:
5. ⭕ **Google Drive API** - only if you want Drive integration
   - Requires service account JSON
   - Requires shared folder

---

## Cost Estimate

**Minimal (Testing)**:
- OpenAI: ~$5-10/month
- MongoDB Atlas: Free tier
- Qdrant: Free (local Docker)
- AWS S3: ~$1-5/month
- **Total: ~$6-15/month**

---

## Troubleshooting

### MongoDB connection failed
- Check if running: `docker ps` or `mongosh`
- Verify connection string in `.env`

### Qdrant connection failed
- Check if running: `curl http://localhost:6333/health`
- Start: `docker run -p 6333:6333 qdrant/qdrant`

### Google Drive auth failed
- Verify `service_account.json` exists in `credentials/`
- Check service account email is added to Drive folder
- Verify folder ID is correct

---

## Next Steps

1. Test health endpoint: http://localhost:8000/api/v1/health
2. Open API docs: http://localhost:8000/api/v1/docs
3. Try uploading a document
4. Read [API_REFERENCE.md](API_REFERENCE.md)

---

**Repository**: https://github.com/koachgg/genai-healthcare-assistant
