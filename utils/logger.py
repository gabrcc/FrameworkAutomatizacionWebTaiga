import logging
import pathlib

def setup_logger(name: str, log_file: str = "test.log") -> logging.Logger:
    """Configura un logger para los tests."""
    out = pathlib.Path("logs")
    out.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler apunta dentro de la carpeta logs
    fh = logging.FileHandler(out / log_file, mode='a', encoding='utf-8')
    fh.setFormatter(formatter)
    
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger
