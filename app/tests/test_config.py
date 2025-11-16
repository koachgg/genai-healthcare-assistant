#!/usr/bin/env python3
"""
Quick test script to verify Google Drive configuration is working properly.
"""


import sys
import os
sys.path.append('src')

def test_google_drive_config():
    """Test Google Drive configuration loading."""
    print("🧪 Testing Google Drive configuration...")

    try:
        from configs.config import google_drive_settings
        print("✅ Google Drive settings imported successfully")

        print(f"📁 Google Drive Folder ID: {google_drive_settings.GOOGLE_DRIVE_FOLDER_ID}")
        print(f"🔑 Service Account Key Path: {google_drive_settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY_PATH}")
        print(f"📊 Qdrant Collection: {google_drive_settings.GOOGLE_DRIVE_QDRANT_COLLECTION}")
        print(f"⚡ Google Drive Enabled: {google_drive_settings.GOOGLE_DRIVE_ENABLED}")
        print(f"🛠️ Is Configured: {google_drive_settings.is_configured}")

        return True

    except Exception as e:
        print(f"❌ Error importing Google Drive settings: {str(e)}")
        return False

def test_other_configs():
    """Test other configuration imports."""
    print("\n🧪 Testing other configurations...")

    try:
        from configs.config import (
            app_info,
            qdrant_settings,
            mongo_db_settings,
            ollama_settings,
            openai_settings,
            aws_settings
        )
        print("✅ All configuration settings imported successfully")
        return True

    except Exception as e:
        print(f"❌ Error importing configuration settings: {str(e)}")
        return False

def test_qdrant_import():
    """Test Qdrant client import."""
    print("\n🧪 Testing Qdrant client import...")

    try:
        from services.qdrant_host import current_qdrant_client
        print("✅ Qdrant client imported successfully")
        # Note: Don't test connection here as it requires Qdrant server to be running
        return True

    except Exception as e:
        print(f"❌ Error importing Qdrant client: {str(e)}")
        return False

def test_google_drive_imports():
    """Test Google Drive service imports."""
    print("\n🧪 Testing Google Drive service imports...")

    try:
        from services.google_drive_service import google_drive_service, DriveDocument
        from services.unified_search import unified_search_service
        print("✅ Google Drive services imported successfully")
        return True

    except Exception as e:
        print(f"❌ Error importing Google Drive services: {str(e)}")
        return False

def test_main_import():
    """Test main application import."""
    print("\n🧪 Testing main application import...")

    try:
        from main import app
        print("✅ Main FastAPI application imported successfully")
        print(f"📱 App title: {app.title}")
        return True

    except Exception as e:
        print(f"❌ Error importing main application: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🚀 Google Drive Integration Configuration Test")
    print("=" * 50)

    success = True

    # Test Google Drive config
    if not test_google_drive_config():
        success = False

    # Test other configs
    if not test_other_configs():
        success = False

    # Test Qdrant import (separate from connection test)
    if not test_qdrant_import():
        success = False

    # Test Google Drive imports
    if not test_google_drive_imports():
        success = False

    # Test main import (this will test connection to Qdrant if server is running)
    if not test_main_import():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! System should start correctly.")
        print("\n💡 To configure Google Drive:")
        print("   1. Set GOOGLE_DRIVE_FOLDER_ID in your .env file")
        print("   2. Place service account key at credentials/service_account.json")
        print("   3. Restart the server")
    else:
        print("💥 Some tests failed. Please check the errors above.")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)