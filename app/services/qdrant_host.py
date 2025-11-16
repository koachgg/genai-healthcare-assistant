"""
Qdrant Vector Database Connection

This module initializes and manages the connection to the Qdrant vector database.
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models

from configs.config import qdrant_settings
from lib.logger import log


def initialize_qdrant_client() -> QdrantClient:
    """
    Initialize and test connection to Qdrant vector database.
    
    Returns:
        QdrantClient: Configured Qdrant client instance
        
    Raises:
        ConnectionError: If unable to connect to Qdrant
    """
    try:
        log("Initializing Qdrant client...")
        client = QdrantClient(
            url=qdrant_settings.QDRANT_HOST_URL,
            timeout=300
        )
        
        # Test connection with a heartbeat
        log("Testing Qdrant connection...")
        client.get_collections()
        
        log("✓ Qdrant client connected successfully!")
        return client
        
    except Exception as e:
        error_message = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ⚠️  QDRANT CONNECTION FAILED                            ║
║                                                          ║
║  Could not connect to Qdrant vector database.           ║
║  Please ensure:                                          ║
║  1. Qdrant server is running                            ║
║  2. QDRANT_HOST_URL is correctly configured             ║
║  3. Network connectivity is available                   ║
║                                                          ║
║  Error: {str(e)[:40]}...                                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        log(error_message)
        raise ConnectionError(f"Failed to connect to Qdrant: {e}")


# Initialize the global Qdrant client
try:
    current_qdrant_client = initialize_qdrant_client()
except ConnectionError as e:
    log(f"WARNING: Qdrant initialization failed. Vector operations will not be available.")
    current_qdrant_client = None