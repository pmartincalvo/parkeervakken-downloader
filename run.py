import logging

from downloader.downloader import download_snapshot
from downloader.config import Config
from downloader.folder_setup import setup_folders_if_needed
from downloader.my_logging import setup_logging

if __name__ == "__main__":

    setup_folders_if_needed(Config)
    setup_logging(Config)

    logging.info("Starting download session")
    download_snapshot(Config)
    logging.info("Download session finished")
