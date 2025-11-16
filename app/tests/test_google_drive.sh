#!/bin/bash

# Google Drive Integration Test Script
# Server URL: http://192.168.10.50:5665/

SERVER_URL="http://192.168.10.50:5665"
API_BASE="${SERVER_URL}/api/v1"

echo "🚀 Google Drive Integration Test Suite"
echo "Server: ${SERVER_URL}"
echo "=" * 60

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print test headers
print_test() {
    echo -e "\n${BLUE}🧪 Test: $1${NC}"
    echo "----------------------------------------"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test 1: Basic Server Health Check
print_test "Basic Server Health Check"
response=$(curl -s -w "%{http_code}" -o /tmp/health_response.json "${API_BASE}/health_check")
http_code="${response: -3}"

if [ "$http_code" = "200" ]; then
    print_success "Server is running and responding"
    echo "Response:"
    cat /tmp/health_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/health_response.json
else
    print_error "Server health check failed (HTTP: $http_code)"
    exit 1
fi

# Test 2: Google Drive Setup Test
print_test "Google Drive Setup and Authentication"
response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -o /tmp/setup_response.json "${API_BASE}/google-drive/setup")
http_code="${response: -3}"

if [ "$http_code" = "200" ]; then
    success=$(cat /tmp/setup_response.json | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))" 2>/dev/null)

    if [ "$success" = "True" ]; then
        print_success "Google Drive setup successful!"
        echo "Response:"
        cat /tmp/setup_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/setup_response.json
    else
        print_warning "Google Drive setup returned success=false"
        echo "Response:"
        cat /tmp/setup_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/setup_response.json
        echo ""
        print_warning "This might mean Google Drive is not configured yet or there's an authentication issue."
    fi
else
    print_error "Google Drive setup test failed (HTTP: $http_code)"
    cat /tmp/setup_response.json
fi

# Test 3: List Google Drive Documents
print_test "List Google Drive Documents"
response=$(curl -s -w "%{http_code}" -X GET -o /tmp/documents_response.json "${API_BASE}/google-drive/documents")
http_code="${response: -3}"

if [ "$http_code" = "200" ]; then
    doc_count=$(cat /tmp/documents_response.json | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('documents', [])))" 2>/dev/null)
    print_success "Found $doc_count documents in Google Drive"
    echo "Response:"
    cat /tmp/documents_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/documents_response.json
else
    print_error "Failed to list Google Drive documents (HTTP: $http_code)"
    cat /tmp/documents_response.json
fi

# Test 4: Sync Google Drive Documents
print_test "Sync Google Drive Documents to Search Index"
response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"userId": "test_user"}' -o /tmp/sync_response.json "${API_BASE}/google-drive/sync")
http_code="${response: -3}"

if [ "$http_code" = "200" ]; then
    sync_count=$(cat /tmp/sync_response.json | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_synced', 0))" 2>/dev/null)
    print_success "Synced $sync_count documents for search indexing"
    echo "Response:"
    cat /tmp/sync_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/sync_response.json
else
    print_error "Failed to sync Google Drive documents (HTTP: $http_code)"
    cat /tmp/sync_response.json
fi

# Test 5: Search Preview (What documents would be discovered)
print_test "Search Preview - Document Auto-Discovery"
response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{
    "query": "medical information clinical trial results",
    "userId": "test_user",
    "max_results": 10,
    "score_threshold": 0.5
}' -o /tmp/preview_response.json "${API_BASE}/search/preview")
http_code="${response: -3}"

if [ "$http_code" = "200" ]; then
    total_found=$(cat /tmp/preview_response.json | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_sources', 0))" 2>/dev/null)
    print_success "Auto-discovery found $total_found relevant documents"
    echo "Response:"
    cat /tmp/preview_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/preview_response.json
else
    print_error "Search preview failed (HTTP: $http_code)"
    cat /tmp/preview_response.json
fi

# Test 6: Smart Chat with Auto-Discovery
print_test "Smart Chat with Auto-Discovery (Key Feature)"
response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{
    "prompt": "What medical information is available in the documents?",
    "userId": "test_user",
    "max_documents": 5,
    "relevance_threshold": 0.6
}' -o /tmp/chat_response.txt "${API_BASE}/chat/smart")
http_code="${response: -3}"

if [ "$http_code" = "200" ]; then
    print_success "Smart chat response received!"
    echo "Response (first 500 characters):"
    head -c 500 /tmp/chat_response.txt
    echo -e "\n...\n"
    print_success "This demonstrates the auto-discovery feature working!"
else
    print_error "Smart chat failed (HTTP: $http_code)"
    cat /tmp/chat_response.txt
fi

# Test 7: Unified Search Health Check
print_test "Unified Search System Health"
response=$(curl -s -w "%{http_code}" -X GET -o /tmp/search_health_response.json "${API_BASE}/search/health")
http_code="${response: -3}"

if [ "$http_code" = "200" ]; then
    print_success "Unified search system is healthy"
    echo "Response:"
    cat /tmp/search_health_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/search_health_response.json
else
    print_error "Search health check failed (HTTP: $http_code)"
    cat /tmp/search_health_response.json
fi

# Summary
echo -e "\n"
echo "=" * 60
echo -e "${BLUE}🎯 Test Summary${NC}"
echo "=" * 60

echo -e "${GREEN}✅ Google Drive Integration Features Tested:${NC}"
echo "  🔌 Server connectivity and health"
echo "  🔑 Google Drive authentication and setup"
echo "  📁 Document listing from Google Drive"
echo "  🔄 Document syncing to search index"
echo "  🔍 Intelligent document auto-discovery"
echo "  💬 Smart chat with auto-discovery"
echo "  🏥 Unified search system health"

echo -e "\n${YELLOW}📋 Next Steps:${NC}"
echo "  1. If Google Drive setup failed, check your .env configuration"
echo "  2. If documents aren't found, verify folder sharing with service account"
echo "  3. Try the smart chat feature with different medical queries"
echo "  4. Upload more medical documents to Google Drive for better testing"

echo -e "\n${BLUE}🚀 Your system now has intelligent auto-discovery!${NC}"
echo "  Users can ask questions without specifying documents"
echo "  System automatically finds relevant content from Google Drive + uploaded files"

# Cleanup
rm -f /tmp/health_response.json /tmp/setup_response.json /tmp/documents_response.json /tmp/sync_response.json /tmp/preview_response.json /tmp/chat_response.txt /tmp/search_health_response.json

echo -e "\n${GREEN}🎉 Testing complete!${NC}"