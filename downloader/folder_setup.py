import os
import logging

def get_missing_folders(config):
    required_folders = [config.BASE_PATH, config.DESTINATION_FOLDER_PATH]
    missing_folders = [required_folder for required_folder in required_folders if not os.path.isdir(required_folder)]
    return missing_folders

def create_folders(folders_to_create):
    for folder_path in folders_to_create:
        os.mkdir(folder_path)

def setup_folders_if_needed(config):
    missing_folders = get_missing_folders(config)
    if missing_folders:
        logging.info(f"Following folders are missing: {missing_folders}. Creating.")
        try:
            create_folders(missing_folders)
            logging.info("Folders created.")
        except Exception as e:
            logging.error("Error happened while creating required folders.")
            logging.error(e)