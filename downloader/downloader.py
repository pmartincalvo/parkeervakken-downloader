import os
import logging
import json
import datetime
import gzip

import requests

import compress_json


class DownloadAttempt:
    def __init__(self, url):
        self._url = url
        self._last_response = None

    def request_data(self, params=dict()):
        self._last_response = requests.get(self._url, params=params)

    def successful(self):
        if self._last_response.ok:
            return True
        return False

    def get_output(self):
        return self._last_response.json()["results"]

    def get_next_page(self):
        return self._last_response.json()["_links"]["next"]["href"]


class PagedEndpointIterator:
    def __init__(self, base_url, resource_path, only_fiscaal=False):
        self._base_url = base_url
        self._resource_path = resource_path
        self.only_fiscaal = only_fiscaal

    def get_pages(self):
        next_page = self._base_url + self._resource_path
        if self.only_fiscaal:
            next_page = next_page + "/?soort=FISCAAL"
        while next_page is not None:
            attempt = DownloadAttempt(next_page)
            attempt.request_data()
            if not attempt.successful():
                raise (Exception("Error while downloading page"))
            next_page = attempt.get_next_page()
            yield attempt.get_output()


class GeoJsonComposer:
    def __init__(self):
        self._vakken_list = []
        self._present_ids = set()

    def insert_records(self, record_list, are_fiscaal=False):
        if are_fiscaal:
            for record in record_list:
                record["soort"] = "FISCAAL"
        else:
            for record in record_list:
                record["soort"] = ""
        self._vakken_list.extend(record_list)

        for record in record_list:
            self._present_ids.add(record["id"])

    def insert_if_not_exist(self, record_list, are_fiscaal=False):
        records_to_insert = [
            record for record in record_list if record["id"] not in self._present_ids
        ]
        self.insert_records(records_to_insert, are_fiscaal)

    def get_content(self):
        return self._vakken_list


class DestinationInterface:
    def __init__(self, destination_folder):
        self._destination_folder = destination_folder

    def write_json(self, filename, content, compressed=False):
        if compressed:
            self._write_compressed_json(filename, content)
        else:
            self._write_normal_json(filename, content)

    def _write_normal_json(self, filename, content):
        with open(
            os.path.join(self._destination_folder, (filename + ".json")), "w"
        ) as destination_file:
            json.dump(content, destination_file)

    def _write_compressed_json(self, filename, content):
        compress_json.dump(
            content, os.path.join(self._destination_folder, (filename + ".json.gz"))
        )


def download_snapshot(config):
    destination = DestinationInterface(config.DESTINATION_FOLDER_PATH)
    json_composer = GeoJsonComposer()
    fiscaal_page_iterator = PagedEndpointIterator(
        config.API_BASE_URL, config.RESOURCE_PATH, only_fiscaal=True
    )
    not_fiscaal_page_iterator = PagedEndpointIterator(
        config.API_BASE_URL, config.RESOURCE_PATH, only_fiscaal=False
    )

    all_iterators = [fiscaal_page_iterator, not_fiscaal_page_iterator]

    try:
        for page_iterator in all_iterators:
            for page_content in page_iterator.get_pages():
                json_composer.insert_if_not_exist(page_content, are_fiscaal=page_iterator.only_fiscaal)
    except Exception as e:
        logging.error(e)
        return

    destination_filename = str(datetime.date.today())
    try:
        destination.write_json(
            destination_filename, json_composer.get_content(), compressed=True
        )
        logging.info("Data stored successfully")
    except Exception as e:
        logging.error("Could not write JSON file")
        logging.error(e)
