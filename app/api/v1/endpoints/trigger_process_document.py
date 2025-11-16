"""
Document Processing Trigger Endpoint

This endpoint initiates document processing for uploaded documents.
It validates the request, retrieves the document from S3, and starts
background processing including text extraction, chunking, and vectorization.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks

from models.doc import DocModel
from lib.hasher import hash_param
from lib.logger import log
from services.s3host import current_s3_client
from services.document_encoder import DocumentEncoder
from schemas.base import TriggerProcessingRequest, TriggerProcessingResponse
from utils.document_handling.process_document import process_document
from utils.document_handling.save_document_data_to_DB import doc_repo, mark_doc_status_in_db

router = APIRouter()


async def run_document_processing_task(
    document_data: bytes,
    document_name: str,
    user_id: str,
    document_id: str
) -> None:
    """
    Execute document processing in the background.
    
    This function runs the complete document processing pipeline including:
    - Text extraction
    - Document chunking
    - Vector embedding generation
    - Metadata extraction
    
    Args:
        document_data: Binary content of the document
        document_name: Name of the document file
        user_id: ID of the user who owns the document
        document_id: Unique identifier for the document
    """
    try:
        log(f"Starting background processing for document: {document_id}")
        await process_document(document_data, document_name, user_id, document_id)
        log(f"Document processing completed successfully: {document_id}")
    except Exception as e:
        log(f"Error during document processing for {document_id}: {str(e)}")
        await mark_doc_status_in_db("error", document_id)


@router.post("/trigger-document-processing", response_model=TriggerProcessingResponse)
async def trigger_document_processing(
    request: TriggerProcessingRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger background processing for an uploaded document.
    
    This endpoint:
    1. Validates the request and user authorization
    2. Verifies document existence in S3
    3. Retrieves document from S3
    4. Initiates background processing
    5. Creates document entry in database
    
    Args:
        request: Processing request containing user_id and document_id
        background_tasks: FastAPI background tasks manager
        
    Returns:
        TriggerProcessingResponse: Status confirmation
        
    Raises:
        HTTPException 400: If required fields are missing
        HTTPException 403: If user is not authorized to access document
        HTTPException 404: If document not found in S3
        HTTPException 500: If processing fails
    """
    document_id = request.uuid
    user_id = request.userId

    try:
        # Validate required fields
        if not document_id.strip() or not user_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Both userId and uuid are required fields"
            )

        # Hash user ID for security
        user_id = await hash_param(user_id)
        
        # Verify user authorization
        decoded_user_id, _, _ = DocumentEncoder.decode_document_id(document_id)
        if decoded_user_id != user_id:
            log(f"Authorization failed: User {user_id} attempted to access document {document_id}")
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access this document"
            )
        
        # Check document existence in S3
        document_exists = await current_s3_client.check_document_exists(document_id=document_id)
        if not document_exists:
            log(f"Document not found in S3: {document_id}")
            raise HTTPException(
                status_code=404,
                detail="Document not found in S3 storage"
            )

        # Retrieve document from S3
        log(f"Retrieving document from S3: {document_id}")
        document_data, document_name = await current_s3_client.get_document(
            document_id=document_id
        )

        # Schedule background processing
        background_tasks.add_task(
            run_document_processing_task,
            document_data,
            document_name,
            user_id,
            document_id
        )

        # Create document entry in database
        await doc_repo.create_doc(
            DocModel(
                _id=document_id,
                userId=user_id,
                filename=document_name
            )
        )
        log(f"Document entry created in database: {document_id}")

        return TriggerProcessingResponse(status="ok")

    except HTTPException:
        await mark_doc_status_in_db("error", document_id)
        raise
    except Exception as e:
        error_message = f"Error processing document {document_id}: {str(e)}"
        log(error_message)
        await mark_doc_status_in_db("error", document_id)
        raise HTTPException(status_code=500, detail=error_message)
