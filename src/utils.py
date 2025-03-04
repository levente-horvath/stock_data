import logging

# Configure logging settings
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose logging
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_logger(name):
    """
    Set up a logger with a specific name.
    
    Parameters:
        name (str): The name of the logger.
    
    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    return logger