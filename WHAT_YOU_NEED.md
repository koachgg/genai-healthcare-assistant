# 🎯 What You Need to Set Up on Your End

## ✅ ALREADY DONE
- ✅ GitHub repository created and code pushed
- ✅ All sensitive files excluded (.env, credentials/, logs/)
- ✅ Comprehensive documentation included
- ✅ Docker configuration ready

## 🔑 WHAT YOU NEED TO CONFIGURE

### 1. **Groq API Key** (RECOMMENDED - FREE)
**Why**: For Q&A and content generation (Open Source!)
**Cost**: 100% FREE with generous rate limits
**Setup**:
1. Go to: https://console.groq.com/
2. Sign up (GitHub authentication available)
3. Go to **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)
5. Save it for your `.env` file

**Why Groq?**
- ✅ Completely FREE
- ✅ Uses open-source models (Llama 3.1 70B)
- ✅ Lightning-fast inference
- ✅ Perfect for this project

---

### 1b. **OpenAI API Key** (OPTIONAL - PAID)
**Alternative if you prefer OpenAI**
**Cost**: ~$5-10/month for testing
**Setup**:
1. Go to: https://platform.openai.com/
2. Sign up or log in
3. Go to **API Keys** → **Create new secret key**
4. Copy the key (starts with `sk-...`)
5. Save it for your `.env` file

---

### 2. **AWS S3 Credentials** (REQUIRED)
**Why**: For document storage
**Cost**: ~$1-5/month for testing
**Setup**:
1. Go to: https://aws.amazon.com/
2. Sign in to AWS Console
3. Go to **IAM** → **Users** → **Create User**
4. Enable "Programmatic access"
5. Attach policy: `AmazonS3FullAccess`
6. Note down:
   - Access Key ID
   - Secret Access Key
7. Create an S3 bucket (any name)

---

### 3. **MongoDB** (REQUIRED)
**Why**: For document metadata storage
**Cost**: FREE (Atlas free tier)
**Setup**:

**Option A: MongoDB Atlas (Recommended)**
1. Go to: https://www.mongodb.com/cloud/atlas
2. Sign up (free tier available - 512MB)
3. Create new cluster (choose FREE tier)
4. Click "Connect" → "Connect your application"
5. Copy connection string
6. Replace `<password>` with your password

**Option B: Local (Easier for testing)**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```
Then use: `mongodb://localhost:27017/healthcare_docs`

---

### 4. **Qdrant Vector Database** (REQUIRED)
**Why**: For semantic search and RAG
**Cost**: FREE (local Docker)
**Setup**:

**Easiest Option (Local Docker)**:
```bash
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant
```
Then use: `http://localhost:6333`

**OR use the docker-compose.yml** (already configured - just run `docker-compose up -d`)

---

### 5. **Google Drive API** (OPTIONAL)
**Why**: Only if you want Google Drive integration
**Cost**: FREE
**Setup**: See detailed guide in `docs/SETUP.md`

**Quick steps**:
1. Create Google Cloud Project
2. Enable Google Drive API
3. Create Service Account
4. Download JSON key file
5. Save as `app/credentials/service_account.json`
6. Share Google Drive folder with service account email
7. Copy folder ID from Drive URL

**⚠️ IMPORTANT**: If you're NOT using Google Drive, just skip this!

---

## 📝 Create Your .env File

1. Copy the example:
```bash
cp app/.env.example app/.env
```

2. Edit `app/.env` with your credentials:
```env
# Groq API (Recommended - FREE)
GROQ_API_KEY=gsk-your-actual-key-here
GROQ_API_MODEL=llama-3.1-70b-versatile

# OpenAI (Optional Alternative)
OPENAI_API_KEY=sk-your-actual-key-here

# AWS S3 (Required)
access_key=your-aws-access-key
secret_key=your-aws-secret-key

# MongoDB (Required)
DOCUMENT_DB_CONNECTION_STRING=mongodb://localhost:27017/healthcare_docs

# Qdrant (Required)
QDRANT_HOST_URL=http://localhost:6333

# Google Drive (Optional - leave blank if not using)
GOOGLE_DRIVE_FOLDER_ID=
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=credentials/service_account.json
GOOGLE_DRIVE_ENABLED=false
```

---

## 🚀 Quick Start Commands

Once you have the above configured:

```bash
# 1. Clone your repo
git clone https://github.com/koachgg/genai-healthcare-assistant.git
cd genai-healthcare-assistant

# 2. Start services with Docker (easiest)
docker-compose up -d

# 3. OR manually start services
docker run -d -p 27017:27017 mongo:7.0
docker run -d -p 6333:6333 qdrant/qdrant

# 4. Install Python dependencies
cd app
pip install -r requirements.txt

# 5. Create .env file (see above)
cp .env.example .env
# Edit .env with your credentials

# 6. Run the application
uvicorn main:app --reload
```

## ✅ Verify It Works

Open browser:
- **API Docs**: http://localhost:8000/api/v1/docs
- **Health Check**: http://localhost:8000/api/v1/health

---

## 💰 Cost Summary

### With Groq (Recommended - FULLY FREE):
- **Groq API**: FREE ✅
- **AWS S3**: $1-5/month  
- **MongoDB Atlas**: FREE (free tier) ✅
- **Qdrant**: FREE (local Docker) ✅
- **Total**: ~$1-5/month (AWS only!)

### With OpenAI (Alternative):
- **OpenAI API**: $5-10/month
- **AWS S3**: $1-5/month  
- **MongoDB Atlas**: FREE (free tier)
- **Qdrant**: FREE (local Docker)
- **Total**: ~$6-15/month

### Google Drive: FREE (optional) ✅

---

## 🛡️ Security Reminder

**NEVER commit these files**:
- ❌ `.env` (has your API keys)
- ❌ `credentials/service_account.json` (Google service account)
- ❌ Any file with passwords or secrets

**Already protected** (in .gitignore):
- ✅ `.env` 
- ✅ `credentials/`
- ✅ `logs/`
- ✅ `__pycache__/`

---

## 📚 Next Steps

1. **Set up the 4 required services** (Groq, AWS, MongoDB, Qdrant)
2. **Create your `.env` file** with the credentials
3. **Run the application** using docker-compose or manually
4. **Test the API** at http://localhost:8000/api/v1/docs
5. **Read the documentation** in the `docs/` folder

---

## 📞 Help & Documentation

- **Setup Guide**: `docs/SETUP.md` (detailed instructions)
- **Architecture**: `docs/ARCHITECTURE.md` (how it works)
- **API Reference**: `docs/API_REFERENCE.md` (all endpoints)
- **Quick Start**: `QUICK_START.md` (for reviewers)
- **GitHub**: https://github.com/koachgg/genai-healthcare-assistant

---

## 🎓 Summary

**YOU NEED**:
1. Groq API key (FREE ✅)
2. AWS S3 credentials ($1-5/month)
3. MongoDB (FREE ✅)
4. Qdrant (FREE ✅)

**OPTIONAL**:
5. OpenAI API key ($5-10/month, alternative to Groq)
6. Google Drive API setup (FREE, but requires more setup)

**ALREADY DONE**:
- ✅ Code on GitHub
- ✅ Documentation complete
- ✅ Docker ready
- ✅ No secrets committed

---

Good luck with your assignment! 🚀
