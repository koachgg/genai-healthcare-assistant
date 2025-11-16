# Deployment Guide

This guide covers deploying the Healthcare Document Assistant to various environments.

## Table of Contents
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
  - [AWS](#aws-deployment)
  - [Google Cloud](#google-cloud-deployment)
  - [Azure](#azure-deployment)
- [Production Checklist](#production-checklist)

---

## Docker Deployment

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed
- Required environment variables configured

### Quick Start

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd healthcare-document-assistant
   ```

2. **Configure environment**
   ```bash
   cp app/.env.example app/.env
   # Edit app/.env with your credentials
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Verify deployment**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

5. **View logs**
   ```bash
   docker-compose logs -f app
   ```

### Service URLs
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs
- **MongoDB**: mongodb://localhost:27017
- **Qdrant**: http://localhost:6333
- **Ollama**: http://localhost:11434

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a specific service
docker-compose restart app

# View logs
docker-compose logs -f app

# Scale services
docker-compose up -d --scale app=3

# Rebuild after code changes
docker-compose up -d --build

# Remove all data (careful!)
docker-compose down -v
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: AWS ECS (Elastic Container Service)

**Prerequisites:**
- AWS Account
- AWS CLI configured
- ECR repository created

**Steps:**

1. **Build and push Docker image**
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   
   # Build image
   cd app
   docker build -t healthcare-doc-assistant .
   
   # Tag image
   docker tag healthcare-doc-assistant:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/healthcare-doc-assistant:latest
   
   # Push image
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/healthcare-doc-assistant:latest
   ```

2. **Set up infrastructure**
   - Create ECS cluster
   - Create task definition with environment variables
   - Create service with load balancer
   - Configure security groups

3. **Configure databases**
   - MongoDB: Use AWS DocumentDB or MongoDB Atlas
   - Qdrant: Deploy on EC2 or use Qdrant Cloud
   - S3: Already configured

4. **Set environment variables in ECS Task Definition**
   ```json
   {
     "environment": [
       {
         "name": "DOCUMENT_DB_CONNECTION_STRING",
         "value": "mongodb://documentdb-cluster:27017"
       },
       {
         "name": "QDRANT_HOST_URL",
         "value": "http://qdrant-instance:6333"
       }
     ]
   }
   ```

#### Option 2: AWS Lambda (Serverless)

For lower traffic scenarios, deploy as Lambda function with API Gateway.

**Note:** May require modifications due to Lambda limitations (15-minute timeout, cold starts).

---

### Google Cloud Deployment

#### Using Google Cloud Run

**Prerequisites:**
- Google Cloud account
- gcloud CLI installed

**Steps:**

1. **Enable required APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

2. **Build and push image**
   ```bash
   cd app
   gcloud builds submit --tag gcr.io/[PROJECT-ID]/healthcare-doc-assistant
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy healthcare-doc-assistant \
     --image gcr.io/[PROJECT-ID]/healthcare-doc-assistant \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars "OPENAI_API_KEY=sk-xxx,DOCUMENT_DB_CONNECTION_STRING=mongodb://xxx"
   ```

4. **Configure databases**
   - MongoDB: Use MongoDB Atlas
   - Qdrant: Deploy on GCE or use Qdrant Cloud
   - Storage: Use Google Cloud Storage instead of S3

---

### Azure Deployment

#### Using Azure Container Instances

**Prerequisites:**
- Azure account
- Azure CLI installed

**Steps:**

1. **Create resource group**
   ```bash
   az group create --name healthcare-rg --location eastus
   ```

2. **Create container registry**
   ```bash
   az acr create --resource-group healthcare-rg --name healthcareregistry --sku Basic
   ```

3. **Build and push image**
   ```bash
   cd app
   az acr build --registry healthcareregistry --image healthcare-doc-assistant:latest .
   ```

4. **Deploy container**
   ```bash
   az container create \
     --resource-group healthcare-rg \
     --name healthcare-doc-assistant \
     --image healthcareregistry.azurecr.io/healthcare-doc-assistant:latest \
     --dns-name-label healthcare-assistant \
     --ports 8000 \
     --environment-variables \
       OPENAI_API_KEY=sk-xxx \
       DOCUMENT_DB_CONNECTION_STRING=mongodb://xxx
   ```

---

## Production Checklist

### Before Deployment

- [ ] **Security**
  - [ ] Change all default passwords
  - [ ] Generate strong secret keys
  - [ ] Enable HTTPS/SSL
  - [ ] Configure CORS for specific domains only
  - [ ] Implement authentication and authorization
  - [ ] Enable rate limiting
  - [ ] Set up Web Application Firewall (WAF)

- [ ] **Configuration**
  - [ ] Set `ALLOWED_ORIGINS` to specific domains
  - [ ] Use production-grade database instances
  - [ ] Configure database backups
  - [ ] Set up log rotation
  - [ ] Configure monitoring and alerting

- [ ] **Infrastructure**
  - [ ] Set up load balancer
  - [ ] Configure auto-scaling
  - [ ] Set up CDN for static assets
  - [ ] Configure database replication
  - [ ] Set up disaster recovery

- [ ] **Monitoring**
  - [ ] Set up application monitoring (e.g., New Relic, DataDog)
  - [ ] Configure log aggregation (e.g., ELK Stack, CloudWatch)
  - [ ] Set up error tracking (e.g., Sentry)
  - [ ] Configure uptime monitoring
  - [ ] Set up performance monitoring

- [ ] **Compliance**
  - [ ] Review HIPAA requirements (if handling real medical data)
  - [ ] Implement audit logging
  - [ ] Set up data encryption at rest and in transit
  - [ ] Configure backup and retention policies
  - [ ] Document security measures

### Environment Variables for Production

```env
# Use strong, unique values
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Use managed database services
DOCUMENT_DB_CONNECTION_STRING=mongodb+srv://prod-user:strong-password@prod-cluster.mongodb.net
QDRANT_HOST_URL=https://prod-qdrant.yourdomain.com

# Use secrets management
OPENAI_API_KEY=sk-prod-key-from-secrets-manager
access_key=aws-key-from-secrets-manager
secret_key=aws-secret-from-secrets-manager
```

### Performance Optimization

1. **Caching**
   - Implement Redis for frequently accessed data
   - Cache vector search results
   - Use CDN for static content

2. **Database Optimization**
   - Add indexes on frequently queried fields
   - Implement connection pooling
   - Use read replicas for scaling

3. **Application Optimization**
   - Enable response compression
   - Implement pagination for large datasets
   - Use async operations throughout
   - Implement request queuing for heavy operations

### Scaling Strategies

1. **Horizontal Scaling**
   - Deploy multiple application instances
   - Use load balancer for distribution
   - Implement sticky sessions if needed

2. **Database Scaling**
   - MongoDB: Sharding or Atlas auto-scaling
   - Qdrant: Cluster mode with multiple nodes

3. **Background Processing**
   - Use message queue (e.g., RabbitMQ, AWS SQS)
   - Separate worker processes for document processing
   - Implement job prioritization

### Backup Strategy

1. **Database Backups**
   - Automated daily backups
   - Point-in-time recovery
   - Cross-region replication

2. **S3 Backups**
   - Enable versioning
   - Configure lifecycle policies
   - Cross-region replication for critical data

3. **Configuration Backups**
   - Version control for all configuration
   - Document all manual changes
   - Keep environment variable backups secure

### Monitoring Metrics

Track these key metrics:

- **Application Metrics**
  - Request rate and latency
  - Error rate
  - API endpoint performance
  - Background job completion time

- **Infrastructure Metrics**
  - CPU and memory usage
  - Disk I/O
  - Network throughput
  - Container health

- **Business Metrics**
  - Documents processed
  - API calls per user
  - Average processing time
  - User engagement

---

## Rollback Procedure

If deployment fails:

1. **Immediate Rollback**
   ```bash
   # Docker
   docker-compose down && docker-compose up -d --scale app=0
   
   # Cloud platforms have rollback in their respective CLIs
   ```

2. **Restore Previous Version**
   - Tag and deploy previous working image
   - Restore database from backup if needed
   - Update DNS if necessary

3. **Post-Mortem**
   - Document what went wrong
   - Update deployment procedures
   - Add tests to prevent recurrence

---

## Support

For deployment issues:
- Check logs: `docker-compose logs -f`
- Review [Troubleshooting Guide](SETUP.md#troubleshooting)
- Open an issue on GitHub

---

**Note:** This guide assumes a basic deployment. For enterprise deployments, consider working with a DevOps team and following your organization's deployment standards and compliance requirements.
