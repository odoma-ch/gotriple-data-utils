import io
import os
import gzip
import json
import base64
import requests
from PyPDF2 import PdfReader

from dotenv import load_dotenv

load_dotenv()

url = os.getenv("GOTRIPLE_API")


def get_document_by_id(document_id: str):
    """
    Get the metadata for a document by its id.

    Args:
        document_id: str, the id of the document

    Returns:
        dict, the metadata for the document
    """
    params = {
        "q": "",
        "include_duplicates": "false",
        "fq": f"id={document_id}",
        "sort": "name:desc",
        "page": 1,
        "size": 25,
    }
    headers = {"accept": "application/ld+json"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()


def is_valid_pdf(pdf_content):
    """
    Check if the PDF content is valid.

    Args:
        pdf_content: bytes, the content of the PDF

    Returns:
        bool, True if the PDF content is valid, False otherwise
    """
    if not pdf_content.startswith(b"%PDF-"):
        raise Exception("Invalid PDF header")
    try:
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        if num_pages > 0:
            _ = pdf_reader.pages[0].extract_text()

        return True
    except Exception as e:
        raise Exception(f"Error validating PDF: {e}")


def read_discipline_pdfs(disc: str):
    """
    Example code to read the PDF from the JSONL file.

    Args:
        disc: str, the discipline to read the PDF from
    """
    storage_local_path = os.getenv("STORAGE_LOCAL_PATH")
    filepath = (
        f"{storage_local_path}/{disc}_pdf_merged.jsonl.gz"
        if not os.getenv("RANDOMIZE_RECORDS")
        else f"{storage_local_path}/{disc}_pdf_merged_randomized.jsonl.gz"
    )
    with gzip.open(filepath, "rb") as f:
        for line in f:
            record = json.loads(line)
            pdf_content = record["content_bytes"]
            pdf_content = base64.b64decode(pdf_content)
            with open(f"extracted_{record['id']}", "wb") as pdf_file:
                pdf_file.write(pdf_content)
