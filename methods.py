import os
import zlib
import time
import json
import gzip
import base64
import random
import logging
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from multiprocessing import Pool
from itertools import product, chain

from helper import is_valid_pdf
from const import HAS_PDF_PARAMS

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
logging.getLogger().setLevel(logging.INFO)

url = os.getenv("GOTRIPLE_API")


def save_data_batch_to_drive(data_batch: str, folder_path: str, batch_number: str):
    """
    Saves a batch of data to a file in the local storage path.

    Args:
        data_batch: list, the data batch to save
        folder_path: str, the local path to save the data to
        batch_number: str, the batch number (for debugging)
    """
    filename = f"data_batch_{batch_number}.json"
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w") as f:
        json.dump(data_batch, f, indent=2, ensure_ascii=False)


def fetch_all_pages(
    url: str, base_params: dict, headers: dict, storage_local_path: str
) -> None:
    """
    Fetches all pages for a given set of parameters. Stores a list of all items across all pages.

    Args:
        url: str, the URL to fetch the data from
        base_params: dict, the base parameters to fetch the data from
        headers: dict, the headers to fetch the data from
        storage_local_path: str, the local path to save the data to
    """
    all_items = []
    current_page = 1
    total_pages = None

    params_str = ", ".join([f"{_}: {str(base_params[_])}" for _ in base_params])

    while total_pages is None or current_page <= total_pages:
        params = base_params.copy()
        params["page"] = current_page

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            data = response.json()

            # Get total pages on first iteration if available in response
            if total_pages is None:
                items_per_page = int(params["size"])
                total_items = int(data["hydra:totalItems"])
                total_pages = (total_items + items_per_page - 1) // items_per_page
                logging.info(
                    f"Total items: {total_items}, Total pages: {total_pages} for {params_str}"
                )

            # extract and store the items from the hydra:member payload
            if "hydra:member" in data:
                items = data["hydra:member"]
                all_items.extend(items)
                logging.info(f"Fetched page {current_page} for {params_str}")
            else:
                logging.warning(
                    f"No 'hydra:member' found in response for page {current_page} for {params_str}"
                )
                break

            if (current_page % 10 == 0) or (current_page == total_pages):
                save_data_batch_to_drive(all_items, storage_local_path, current_page)
                all_items = []

            current_page += 1
            # their API only allows 100 pages per request
            if current_page > 100:
                break

            # small delay to not hit rate limits
            time.sleep(1.5)

        except requests.exceptions.RequestException as e:
            logging.error(
                f"Error fetching page {current_page} for {params_str}: {str(e)}"
            )
            break


def store_metadata(tly_combination):
    """
    Store the metadata for a given topic, language, conditions of access, year, datestamp.

    Args:
        tly_combination: tuple which consists ofthe topic, language, conditions of access, year, datestamp
    """
    topic, language, conditions_of_access, year, datestamp, _ = tly_combination
    base_params = {
        "q": "",
        "include_duplicates": "false",
        "fq": f"topic={topic};in_language={language};year={year};conditions_of_access={conditions_of_access};datestamp={datestamp};datestamp={datestamp}",
        "sort": "name:desc",
        "size": "100",
    }

    if HAS_PDF_PARAMS:
        base_params["fq"] = base_params["fq"] + ";" + "has_pdf=true"

    headers = {"accept": "application/ld+json"}
    logging.info(
        f"Starting to fetch all pages for {', '.join([str(_) for _ in tly_combination])}"
    )

    storage_local_path = os.getenv("STORAGE_LOCAL_PATH")
    folder_path = f"{storage_local_path}/{topic}/{language}/{str(year)}/{conditions_of_access}/{str(datestamp)}"
    os.makedirs(folder_path, exist_ok=True)

    _ = fetch_all_pages(url, base_params, headers, folder_path)
    logging.info(
        f"Completed fetching all pages for {', '.join([str(_) for _ in tly_combination])}."
    )


