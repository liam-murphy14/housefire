import os
import uuid
from housefire.utils.logger import get_logger

logger = get_logger(__name__)


def create_temp_dir(base_path: str) -> str:
    """
    Create a new directory with a random name in the temp directory

    param: base_path: the path to the base directory to create the new directory in

    returns: the full path to the new directory
    """
    dir_name = str(uuid.uuid4())
    new_dir_path = os.path.join(base_path, dir_name)
    logger.debug(f"Creating temp directory at {new_dir_path}")
    os.mkdir(new_dir_path)
    logger.info(f"Created temp directory at {new_dir_path}")
    return new_dir_path


def delete_temp_dir(temp_dir_path: str) -> None:
    """
    Delete a directory and all of its contents
    USE WITH CAUTION

    param: temp_dir_path: the path to the directory to delete
    """
    logger.debug(f"Deleting directory at {temp_dir_path}")
    try:
        for filename in os.listdir(temp_dir_path):
            file_path = os.path.join(temp_dir_path, filename)
            logger.debug(f"Deleting file at {file_path}")
            os.remove(file_path)
        os.rmdir(temp_dir_path)
        logger.info(f"Deleted directory at {temp_dir_path}")
    except Exception as e:
        logger.error(f"Error deleting directory at {temp_dir_path}: {e}", exc_info=True)
