# import logging
# import pathlib

# def setup_logger(name: str, log_file: str = "test.log") -> logging.Logger:
#     """Configura un logger para los tests."""
#     out = pathlib.Path("logs")
#     out.mkdir(parents=True, exist_ok=True)
    
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)
    
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
#     # File handler apunta dentro de la carpeta logs
#     fh = logging.FileHandler(out / log_file, mode='a', encoding='utf-8')
#     fh.setFormatter(formatter)
    
#     ch = logging.StreamHandler()
#     ch.setFormatter(formatter)
    
#     if not logger.handlers:
#         logger.addHandler(fh)
#         logger.addHandler(ch)
    
#     return logger

import logging
import pathlib

def setup_logger(log_file: str = "test_log.log", level=logging.INFO) -> logging.Logger:
    """
    Configura un logger unificado para todo el proyecto de tests.
    - log_file: nombre del archivo de log dentro de 'logs/'.
    - level: nivel de logging (DEBUG, INFO, ERROR, etc.)
    """
    # Carpeta base para logs
    out = pathlib.Path("logs")
    out.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("tests")  # Logger global para todos los tests
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler (escribe todo en logs/test_log.log)
    fh = logging.FileHandler(out / log_file, mode="a", encoding="utf-8")
    fh.setFormatter(formatter)

    # Stream handler (muestra logs en consola al correr pytest)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # Evita agregar handlers múltiples si ya existen
    if not logger.hasHandlers():
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
