"""
Document Encoder Service

This module provides utilities for encoding and decoding document identifiers,
as well as generating file paths for various document-related resources in S3.
"""

import base64
import json
import re
from datetime import datetime
from typing import Tuple, Optional
import pytz


class DocumentEncoder:
    """
    Utility class for encoding/decoding document identifiers and generating S3 file paths.
    
    This class provides static methods for:
    - Encoding document metadata into unique identifiers
    - Decoding identifiers back into metadata
    - Generating S3 file paths for documents and related resources
    """
    
    @staticmethod
    def encode_document_id(user_id: str, document_name: str) -> str:
        """
        Generate a unique encoded document identifier.
        
        Creates a base64-encoded string containing user ID, document name (without .pdf extension),
        and timestamp in Europe/Madrid timezone.
        
        Args:
            user_id: Unique identifier for the user
            document_name: Name of the document (with or without .pdf extension)
            
        Returns:
            str: Base64-encoded document identifier
        """
        # Remove .pdf extension if present
        document_name = document_name.replace(".pdf", "")
        
        # Generate timestamp in Madrid timezone
        madrid_tz = pytz.timezone("Europe/Madrid")
        timestamp = datetime.now(madrid_tz).isoformat()
        
        # Create JSON data structure
        data = json.dumps({
            "userId": user_id,
            "document_name": document_name,
            "timestamp": timestamp
        })
        
        # Encode to base64
        encoded_bytes = base64.b64encode(data.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
        
    @staticmethod
    def decode_document_id(encoded_string: str) -> Tuple[str, str, str]:
        """
        Decode an encoded document identifier.
        
        Extracts user ID, document name, and upload timestamp from the encoded string.
        
        Args:
            encoded_string: Base64-encoded document identifier
            
        Returns:
            Tuple[str, str, str]: (user_id, document_name, upload_timestamp)
        """
        decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
        data = json.loads(decoded_bytes.decode('utf-8'))
        
        user_id = data["userId"]
        document_name = data["document_name"]
        upload_timestamp = data["timestamp"]
        
        return user_id, document_name, upload_timestamp
    
    @staticmethod
    def get_thumbnail_image_id(encoded_string: str) -> str:
        """
        Generate a thumbnail image identifier.
        
        Args:
            encoded_string: Encoded document identifier
            
        Returns:
            str: Thumbnail image identifier
        """
        return f'{encoded_string}_thumb'
    
    @staticmethod
    def get_thumbnail_image_file_key(document_id: str) -> str:
        """
        Get S3 key for document thumbnail image.
        
        Args:
            document_id: Encoded document identifier
            
        Returns:
            str: S3 key path (e.g., 'DB/USERS/john_doe/doc_preview_images/document/Page 1.png')
        """
        user_id, document_name, _ = DocumentEncoder.decode_document_id(document_id)
        return f'DB/USERS/{user_id}/doc_preview_images/{document_name}/Page 1.png'

    @staticmethod
    def get_original_document_file_key(encoded_string: str) -> str:
        """
        Get S3 key for the original document PDF.
        
        Args:
            encoded_string: Encoded document identifier
            
        Returns:
            str: S3 key path for the original document
        """
        user_id, document_name, _ = DocumentEncoder.decode_document_id(encoded_string)
        return f'DB/USERS/{user_id}/docs/{document_name}.pdf'
    
    @staticmethod
    def get_preview_images_folder_key(encoded_string: str) -> str:
        """
        Get S3 folder key for all document preview images.
        
        Args:
            encoded_string: Encoded document identifier
            
        Returns:
            str: S3 folder path for preview images
        """
        user_id, document_name, _ = DocumentEncoder.decode_document_id(encoded_string)
        return f'DB/USERS/{user_id}/doc_preview_images/{document_name}/'
    
    @staticmethod
    def get_preview_images_file_key(encoded_string: str, page_number: int) -> str:
        """
        Get S3 key for a specific page preview image.
        
        Args:
            encoded_string: Encoded document identifier
            page_number: Page number (1-indexed)
            
        Returns:
            str: S3 key path for the specific page preview
        """
        user_id, document_name, _ = DocumentEncoder.decode_document_id(encoded_string)
        return f'DB/USERS/{user_id}/doc_preview_images/{document_name}/Page {page_number}.png'

    @staticmethod
    def get_table_images_folder_key(encoded_string: str) -> str:
        """
        Get S3 folder key for all extracted table images.
        
        Args:
            encoded_string: Encoded document identifier
            
        Returns:
            str: S3 folder path for table images
        """
        user_id, document_name, _ = DocumentEncoder.decode_document_id(encoded_string)
        return f'DB/USERS/{user_id}/docs_tables/{document_name}/'
    
    @staticmethod
    def get_extracted_table_image_file_key(table_image_id: str) -> Optional[str]:
        """
        Get S3 key for an extracted table image.
        
        Table image ID format: {document_id}_PN{page_number}_TN{table_number}
        
        Args:
            table_image_id: Encoded table image identifier
            
        Returns:
            Optional[str]: S3 key path for the table image, or None if invalid ID format
        """
        pattern = r"(.+)_PN(\d+)_TN(\d+)"
        match = re.match(pattern, table_image_id)
        
        if match:
            document_id, page_number, table_number = match.groups()
            user_id, document_name, _ = DocumentEncoder.decode_document_id(document_id)
            return f'DB/USERS/{user_id}/docs_tables/{document_name}/Page {page_number} Table {table_number}.png'
        
        return None
 
    @staticmethod
    def get_document_outline_source_images_folder_key(encoded_string: str) -> str:
        """
        Get S3 folder key for document outline source images.
        
        Args:
            encoded_string: Encoded document identifier
            
        Returns:
            str: S3 folder path for outline source images
        """
        user_id, document_name, _ = DocumentEncoder.decode_document_id(encoded_string)
        return f'DB/USERS/{user_id}/document_outline_sources/{document_name}/'
    
    @staticmethod
    def get_document_outline_source_image_file_key(document_outline_source_image_id: str) -> Optional[str]:
        """
        Get S3 key for a document outline source image.
        
        Image ID format: {document_id}_PN{page_number}_DOSI
        
        Args:
            document_outline_source_image_id: Encoded outline source image identifier
            
        Returns:
            Optional[str]: S3 key path for the outline source image, or None if invalid ID
        """
        match = re.match(r"^(.*)_PN(\d+)_DOSI$", document_outline_source_image_id)
        
        if match:
            document_id = match.group(1)
            page_number = int(match.group(2))
            user_id, document_name, _ = DocumentEncoder.decode_document_id(document_id)
            return f'DB/USERS/{user_id}/document_outline_sources/{document_name}/Page_{page_number}.png'
        
        return None
        
    @staticmethod
    def get_highlight_helper_table_file_key(encoded_string: str) -> str:
        """
        Get S3 key for highlight helper table CSV file.
        
        Args:
            encoded_string: Encoded document identifier
            
        Returns:
            str: S3 key path for the highlight helper table
        """
        user_id, document_name, _ = DocumentEncoder.decode_document_id(encoded_string)
        return f'DB/USERS/{user_id}/highlight_helper_tables/{document_name}.csv'