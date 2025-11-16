"""
Configuration settings for the Healthcare Document Assistant application.

This module defines all configuration classes using Pydantic Settings for
environment variable management and validation.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AppInfo(BaseSettings):
    """
    General application configuration.
    
    Attributes:
        PROJECT_NAME: Name of the application
        VERSION: Current version of the application
        DESCRIPTION: Brief description of the application
        API_V1_STR: API version 1 base path
        ALLOWED_ORIGINS: List of allowed CORS origins
    """
    PROJECT_NAME: str = "Healthcare Document Assistant API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered assistant for healthcare document management and analysis"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["*"]  # Configure with specific domains in production

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class QdrantSettings(BaseSettings):
    """
    Qdrant vector database configuration.
    
    Attributes:
        QDRANT_HOST_URL: URL endpoint for Qdrant server
    """
    QDRANT_HOST_URL: str
 
    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"
        extra = "ignore"


class MongoDBSettings(BaseSettings):
    """
    MongoDB database configuration.
    
    Attributes:
        DOCUMENT_DB_CONNECTION_STRING: MongoDB connection string
    """
    DOCUMENT_DB_CONNECTION_STRING: str
 
    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"
        extra = "ignore"


class OllamaSettings(BaseSettings):
    """
    Ollama LLM configuration.
    
    Attributes:
        OLLAMA_ENDPOINT_URL: URL endpoint for Ollama API
        OLLAMA_EMBEDDING_MODEL: Model name for embeddings
        OLLAMA_ANALYTICAL_MODEL: Primary model for analysis
        OLLAMA_ANALYTICAL_MODEL2: Secondary model for analysis
    """
    OLLAMA_ENDPOINT_URL: str = "http://localhost:11434"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    OLLAMA_ANALYTICAL_MODEL: str = "gpt-4o"
    OLLAMA_ANALYTICAL_MODEL2: str = "gpt-4o"
 
    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"
        extra = "ignore"


class AWSSettings(BaseSettings):
    """
    AWS S3 configuration for document storage.
    
    Attributes:
        access_key: AWS access key ID
        secret_key: AWS secret access key
        qdrant_host_url: Qdrant host URL (deprecated, use QdrantSettings)
        ollama_endpoint_url: Ollama endpoint URL (deprecated, use OllamaSettings)
        document_db_connection_string: MongoDB connection (deprecated, use MongoDBSettings)
    """
    access_key: str
    secret_key: str
    qdrant_host_url: str
    ollama_endpoint_url: str
    document_db_connection_string: str

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


class OpenAISettings(BaseSettings):
    """
    OpenAI API configuration.
    
    Attributes:
        OPENAI_API_KEY: OpenAI API key for authentication
        OPENAI_API_MODEL: Default model to use for OpenAI requests
    """
    OPENAI_API_KEY: str
    OPENAI_API_MODEL: str = "gpt-4o"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class GroqSettings(BaseSettings):
    """
    Groq API configuration (Open-source LLM inference).
    
    Attributes:
        GROQ_API_KEY: Groq API key for authentication (free tier available)
        GROQ_API_MODEL: Default model to use (llama-3.1-70b-versatile, mixtral-8x7b, etc.)
        GROQ_API_BASE: Groq API base URL
    """
    GROQ_API_KEY: Optional[str] = None
    GROQ_API_MODEL: str = "llama-3.1-70b-versatile"
    GROQ_API_BASE: str = "https://api.groq.com/openai/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class GoogleDriveSettings(BaseSettings):
    """
    Google Drive API configuration.

    Attributes:
        GOOGLE_DRIVE_FOLDER_ID: ID of the shared Google Drive folder containing medical documents
        GOOGLE_SERVICE_ACCOUNT_KEY_PATH: Path to the service account JSON key file
        GOOGLE_DRIVE_QDRANT_COLLECTION: Qdrant collection name for Drive documents
        GOOGLE_DRIVE_ENABLED: Whether Google Drive integration is enabled
    """
    GOOGLE_DRIVE_FOLDER_ID: Optional[str] = None
    GOOGLE_SERVICE_ACCOUNT_KEY_PATH: str = "credentials/service_account.json"
    GOOGLE_DRIVE_QDRANT_COLLECTION: str = "creator"
    GOOGLE_DRIVE_ENABLED: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-enable Google Drive if folder ID is provided
        if self.GOOGLE_DRIVE_FOLDER_ID:
            self.GOOGLE_DRIVE_ENABLED = True

    @property
    def is_configured(self) -> bool:
        """
        Check if Google Drive is properly configured.
        
        Returns:
            bool: True if all required configuration is present and valid
        """
        import os
        return (
            self.GOOGLE_DRIVE_ENABLED and
            self.GOOGLE_DRIVE_FOLDER_ID is not None and
            os.path.exists(self.GOOGLE_SERVICE_ACCOUNT_KEY_PATH)
        )


# Initialize settings instances
mongo_db_settings = MongoDBSettings()
qdrant_settings = QdrantSettings()
ollama_settings = OllamaSettings()
aws_settings = AWSSettings()
openai_settings = OpenAISettings()
groq_settings = GroqSettings()
google_drive_settings = GoogleDriveSettings()


# Initialize settings instances
app_info = AppInfo()
qdrant_settings = QdrantSettings()
mongo_db_settings = MongoDBSettings()
ollama_settings = OllamaSettings()
openai_settings = OpenAISettings()
aws_settings = AWSSettings()
google_drive_settings = GoogleDriveSettings()