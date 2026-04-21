import psutil 
import logging

logger = logging.getLogger(__name__)

# Iterate over the list of processes through "psutil" and check if anki is running
def is_anki_running():
    process_name = "anki"

    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                logger.info("Anki is running")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass 
    logger.error("Anki is not running. Please start it before calling any other functions")
    return False
