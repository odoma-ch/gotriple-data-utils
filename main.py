# Extract data for the preselected domains: https://api.gotriple.eu/

import os
import json
import logging
import pandas as pd
from itertools import product
from multiprocessing import Pool

from dotenv import load_dotenv

load_dotenv()

from aggregation_by_year import get_list_of_years
from const import TOPICS, LANGUAGES, HAS_PDF_PARAMS
from methods import (
    store_metadata,
    save_discipline_pdfs,
)
from file_merger import merge_discipline_jsons_to_jsonl


# open parallel process equal to the number of topics, years and languages
if not os.path.exists("tly_combinations.json"):
    tl_combinations = list(product(TOPICS, LANGUAGES))
    conditions_of_access = [
        "acr_open-access",
        "undefined",
        "acr_closed-access",
        "other",
        "acr_restricted-access-or-use",
    ]
    tlca_combinations = list(product(tl_combinations, conditions_of_access))
    # flatten the list of tuple, elements of the list into one
    tlca_combinations = [(*item[0], item[1]) for item in tlca_combinations]
    years_list = get_list_of_years(
        tlca_combinations,
        has_pdf_params=HAS_PDF_PARAMS,
        with_datestamp=False,
        only_return_years=True,
    )
    logging.info(
        f"Total disciplines: {len(years_list)} and total tlca combinations: {len(tlca_combinations)}"
    )

    with_datestamp = True
    years_metadata = (
        get_list_of_years(
            tlca_combinations,
            has_pdf_params=HAS_PDF_PARAMS,
            with_datestamp=False,
            only_return_years=False,
        )
        if not with_datestamp
        else get_list_of_years(
            [
                (t, l, c_a, y)
                for t, l, c_a in tlca_combinations
                for y in years_list[t][l][c_a]["year"]
            ],
            has_pdf_params=HAS_PDF_PARAMS,
            with_datestamp=True,
            only_return_years=False,
        )
    )
    tly_combinations = (
        [
            (t, l, c_a, y[0], y[1])
            for t, l, c_a in tlca_combinations
            for y in years_metadata[t][l][c_a]
        ]
        if not with_datestamp
        else [
            (t, l, c_a, y, d[0], d[1])
            for t, l, c_a in tlca_combinations
            for y in years_list[t][l][c_a]["year"]
            for d in years_metadata[t][l][c_a][y]["datestamp"]
        ]
    )
    logging.info(f"Total topic-language-year combinations: {len(tly_combinations)}\n")
    with open("tly_combinations.json", "w") as f:
        json.dump(tly_combinations, f, indent=4)
else:
    with open("tly_combinations.json", "r") as f:
        tly_combinations = json.load(f)

# print out all the combinations that have more than 10000 items which exceeds the limit of 10000 items per request
elements = [
    (t, l, c_a, y, d, c - 10000) for t, l, c_a, y, d, c in tly_combinations if c > 10000
]
if len(elements) > 0:
    all_combinations_above_threshold = pd.DataFrame(elements)
    all_combinations_above_threshold.columns = [
        "topic",
        "language",
        "conditions_of_access",
        "year",
        "datestamp",
        "delta_num_items",
    ]
    all_combinations_above_threshold.to_csv(
        "all_combinations_above_threshold_datestamp.csv", index=False
    )
    print(
        f"Total combinations above threshold: {len(all_combinations_above_threshold)}"
    )
else:
    logging.info("No combinations above threshold")

if __name__ == "__main__":
    num_processes = int(os.getenv("NUM_PROCESSES"))
    with Pool(num_processes) as pool:
        # Map the function to all items
        results = pool.map(store_metadata, tly_combinations)

    # merge_discipline_jsons_to_jsonl(os.getenv("STORAGE_LOCAL_PATH"))
    # for _ in ["archeo"]:
    #     logging.info(f"Starting to save PDFs for discipline: {_}")
    #     save_discipline_pdfs(_)
