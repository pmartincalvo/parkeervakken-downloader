import os

from dotenv import load_dotenv

load_dotenv()

class Config:

    ######### Paths
    BASE_PATH = os.environ["BASE_PATH"]
    DESTINATION_FOLDER_PATH = os.path.join(BASE_PATH, "downloaded_data/")
    LOGGING_FILE_PATH = os.path.join(BASE_PATH, "downloader.log")

    ######### API
    API_BASE_URL = os.environ["API_BASE_URL"]
    RESOURCE_PATH = "parkeervakken/parkeervakken"
