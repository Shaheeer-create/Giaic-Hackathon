import logging
import sys
from typing import Optional
from .core.config import settings


def setup_logging() -> None:
    """
    Setup logging configuration for the application.
    """
    # Create custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Prevent duplicate logs if logging is set up multiple times
    root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name of the logger (typically __name__ of the module)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    return logger


# Initialize logging when module is imported
setup_logging()