def extract_pdf(record: tuple):
    """
    Extract the PDF from the URL and save it to the local file system in JSONL GZ format with the corresponding id.

    Args:
        record: tuple, the record to extract the PDF from
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    id_, id_full, pdf_url, disc, conditions_of_access, output_file, error_file = record

    try:
        # use verify=False to bypass SSL certificate verification
        response = requests.get(pdf_url, headers=headers, verify=False, timeout=30)
        time.sleep(0.5)

        if response.status_code == 200:
            pdf_content = response.content

            ## uncomment if one wants to validate the PDF content
            # if not is_valid_pdf(pdf_content):
            #     with open(error_file, "a") as file:
            #         file.write(f"{disc},{id_},{id_full},{conditions_of_access},{pdf_url},error:invalid_pdf_content\n")
            #     logging.error(f"Invalid PDF content for id: {id_} for url: {pdf_url}")
            #     return None

            record = {
                "id": id_,
                "@id": id_full,
                "url": pdf_url,
                "filename": os.path.basename(pdf_url),
                "content_type": response.headers.get("Content-Type", "application/pdf"),
                "content_length": len(pdf_content),
                "content_bytes": base64.b64encode(pdf_content).decode("utf-8"),
            }

            return record
        else:
            # gives me some status code which is not 200
            with open(error_file, "a") as file:
                file.write(
                    f"{disc},{id_},{id_full},{conditions_of_access},{pdf_url},{response.status_code}\n"
                )
            logging.error(
                f"Failed to download PDF: {response.status_code} for id: {id_} for url: {pdf_url}"
            )

    except Exception as e:
        with open(error_file, "a") as file:
            file.write(
                f"{disc},{id_},{id_full},{conditions_of_access},{pdf_url},error:{str(e)}\n"
            )
        logging.error(
            f"Error downloading PDF for id: {id_}, url: {pdf_url}, error: {str(e)}"
        )


def save_discipline_pdfs(disc: str):
    """
    Read the merged JSONL file and extract the PDFs from the URLs.

    Args:
        disc: str, the discipline to save the PDFs for
    """
    storage_local_path = os.getenv("STORAGE_LOCAL_PATH")
    start_from_point = False if os.getenv("START_FROM_POINT") == "False" else True
    randomize_records = False if os.getenv("RANDOMIZE_RECORDS") == "False" else True
    num_records = int(os.getenv("NUM_RECORDS"))
    point_id = os.getenv("POINT_ID")

    if start_from_point:
        logging.info(
            f"Starting to save PDFs for discipline: {disc}, start_from_point: {start_from_point}, point_id: {point_id}"
        )

    output_file = (
        f"{storage_local_path}/{disc}_pdf_merged.jsonl.gz"
        if not randomize_records
        else f"{storage_local_path}/{disc}_pdf_merged_randomized.jsonl.gz"
    )

    error_file = (
        f"{disc}_pdf_extraction_errors.csv"
        if not randomize_records
        else f"{disc}_pdf_extraction_errors_randomized.csv"
    )
    with open(error_file, "w") as file:
        file.write("discipline,id,id_full,conditions_of_access,url,status_code\n")

    records_to_process = []
    with gzip.open(f"{storage_local_path}/{disc}_merged.jsonl.gz", "rt") as f:
        if not start_from_point:
            for line in f:
                record = json.loads(line.strip())
                record_data = (
                    record["id"],
                    record["@id"],
                    record["url"][-1],
                    disc,
                    "|".join(record["conditions_of_access"]),
                    output_file,
                    error_file,
                )
                records_to_process.append(record_data)
        else:
            point_reached = False
            for line in f:
                record = json.loads(line.strip())
                if not point_reached:
                    if record["id"] != point_id:
                        continue
                    point_reached = True
                else:
                    record_data = (
                        record["id"],
                        record["@id"],
                        record["url"][-1],
                        disc,
                        "|".join(record["conditions_of_access"]),
                        output_file,
                        error_file,
                    )
                    records_to_process.append(record_data)

    if randomize_records:
        random.shuffle(records_to_process)
        records_to_process = records_to_process[:num_records]
        with open("records.json", "w") as file:
            json.dump(records_to_process, file, indent=4)
        logging.info(f"Randomized {len(records_to_process)} records")

    with Pool(processes=int(os.getenv("NUM_PROCESSES"))) as pool:
        for record in pool.imap(extract_pdf, records_to_process):
            if not record:
                continue
            line = json.dumps(record) + "\n"

            try:
                if os.path.exists(output_file):
                    try:
                        with gzip.open(output_file, "rb") as test_f:
                            test_f.read(1)
                        mode = "ab"
                    except Exception as gz_error:
                        logging.warning(
                            f"\nExisting gzip file {output_file} is corrupted: {gz_error}. Creating new file.\n"
                        )
                        mode = "wb"
                else:
                    mode = "wb"

                with gzip.open(output_file, mode, compresslevel=6) as f:
                    f.write(line.encode("utf-8"))
                logging.info(
                    f"Downloaded PDF for id: {record['id']} for url:{record['url']}"
                )

            except Exception as gz_error:
                with open(error_file, "a") as file:
                    file.write(
                        f"{disc},{record['id']},{record['@id']},{'|'.join(record['conditions_of_access'])},{record['url']},pdf_gz_error\n"
                    )
                logging.error(f"Failed to write PDF to file: {gz_error}")
