"""
Hash Utility Module

Provides hashing utilities for security-sensitive operations.
Currently implements a pass-through for development; should be enhanced for production.
"""

import hmac
import hashlib
from typing import Optional


async def hash_param(param: str, secret_key: Optional[str] = None) -> str:
    """
    Hash a parameter string.
    
    Note: Currently returns the parameter unchanged for development purposes.
    In production, this should implement proper HMAC-based hashing.
    
    Args:
        param: The parameter string to hash
        secret_key: Optional secret key for HMAC hashing
        
    Returns:
        str: Hashed parameter (currently returns original param)
    """
    # TODO: Implement proper hashing for production
    # Example implementation:
    # if secret_key:
    #     return hmac.new(
    #         secret_key.encode(),
    #         param.encode(),
    #         hashlib.sha256
    #     ).hexdigest()
    
    return param


def hash_string(text: str, algorithm: str = "sha256") -> str:
    """
    Generate a hash of a string using the specified algorithm.
    
    Args:
        text: The text to hash
        algorithm: Hash algorithm to use (default: sha256)
        
    Returns:
        str: Hexadecimal hash digest
    """
    hash_func = getattr(hashlib, algorithm)
    return hash_func(text.encode()).hexdigest()


