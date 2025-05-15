import os
import requests
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("GOTRIPLE_API")


def get_list_of_years(
    topics_languages: list,
    has_pdf_params: bool = False,
    with_datestamp: bool = False,
    only_return_years: bool = False,
):
    """
    Get the year metadata per topic-language

    Args:
        topics_languages: list of tuples (topic, language, conditions_of_access)
        has_pdf_params: bool, whether to filter by has_pdf
        with_datestamp: bool, whether to return the datestamp
        only_return_years: bool, whether to return only the years

    Returns:
        year_metadata_per_discipline: dict, year metadata per topic-language
    """
    year_metadata_per_discipline = dict()

    for row_index in tqdm(range(len(topics_languages))):
        row = topics_languages[row_index]
        t, l, c_a = row[0], row[1], row[2]
        fq_prefix = f"topic={t};in_language={l};conditions_of_access={c_a}"
        aggs_suffix = "datestamp,size=18000" if with_datestamp else "year,size=100"
        column_suffix = "datestamp" if with_datestamp else "year"
        params = {
            "q": "",
            "include_duplicates": "false",
            "fq": fq_prefix if not with_datestamp else f"{fq_prefix};year={row[3]}",
            "aggs": aggs_suffix,
            "sort": "most_recent",
            "page": 1,
            "size": "",
        }
        if has_pdf_params:
            params["fq"] = params["fq"] + ";" + "has_pdf=true"

        headers = {"accept": "application/ld+json"}

        # Make the request to the GoTripleAPI
        response = requests.get(url, params=params, headers=headers)
        total_items = response.json()["hydra:totalItems"]
        year_bucket_counts = response.json()["aggs"][column_suffix]["buckets"]

        year_metadata_per_discipline.setdefault(t, dict())
        year_metadata_per_discipline[t].setdefault(l, dict())
        if not with_datestamp and not only_return_years:
            year_metadata_per_discipline[t][l].setdefault(c_a, dict())
        if not with_datestamp and only_return_years:
            year_metadata_per_discipline[t][l].setdefault(c_a, dict())
            year_metadata_per_discipline[t][l][c_a].setdefault("year", [])
        if with_datestamp:
            year_metadata_per_discipline[t][l].setdefault(c_a, dict())
            year_metadata_per_discipline[t][l][c_a].setdefault(row[3], dict())

        if with_datestamp:
            year_metadata_per_discipline[t][l][c_a][row[3]]["total_items"] = total_items
            year_metadata_per_discipline[t][l][c_a][row[3]]["datestamp"] = [
                (_["key_as_string"], _["doc_count"])
                for _ in year_bucket_counts
                if _["doc_count"] > 0
            ]
        if not with_datestamp and not only_return_years:
            year_metadata_per_discipline[t][l][c_a]["total_items"] = total_items
            year_metadata_per_discipline[t][l][c_a]["year"] = [
                (_["key_as_string"], _["doc_count"])
                for _ in year_bucket_counts
                if _["doc_count"] > 0
            ]
        if not with_datestamp and only_return_years:
            year_metadata_per_discipline[t][l][c_a]["year"] += [
                _["key_as_string"] for _ in year_bucket_counts if _["doc_count"] > 0
            ]

    return year_metadata_per_discipline
